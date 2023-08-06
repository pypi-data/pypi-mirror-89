import sys

from .release import make_release


if __name__ == "__main__":
    sys.exit(make_release.console_script())
