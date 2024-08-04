import click

from anixart_playlist_extractor.cli.commands import COMMANDS


@click.group()
def cli() -> None: ...


def main():
    for command in COMMANDS:
        cli.add_command(command)
    cli()


if __name__ == "__main__":
    main()
