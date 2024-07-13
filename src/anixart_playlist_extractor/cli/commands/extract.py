from pathlib import Path
import click

from anixart_playlist_extractor import Quality, extract_playlist


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
    quality: Quality,
    output_dir: Path,
):
    extract_playlist(
        release_id,
        type_id,
        quality=Quality(quality),
        output_dir=str(output_dir),
    )
