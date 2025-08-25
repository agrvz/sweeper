import click


class OptionRequiredIf(click.Option):
    """
    Custom Click option that is required if another option has a specific value.

    Credit:
    - https://gist.github.com/drorata/1fa68b477d94aea5d37e87aa56e09295
    - https://stackoverflow.com/a/46451650/671013
    """

    def __init__(self, *args, **kwargs) -> None:
        """
        `required_if_option`: the name of the other option that makes this
        option required
        `required_if_value`: the value of the other option that makes this
        option required
        `required_if_value_func`: an optional function that takes the other
        option's value and returns a value to compare against.
        e.g. to make --abbrev required if --name is more than 5 characters:
            @click.option(
                "--abbrev",
                cls=OptionRequiredIf,
                required_if_option="name",
                required_if_value=".csv",
                required_if_option_op=lambda v: v.suffix,
            )
        """
        self.required_if_option = kwargs.pop("required_if_option")
        self.required_if_value = kwargs.pop("required_if_value")
        self.required_if_option_op = kwargs.pop("required_if_option_op", None)

        assert self.required_if_option, "'required_if_option' parameter required"
        assert self.required_if_value, "'required_if_value' parameter required"

        if self.required_if_option_op:
            kwargs["help"] = (
                f"{kwargs.get('help', '')} Option required if {self.required_if_option_op.__name__}(--{self.required_if_option}) is '{self.required_if_value}'"
            ).strip()
        else:
            kwargs["help"] = (
                f"{kwargs.get('help', '')} Option required if --{self.required_if_option} is '{self.required_if_value}'"
            ).strip()
        super(OptionRequiredIf, self).__init__(*args, **kwargs)

    def process_value(self, ctx, value) -> click.Option:
        value = super(OptionRequiredIf, self).process_value(ctx, value)

        if value is None:
            if self.required_if_option_op:
                value_to_check = self.required_if_option_op(
                    ctx.params[self.required_if_option]
                )
                msg = f"Required if {self.required_if_option_op.__name__}(--{self.required_if_option})={self.required_if_value}"
            else:
                value_to_check = ctx.params[self.required_if_option]
                msg = (
                    f"Required if --{self.required_if_option}={self.required_if_value}"
                )

            if value_to_check == self.required_if_value:
                raise click.MissingParameter(ctx=ctx, param=self, message=msg)

        return value
