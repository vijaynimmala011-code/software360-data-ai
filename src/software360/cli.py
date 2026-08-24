import argparse

from software360.common.config import load_settings


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="software360")
    parser.add_argument("command", choices=["generate-data", "show-config"])
    return parser


def main() -> None:
    args = build_parser().parse_args()
    settings = load_settings()
    if args.command == "show-config":
        print(settings.model_dump())
    elif args.command == "generate-data":
        from software360.data.generate import generate_all

        generate_all()


if __name__ == "__main__":
    main()
