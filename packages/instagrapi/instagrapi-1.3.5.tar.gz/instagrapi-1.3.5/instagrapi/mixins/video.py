import time
import random
import requests
from pathlib import Path
from typing import List
from uuid import uuid4
from urllib.parse import urlparse

from instagrapi import config
from instagrapi.extractors import extract_media_v1
from instagrapi.exceptions import (
    VideoNotDownload, VideoNotUpload, VideoConfigureError,
    VideoConfigureStoryError
)
from instagrapi.types import Usertag, Location, StoryMention, StoryLink, Media
from instagrapi.utils import dumps


class DownloadVideoMixin:

    def video_download(self, media_pk: int, folder: Path = "") -> Path:
        media = self.media_info(media_pk)
        assert media.media_type == 2, "Must been video"
        filename = "{username}_{media_pk}".format(
            username=media.user.username, media_pk=media_pk
        )
        return self.video_download_by_url(media.video_url, filename, folder)

    def video_download_by_url(self, url: str, filename: str = "", folder: Path = "") -> Path:
        fname = urlparse(url).path.rsplit('/', 1)[1]
        filename = "%s.%s" % (filename, fname.rsplit('.', 1)[
                              1]) if filename else fname
        path = Path(folder) / filename
        response = requests.get(url, stream=True)
        response.raise_for_status()
        content_length = int(response.headers.get("Content-Length"))
        file_length = len(response.content)
        if content_length != file_length:
            raise VideoNotDownload(
                'Broken file "%s" (Content-length=%s, but file length=%s)'
                % (path, content_length, file_length)
            )
        with open(path, "wb") as f:
            f.write(response.content)
            f.close()
        return path.resolve()


