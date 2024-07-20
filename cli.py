import argparse
from injector import inject_dll

def handle_cli():
    parser = argparse.ArgumentParser(description="DLL Injector CLI")
    parser.add_argument('-p', '--pid', type=int, required=True, help="Process ID to inject the DLL into")
    parser.add_argument('-d', '--dll', type=str, required=True, help="Path to the DLL to inject")
    args = parser.parse_args()

    if inject_dll(args.pid, args.dll):
        print(f"Successfully injected {args.dll} into process {args.pid}")
    else:
        print(f"Failed to inject {args.dll} into process {args.pid}")
