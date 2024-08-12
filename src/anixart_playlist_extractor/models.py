from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class PlaylistVideo(BaseModel):
    id: int
    title: str
    location: str


class Playlist(BaseModel):
    title: str
    videos: list[PlaylistVideo]


class Related(BaseModel):
    id: int
    name: str | None
    description: str | None
    image: str | None
    images: Any  # TODO: obtain real type (list[str])
    name_ru: str | None
    release_count: int | None


class Category(BaseModel):
    id: int
    name: str


class Status(BaseModel):
    id: int
    name: str


class Profile(BaseModel):
    id: int
    login: str | None
    avatar: str | None
    ban_expires: int | None
    ban_reason: str | None
    privilege_level: int | None
    badge_id: Any  # TODO: obtain real type (int)
    badge_name: Any  # TODO: obtain real type (str)
    badge_type: Any  # TODO: obtain real type (int)
    badge_url: Any  # TODO: obtain real type (str)
    is_banned: bool | None
    is_sponsor: bool | None
    is_verified: bool | None


class Comment(BaseModel):
    id: int
    profile: Profile | int | None  # NOTE: jackson feature
    message: str | None
    timestamp: int | None
    type: int | None
    vote: int | None
    release: Release | int | None  # NOTE: jackson feature
    parent_comment_id: int | None
    vote_count: int | None
    likes_count: int | None
    is_spoiler: bool | None
    is_edited: bool | None
    is_deleted: bool | None
    is_reply: bool | None
    reply_count: int | None
    can_like: bool | None


class VideoBanner(BaseModel):
    name: str
    image: str | None
    value: str | None
    action_id: int | None
    is_new: bool | None


class Release(BaseModel):
    field_id: int = Field(..., alias="@id")
    id: int
    poster: str | None
    image: str | None
    year: str | None
    genres: str | None
    country: str | None
    director: str | None
    author: str | None
    translators: str | None
    studio: str | None
    description: str | None
    note: str | None
    related: Related | int | None  # NOTE: jackson feature]
    category: Category | int  # NOTE: jackson feature
    rating: int | None
    grade: float | None
    status: Status | None | int  # NOTE: jackson feature
    duration: int | None
    season: int | None
    broadcast: int | None
    screenshots: list[str] | None
    comments: list[Comment | int]  # NOTE: jackson feature
    title_original: str | None
    title_ru: str | None
    title_alt: str | None
    episodes_released: int | None
    episodes_total: int | None
    release_date: str | None
    vote_1_count: int | None
    vote_2_count: int | None
    vote_3_count: int | None
    vote_4_count: int | None
    vote_5_count: int | None
    vote_count: int | None
    creation_date: int | None
    last_update_date: int | None
    aired_on_date: int | None
    favorites_count: int | None
    watching_count: int | None
    plan_count: int | None
    completed_count: int | None
    hold_on_count: int | None
    dropped_count: int | None
    is_adult: bool | None
    is_play_disabled: bool | None
    is_tpp_disabled: bool | None
    can_video_appeal: bool | None
    can_torlook_search: bool | None
    is_deleted: bool | None
    age_rating: int | None
    your_vote: int | None
    related_count: int | None
    comment_count: int | None
    comments_count: int | None
    collection_count: int | None
    profile_list_status: int | None
    status_id: int | None
    last_view_timestamp: int | None
    last_view_episode: int | None
    is_viewed: bool | None
    is_favorite: bool | None
    is_view_blocked: bool | None
    screenshot_images: list[str]
    related_releases: list[Release | int]  # NOTE: jackson feature
    recommended_releases: list[Release | int]  # NOTE: jackson feature
    episode_last_update: Any  # TODO: obtain real type (timestamp -> int)
    comment_per_day_count: int | None
    video_banners: list[VideoBanner | int]  # NOTE: jackson feature
    profile_release_type_notification_preference_count: int | None
    is_release_type_notifications_enabled: bool | None


class Type(BaseModel):
    field_id: int = Field(..., alias="@id")
    id: int
    name: str
    icon: str | None
    workers: str | None
    is_sub: bool | None
    episodes_count: int | None
    view_count: int | None
    pinned: bool | None


class Source(BaseModel):
    field_id: int = Field(..., alias="@id")
    id: int
    type: Type | int | None  # NOTE: jackson feature
    name: str
    episodes_count: int | None


class Episode(BaseModel):
    field_id: int = Field(..., alias="@id")
    position: int
    release: Release | int  # NOTE: jackson feature
    source: Source | int  # NOTE: jackson feature
    name: str
    url: str
    iframe: bool | None
    addedDate: int | None
    is_filler: bool | None
    is_watched: bool | None


class LinksField(BaseModel):
    Src: str
    Type: str


class Links(BaseModel):
    field_360: LinksField = Field(..., alias="360")
    field_480: LinksField = Field(..., alias="480")
    field_720: LinksField = Field(..., alias="720")


class EpisodeUpdate(BaseModel):
    last_episode_update_date: int
    last_episode_update_name: str
    last_episode_source_update_id: int
    last_episode_source_update_name: str
    last_episode_type_update_id: int
    lastEpisodeTypeUpdateName: str


class AnixartResponse(BaseModel):
    code: int


class ReleaseResponse(AnixartResponse):
    release: Release | None


class EpisodeTypesResponse(AnixartResponse):
    types: list[Type]


class EpisodeSourcesResponse(AnixartResponse):
    sources: list[Source]


class EpisodesResponse(AnixartResponse):
    episodes: list[Episode]


class EpisodeResponse(AnixartResponse):
    episode: Episode | None


class VideoLinksResponse(BaseModel):
    links: Links


class EpisodeUpdatesResponse(AnixartResponse):
    content: list[EpisodeUpdate]
    total_count: int
    total_page_count: int
    current_page: int


class TypeAllResponse(AnixartResponse):
    types: list[Type]


def model_validate_json[ModelType: BaseModel](
    model_type: ModelType,
    json_data: str | bytes | bytearray,
) -> ModelType:
    return model_type.model_validate_json(json_data=json_data)


__all__ = (
    PlaylistVideo,
    Playlist,
    # Data
    Related,
    Category,
    Status,
    Profile,
    Comment,
    VideoBanner,
    Release,
    Type,
    Source,
    Episode,
    LinksField,
    Links,
    EpisodeUpdate,
    # Responses
    AnixartResponse,
    ReleaseResponse,
    EpisodeTypesResponse,
    EpisodeSourcesResponse,
    EpisodesResponse,
    EpisodeResponse,
    VideoLinksResponse,
    EpisodeUpdatesResponse,
    TypeAllResponse,
    # functions
    model_validate_json,
)
