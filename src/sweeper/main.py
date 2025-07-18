import click

from sweeper.draw import draw


@click.group()
def sweep():
    pass


sweep.add_command(draw)
