import shutil
import json
import time
import random
import requests
from pathlib import Path
from typing import List
from uuid import uuid4
from PIL import Image
from urllib.parse import urlparse

from instagrapi import config
from instagrapi.extractors import extract_media_v1
from instagrapi.exceptions import (
    PhotoNotUpload, PhotoConfigureError, PhotoConfigureStoryError
)
from instagrapi.types import Usertag, Location, StoryMention, StoryLink, Media
from instagrapi.utils import dumps


class DownloadPhotoMixin:

    def photo_download(self, media_pk: int, folder: Path = "") -> Path:
        media = self.media_info(media_pk)
        assert media.media_type == 1, "Must been photo"
        filename = "{username}_{media_pk}".format(
            username=media.user.username, media_pk=media_pk
        )
        return self.photo_download_by_url(media.thumbnail_url, filename, folder)

    def photo_download_by_url(self, url: str, filename: str = "", folder: Path = "") -> Path:
        fname = urlparse(url).path.rsplit('/', 1)[1]
        filename = "%s.%s" % (filename, fname.rsplit('.', 1)[
                              1]) if filename else fname
        path = Path(folder) / filename
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(path, "wb") as f:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, f)
        return path.resolve()


class UploadPhotoMixin:

    def photo_rupload(
        self,
        path: Path,
        upload_id: str = "",
        to_album: bool = False
    ) -> tuple:
        """Upload photo to Instagram

        :param path:         Path to photo file
        :param upload_id:    Unique upload_id (String). When None, then generate
                             automatically. Example from video.video_configure

        :return: Tuple (upload_id, width, height)
        """
        assert isinstance(path, Path), f"Path must been Path, now {path} ({type(path)})"
        upload_id = upload_id or str(int(time.time() * 1000))
        assert path, "Not specified path to photo"
        waterfall_id = str(uuid4())
        # upload_name example: '1576102477530_0_7823256191'
        upload_name = "{upload_id}_0_{rand}".format(
            upload_id=upload_id, rand=random.randint(1000000000, 9999999999)
        )
        rupload_params = {
            "retry_context": '{"num_step_auto_retry":0,"num_reupload":0,"num_step_manual_retry":0}',
            "media_type": "1",  # "2" if upload_id else "1",  # "2" when from video/igtv/album thumbnail, "1" - upload photo only
            "xsharing_user_ids": "[]",
            "upload_id": upload_id,
            "image_compression": json.dumps(
                {"lib_name": "moz", "lib_version": "3.1.m", "quality": "80"}
            ),
        }
        if to_album:
            rupload_params["is_sidecar"] = "1"
        photo_data = open(path, "rb").read()
        photo_len = str(len(photo_data))
        headers = {
            "Accept-Encoding": "gzip",
            "X-Instagram-Rupload-Params": json.dumps(rupload_params),
            "X_FB_PHOTO_WATERFALL_ID": waterfall_id,
            "X-Entity-Type": "image/jpeg",
            "Offset": "0",
            "X-Entity-Name": upload_name,
            "X-Entity-Length": photo_len,
            "Content-Type": "application/octet-stream",
            "Content-Length": photo_len,
        }
        response = self.private.post(
            "https://{domain}/rupload_igphoto/{name}".format(
                domain=config.API_DOMAIN, name=upload_name
            ),
            data=photo_data, headers=headers
        )
        self.request_log(response)
        if response.status_code != 200:
            self.logger.error(
                "Photo Upload failed with the following response: %s", response
            )
            last_json = self.last_json  # local variable for read in sentry
            raise PhotoNotUpload(response.text, response=response, **last_json)
        width, height = Image.open(path).size
        return upload_id, width, height

    def photo_upload(
        self,
        path: Path,
        caption: str,
        upload_id: str = "",
        usertags: List[Usertag] = [],
        location: Location = None,
        links: List[StoryLink] = [],
        configure_timeout: int = 3,
        configure_handler=None,
        configure_exception=None
    ) -> Media:
        """Upload photo and configure to feed

        :param path:                Path to photo file
        :param caption:             Media description (String)
        :param upload_id:           Unique upload_id (String). When None, then generate
                                        automatically. Example from video.video_configure
        :param usertags:            Mentioned users (List)
        :param location:            Location
        :param links:               URLs for Swipe Up (List of dicts)
        :param configure_timeout:   Timeout between attempt to configure media (set caption, etc)
        :param configure_handler:   Configure handler method
        :param configure_exception: Configure exception class

        :return: Media
        """
        path = Path(path)
        upload_id, width, height = self.photo_rupload(path, upload_id)
        for attempt in range(10):
            self.logger.debug(f"Attempt #{attempt} to configure Photo: {path}")
            time.sleep(configure_timeout)
            if (configure_handler or self.photo_configure)(upload_id, width, height, caption, usertags, location, links):
                media = self.last_json.get("media")
                self.expose()
                return extract_media_v1(media)
        raise (configure_exception or PhotoConfigureError)(
            response=self.last_response, **self.last_json)

    def photo_configure(
        self,
        upload_id: str,
        width: int,
        height: int,
        caption: str,
        usertags: List[Usertag] = [],
        location: Location = None,
        links: List[StoryLink] = []
    ) -> dict:
        """Post Configure Photo (send caption to Instagram)

        :param upload_id:  Unique upload_id (String)
        :param width:      Width in px (Integer)
        :param height:     Height in px (Integer)
        :param caption:    Media description (String)
        :param usertags:   Mentioned users (List)
        :param location:   Location
        :param links:      URLs for Swipe Up (List of dicts)

        :return: Media (Dict)
        """
        usertags = [
            {"user_id": tag.user.pk, "position": [tag.x, tag.y]}
            for tag in usertags
        ]
        data = {
            "timezone_offset": "10800",
            "creation_logger_session_id": self.client_session_id,
            "multi_sharing": "1",
            "location": self.location_build(location),
            "media_folder": "Camera",
            "source_type": "4",
            "caption": caption,
            "upload_id": upload_id,
            "device": self.device,
            "usertags": json.dumps({"in": usertags}),
            "edits": {
                "crop_original_size": [width * 1.0, height * 1.0],
                "crop_center": [0.0, 0.0],
                "crop_zoom": 1.0,
            },
            "extra": {"source_width": width, "source_height": height},
        }
        return self.private_request("media/configure/", self.with_default_data(data))

    def photo_upload_to_story(
        self,
        path: Path,
        caption: str,
        upload_id: str = "",
        mentions: List[StoryMention] = [],
        links: List[StoryLink] = [],
        configure_timeout: int = 3
    ) -> Media:
        """Upload photo and configure to story

        :param path:                Path to photo file
        :param caption:             Media description (String)
        :param upload_id:           Unique upload_id (String). When None, then generate
                                        automatically. Example from video.video_configure
        :param mentions:            Mentioned users (List)
        :param links:               URLs for Swipe Up (List of dicts)
        :param configure_timeout:   Timeout between at<tempt to configure media (set caption, etc)

        :return: Media
        """
        return self.photo_upload(
            path, caption, upload_id, mentions,
            links=links,
            configure_timeout=configure_timeout,
            configure_handler=self.photo_configure_to_story,
            configure_exception=PhotoConfigureStoryError
        )

    def photo_configure_to_story(
        self,
        upload_id: str,
        width: int,
        height: int,
        caption: str,
        mentions: List[StoryMention] = [],
        location: Location = None,
        links: List[StoryLink] = []
    ) -> dict:
        """Story Configure for Photo

        :param upload_id:  Unique upload_id (String)
        :param width:      Width in px (Integer)
        :param height:     Height in px (Integer)
        :param caption:    Media description (String)
        :param usertags:   Mentioned users (List)
        :param location:   Temporary unused
        :param links:      URLs for Swipe Up (List of dicts)

        :return: Media (Dict)
        """
        timestamp = int(time.time())
        data = {
            "text_metadata": '[{"font_size":40.0,"scale":1.0,"width":611.0,"height":169.0,"x":0.51414347,"y":0.8487708,"rotation":0.0}]',
            "supported_capabilities_new": json.dumps(config.SUPPORTED_CAPABILITIES),
            "has_original_sound": "1",
            "camera_session_id": self.client_session_id,
            "scene_capture_type": "",
            "timezone_offset": "10800",
            "client_shared_at": str(timestamp - 5),  # 5 seconds ago
            "story_sticker_ids": "time_sticker_digital",
            "media_folder": "Camera",
            "configure_mode": "1",
            "source_type": "4",
            "creation_surface": "camera",
            "imported_taken_at": (timestamp - 3 * 24 * 3600),  # 3 days ago
            "caption": caption,
            "capture_type": "normal",
            "rich_text_format_types": '["default"]',
            "upload_id": upload_id,
            "client_timestamp": str(timestamp),
            "device": self.device,
            "implicit_location": {
                "media_location": {
                    "lat": 44.64972222222222,
                    "lng": 33.541666666666664
                }
            },
            "edits": {
                "crop_original_size": [width * 1.0, height * 1.0],
                "crop_center": [0.0, 0.0],
                "crop_zoom": 1.0,
            },
            "extra": {"source_width": width, "source_height": height},
        }
        if links:
            links = [link.dict() for link in links]
            data["story_cta"] = dumps([{"links": links}])
        if mentions:
            mentions = [
                {
                    "x": 0.5002546, "y": 0.8583542, "z": 0,
                    "width": 0.4712963, "height": 0.0703125, "rotation": 0.0,
                    "type": "mention", "user_id": str(mention.user.pk),
                    "is_sticker": False, "display_type": "mention_username"
                } for mention in mentions
            ]
            data["tap_models"] = data["reel_mentions"] = json.dumps(mentions)
        return self.private_request("media/configure_to_story/", self.with_default_data(data))
