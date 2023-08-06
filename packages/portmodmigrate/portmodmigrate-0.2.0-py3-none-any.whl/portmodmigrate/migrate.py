# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

import argparse
import os
import sys
from fnmatch import fnmatch
from functools import lru_cache, total_ordering
from logging import warning
from queue import PriorityQueue
from types import SimpleNamespace
from typing import Any, Dict, List, Set

from fuzzywuzzy import fuzz
from portmod.colour import green
from portmod.config import get_config
from portmod.download import get_filename
from portmod.fs.util import get_hash
from portmod.globals import env
from portmod.loader import load_all
from portmod.merge import configure
from portmod.parsers.list import read_list
from portmod.parsers.manifest import HashAlg
from portmod.prefix import get_prefixes
from portmod.prompt import prompt_bool, prompt_num
from portmod.query import display_search_results

from .datadir import find_esp_bsa


def find_config(config: List[str], pattern: str) -> List[str]:
    """
    Returns elements in the config matching the given pattern

    Pattern can include wildcards as defined by fnmatch
    """
    results = []
    for line in config:
        if fnmatch(line, pattern):
            results.append(line)
    return results


def remove_config(config: List[str], pattern: str):
    """
    Removes elements in the config matching the given pattern

    Pattern can include wildcards as defined by fnmatch
    """
    to_remove = set(find_config(config, pattern))

    for index, line in reversed(list(enumerate(config))):
        if line in to_remove:
            del config[index]


@total_ordering
class PrioritizedItem(SimpleNamespace):
    priority: int
    item: Any

    def __init__(self, priority, item):
        self.priority = priority
        self.item = item

    def __lt__(self, other):
        return self.priority < other.priority


def import_archives(args):
    # Create mapping of hashes to file names
    hashes: Dict[HashAlg, Dict[str, str]] = {}
    for prefix in get_prefixes():
        env.set_prefix(prefix)
        sources = list(
            [
                source
                for mod in load_all()
                for source in mod.get_sources([], [], matchall=True)
            ]
        )
        for alg in HashAlg:
            hashes[alg] = {}
        seen = set()
        for source in sources:
            for alg, value in source.hashes.items():
                seen.add(alg)
                hashes[alg][value] = source.name
        seen_tuple = tuple(sorted(seen))

    # Hash each file in the given directory. If it is in our map, rename it
    roots = args.directory or [os.getcwd(), env.DOWNLOAD_DIR]
    files = []
    for root in roots:
        files += os.listdir(root)
    for file in files:
        path = os.path.join(root, file)
        if os.path.isfile(path):
            source_hashes = get_hash(path, seen_tuple)
            for index, alg in enumerate(seen_tuple):
                source_hash = source_hashes[index]
                if source_hash in hashes[alg]:
                    dest = get_filename(hashes[alg][source_hash])
                    if not os.path.exists(dest):
                        print("Moving {} -> {}".format(path, dest))
                        if not args.pretend:
                            os.rename(path, dest)
                    else:
                        print("Skipping {}. Already in cache".format(path))
                    break
    if args.pretend:
        warning(
            "The above changes have not actually been applied. "
            "To apply these changes, rerun the command without the --pretend flag"
        )


