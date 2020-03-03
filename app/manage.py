#!/usr/bin/env python3
import os
import sys

if __name__ == "__main__":
    sys.path.append(os.path.dirname('.'))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
