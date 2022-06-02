import argparse
import logging
import subprocess
import sys
from pathlib import Path
from re import findall

from termcolor import colored


class vnu:

    installed_versions = []
    verbosity = 0

    def __init__(self, args):
        if args.list:
            print(colored("Currently installed versions:", "yellow"))
            self.get_installed_versions(show=True)
            exit()
        if args.version != None:
            if self.uninstall(args.version):
                print(colored("✌️ Success!", "green", attrs=["bold"]))

    def get_installed_versions(self, show: bool = False) -> list:
        versions = subprocess.run(
            ["volta", "list", "node", "--format", "plain"],
            capture_output=True,
            text=True,
        )
        logging.info(versions.stdout)
        versions = findall(r"node@([0-9.]+)", versions.stdout)
        if show:
            print("\n".join(versions))
        else:
            return versions

    def uninstall(self, version: str):
        print(f"Checking if version {version} exists...")
        if version in self.get_installed_versions():
            print(f"Removing Node v{version}")
            remove_image = subprocess.run(
                [
                    "fd",
                    "-td",
                    f"{version}",
                    f"{Path.home()}/.volta/tools/image/node",
                    "-X",
                    "rm",
                    "-r",
                ]
            )
            logging.info(f"{' '.join(remove_image.args)}")
            remove_archives = subprocess.run(
                [
                    "fd",
                    "-tf",
                    f"v{version}",
                    f"{Path.home()}/.volta/tools/inventory/node",
                    "-X",
                    "rm",
                    "-r",
                ]
            )
            logging.info(f"{' '.join(remove_archives.args)}")
            return remove_image and remove_archives
        else:
            print(
                colored(f"❌ Version {version} is not installed!", "red", attrs=["bold"])
            )


parser = argparse.ArgumentParser()

parser.add_argument("-v", "--verbose", action="store_true")
parser.add_argument("-V", "--version", type=str, help="Version to uninstall")
parser.add_argument(
    "-l", "--list", help="List all installed versions", action="store_true"
)

args = parser.parse_args()
print(colored("VNU (Volta Node Uninstaller)", "green"))
if len(sys.argv) <= 1:
    parser.print_help()
    exit()
vnu(args)