def scan_installed(args):
    env.set_prefix(args.prefix)
    if get_prefixes()[args.prefix] not in {"openmw", "tes3mp"}:
        raise Exception(
            "Architectures other than openmw and tes3mp are not currently "
            "supported for scanning"
        )

    for config_dir in os.path.expanduser(get_config()["OPENMW_CONFIG_DIR"]).split(":"):
        configpath = os.path.join(config_dir, "openmw.cfg")
        if os.path.exists(configpath):
            break
    config = read_list(configpath)
    mods = []
    ambiguousmods = []
    fuzzymods = []
    ambiguousfuzzymods = []

    # Try to find possible replacement mods in the repo
    for path in find_config(config, "data=*"):
        path = path.replace("data=", "")
        fullpath = os.path.normpath(os.path.expanduser(path)).lstrip('"').rstrip('"')
        if not fullpath.startswith(env.prefix().PACKAGE_DIR):
            modq = find_mod(fullpath)
            if isinstance(modq, list):
                if len(modq) == 1:
                    mods.append((path, modq[0].item))
                elif len(modq) > 1:
                    if args.interactive:
                        result = prompt_mods(path, modq)
                        if result is not None:
                            mods.append(result)
                    else:
                        ambiguousmods.append((path, modq[0].item))
                elif args.fuzzy:
                    fuzzymodq = find_fuzzy_mod(fullpath)
                    if len(fuzzymodq) > 1:
                        if args.interactive:
                            result = prompt_mods(path, fuzzymodq)
                            if result is not None:
                                fuzzymods.append(result)
                        elif len(fuzzymodq) == 1:
                            fuzzymods.append((path, fuzzymodq[0].item))
                        else:
                            ambiguousfuzzymods.append((path, fuzzymodq[0].item))
                    else:
                        warning("Could not find mod in repo for {}".format(path))
                else:
                    warning("Could not find mod in repo for {}".format(path))
            else:  # Is a pybuild that perfectly matched the directory
                mods.append((path, modq))

    # Present changes to user and prompt them to apply them automatically
    # Also print command in case they want to install the mods manually
    modnames = []
    paths = []

    print()

    if mods:
        print(
            "The following mods matched unambiguously "
            "using plugin and archive file names:"
        )

        for (path, mod) in mods:
            print("{} : {}".format(green(mod.ATOM), path))
            modnames.append(mod.ATOM.CPN)
            paths.append(path)

    if ambiguousmods:
        warning(
            "The following mods matched ambiguously using plugin and archive "
            "file names. Double check this list before continuing, or rerun with "
            "--interactive if you would like to check the other possible matches"
        )
        for (path, mod) in ambiguousmods:
            print("{} : {}".format(green(mod.ATOM), path))
            modnames.append(mod.ATOM.CPN)
            paths.append(path)

    if fuzzymods:
        warning(
            "The following mods matched unambiguously using fuzzy search on their "
            "directory name. Double check these before continuing."
        )
        for (path, mod) in fuzzymods:
            print("{} : {}".format(green(mod.ATOM), path))
            modnames.append(mod.ATOM.CPN)
            paths.append(path)

    if ambiguousfuzzymods:
        warning(
            "The following mods matched ambiguously using fuzzy search on their "
            "directory name. Double check this list before continuing, or rerun "
            "with --interactive if you would like to check the other possible "
            "matches"
        )
        for (path, mod) in ambiguousfuzzymods:
            print("{} : {}".format(green(mod.ATOM), path))
            modnames.append(mod.ATOM.CPN)
            paths.append(path)

    command = f"portmod {args.prefix} merge "
    command += " ".join(modnames)

    if not modnames:
        print("Nothing to do.")
        return

    # If interactive, prompt to install mods,
    # removing outdated lines from the config
    if args.interactive:
        if prompt_bool(
            "Would you like to replace the above manually installed mods "
            "with the ones in the repository?"
        ):

            config = read_list(configpath)
            for path in paths:
                remove_config(config, f"data=*{path}*")

            with open(configpath, "w") as file:
                for line in config:
                    print(line, file=file)
            configure(modnames, update=True, newuse=True, noreplace=True)
    else:
        print('To install these mods, run "{}"'.format(command))


def migrate():
    parser = argparse.ArgumentParser(
        description="Command line tool for migrating mod setup to portmod"
    )
    subparsers = parser.add_subparsers()
    archive_parser = subparsers.add_parser(
        "import-archives",
        help="Imports archives from a given directory. If directory is not specified,"
        "looks for them in both the current directory and the cache directory",
    )
    archive_parser.add_argument(
        "directory",
        help="Directories to search when importing archives",
        nargs="*",
    )
    archive_parser.add_argument(
        "--pretend",
        help="Instead of committing changes, just show what would have been done",
        action="store_true",
    )
    archive_parser.set_defaults(func=import_archives)
    scan_parser = subparsers.add_parser(
        "scan-installed",
        help="Scans mods installed manually and creates a list of packages in the repository "
        "that would satisfy as many mods as possible. If run with the interactive "
        "option, prompts to handle ambiguous mods and also prompts to install them",
    )
    scan_parser.add_argument(
        "prefix",
        help="Name of the portmod prefix you want to use. You may need to create a prefix "
        "if you do not already have one. See the portmod installation guide for details.",
        choices=list(get_prefixes().keys()),
    )
    scan_parser.add_argument(
        "--interactive", help="Resolve ambiguity interactively", action="store_true"
    )
    scan_parser.add_argument(
        "--fuzzy",
        help="Does fuzzy matching when scanning mods (experimental)",
        action="store_true",
    )
    scan_parser.set_defaults(func=scan_installed)

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(2)

    args.func(args)


