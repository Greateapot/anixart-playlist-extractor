from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class Related(BaseModel):
    id: int
    name: str
    description: str
    image: str
    images: Any  # TODO: obtain real type (list[str])
    name_ru: str
    release_count: int


class Category(BaseModel):
    id: int
    name: str


class Status(BaseModel):
    id: int
    name: str


class Profile(BaseModel):
    id: int
    login: str
    avatar: str
    ban_expires: int
    ban_reason: str | None
    privilege_level: int
    badge_id: Any  # TODO: obtain real type (int)
    badge_name: Any  # TODO: obtain real type (str)
    badge_type: Any  # TODO: obtain real type (int)
    badge_url: Any  # TODO: obtain real type (str)
    is_banned: bool
    is_sponsor: bool
    is_verified: bool


class Comment(BaseModel):
    id: int
    profile: Profile | int  # NOTE: jackson feature
    message: str
    timestamp: int
    type: int
    vote: int
    release: Release | int  # NOTE: jackson feature
    parent_comment_id: int | None
    vote_count: int
    likes_count: int
    is_spoiler: bool
    is_edited: bool
    is_deleted: bool
    is_reply: bool
    reply_count: int
    can_like: bool


class VideoBanner(BaseModel):
    name: str
    image: str
    value: str
    action_id: int
    is_new: bool


class Release(BaseModel):
    field_id: int = Field(..., alias="@id")
    id: int
    poster: str
    image: str
    year: str | None
    genres: str
    country: str
    director: str | None
    author: str | None
    translators: str | None
    studio: str
    description: str
    note: str | None
    related: Related | int | None  # NOTE: jackson feature]
    category: Category | int  # NOTE: jackson feature
    rating: int
    grade: float
    status: Status | int  # NOTE: jackson feature
    duration: int
    season: int
    broadcast: int
    screenshots: list[str]
    comments: list[Comment | int]  # NOTE: jackson feature
    title_original: str
    title_ru: str
    title_alt: str | None
    episodes_released: int | None
    episodes_total: int | None
    release_date: str | None
    vote_1_count: int
    vote_2_count: int
    vote_3_count: int
    vote_4_count: int
    vote_5_count: int
    vote_count: int
    creation_date: int
    last_update_date: int
    aired_on_date: int
    favorites_count: int
    watching_count: int
    plan_count: int
    completed_count: int
    hold_on_count: int
    dropped_count: int
    is_adult: bool
    is_play_disabled: bool
    is_tpp_disabled: bool
    can_video_appeal: bool
    can_torlook_search: bool
    is_deleted: bool
    age_rating: int
    your_vote: int | None
    related_count: int
    comment_count: int
    comments_count: int
    collection_count: int
    profile_list_status: int | None
    status_id: int
    last_view_timestamp: int
    last_view_episode: int | None
    is_viewed: bool
    is_favorite: bool
    is_view_blocked: bool
    screenshot_images: list[str]
    related_releases: list[Release | int]  # NOTE: jackson feature
    recommended_releases: list[Release | int]  # NOTE: jackson feature
    episode_last_update: Any  # TODO: obtain real type (timestamp -> int)
    comment_per_day_count: int
    video_banners: list[VideoBanner | int]  # NOTE: jackson feature
    profile_release_type_notification_preference_count: int
    is_release_type_notifications_enabled: bool


class Type(BaseModel):
    field_id: int = Field(..., alias="@id")
    id: int
    name: str
    icon: str | None
    workers: str | None
    is_sub: bool
    episodes_count: int
    view_count: int
    pinned: bool


class Source(BaseModel):
    field_id: int = Field(..., alias="@id")
    id: int
    type: Type | int  # NOTE: jackson feature
    name: str
    episodes_count: int


class Episode(BaseModel):
    field_id: int = Field(..., alias="@id")
    position: int
    release: Release | int  # NOTE: jackson feature
    source: Source | int  # NOTE: jackson feature
    name: str
    url: str
    iframe: bool
    addedDate: int
    is_filler: bool
    is_watched: bool


class LinksField(BaseModel):
    Src: str
    Type: str


class Links(BaseModel):
    field_360: LinksField = Field(..., alias="360")
    field_480: LinksField = Field(..., alias="480")
    field_720: LinksField = Field(..., alias="720")


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


def model_validate_json[ModelType: BaseModel](
    model_type: ModelType,
    json_data: str | bytes | bytearray,
) -> ModelType:
    return model_type.model_validate_json(json_data=json_data)


__all__ = (
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
    # Responses
    AnixartResponse,
    ReleaseResponse,
    EpisodeTypesResponse,
    EpisodeSourcesResponse,
    EpisodesResponse,
    EpisodeResponse,
    VideoLinksResponse,
    # functions
    model_validate_json,
)
