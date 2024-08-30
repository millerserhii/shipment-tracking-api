import os


def plugin() -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
    os.environ.setdefault("DJANGO_CONFIGURATION", "Base")

    from configurations import (  # pylint: disable=import-outside-toplevel
        importer,
    )

    importer.install()


if __name__ == "<run_path>":
    plugin()
