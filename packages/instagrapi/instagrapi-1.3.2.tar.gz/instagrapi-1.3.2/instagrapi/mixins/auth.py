import re
import json
import base64
import time
import uuid
import pytz
import hmac
import hashlib
import random
import datetime
import requests

from instagrapi import config
from instagrapi.exceptions import ReloginAttemptExceeded


class PreLoginFlowMixin:

    def pre_login_flow(self) -> bool:
        """Emulation mobile app behaivor before login
        """
        # /api/v1/accounts/get_prefill_candidates
        self.get_prefill_candidates(True)
        # /api/v1/qe/sync (server_config_retrieval)
        self.sync_device_features(True)
        # /api/v1/launcher/sync/ (server_config_retrieval)
        self.sync_launcher(True)
        # /api/v1/accounts/contact_point_prefill/
        self.set_contact_point_prefill("prefill")
        return True

    def get_prefill_candidates(self, login: bool = False) -> dict:
        # "android_device_id":"android-f14b9731e4869eb",
        # "phone_id":"b4bd7978-ca2b-4ea0-a728-deb4180bd6ca",
        # "usages":"[\"account_recovery_omnibox\"]",
        # "_csrftoken":"9LZXBXXOztxNmg3h1r4gNzX5ohoOeBkI",
        # "device_id":"70db6a72-2663-48da-96f5-123edff1d458"
        data = {
            "android_device_id": self.device_id,
            "phone_id": self.phone_id,
            "usages": '["account_recovery_omnibox"]',
            "device_id": self.device_id,
        }
        if login is False:
            data["_csrftoken"] = self.token
        return self.private_request(
            "accounts/get_prefill_candidates/", data, login=login
        )

    def sync_device_features(self, login: bool = False) -> dict:
        data = {
            "id": self.uuid,
            "server_config_retrieval": "1",
            "experiments": config.LOGIN_EXPERIMENTS,
        }
        if login is False:
            data["_uuid"] = self.uuid
            data["_uid"] = self.user_id
            data["_csrftoken"] = self.token
        return self.private_request(
            "qe/sync/", data, login=login, headers={"X-DEVICE-ID": self.uuid}
        )

    def sync_launcher(self, login: bool = False) -> dict:
        data = {
            "id": self.uuid,
            "server_config_retrieval": "1",
        }
        if login is False:
            data["_uid"] = self.user_id
            data["_uuid"] = self.uuid
            data["_csrftoken"] = self.token
        return self.private_request("launcher/sync/", data, login=login)

    def set_contact_point_prefill(self, usage: str = "prefill") -> dict:
        data = {"phone_id": self.phone_id, "usage": usage}
        return self.private_request("accounts/contact_point_prefill/", data, login=True)


class PostLoginFlowMixin:

    def login_flow(self) -> bool:
        """Emulation mobile app behaivor after login
        """
        check_flow = []
        chance = random.randint(1, 100) % 2 == 0
        check_flow.append(self.get_timeline_feed(
            [chance and "is_pull_to_refresh"]))
        check_flow.append(
            self.get_reels_tray_feed(
                reason="pull_to_refresh" if chance else "cold_start"
            )
        )
        return all(check_flow)

    def get_timeline_feed(self, options: list = []) -> dict:
        headers = {
            "X-Ads-Opt-Out": "0",
            "X-DEVICE-ID": self.uuid,
            "X-CM-Bandwidth-KBPS": str(random.randint(2000, 5000)),
            "X-CM-Latency": str(random.randint(1, 5)),
        }
        data = {
            "feed_view_info": "",
            "phone_id": self.phone_id,
            "battery_level": random.randint(25, 100),
            "timezone_offset": datetime.datetime.now(pytz.timezone("CET")).strftime(
                "%z"
            ),
            "_csrftoken": self.token,
            "device_id": self.uuid,
            "request_id": self.device_id,
            "_uuid": self.uuid,
            "is_charging": random.randint(0, 1),
            "will_sound_on": random.randint(0, 1),
            "session_id": self.client_session_id,
            "bloks_versioning_id": "e538d4591f238824118bfcb9528c8d005f2ea3becd947a3973c030ac971bb88e",
        }

        if "is_pull_to_refresh" in options:
            data["reason"] = "pull_to_refresh"
            data["is_pull_to_refresh"] = "1"
        elif "is_pull_to_refresh" not in options:
            data["reason"] = "cold_start_fetch"
            data["is_pull_to_refresh"] = "0"

        if "push_disabled" in options:
            data["push_disabled"] = "true"

        if "recovered_from_crash" in options:
            data["recovered_from_crash"] = "1"

        return self.private_request(
            "feed/timeline/", json.dumps(data), with_signature=False, headers=headers
        )

    def get_reels_tray_feed(self, reason: str = "pull_to_refresh") -> dict:
        """
        :param reason: can be = cold_start, pull_to_refresh
        """
        data = {
            "supported_capabilities_new": config.SUPPORTED_CAPABILITIES,
            "reason": reason,
            "_csrftoken": self.token,
            "_uuid": self.uuid,
        }
        return self.private_request("feed/reels_tray/", data)


