"""An actual generation check, not a stub or a success-only health check."""
import argparse
from project.engine import get_engine


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--language', choices=['pt', 'en'], default='en')
    parser.add_argument('--context', default='Once upon a time, a traveller discovered a mysterious castle.')
    args = parser.parse_args()
    choices = get_engine().generate(args.context, args.language)
    assert len(choices) == 3 and all(t.strip() for t in choices)
    for i, text in enumerate(choices, 1):
        print(f'\n{i}. {text}')


if __name__ == '__main__':
    main()
