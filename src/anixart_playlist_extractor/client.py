from pydantic import BaseModel, ValidationError
from requests import Session

from anixart_playlist_extractor.models import (
    EpisodeResponse,
    EpisodeSourcesResponse,
    EpisodeTypesResponse,
    EpisodesResponse,
    ReleaseResponse,
    VideoLinksResponse,
)

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
        session: Session = None,
    ) -> None:
        self.session: Session = session if session is not None else Session()

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        self.session.close()

    def request[ResponseModel: BaseModel](
        self,
        url: str,
        response_model: ResponseModel,
        *,
        headers: dict[str, str] = None,
        params: dict[str, str] = None,
    ) -> ResponseModel:
        resp = self.session.get(
            url,
            headers=headers,
            params=params,
        )

        if resp.status_code != 200:
            raise Exception(f"Req {url} ends with status code: {resp.status_code}")

        try:
            return response_model.model_validate_json(resp.content)
        except ValidationError:
            print(resp.content)
            raise

    def release(
        self,
        release_id: int,
        *,
        host: str = ANIXART_URL,
        headers: dict[str, str] = ANIXART_HEADERS,
    ) -> ReleaseResponse:
        return self.request(
            f"https://{host}/release/{release_id}",
            ReleaseResponse,
            headers=headers,
            params={
                "extended_mode": True,
            },
        )

    def episode_types(
        self,
        release_id: int,
        *,
        host: str = ANIXART_URL,
        headers: dict[str, str] = ANIXART_HEADERS,
    ) -> EpisodeTypesResponse:
        return self.request(
            f"https://{host}/episode/{release_id}",
            EpisodeTypesResponse,
            headers=headers,
        )

    def episode_sources(
        self,
        release_id: int,
        type_id: int,
        *,
        host: str = ANIXART_URL,
        headers: dict[str, str] = ANIXART_HEADERS,
    ) -> EpisodeSourcesResponse:
        return self.request(
            f"https://{host}/episode/{release_id}/{type_id}",
            EpisodeSourcesResponse,
            headers=headers,
        )

    def episodes(
        self,
        release_id: int,
        type_id: int,
        source_id: int,
        *,
        host: str = ANIXART_URL,
        headers: dict[str, str] = ANIXART_HEADERS,
    ) -> EpisodesResponse:
        return self.request(
            f"https://{host}/episode/{release_id}/{type_id}/{source_id}",
            EpisodesResponse,
            headers=headers,
        )

    def episode(
        self,
        release_id: int,
        source_id: int,
        position: int,
        *,
        host: str = ANIXART_URL,
        headers: dict[str, str] = ANIXART_HEADERS,
    ) -> EpisodeResponse:
        return self.request(
            f"https://{host}/episode/target/{release_id}/{source_id}/{position}",
            EpisodeResponse,
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
    ) -> VideoLinksResponse:
        return self.request(
            f"http://{host}/api/video-links",
            VideoLinksResponse,
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
