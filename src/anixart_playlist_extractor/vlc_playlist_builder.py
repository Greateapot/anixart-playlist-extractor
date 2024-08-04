from jinja2 import Template
from anixart_playlist_extractor.models import Playlist


PLAYLIST_TEMPLATE = Template("""<?xml version="1.0" encoding="UTF-8"?>
<playlist xmlns="http://xspf.org/ns/0/"
	xmlns:vlc="http://www.videolan.org/vlc/playlist/ns/0/" version="1">
	<title>{{ playlist.title }}</title>
	<trackList>

		{% for video in playlist.videos %}
		<track>
			<location>{{ video.location }}</location>
			<title>{{ video.title }}</title>
			<extension application="http://www.videolan.org/vlc/playlist/0">
				<vlc:id>{{ video.id }}</vlc:id>
			</extension>
		</track>
		{% endfor %}

	</trackList>
	<extension application="http://www.videolan.org/vlc/playlist/0">

		{% for video in playlist.videos %}
		<vlc:item tid="{{ video.id }}" />
		{% endfor %}

	</extension>
</playlist>""")


def build_playlist(playlist: Playlist) -> str:
    return PLAYLIST_TEMPLATE.render(playlist=playlist.model_dump())


__all__ = (build_playlist,)
