#!/usr/bin/python
"""
This is a script to take a court opinion or other text file and insert appropriate hyperlinks to any referenced statutory provision. Requires citation-schemas.yml, which must exist in the same directory as citeurl.py."""

# python standard imports
from argparse import ArgumentParser

# internal imports
from . import lookup_query, insert_links, load_schemas

def main():
    p = ArgumentParser(description=__doc__)
    p.add_argument(
        "text", help="a string containing legal citations", nargs="*"
    )
    p.add_argument("-i", "--input", help="the file to read from")
    p.add_argument(
        "-o",
        "--output",
        help="the file to write to. Defaults to standard output",
    )
    p.add_argument(
        "-l",
        "--lookup",
        action="store_true",
        help=(
            "return URL for a single citation instead of inserting links"
            + "into a body of text. Uses broader regex if available"
        ),
    )
    p.add_argument(
        "-s",
        "--supplemental-yaml",
        help="specify a YAML file with additional citation schemas",
    )
    args = p.parse_args()
    if args.supplemental_yaml:
        load_schemas(args.supplemental_yaml)
    if args.input:
        with open(args.input, "r") as f:
            query = f.read()
    else:
        query = " ".join(args.text)
    if args.lookup:
        print(lookup_query(query))
    elif args.output:
        with open(args.output, "w") as f:
            f.write(insert_links(query))
    else:
        print(insert_links(query))

if __name__ == "__main__":
    main()
