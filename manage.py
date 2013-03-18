#!/usr/bin/env python
import os
import sys
import sef

if __name__ == "__main__":
    env_file_name = os.path.join(os.path.dirname(__file__), '.env')
    sef.set_defaults(env_file_name)

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
