import click

from anixart_playlist_extractor.cli.commands import commands


@click.group()
def cli() -> None: ...


def main():
    for command in commands:
        cli.add_command(command)
    cli()


if __name__ == "__main__":
    main()
