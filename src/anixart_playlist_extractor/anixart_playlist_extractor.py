import os

from urllib.parse import urlparse

from anixart_playlist_extractor.client import Client
from anixart_playlist_extractor.enums import Quality
from anixart_playlist_extractor.models import (
    AnixartResponse,
    EpisodeUpdate,
    Playlist,
    PlaylistVideo,
    Type,
)
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

    def get_location(
        self,
        url: str,
        *,
        quality: Quality = Quality.q720,
    ) -> str:
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

        video_links = self.client.get_video_links(
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

        return f"https:{video_link}"

    def get_playlist_video(
        self,
        release_id: int,
        source_id: int,
        position: int,
        *,
        quality: Quality = Quality.q720,
    ) -> PlaylistVideo:
        episode = self.client.get_episode(release_id, source_id, position)

        self.assert_code(episode)

        return PlaylistVideo(
            id=episode.episode.position,
            title=episode.episode.name,
            location=self.get_location(
                episode.episode.url,
                quality=quality,
            ),
        )
        ...

    def get_playlist(
        self,
        release_id: int,
        type_id: int,
        *,
        extract_only: list[int] | None = None,
        extract_last: bool | None = None,
        quality: Quality = Quality.q720,
    ) -> Playlist:
        release = self.client.get_release(release_id)

        self.assert_code(release)

        episode_sources = self.client.get_episode_sources(release_id, type_id)

        self.assert_code(episode_sources)

        if len(episode_sources.sources) < 1:
            raise Exception(
                f"No sources for TypeID: {type_id} (ReleaseID: {release_id})"
            )

        source_id = episode_sources.sources[0].id
        episodes = self.client.get_episodes(release_id, type_id, source_id)

        self.assert_code(episodes)

        episodes = (
            episodes.episodes[-1:]
            if extract_last
            else filter(
                lambda episode: episode.position in extract_only,
                episodes.episodes,
            )
            if extract_only
            else episodes.episodes
        )

        videos: list[PlaylistVideo] = [
            self.get_playlist_video(
                release_id,
                source_id,
                episode.position,
                quality=quality,
            )
            for episode in episodes
        ]

        return Playlist(
            title=release.release.title_ru,
            videos=videos,
        )

    def list_release_types(
        self,
        release_id: int,
        *,
        pages_max: int = 2,
    ) -> list[Type]:
        # --- classic method ---
        episode_types = self.client.get_episode_types(release_id)

        if episode_types.code == 0:
            return sorted(episode_types.types, key=lambda type: type.name)

        # --- workaround (for releases banned in the region) ---
        episode_updates: list[EpisodeUpdate] = []

        for page in range(1, pages_max + 1):
            _episode_updates = self.client.get_episode_updates(release_id, page=page)

            self.assert_code(_episode_updates)
            episode_updates += _episode_updates.content

        types: list[Type] = []
        for episode_update in episode_updates:
            if not any(
                map(
                    lambda type: type.id == episode_update.last_episode_type_update_id,
                    types,
                )
            ):
                types.append(
                    Type.model_validate(
                        {
                            "@id": 0,
                            "id": episode_update.last_episode_type_update_id,
                            "name": episode_update.lastEpisodeTypeUpdateName,
                            "icon": None,
                            "workers": None,
                            "is_sub": False,
                            "episodes_count": 0,
                            "view_count": 0,
                            "pinned": False,
                        }
                    )
                )

        return sorted(types, key=lambda type: type.name)

    def print_types(
        self,
        *,
        release_id: int | None = None,
        pages_max: int = 2,
    ) -> None:
        if release_id is not None:
            types = self.list_release_types(release_id, pages_max=pages_max)
        else:
            type_all = self.client.get_type_all()
            self.assert_code(type_all)
            types = type_all.types

        print("TypeID | Название озвучки")
        for type in types:
            print(f"{type.id: >6} | {type.name}")

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
        playlist = self.get_playlist(
            release_id=release_id,
            type_id=type_id,
            extract_only=extract_only,
            extract_last=extract_last,
            quality=quality,
        )

        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, f"{playlist.title}.xspf")

        with open(path, "w", encoding="utf-8") as file:
            file.write(build_playlist(playlist))


def print_types(
    *,
    release_id: int | None = None,
    pages_max: int = 2,
) -> None:
    with Client() as client:
        AnixartPlaylistExtractor(client).print_types(
            release_id=release_id,
            pages_max=pages_max,
        )


def extract_playlist(
    release_id: int,
    type_id: int,
    *,
    extract_only: list[int] | None = None,
    extract_last: bool | None = None,
    quality: Quality = Quality.q720,
    output_dir: str = "output",
) -> None:
    with Client() as client:
        AnixartPlaylistExtractor(client).extract_playlist(
            release_id=release_id,
            type_id=type_id,
            extract_only=extract_only,
            extract_last=extract_last,
            quality=quality,
            output_dir=output_dir,
        )


__all__ = (
    AnixartPlaylistExtractor,
    print_types,
    extract_playlist,
)