class UploadVideoMixin:

    def video_rupload(
        self,
        path: Path,
        thumbnail: Path = None,
        to_album: bool = False,
        to_story: bool = False
    ) -> tuple:
        """Upload video to Instagram

        :param path:          Path to video file
        :param thumbnail:     Path to thumbnail for video. When None, then
                              thumbnail is generate automatically

        :return: Tuple (upload_id, width, height, duration)
        """
        assert isinstance(path, Path), f"Path must been Path, now {path} ({type(path)})"
        upload_id = str(int(time.time() * 1000))
        width, height, duration, thumbnail = analyze_video(path, thumbnail)
        waterfall_id = str(uuid4())
        # upload_name example: '1576102477530_0_7823256191'
        upload_name = "{upload_id}_0_{rand}".format(
            upload_id=upload_id, rand=random.randint(1000000000, 9999999999)
        )
        rupload_params = {
            "retry_context": '{"num_step_auto_retry":0,"num_reupload":0,"num_step_manual_retry":0}',
            "media_type": "2",
            "xsharing_user_ids": dumps([self.user_id]),
            "upload_id": upload_id,
            "upload_media_duration_ms": str(int(duration * 1000)),
            "upload_media_width": str(width),
            "upload_media_height": str(height),  # "1138" for Mi5s
        }
        if to_album:
            rupload_params["is_sidecar"] = "1"
        if to_story:
            rupload_params = {
                "extract_cover_frame": "1",
                "content_tags": "has-overlay",
                "for_album": "1",
                **rupload_params
            }
        headers = {
            "Accept-Encoding": "gzip, deflate",
            "X-Instagram-Rupload-Params": dumps(rupload_params),
            "X_FB_VIDEO_WATERFALL_ID": waterfall_id,
            # "X_FB_VIDEO_WATERFALL_ID": "88732215909430_55CF262450C9_Mixed_0",  # ALBUM
            # "X_FB_VIDEO_WATERFALL_ID": "1594919079102",  # VIDEO
        }
        if to_album:
            headers = {
                "Segment-Start-Offset": "0",
                "Segment-Type": "3",
                **headers
            }
        response = self.private.get(
            "https://{domain}/rupload_igvideo/{name}".format(
                domain=config.API_DOMAIN, name=upload_name
            ), headers=headers
        )
        self.request_log(response)
        if response.status_code != 200:
            raise VideoNotUpload(
                response.text, response=response, **self.last_json
            )
        video_data = open(path, "rb").read()
        video_len = str(len(video_data))
        headers = {
            "Offset": "0",
            "X-Entity-Name": upload_name,
            "X-Entity-Length": video_len,
            "Content-Type": "application/octet-stream",
            "Content-Length": video_len,
            "X-Entity-Type": "video/mp4",
            **headers
        }
        response = self.private.post(
            "https://{domain}/rupload_igvideo/{name}".format(
                domain=config.API_DOMAIN, name=upload_name
            ),
            data=video_data, headers=headers
        )
        self.request_log(response)
        if response.status_code != 200:
            raise VideoNotUpload(
                response.text, response=response, **self.last_json
            )
        return upload_id, width, height, duration, Path(thumbnail)

    def video_upload(
        self,
        path: Path,
        caption: str,
        thumbnail: Path = None,
        usertags: List[Usertag] = [],
        location: Location = None,
        links: List[StoryLink] = [],
        configure_timeout: int = 3,
        configure_handler=None,
        configure_exception=None,
        to_story: bool = False
    ) -> Media:
        """Upload video to feed

        :param path:                Path to video file
        :param caption:             Media description (String)
        :param thumbnail:           Path to thumbnail for video. When None, then
                                        thumbnail is generate automatically
        :param usertags:            Mentioned users (List)
        :param location:            Location
        :param links:               URLs for Swipe Up (List of dicts)
        :param configure_timeout:   Timeout between attempt to configure media (set caption, etc)
        :param configure_handler:   Configure handler method
        :param configure_exception: Configure exception class

        :return: Media
        """
        path = Path(path)
        if thumbnail is not None:
            thumbnail = Path(thumbnail)
        upload_id, width, height, duration, thumbnail = self.video_rupload(
            path, thumbnail, to_story=to_story
        )
        for attempt in range(20):
            self.logger.debug(f"Attempt #{attempt} to configure Video: {path}")
            time.sleep(configure_timeout)
            try:
                configured = (configure_handler or self.video_configure)(
                    upload_id, width, height, duration, thumbnail, caption, usertags, location, links
                )
            except Exception as e:
                if "Transcode not finished yet" in str(e):
                    """
                    Response 202 status:
                    {"message": "Transcode not finished yet.", "status": "fail"}
                    """
                    time.sleep(10)
                    continue
                raise e
            else:
                if configured:
                    media = configured.get("media")
                    self.expose()
                    return extract_media_v1(media)
        raise (configure_exception or VideoConfigureError)(
            response=self.last_response, **self.last_json)

    def video_configure(
        self,
        upload_id: str,
        width: int,
        height: int,
        duration: int,
        thumbnail: Path,
        caption: str,
        usertags: List[Usertag] = [],
        location: Location = None,
        links: List[StoryLink] = []
    ) -> dict:
        """Post Configure Video (send caption, thumbnail and more to Instagram)

        :param upload_id:  Unique upload_id (String)
        :param width:      Width in px (Integer)
        :param height:     Height in px (Integer)
        :param duration:   Duration in seconds (Integer)
        :param thumbnail:  Path to thumbnail for video
        :param caption:    Media description (String)
        :param usertags:   Mentioned users (List)
        :param location:   Location
        :param links:      URLs for Swipe Up (List of dicts)

        :return: Media (Dict)
        """
        self.photo_rupload(Path(thumbnail), upload_id)
        usertags = [
            {"user_id": tag.user.pk, "position": [tag.x, tag.y]}
            for tag in usertags
        ]
        data = {
            "multi_sharing": "1",
            "creation_logger_session_id": self.client_session_id,
            "upload_id": upload_id,
            "source_type": "4",
            "location": self.location_build(location),
            "poster_frame_index": 0,
            "length": duration,
            "audio_muted": False,
            "usertags": dumps({"in": usertags}),
            "filter_type": "0",
            "date_time_original": time.strftime("%Y%m%dT%H%M%S.000Z", time.localtime()),
            "timezone_offset": "10800",
            "clips": [{"length": duration, "source_type": "4"}],
            "extra": {"source_width": width, "source_height": height},
            "device": self.device,
            "caption": caption,
        }
        return self.private_request("media/configure/?video=1", self.with_default_data(data))

    def video_upload_to_story(
        self,
        path: Path,
        caption: str,
        thumbnail: Path = None,
        mentions: List[StoryMention] = [],
        links: List[StoryLink] = [],
        configure_timeout: int = 3
    ) -> Media:
        """Upload video to feed

        :param path:              Path to video file
        :param caption:           Media description (String)
        :param thumbnail:         Path to thumbnail for video. When None, then
                                  thumbnail is generate automatically
        :param mentions:          Mentioned users (List)
        :param links:             URLs for Swipe Up (List of dicts)
        :param configure_timeout: Timeout between attempt to configure media (set caption, etc)

        :return: Media
        """
        return self.video_upload(
            path, caption, thumbnail, mentions,
            links=links,
            configure_timeout=configure_timeout,
            configure_handler=self.video_configure_to_story,
            configure_exception=VideoConfigureStoryError,
            to_story=True
        )

    def video_configure_to_story(
        self,
        upload_id: str,
        width: int,
        height: int,
        duration: int,
        thumbnail: Path,
        caption: str,
        mentions: List[StoryMention] = [],
        location: Location = None,
        links: List[StoryLink] = []
    ) -> dict:
        """Post Configure Video (send caption, thumbnail and more to Instagram)

        :param upload_id:  Unique upload_id (String)
        :param thumbnail:  Path to thumbnail for video
        :param width:      Width in px (Integer)
        :param height:     Height in px (Integer)
        :param duration:   Duration in seconds (Integer)
        :param caption:    Media description (String)
        :param mentions:   Mentioned users (List)
        :param location:   Temporary unused
        :param links:      URLs for Swipe Up (List of dicts)

        :return: Media (Dict)
        """
        timestamp = int(time.time())
        data = {
            "supported_capabilities_new": dumps(config.SUPPORTED_CAPABILITIES),
            "has_original_sound": "1",
            # Segment mode (when file is too big):
            # "allow_multi_configures": "1",
            # "segmented_video_group_id": str(uuid4()),
            # "multi_upload_session_id": str(uuid4()),
            # "segmented_video_count": "4",  # "4"  # SEGMENT MODE
            # "segmented_video_index": "0",  # 0,1,2,3  # SEGMENT MODE
            # "is_multi_upload": "1",  # SEGMENT MODE
            # "is_segmented_video": "1",  # SEGMENT MODE
            "filter_type": "0",
            "camera_session_id": self.client_session_id,
            "timezone_offset": "10800",
            "client_timestamp": str(timestamp),
            "client_shared_at": str(timestamp - 7),  # 7 seconds ago
            "imported_taken_at": str(timestamp - 5 * 24 * 3600),  # 5 days ago
            "date_time_original": time.strftime("%Y%m%dT%H%M%S.000Z", time.localtime()),
            "media_folder": "Camera",
            "configure_mode": "1",
            "source_type": "4",
            "video_result": "",
            "creation_surface": "camera",
            "caption": caption,
            "capture_type": "normal",
            "rich_text_format_types": "[\"strong\"]",  # default, typewriter
            "upload_id": upload_id,
            # Facebook Sharing Part:
            # "xpost_surface": "auto_xpost",
            # "share_to_fb_destination_type": "USER",
            # "share_to_fb_destination_id":"832928543",
            # "share_to_facebook":"1",
            # "fb_access_token":"EAABwzLixnjYBACVgqBfLyDuPWs6RN2sTZC........cnNkjHCH2",
            # "attempt_id": str(uuid4()),
            "device": self.device,
            "length": duration,
            "implicit_location": {
                "media_location": {
                    "lat": 0.0,
                    "lng": 0.0
                }
            },
            "clips": [{"length": duration, "source_type": "4"}],
            "extra": {"source_width": width, "source_height": height},
            "audio_muted": False,
            "poster_frame_index": 0
        }
        if links:
            links = [link.dict() for link in links]
            data["story_cta"] = dumps([{"links": links}])
        if mentions:
            reel_mentions = []
            text_metadata = []
            for mention in mentions:
                reel_mentions.append({
                    "x": mention.x, "y": mention.y, "z": 0,
                    "width": mention.width, "height": mention.height, "rotation": 0.0,
                    "type": "mention", "user_id": str(mention.user.pk), "is_sticker": False, "display_type": "mention_username"
                })
                text_metadata.append({
                    "font_size": 40.0, "scale": 1.2798771,
                    "width": 1017.50226, "height": 216.29922,
                    "x": mention.x, "y": mention.y, "rotation": 0.0
                })
            data["text_metadata"] = dumps(text_metadata)
            data["tap_models"] = data["reel_mentions"] = dumps(reel_mentions)
        return self.private_request("media/configure_to_story/?video=1", self.with_default_data(data))


def analyze_video(path: Path, thumbnail: Path = None) -> tuple:
    """Analyze video file
    """

    try:
        import moviepy.editor as mp
    except ImportError:
        raise Exception('Please install moviepy>=1.0.3 and retry')

    print(f'Analizing video file "{path}"')
    video = mp.VideoFileClip(str(path))
    width, height = video.size
    if not thumbnail:
        thumbnail = f"{path}.jpg"
        print(f'Generating thumbnail "{thumbnail}"...')
        video.save_frame(thumbnail, t=(video.duration / 2))
    # duration = round(video.duration + 0.001, 3)
    return width, height, video.duration, thumbnail
