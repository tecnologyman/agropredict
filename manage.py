#!/usr/bin/env python
<<<<<<< HEAD
import os
import sys
=======
import os, sys
>>>>>>> 1929edb89119ee1b7292b948c6f40e50284b9889

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agropredict_project.settings')
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
