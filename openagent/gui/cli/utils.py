import os

import click


def check_file(target: str):
    # Define accepted file extensions for Gui
    ACCEPTED_FILE_EXTENSIONS = ("py", "py3")

    _, extension = os.path.splitext(target)

    # Check file extension
    if extension[1:] not in ACCEPTED_FILE_EXTENSIONS:
        if extension[1:] == "":
            raise click.BadArgumentUsage(
                "Gui requires raw Python (.py) files, but the provided file has no extension."
            )
        else:
            raise click.BadArgumentUsage(
                f"Gui requires raw Python (.py) files, not {extension}."
            )

    if not os.path.exists(target):
        raise click.BadParameter(f"File does not exist: {target}")
