#!/usr/bin/env python
# pylint: disable=C0415
import os
import sys


def main() -> None:
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
    os.environ.setdefault("DJANGO_CONFIGURATION", "Base")

    from configurations import (  # pylint: disable=import-outside-toplevel
        management,
    )
    from django.conf import settings

    if settings.DEBUG:
        # configuration to debug contenerized app
        if os.environ.get("RUN_MAIN") or os.environ.get("WERKZEUG_RUN_MAIN"):
            import debugpy  # pylint: disable=import-outside-toplevel

            debugpy.listen(("0.0.0.0", 3030))  # nosec
            print("Attached!")

    management.execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
