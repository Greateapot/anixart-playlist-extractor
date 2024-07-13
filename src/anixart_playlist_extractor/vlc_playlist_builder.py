_track_pattern = """
		<track>
			<location>{location}</location>
			<title>{title}</title>
			<extension application="http://www.videolan.org/vlc/playlist/0">
				<vlc:id>{track_id}</vlc:id>
			</extension>
		</track>
""".strip("\n")

_track_list_pattern = """
	<trackList>
{tracks}
	</trackList>
""".strip("\n")

_item_pattern = """
		<vlc:item tid="{track_id}"/>
""".strip("\n")

_queue_pattern = """
	<extension application="http://www.videolan.org/vlc/playlist/0">
{items}
	</extension>
""".strip("\n")

_playlist_pattern = """
<?xml version="1.0" encoding="UTF-8"?>
<playlist xmlns="http://xspf.org/ns/0/" xmlns:vlc="http://www.videolan.org/vlc/playlist/ns/0/" version="1">
	<title>{playlist_title}</title>
{track_list}
{queue}
</playlist>
""".strip("\n")


def build_playlist(
    video_links: dict[str, str],
    playlist_title: str,
) -> str:
    tracks = []
    items = []

    for track_id, (title, location) in enumerate(video_links.items()):
        tracks.append(
            _track_pattern.format(
                track_id=track_id,
                title=title,
                location=location,
            )
        )
        items.append(
            _item_pattern.format(
                track_id=track_id,
            )
        )

    track_list = _track_list_pattern.format(
        tracks="\n".join(tracks),
    )
    queue = _queue_pattern.format(
        items="\n".join(items),
    )

    return _playlist_pattern.format(
        playlist_title=playlist_title,
        track_list=track_list,
        queue=queue,
    )


__all__ = (build_playlist,)
