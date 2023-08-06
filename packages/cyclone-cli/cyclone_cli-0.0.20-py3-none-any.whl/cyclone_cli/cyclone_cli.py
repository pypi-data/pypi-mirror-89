import argparse
from ._version import __version__
import requests
import json


def main(parser=argparse.ArgumentParser()):

    print("Executing 'main()' from my app!")

    subparsers = parser.add_subparsers(help="valid commands", dest="command")

    sub_parser_put = subparsers.add_parser("put")
    sub_parser_put.add_argument(
        "-k", "--key", type=str, help="Unique key to write to.", required=True
    )
    sub_parser_put.add_argument("file", type=str, help="Path to the JSON file to put.")

    version_subparser = subparsers.add_parser("version")

    args = parser.parse_args()

    if args.command is None:
        print("No command detected. Please add --help to see all commands.")
    elif args.command == "put":
        put_command(args.key, args.file)
    elif args.command == "version":
        show_version()


def show_version():
    print(__version__)


def put_command(key: str, file: str):
    with open(file, "r") as f:
        data = json.load(f)
    put(key, data)


def put(key: str, content: dict):
    endpoint = "https://api.cyclonecms.com/putContent"
    request_body = {"key": key, "content": content}
    r = requests.post(endpoint, json=request_body)
    print("Got Response")
    print(r.status_code)
    print(r.json())
