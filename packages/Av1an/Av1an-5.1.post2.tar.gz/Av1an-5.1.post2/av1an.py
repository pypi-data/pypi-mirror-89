#!/usr/bin/env python3

from av1an import Args
from manager import Manager
from startup.setup import startup_check

def main():
    parser = Args()
    project = parser.get_project()
    startup_check(project)
    manager = Manager.Main(project)
    manager.run()

if __name__ == '__main__':
    main()
