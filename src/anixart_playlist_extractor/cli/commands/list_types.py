import click

from anixart_playlist_extractor import print_types


@click.command(
    "list-types",
    help="List available types (to get TypeID)",
)
@click.option(
    "-rid",
    "--release-id",
    default=None,
    help="Release ID (if provided, print release types, otherwise, print all types)",
    type=click.INT,
)
@click.option(
    "-pm",
    "--pages-max",
    show_default=True,
    default=2,
    help="Max pages (used for a workaround to get release types)",
    type=click.INT,
)
def command_list_types(
    release_id: int | None = None,
    pages_max: int = 2,
):
    print_types(
        release_id=release_id,
        pages_max=pages_max,
    )
