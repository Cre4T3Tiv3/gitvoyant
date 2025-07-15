"""
Module: src/gitvoyant/cli/repo_resolver.py

GitVoyant Repository Resolution Module

Provides intelligent repository path resolution supporting both local filesystem
paths and remote Git repositories. Handles automatic cloning, caching, and
path normalization for seamless repository access across different sources.

This module abstracts the complexity of working with various repository sources,
ensuring consistent local access regardless of the original repository location.

Author: Jesse Moses (@Cre4T3Tiv3) <jesse@bytestacklabs.com>

Version: 0.2.0

License: Apache 2.0
"""

import tempfile
from pathlib import Path
from urllib.parse import urlparse

from git import Repo

__version__ = "0.2.0"
__author__ = "Jesse Moses (@Cre4T3Tiv3) - jesse@bytestacklabs.com"


def resolve_repo_path(repo_input: str) -> Path:
    """
    Resolve repository input to a local filesystem path.

     Accepts either a local repository path or a remote Git URL and ensures
     a local filesystem path is returned. For remote repositories, performs
     automatic cloning to a temporary directory with intelligent caching to
     avoid redundant clone operations.

     Args:
         repo_input (str): Repository identifier that can be either:
             - Local filesystem path (absolute or relative)
             - Remote Git URL (http:// or https://)
             - The path/URL will be validated and processed accordingly

     Returns:
         Path: Absolute path to the local repository directory. For remote
             repositories, this will be a path within the system temporary
             directory. For local paths, this will be the resolved absolute path.

     Note:
         Remote repositories are cloned to temporary directories named with
         the pattern 'gitvoyant_{repo_name}' where repo_name is extracted
         from the URL path. Existing clones are reused to improve performance
         and reduce network usage.

         The function provides user feedback during clone operations and
         cache reuse to maintain transparency about repository access patterns.

     Example:
         >>> # Local repository
         >>> path = resolve_repo_path("./my-local-repo")
         >>> print(path)
         /home/user/my-local-repo

         >>> # Remote repository (first time)
         >>> path = resolve_repo_path("https://github.com/user/project.git")
         ⬇️  Cloning https://github.com/user/project.git into /tmp/gitvoyant_project ...
         >>> print(path)
         /tmp/gitvoyant_project

         >>> # Remote repository (subsequent access)
         >>> path = resolve_repo_path("https://github.com/user/project.git")
         📦 Reusing existing clone: /tmp
    """
    if repo_input.startswith("http://") or repo_input.startswith("https://"):
        parsed = urlparse(repo_input)
        name = Path(parsed.path).stem
        temp_dir = Path(tempfile.gettempdir()) / f"gitvoyant_{name}"

        if not temp_dir.exists():
            print(f"⬇️  Cloning {repo_input} into {temp_dir} ...")
            Repo.clone_from(repo_input, temp_dir)
        else:
            print(f"📦 Reusing existing clone: {temp_dir}")

        return temp_dir
    else:
        return Path(repo_input).resolve()
