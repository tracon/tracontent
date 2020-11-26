#!/usr/bin/env python
import os
import sys
from django.urls import re_path

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tracontent.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
