import sys
from gui import run_gui
from cli import handle_cli
from config import elevate_privileges

if __name__ == '__main__':
    if len(sys.argv) > 1:
        elevate_privileges()
        handle_cli()
    else:
        elevate_privileges()
        run_gui()