class LoginMixin(PreLoginFlowMixin, PostLoginFlowMixin):
    username = None
    password = None
    last_login = None
    relogin_attempt = 0
    device_settings = {}
    client_session_id = ""
    advertising_id = ""
    device_id = ""
    phone_id = ""
    uuid = ""

    def init(self) -> bool:
        if "cookies" in self.settings:
            self.private.cookies = requests.utils.cookiejar_from_dict(
                self.settings["cookies"]
            )
        self.last_login = self.settings.get("last_login")
        self.set_device(self.settings.get("device_settings"))
        self.set_user_agent(self.settings.get("user_agent"))
        self.set_uuids(self.settings.get("uuids", {}))
        return True

    def login_by_sessionid(self, sessionid: str) -> bool:
        assert isinstance(sessionid, str) and len(
            sessionid) > 30, 'Invalid sessionid'
        self.settings = {'cookies': {'sessionid': sessionid}}
        self.init()
        user_id = re.search(r'^\d+', sessionid).group()
        user = self.user_info_v1(int(user_id))
        self.username = user.username
        return True

    def login(self, username: str, password: str, relogin: bool = False) -> bool:
        self.username = username
        self.password = password
        self.init()
        if relogin:
            self.private.cookies.clear()
            if self.relogin_attempt > 1:
                raise ReloginAttemptExceeded()
            self.relogin_attempt += 1
        # if self.user_id and self.last_login:
        #     if time.time() - self.last_login < 60 * 60 * 24:
        #        return True  # already login
        if self.user_id:
            return True  # already login
        self.pre_login_flow()
        data = {
            "phone_id": self.phone_id,
            "_csrftoken": self.token,
            "username": username,
            "guid": self.uuid,
            "device_id": self.device_id,
            "password": password,
            "login_attempt_count": "0",
        }
        if self.private_request("accounts/login/", data, login=True):
            self.login_flow()
            self.last_login = time.time()
            return True
        return False

    def relogin(self) -> bool:
        """Relogin shortcut
        """
        return self.login(self.username, self.password, relogin=True)

    @property
    def cookie_dict(self) -> dict:
        return self.private.cookies.get_dict()

    @property
    def token(self) -> str:
        return self.cookie_dict.get("csrftoken")

    @property
    def rank_token(self) -> str:
        return f"{self.user_id}_{self.uuid}"

    @property
    def user_id(self) -> int:
        user_id = self.cookie_dict.get("ds_user_id")
        if user_id:
            return int(user_id)
        return None

    # @property
    # def username(self):
    #     return self.cookie_dict.get("ds_user")

    @property
    def mid(self) -> str:
        return self.cookie_dict.get("mid")

    @property
    def device(self) -> dict:
        return {
            key: val
            for key, val in self.device_settings.items()
            if key in ["manufacturer", "model", "android_version", "android_release"]
        }

    def get_settings(self) -> dict:
        return {
            "uuids": {
                "phone_id": self.phone_id,
                "uuid": self.uuid,
                "client_session_id": self.client_session_id,
                "advertising_id": self.advertising_id,
                "device_id": self.device_id,
            },
            "cookies": requests.utils.dict_from_cookiejar(self.private.cookies),
            "last_login": self.last_login,
            "device_settings": self.device_settings,
            "user_agent": self.user_agent,
        }

    def set_device(self, device: dict = {}) -> bool:
        self.device_settings = device or {
            "app_version": "105.0.0.18.119",
            "android_version": 28,
            "android_release": "9.0",
            "dpi": "640dpi",
            "resolution": "1440x2560",
            "manufacturer": "samsung",
            "device": "SM-G965F",
            "model": "star2qltecs",
            "cpu": "samsungexynos9810",
            "version_code": "168361634",
        }
        self.set_uuids({})
        return True

    def set_user_agent(self, user_agent: str = "") -> bool:
        self.user_agent = user_agent or config.USER_AGENT_BASE.format(
            **self.device_settings
        )
        self.private.headers.update({"User-Agent": self.user_agent})
        self.set_uuids({})
        return True

    def set_uuids(self, uuids: dict = {}) -> bool:
        self.phone_id = uuids.get("phone_id", self.generate_uuid())
        self.uuid = uuids.get("uuid", self.generate_uuid())
        self.client_session_id = uuids.get(
            "client_session_id", self.generate_uuid())
        self.advertising_id = uuids.get("advertising_id", self.generate_uuid())
        self.device_id = uuids.get("device_id", self.generate_device_id())
        return True

    def generate_uuid(self) -> str:
        return str(uuid.uuid4())

    def generate_device_id(self) -> str:
        return "android-%s" % hashlib.md5(
            bytes(random.randint(1, 1000))
        ).hexdigest()[:16]

    def expose(self) -> dict:
        data = {
            "id": self.uuid,
            "experiment": "ig_android_profile_contextual_feed"
        }
        return self.private_request("qe/expose/", self.with_default_data(data))

    def with_default_data(self, data: dict) -> dict:
        return dict(
            {
                "_uuid": self.uuid,
                "_uid": str(self.user_id),
                "_csrftoken": self.token,
                "device_id": self.device_id,
            },
            **data
        )

    def with_action_data(self, data: dict) -> dict:
        return dict(self.with_default_data({"radio_type": "wifi-none"}), **data)

    def gen_user_breadcrumb(self, size: int) -> str:
        key = "iN4$aGr0m"
        dt = int(time.time() * 1000)
        time_elapsed = random.randint(500, 1500) + size * random.randint(500, 1500)
        text_change_event_count = max(1, size / random.randint(3, 5))
        data = "{size!s} {elapsed!s} {count!s} {dt!s}".format(
            **{
                "size": size,
                "elapsed": time_elapsed,
                "count": text_change_event_count,
                "dt": dt,
            }
        )
        return "{!s}\n{!s}\n".format(
            base64.b64encode(
                hmac.new(
                    key.encode("ascii"), data.encode("ascii"), digestmod=hashlib.sha256
                ).digest()
            ),
            base64.b64encode(data.encode("ascii")),
        )

    def inject_sessionid_to_public(self):
        """Inject sessionid from private session to public session
        """
        sessionid = self.private.cookies.get('sessionid')
        if sessionid:
            self.public.cookies.set('sessionid', sessionid)
            return True
        return False
