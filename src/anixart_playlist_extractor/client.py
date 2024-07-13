import json
import typing

import requests

ANIXART_URL = "api.anixart.tv"
ANIXART_USER_AGENT = (
    "AnixartApp/8.1.2-22101520 (Android 13; SDK 33; arm64-v8a; Xiaomi Redmi K20; ru)"
)
ANIXART_HEADERS = {"User-Agent": ANIXART_USER_AGENT}


KODIK_UNKNOWN_PARAM = "56a768d08f43091901c44b54fe970049"
KODIK_URL = "kodik.biz"
KODIK_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/86.0.4240.198 "
    "Safari/537.36"
)
KODIK_HEADERS = {"User-Agent": KODIK_USER_AGENT}


class Client:
    def __init__(
        self,
        session: requests.Session = None,
    ) -> None:
        self.session: requests.Session = (
            session if session is not None else requests.Session()
        )

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        self.session.close()

    def request(
        self,
        url: str,
        *,
        params: dict[str, str] = None,
        headers: dict[str, str] = None,
    ) -> dict[str, typing.Any]:
        resp = self.session.get(
            url,
            params=params,
            headers=headers,
        )

        if resp.status_code != 200:
            raise Exception(
                f"Req {url} ends with status code: "
                f"{resp.status_code}; content: {resp.content.decode()}"
            )

        return json.loads(resp.content)

    def release(
        self,
        release_id: int,
        *,
        host: str = ANIXART_URL,
        headers: dict[str, str] = ANIXART_HEADERS,
    ) -> dict[str, typing.Any]:
        return self.request(
            f"https://{host}/release/{release_id}",
            params={"extended_mode": True},
            headers=headers,
        )

    def episode(
        self,
        release_id: int,
        *,
        type_id: int = None,
        source_id: int = None,
        host: str = ANIXART_URL,
        headers: dict[str, str] = ANIXART_HEADERS,
    ) -> dict[str, typing.Any]:
        return self.request(
            f"https://{host}/episode/{release_id}"
            if type_id is None
            else f"https://{host}/episode/{release_id}/{type_id}"
            if source_id is None
            else f"https://{host}/episode/{release_id}/{type_id}/{source_id}",
            headers=headers,
        )

    def episode_target(
        self,
        release_id: int,
        source_id: int,
        position: int,
        *,
        host: str = ANIXART_URL,
        headers: dict[str, str] = ANIXART_HEADERS,
    ) -> dict[str, typing.Any]:
        return self.request(
            f"https://{host}/episode/target/{release_id}/{source_id}/{position}",
            headers=headers,
        )

    def video_links(
        self,
        link: str,
        d: str,
        s: str,
        ip: str,
        *,
        p: str = KODIK_UNKNOWN_PARAM,
        host: str = KODIK_URL,
        headers: dict[str, str] = KODIK_HEADERS,
    ) -> dict[str, typing.Any]:
        return self.request(
            f"http://{host}/api/video-links",
            headers=headers,
            params={
                "p": p,
                "link": link,
                "d": d,
                "s": s,
                "ip": ip,
            },
        )


__all__ = (
    ANIXART_URL,
    ANIXART_HEADERS,
    ANIXART_USER_AGENT,
    KODIK_UNKNOWN_PARAM,
    KODIK_URL,
    KODIK_HEADERS,
    KODIK_USER_AGENT,
    Client,
)
