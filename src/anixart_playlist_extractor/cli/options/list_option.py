import click


class ListOption(click.Option):
    def type_cast_value(self, ctx: click.Context, value: str | None):
        try:
            return (
                None
                if value is None
                else list(map(int, value.replace(" ", "").split(",")))
            )
        except Exception:
            raise click.BadParameter(value)
