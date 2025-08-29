from copy import deepcopy
from typing import Any

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
        `required_if_value`: [optional] the value of the other option that makes this
        option required. If not passed, `required_if_option` just needs to be passed to
        make this option required (i.e. regardless of its value).
        `required_if_value_transform`: [optiona] a function to apply to the other
        option's value, returning a value to compare against.
        `required_if_value_check`: [optiona] a function to apply to the other
        option's value, asserting True or False. True means this option is required.

        Examples:

        1. Make --abbrev required if --name is more than 5 characters:
            @click.option(
                "--abbrev",
                cls=OptionRequiredIf,
                required_if_option="name",
                required_if_value_check=lambda x: len(x) > 5,
            )

        2. Make --abbrev required if the value of --name, when transformed to
           UPPERCASE, is "JOHN":
            @click.option(
                "--abbrev",
                cls=OptionRequiredIf,
                required_if_option="name",
                required_if_value="JOHN",
                required_if_value_transform=lambda x: x.upper(),
            )
        """
        self.required_if_option = kwargs.pop("required_if_option")
        self.required_if_value = kwargs.pop("required_if_value", None)
        self.required_if_value_transform = kwargs.pop(
            "required_if_value_transform", None
        )
        self.required_if_value_check = kwargs.pop("required_if_value_check", None)

        assert self.required_if_option, "'required_if_option' parameter required"
        if self.required_if_value_transform:
            assert self.required_if_value, (
                "'required_if_value' parameter required if using 'required_if_value_transform'"
            )

        if self.required_if_value_transform:
            kwargs["help"] = (
                f"{kwargs.get('help', '')} Option required if {self.required_if_value_transform.__name__}(--{self.required_if_option}) is '{self.required_if_value}'"
            ).strip()
        elif self.required_if_value_check:
            kwargs["help"] = (
                f"{kwargs.get('help', '')} Option required if {self.required_if_value_check.__name__}(--{self.required_if_option}) is True"
            ).strip()
        else:
            kwargs["help"] = (
                f"{kwargs.get('help', '')} Option required if --{self.required_if_option} is '{self.required_if_value}'"
            ).strip()
        super(OptionRequiredIf, self).__init__(*args, **kwargs)

    def should_be_required(
        self, required_if_option: str, other_option_value: Any
    ) -> bool:
        """
        Determine if this option (self) should be required based on the other
        option's value.

        Logic as follows:
            1. If there's a transform, do that first
            2. If there's a check, do that and return bool
            3. Else if there's a value to compare against, compare and return bool
            4. If there's none of the above, return True if the option is set
        """
        actual_value = deepcopy(other_option_value)

        if self.required_if_transform is not None:
            actual_value = self.required_if_transform(actual_value)

        if self.required_if_value_check is not None:
            return self.required_if_value_check(actual_value)

        if self.required_if_value is not None:
            return actual_value == self.required_if_value

        if required_if_option is not None:
            return True

    def process_value(self, ctx, value) -> click.Option:
        """
        Override `process_value` to add custom required logic.

        Logic to determine if this option (self) should be required based on the other
        option's value:
            1. If there's a transform, do that first
            2. If there's a boolean check, do that and raise MissingParameter
               if True
            3. Else if there's a value to compare against, do the comparison and raise
               MissingParameter if they match
            4. If there's none of the above, raise MissingParameter if the option is set
               regardless of its value
        """
        value = super(OptionRequiredIf, self).process_value(ctx, value)

        if value is None:
            if self.required_if_value_transform is not None:
                actual_value = self.required_if_value_transform(
                    ctx.params[self.required_if_option]
                )
                msg = f"Required if {self.required_if_value_transform.__name__}(--{self.required_if_option})={self.required_if_value}"

                if actual_value == self.required_if_value:
                    raise click.MissingParameter(ctx=ctx, param=self, message=msg)

            elif self.required_if_value_check is not None:
                value_to_check = ctx.params[self.required_if_option]
                msg = f"Required if {self.required_if_value_check.__name__}(--{self.required_if_option}) is True"

                value_meets_criteria = self.required_if_value_check(value_to_check)
                if value_meets_criteria:
                    raise click.MissingParameter(ctx=ctx, param=self, message=msg)

            elif self.required_if_value is not None:
                value_to_check = ctx.params[self.required_if_option]
                msg = (
                    f"Required if --{self.required_if_option}={self.required_if_value}"
                )
                if value_to_check == self.required_if_value:
                    raise click.MissingParameter(ctx=ctx, param=self, message=msg)

            elif self.required_if_option is not None:
                msg = f"Required if --{self.required_if_option} is passed"
                raise click.MissingParameter(ctx=ctx, param=self, message=msg)

        return value
