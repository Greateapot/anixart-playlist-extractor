import typing
import os

from urllib.parse import urlparse


from anixart_playlist_extractor.client import Client
from anixart_playlist_extractor.enums import Quality
from anixart_playlist_extractor.vlc_playlist_builder import build_playlist


class AnixartPlaylistExtractor:
    def __init__(self, client: Client = None) -> None:
        self.client: Client = client if client is not None else Client()

    def assert_code(self, content: dict[str, typing.Any]) -> None:
        if content["code"] != 0:
            raise Exception(f"Anixart returns error; content: {content}")

    def get_video_link(
        self,
        release_id: int,
        source_id: int,
        position: int,
        *,
        quality: Quality = Quality.q720,
    ) -> tuple[str, str]:
        content = self.client.episode_target(
            release_id,
            source_id,
            position,
        )

        self.assert_code(content)

        name: str = content["episode"]["name"]
        url: str = content["episode"]["url"]

        parse_result = urlparse(url)

        netloc = parse_result.netloc
        path = parse_result.path
        params = {
            key: value
            for key, value in map(
                lambda param: tuple(param.split("=")),
                parse_result.query.split("&"),
            )
        }

        content = self.client.video_links(
            f"//{netloc}{path}",
            params["d"],
            params["s"],
            params["ip"],
        )

        kodik_storage_url: str = content["links"][quality.value]["Src"]

        return (name, f"https:{kodik_storage_url}")

    def extract_playlist(
        self,
        release_id: int,
        type_id: int,
        *,
        quality: Quality = Quality.q720,
        output_dir: str = "output",
    ) -> None:
        content = self.client.release(release_id)

        self.assert_code(content)

        title = content["release"]["title_ru"]

        content = self.client.episode(
            release_id,
            type_id=type_id,
        )

        self.assert_code(content)

        source_id = content["sources"][0]["id"]

        content = self.client.episode(
            release_id,
            type_id=type_id,
            source_id=source_id,
        )

        self.assert_code(content)

        links = dict(
            [
                self.get_video_link(
                    release_id,
                    source_id,
                    episode["position"],
                    quality=quality,
                )
                for episode in content["episodes"]
            ]
        )

        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, f"{title}.xspf")

        with open(path, "w", encoding="utf-8") as file:
            file.write(build_playlist(links, title))

        print(f"Done! Output: {path}")
        ...


def extract_playlist(
    release_id: int,
    type_id: int,
    *,
    quality: Quality = Quality.q720,
    output_dir: str = "output",
) -> None:
    AnixartPlaylistExtractor().extract_playlist(
        release_id=release_id,
        type_id=type_id,
        quality=quality,
        output_dir=output_dir,
    )


__all__ = (
    AnixartPlaylistExtractor,
    extract_playlist,
)
