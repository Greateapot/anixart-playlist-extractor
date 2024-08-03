import os

from urllib.parse import urlparse

from anixart_playlist_extractor.client import Client
from anixart_playlist_extractor.enums import Quality
from anixart_playlist_extractor.models import AnixartResponse
from anixart_playlist_extractor.vlc_playlist_builder import build_playlist


class AnixartPlaylistExtractor:
    def __init__(self, client: Client = None) -> None:
        self.client: Client = client if client is not None else Client()

    def assert_code[ResponseModel: AnixartResponse](
        self,
        response: ResponseModel,
    ) -> None:
        if response.code != 0:
            raise Exception(f"Got AnixartResponse with error code: {response.code}")

    def get_video_link(
        self,
        release_id: int,
        source_id: int,
        position: int,
        *,
        quality: Quality = Quality.q720,
    ) -> tuple[str, str]:
        episode = self.client.episode(release_id, source_id, position)

        self.assert_code(episode)

        parse_result = urlparse(episode.episode.url)

        netloc = parse_result.netloc
        path = parse_result.path
        params = {
            key: value
            for key, value in map(
                lambda param: tuple(param.split("=")),
                parse_result.query.split("&"),
            )
        }

        video_links = self.client.video_links(
            f"//{netloc}{path}",
            params["d"],
            params["s"],
            params["ip"],
        )

        # TODO: find easier way to get `Src` field
        match quality:
            case Quality.q360:
                video_link = video_links.links.field_360.Src
            case Quality.q480:
                video_link = video_links.links.field_480.Src
            case Quality.q720:
                video_link = video_links.links.field_720.Src

        return (episode.episode.name, f"https:{video_link}")

    def extract_playlist(
        self,
        release_id: int,
        type_id: int,
        *,
        extract_only: list[int] | None = None,
        extract_last: bool | None = None,
        quality: Quality = Quality.q720,
        output_dir: str = "output",
    ) -> None:
        release = self.client.release(release_id)

        self.assert_code(release)

        title = release.release.title_ru
        episode_sources = self.client.episode_sources(release_id, type_id)

        self.assert_code(episode_sources)

        if len(episode_sources.sources) < 1:
            raise Exception(
                f"No sources for TypeID: {type_id} (ReleaseID: {release_id})"
            )

        source_id = episode_sources.sources[0].id
        episodes = self.client.episodes(release_id, type_id, source_id)

        self.assert_code(episodes)

        positions = map(
            lambda episode: episode.position,
            (
                episodes.episodes[-1:]
                if extract_last
                else filter(
                    lambda episode: episode.position in extract_only,
                    episodes.episodes,
                )
                if extract_only
                else episodes.episodes
            ),
        )

        links = dict(
            map(
                lambda position: self.get_video_link(
                    release_id,
                    source_id,
                    position,
                    quality=quality,
                ),
                positions,
            )
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
    extract_only: list[int] | None = None,
    extract_last: bool | None = None,
    quality: Quality = Quality.q720,
    output_dir: str = "output",
) -> None:
    AnixartPlaylistExtractor().extract_playlist(
        release_id=release_id,
        type_id=type_id,
        extract_only=extract_only,
        extract_last=extract_last,
        quality=quality,
        output_dir=output_dir,
    )


__all__ = (
    AnixartPlaylistExtractor,
    extract_playlist,
)