def prompt_mods(path, modlist):
    """
    Prompts the user to select from a list of mods that may match
    the mod installed at the given path
    """
    desc = (
        "The above mods partially matched the mod "
        "installed at {}. Higher priority means closer match.\n"
        "Which would you like to select? 0 - {}, "
        "or -1 to select none".format(path, len(modlist) - 1)
    )

    i = 0
    for pitem in modlist:
        print("{}) Priority: {}".format(i, 100 - pitem.priority))
        display_search_results([pitem.item], summarize=False)
        i += 1

    index = prompt_num(desc, len(modlist), cancel=True)
    if index == -1:
        return None
    return (path, modlist[index].item)


@lru_cache(maxsize=None)
def get_plugin_map():
    """Returns a map of File names (plugins and archives) to the mod containing them"""
    mod_files = {}
    for mod in load_all():
        mod_files[
            frozenset(
                [file.NAME for idir in mod.INSTALL_DIRS for file in idir.get_files()]
            )
        ] = mod
    return mod_files


def find_mod(path):
    """
    Determines possible mods installed at the given path
    using the contained plugin files
    """
    # Collect esps and bsas in directory (recursively)
    files: Set[str] = set()
    for root, _, _ in os.walk(path):
        esps, bsas = find_esp_bsa(root)
        files |= set(esps)
        files |= set(bsas)

    frozen_files = frozenset(files)

    if not frozen_files:
        return []

    # Find mods matching the given files
    # If we only find a perfect match, return immediately. This is f
    mod_files = get_plugin_map()
    if mod_files.get(frozen_files) is not None:
        return mod_files[frozen_files]

    modq: PriorityQueue = PriorityQueue()
    for key in mod_files:
        length = len(frozen_files.intersection(key))
        if length > 0:
            modq.put(PrioritizedItem(len(frozen_files) - length, mod_files[key]))

    results = []
    result_atoms: Set[str] = set()
    while not modq.empty():
        mod = modq.get()
        if mod.item.CPN not in result_atoms:
            results.append(mod)
            result_atoms.add(mod.item.CPN)
    return results


def find_fuzzy_mod(path):
    """
    Determines possible mods installed at the given path using fuzzy search
    on the directory name
    """
    name = os.path.basename(path).rstrip('"')
    modq: PriorityQueue = PriorityQueue()
    seen: Set[str] = set()
    for mod in load_all():
        match = fuzz.token_set_ratio(name, mod.NAME)
        # PriorityQueues work on lowest items, so reverse the value
        if mod.ATOM.CM not in seen:
            modq.put(PrioritizedItem(100 - match, mod))
            seen.add(mod.ATOM.CM)

    # If any matches are greater than 90%, return them
    results = []
    result_atoms: Set[str] = set()

    nextentry = modq.get()

    def get_next():
        nonlocal nextentry
        nonlocal modq
        nonlocal result_atoms
        while nextentry.item.CPN in result_atoms and not modq.empty():
            nextentry = modq.get()

    while nextentry.priority <= 10 and not modq.empty():
        results.append(nextentry)
        result_atoms.add(nextentry.item.CPN)
        get_next()

    if modq.empty() and nextentry.priority <= 10:
        results.append(nextentry)
        result_atoms.add(nextentry.item.CPN)

    # Otherwise, return best 5 that are greater than 50%
    # to avoid overwhelming user with weak matches
    threshold = 50
    if not results:
        i = 5
        if nextentry.priority <= threshold and nextentry.item.CPN not in result_atoms:
            results.append(nextentry)
            result_atoms.add(nextentry.item.CPN)
            get_next()
            i -= 1

        while i > 0 and nextentry.priority <= threshold and not modq.empty():
            results.append(nextentry)
            result_atoms.add(nextentry.item.CPN)
            get_next()
            i -= 1

        if i > 0 and nextentry.priority <= threshold and modq.empty():
            results.append(nextentry)
            result_atoms.add(nextentry.item.CPN)

    return results
