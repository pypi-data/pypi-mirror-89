# Copyright 2019-2020 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Quality assurance for the mod repo
"""

import argparse
import glob
import os
import re
import sys
import traceback
from logging import error

from portmod.atom import Atom
from portmod.globals import env
from portmod.loader import SandboxedError
from portmod.log import add_logging_arguments, init_logger
from portmod.news import validate_news
from portmod.parsers.list import read_list
from portmod.portmod import (
    parse_category_metadata,
    parse_groups,
    parse_yaml_dict,
    parse_yaml_dict_dict,
)
from portmod.repo import Repo, get_repo_name, get_repo_root
from portmod.repo.metadata import get_categories, license_exists

from .pybuild import pybuild_manifest, pybuild_validate


def scan(repo_root, err):
    # Run pybuild validate on every pybuild in repo
    for category in get_categories(repo_root):
        for directory in glob.glob(os.path.join(repo_root, category, "*")):
            if (
                os.path.isdir(directory)
                and Atom(os.path.basename(directory)).PV is not None
            ):
                err(f"Package name {directory} must not end in a version")
        for file in glob.glob(os.path.join(repo_root, category, "*", "*.pybuild")):
            dir_name = os.path.basename(os.path.dirname(file))
            file_name = Atom(os.path.splitext(os.path.basename(file))[0]).PN
            if dir_name != file_name:
                err(
                    f"The package name in filename {file} should match its parent directory's name!"
                )

            try:
                pybuild_validate(file)
            except SandboxedError as e:
                err(f"{e}")
            except Exception as e:
                traceback.print_exc()
                err(f"{e}")

    for category in get_categories(repo_root):
        # Note: Package metadata is already validated as part of pybuild_validate
        for file in glob.glob(os.path.join(repo_root, category, "metadata.yaml")):
            try:
                parse_category_metadata(file)
            except Exception as e:
                traceback.print_exc()
                err("{}".format(e))

    # Check files in metadata and profiles.
    # These may not exist, as they might be inherited from another repo instead

    # Check profiles/arch.list
    path = os.path.join(repo_root, "profiles", "arch.list")
    if os.path.exists(path):
        archs = read_list(path)
        for arch in archs:
            if " " in arch:
                err(
                    f'arch.list: in entry "{arch}". '
                    "Architectures cannot contain spaces"
                )

    # Check profiles/categories
    path = os.path.join(repo_root, "profiles", "categories")
    if os.path.exists(path):
        lines = read_list(path)
        for category in lines:
            if " " in category:
                err(
                    f'categories.list: in category "{category}". '
                    "Categories cannot contain spaces"
                )

    # Check metadata/groups.yaml
    path = os.path.join(repo_root, "metadata", "groups.yaml")
    if os.path.exists(path):
        parse_groups(path)

    # Check metadata/license_groups.yaml
    # All licenses should exist in licenses/LICENSE_NAME
    path = os.path.join(repo_root, "profiles", "license_groups.yaml")
    if os.path.exists(path):
        license_groups = parse_yaml_dict(path)
        for key, value in license_groups.items():
            if value is not None:
                for license in value.split():
                    if not license_exists(repo_root, license) and not (
                        license.startswith("@")
                    ):
                        err(
                            f'license_groups.yaml: License "{license}" in group {key} '
                            "does not exist in licenses directory"
                        )

    # Check profiles/repo_name
    path = os.path.join(repo_root, "profiles", "repo_name")
    if os.path.exists(path):
        lines = read_list(path)
        if len(lines) == 0:
            err("repo_name: profiles/repo_name cannot be empty")
        elif len(lines) > 1:
            err(
                "repo_name: Extra lines detected. "
                "File must contain just the repo name."
            )
        elif " " in lines[0]:
            err("repo_name: Repo name must not contain spaces.")

    # Check profiles/use.yaml
    path = os.path.join(repo_root, "profiles", "use.yaml")
    if os.path.exists(path):
        flags = parse_yaml_dict(path)
        for desc in flags.values():
            if not isinstance(desc, str):
                err(f'use.yaml: Description "{desc}" is not a string')

    # Check profiles/profiles.yaml
    path = os.path.join(repo_root, "profiles", "profiles.yaml")
    if os.path.exists(path):
        keywords = parse_yaml_dict_dict(path)
        for keyword, profiles in keywords.items():
            if keyword not in archs:
                err(
                    f"profiles.yaml: keyword {keyword} " "was not declared in arch.list"
                )
            for profile in profiles:
                if not isinstance(profile, str):
                    err('profiles.yaml: Profile "{profile}" is not a string')
                path = os.path.join(repo_root, "profiles", profile)
                if not os.path.exists(path):
                    err(f"profiles.yaml: Profile {path} does not exist")

    for filename in glob.glob(os.path.join(repo_root, "profiles", "desc", "*.yaml")):
        entries = parse_yaml_dict(filename)
        for entry in dict(entries):
            if not re.match("[A-Za-z0-9][A-Za-z0-9+_-]*", entry):
                err(f"USE_EXPAND flag {entry} in {file} contains invalid characters")

    # Check news
    validate_news(repo_root, err)


def main():
    """
    Main function for the inquisitor executable
    """
    parser = argparse.ArgumentParser(
        description="Quality assurance program for the package repository"
    )
    parser.add_argument(
        "mode",
        metavar="[mode]",
        nargs="?",
        choices=["manifest", "scan"],
        help='Mode in which to run. One of "manifest" "scan". Default is "scan"',
    )
    # TODO: specify path
    parser.add_argument("--debug", help="Enables debug traces", action="store_true")
    add_logging_arguments(parser)

    args = parser.parse_args()
    init_logger(args)

    repo_root = get_repo_root(os.getcwd())

    has_errored = False
    env.ALLOW_LOAD_ERROR = False

    def err(string: str):
        nonlocal has_errored
        error(string)
        has_errored = True

    if repo_root is None:
        err(
            "Cannot find repository for the current directory. "
            "Please run from within the repository you wish to inspect"
        )
        sys.exit(1)

    # Register repo in case it's not already in repos.cfg
    real_root = os.path.realpath(repo_root)
    if not any([real_root == os.path.realpath(repo.location) for repo in env.REPOS]):
        sys.path.insert(0, os.path.join(repo_root))
        env.REPOS.insert(0, Repo(get_repo_name(repo_root), repo_root))

    if args.debug:
        env.DEBUG = True
    if args.mode is None or args.mode == "scan":
        scan(repo_root, err)
    elif args.mode == "manifest":
        # Run pybuild manifest on every pybuild in repo
        for category in get_categories(repo_root):
            for file in glob.glob(os.path.join(repo_root, category, "*", "*.pybuild")):
                try:
                    pybuild_manifest(file)
                except Exception as e:
                    traceback.print_exc()
                    err(f"{e}")
    if has_errored:
        sys.exit(1)
