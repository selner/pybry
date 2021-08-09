import shutil
import os

import click

def link_if_not_exist(*args, **kwargs):
    print(args)
    print(kwargs)
    if not os.path.isdir(os.path.dirname(args[1])):
        os.makedirs(args[1], exist_ok=True)
    if os.path.isfile(args[1]) or os.path.islink(args[1]):
        return
    os.link(*args, **kwargs)


@click.command()
@click.option("--src", type=click.Path(exists=True, dir_okay=True, file_okay=False, readable=True, resolve_path=True), default=None, help="Source directory")
@click.option("--dest", type=click.Path(exists=False, dir_okay=True, file_okay=False, writable=True, resolve_path=True), prompt="Destination path", help="Where to create the linked files")
def linktree(src, dest):
    """Simple program that greets NAME for a total of COUNT times."""
    click.echo(f"Creating hard links from {src} to {dest}...")
    if not os.path.exists(dest) or not os.path.isdir(dest):
        os.makedirs(dest, exist_ok=True)

    shutil.copytree(src, dest,
                    copy_function=link_if_not_exist, dirs_exist_ok=True)
    click.echo(f"Completed.")
    exit(1)


if __name__ == '__main__':
    linktree()