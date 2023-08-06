# Copyright 2019-2020 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""Module for parsing and modifying sets such as @world"""

import os
from typing import Optional, Set

from portmod.atom import Atom, atom_sat
from portmod.globals import env
from portmod.repo.profiles import get_system

BUILTIN_SETS = {
    "world",
    "selected",
    "system",
    "selected-packages",
    "selected-sets",
    "rebuild",
    "modules",
}


def is_selected(atom):
    """
    Returns true if and only if a mod is selected

    selected mods are either system mods, or included in the world file
    """
    selected = get_set("world") | get_system()
    for selatom in selected:
        if atom_sat(atom, selatom):
            return True
    return False


def get_set(mod_set: str, parent_dir: Optional[str] = None) -> Set[Atom]:
    if mod_set == "world":
        return get_set("system") | get_set("selected")
    if mod_set == "selected":
        return get_set("selected-packages") | get_set("selected-sets")
    elif mod_set == "system":
        return get_system()

    if parent_dir is None:
        parent_dir = env.prefix().SET_DIR

    if mod_set == "selected-packages":
        set_file = os.path.join(env.prefix().PORTMOD_LOCAL_DIR, "world")
    elif mod_set == "selected-sets":
        set_file = os.path.join(env.prefix().PORTMOD_LOCAL_DIR, "world_sets")
    elif mod_set in ("rebuild", "modules"):
        set_file = os.path.join(env.prefix().PORTMOD_LOCAL_DIR, mod_set)
    else:
        set_file = os.path.join(parent_dir, mod_set)
    if os.path.exists(set_file):
        with open(set_file, "r") as file:
            return {Atom(s) for s in file.read().splitlines()}
    return set()


def add_set(mod_set: str, atom: Atom, parent_dir: Optional[str] = None):
    if parent_dir is None:
        parent_dir = env.prefix().SET_DIR

    if mod_set == "selected-packages":
        set_file = os.path.join(env.prefix().PORTMOD_LOCAL_DIR, "world")
    elif mod_set == "selected-sets":
        set_file = os.path.join(env.prefix().PORTMOD_LOCAL_DIR, "world_sets")
    elif mod_set in ("rebuild", "modules"):
        set_file = os.path.join(env.prefix().PORTMOD_LOCAL_DIR, mod_set)
    else:
        set_file = os.path.join(parent_dir, mod_set)
    os.makedirs(env.prefix().SET_DIR, exist_ok=True)
    if os.path.exists(set_file):
        with open(set_file, "r+") as file:
            for line in file:
                if atom in line:
                    break
            else:
                print(atom, file=file)
    else:
        with open(set_file, "a+") as file:
            print(atom, file=file)


def remove_set(mod_set: str, atom: Atom, parent_dir: Optional[str] = None):
    if mod_set == "world" or mod_set == "rebuild":
        parent_dir = env.prefix().PORTMOD_LOCAL_DIR
    elif parent_dir is None:
        parent_dir = env.prefix().SET_DIR

    set_file = os.path.join(parent_dir, mod_set)
    if os.path.exists(set_file):
        with open(set_file, "r+") as f:
            new_f = f.readlines()
            f.seek(0)
            for line in new_f:
                if atom not in line:
                    f.write(line)
            f.truncate()
