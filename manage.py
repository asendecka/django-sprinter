#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    # This is disabled to avoid launching with wrong settings file
    # "Explicit is better than implicit"
    # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sprinter.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
