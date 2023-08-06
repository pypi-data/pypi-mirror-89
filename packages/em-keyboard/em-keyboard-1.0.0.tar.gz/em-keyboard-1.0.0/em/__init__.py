"""em: the technicolor cli emoji keyboard™

Usage:
  em <name>... [--no-copy]
  em -s <name>...

Options:
  -s            Search for emoji.
  -h --help     Show this screen.
  --no-copy     Does not copy emoji to clipboard.

Examples:

  $ em sparkle cake sparkles
  $ em heart

  $ em -s food

Notes:
  - If all names provided map to emojis, the resulting emojis will be
    automatically added to your clipboard.
  - ✨ 🍰 ✨  (sparkles cake sparkles)
"""


import fnmatch
import itertools
import json
import os
import re
import sys
from collections import defaultdict

import xerox
from docopt import docopt

EMOJI_PATH = os.path.join(os.path.dirname(__file__), "emojis.json")
CUSTOM_EMOJI_PATH = os.path.join(os.path.expanduser("~/.emojis.json"))


def parse_emojis(filename=EMOJI_PATH):
    return json.load(open(filename))


def translate(lookup, code):
    output = []
    if code[0] == ":" and code[-1] == ":":
        code = code[1:-1]

    output.append(lookup.get(code, {"char": None})["char"])

    return output


def do_list(lookup, term):
    """Matches term glob against short-name."""

    space = lookup.keys()
    matches = fnmatch.filter(space, term)

    return [(m, translate(lookup, m)) for m in matches]


def do_find(lookup, term):
    """Matches term glob against short-name, keywords and categories."""

    space = defaultdict(list)

    for name in lookup.keys():
        space[name].append(name)

    try:
        iter_lookup = lookup.iteritems()  # Python 2
    except AttributeError:
        iter_lookup = lookup.items()  # Python 3

    for name, definition in iter_lookup:
        for keyword in definition["keywords"]:
            space[keyword].append(name)
        space[definition["category"]].append(name)

    matches = fnmatch.filter(space.keys(), term)

    results = set()
    for match in matches:
        results.update(space[match])

    return [(r, translate(lookup, r)) for r in results]


def clean_name(name):
    """Clean emoji name replacing specials chars by underscore"""
    special_chars = "[-. ]"  # square brackets are part of the regex
    return re.sub(special_chars, "_", name)


def cli():
    # CLI argument parsing.
    arguments = docopt(__doc__)
    names = tuple(map(clean_name, arguments["<name>"]))
    no_copy = arguments["--no-copy"]

    # Marker for if the given emoji isn't found.
    missing = False

    # Grab the lookup dictionary.
    lookup = parse_emojis()

    if os.path.isfile(CUSTOM_EMOJI_PATH):
        lookup.update(parse_emojis(CUSTOM_EMOJI_PATH))

    # Search mode.
    if arguments["-s"]:

        # Lookup the search term.
        found = do_find(lookup, names[0])

        # print them to the screen.
        for (n, v) in found:
            # Some registered emoji have no value.
            try:
                print("{}  {}".format(" ".join(v), n))
            # Sometimes, an emoji will have no value.
            except TypeError:
                pass

        return sys.exit(0)

    # Process the results.
    results = (translate(lookup, name) for name in names)
    results = list(itertools.chain.from_iterable(results))

    if None in results:
        no_copy = True
        missing = True
        results = (r for r in results if r)

    # Prepare the result strings.
    print_results = " ".join(results)
    results = "".join(results)

    # Copy the results (and say so!) to the clipboard.
    if not no_copy and not missing:
        xerox.copy(results)
        print(f"Copied! {print_results}")

    # Script-kiddies.
    else:
        print(print_results)

    sys.exit(int(missing))


if __name__ == "__main__":
    cli()
