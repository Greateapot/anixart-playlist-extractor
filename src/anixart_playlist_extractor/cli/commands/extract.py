from pathlib import Path
import click

from anixart_playlist_extractor import Quality, extract_playlist
from anixart_playlist_extractor.cli.options import ListOption


@click.command(
    "extract",
    help="Extract release as .xspf (vlc) playlist with given Release ID and Type ID",
)
@click.option(
    "-rid",
    "--release-id",
    required=True,
    help="Release ID",
    type=click.INT,
)
@click.option(
    "-tid",
    "--type-id",
    required=True,
    help="Type ID",
    type=click.INT,
)
@click.option(
    "-L",
    "--extract-last",
    show_default=True,
    default=False,
    help="Extract only last episode",
    is_flag=True,
)
@click.option(
    "-O",
    "--extract-only",
    show_default=True,
    default=None,
    help="Extract only provided positions (starts with 1; ignored with --last option)",
    cls=ListOption,
)
@click.option(
    "-q",
    "--quality",
    show_default=True,
    default=Quality.q720.value,
    help="Video quality",
    type=click.Choice(
        [quality.value for quality in Quality],
        case_sensitive=False,
    ),
)
@click.option(
    "-o",
    "--output-dir",
    show_default=True,
    default="output",
    help="Directory to save the output playlist",
    type=click.Path(file_okay=False, path_type=Path),
)
def command_extract(
    release_id: int,
    type_id: int,
    extract_only: list[int] | None,
    extract_last: bool | None,
    quality: Quality,
    output_dir: Path,
):
    extract_playlist(
        release_id,
        type_id,
        extract_only=extract_only,
        extract_last=extract_last,
        quality=Quality(quality),
        output_dir=str(output_dir),
    )
