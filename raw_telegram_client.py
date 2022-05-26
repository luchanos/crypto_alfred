from http.client import HTTPException

import requests
from uuid import uuid4
from logging import getLogger
import urllib.parse
import json

logger = getLogger(__name__)


class TelegramClientRaw:
    def __init__(self, base_url: str, token: str) -> None:
        self.token = token
        self.base_url = base_url

    def build_url(self, chat_id: str, expire_date: int, member_limit, creates_join_request):
        uuid_id = uuid4()
        params = {
            "chat_id": chat_id,
            "name": uuid_id
        }
        if expire_date is not None:
            params["expire_date"] = expire_date
        if member_limit is not None:
            params["member_limit"] = member_limit
        if creates_join_request is not None:
            params["creates_join_request"] = creates_join_request

        url = f"{self.base_url}/bot{self.token}/createChatInviteLink?"
        url += urllib.parse.urlencode(params)
        return url

    def generate_invite_link(self,
                             chat_id: str,
                             expire_date: int = None,
                             member_limit: int = None,
                             creates_join_request: bool = None) -> str:

        url = self.build_url(chat_id, expire_date, member_limit, creates_join_request)
        res = requests.get(url)
        if res.status_code == 200:
            res = json.loads(res.text)
            return res
        raise HTTPException(f"Smth happened due to generation invite link. "
                            f"Status: {res.status_code}. Message: {res.text}")
