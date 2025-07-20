import click

from sweeper.draw import draw_command


@click.group()
def sweep():
    pass


sweep.add_command(draw_command)


if __name__ == "__main__":
    sweep()
