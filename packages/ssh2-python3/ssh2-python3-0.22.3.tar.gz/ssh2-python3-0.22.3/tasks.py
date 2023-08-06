#!/usr/bin/env python3.8
"""Tasks file used by the *invoke* command.

This simplifies some common development tasks.

Run these tasks with the `invoke` tool.
"""

from __future__ import annotations

import sys
import os
import shutil
import getpass
from glob import glob

import semver
import keyring
from invoke import task, run, Exit

# local user account name
SIGNERS = ["keithdart", "keith"]
CURRENT_USER = getpass.getuser()

PYTHONBIN = os.environ.get("PYTHONBIN", sys.executable)
# Put the path in quotes in case there is a space in it.
PYTHONBIN = f'"{PYTHONBIN}"'

GPG = "gpg2"


# Package repo location. Putting info here eliminates the need for user-private ~/.pypirc file.
REPO_HOST = "upload.pypi.org"
REPOSITORY_URL = f"https://{REPO_HOST}/legacy/"
REPO_USERNAME = "__token__"


@task
def info(ctx):
    """Show information about the current Python and environment."""
    suffix = get_suffix()
    version = open("VERSION").read().strip()
    print(f"Project version: {version}")
    print(f"Python being used: {PYTHONBIN}")
    print(f"Python extension suffix: {suffix}")
    print(f"repo URL: {REPOSITORY_URL}")


@task
def build(ctx):
    """Build the intermediate package components."""
    ctx.run(f"{PYTHONBIN} setup.py build")


@task
def dev_requirements(ctx):
    """Install development requirements."""
    ctx.run(f"{PYTHONBIN} -m pip install -r requirements_dev.txt --user")


@task(pre=[dev_requirements])
def develop(ctx, uninstall=False):
    """Start developing in developer mode."""
    if uninstall:
        ctx.run(f"{PYTHONBIN} setup.py develop --uninstall --user")
    else:
        ctx.run(f'{PYTHONBIN} setup.py develop --user')


@task
def clean(ctx):
    """Clean out build and cache files. Remove extension modules."""
    ctx.run(f"{PYTHONBIN} setup.py clean")
    ctx.run(r"find . -depth -type d -name __pycache__ -exec rm -rf {} \;")
    ctx.run('find ssh2 -name "*.so" -delete')
    with ctx.cd("doc"):
        ctx.run(f"{PYTHONBIN} -m sphinx.cmd.build -M clean . _build")


@task
def cleandist(ctx):
    """Clean out dist subdirectory."""
    if os.path.isdir("dist"):
        shutil.rmtree("dist", ignore_errors=True)
        os.mkdir("dist")
    if os.path.isdir("wheelhouse"):
        shutil.rmtree("wheelhouse", ignore_errors=True)


@task
def test(ctx, testfile=None, ls=False):
    """Run unit tests. Use ls option to only list them."""
    if ls:
        ctx.run(f"{PYTHONBIN} -m pytest --collect-only -qq tests")
    elif testfile:
        ctx.run(f"{PYTHONBIN} -m pytest -s {testfile}")
    else:
        ctx.run(f"{PYTHONBIN} -m pytest tests", hide=False, in_stream=False)


@task(cleandist)
def sdist(ctx):
    """Build source distribution."""
    ctx.run(f"{PYTHONBIN} setup.py sdist")


@task
def build_ext(ctx):
    """Build compiled extension modules, in place."""
    ctx.run(f"{PYTHONBIN} setup.py build_ext --inplace")


@task(sdist)
def bdist(ctx):
    """Build a standard wheel file, an installable format, for manylinux target."""
    cwd = os.getcwd()
    uid = os.getuid()
    gid = os.getgid()
    cmd = (f'docker run -e PLAT=manylinux2014_x86_64 '
           f'-e USER_ID={uid} -e GROUP_ID={gid} '
           f'--mount type=bind,src={cwd},dst=/io '
           f'quay.io/pypa/manylinux2014_x86_64 bash /io/building/build-wheels.sh')
    ctx.run(cmd)


@task(bdist)
def sign(ctx):
    """Cryptographically sign dist with your default GPG key."""
    if CURRENT_USER in SIGNERS:
        distfiles = glob("wheelhouse/*.whl")
        distfiles.extend(glob("dist/*.tar.gz"))
        for distfile in distfiles:
            ctx.run(f"{GPG} --detach-sign -a {distfile}")
    else:
        print("Not signing.")


@task(pre=[sign])
def publish(ctx):
    """Publish built wheel files to package repo."""
    token = get_repo_token()
    distfiles = glob("wheelhouse/*.whl")
    distfiles.extend(glob("dist/*.tar.gz"))
    if not distfiles:
        raise Exit("Nothing to publish folder!")
    distfiles = " ".join(distfiles)
    ctx.run(f'{PYTHONBIN} -m twine upload --repository-url \"{REPOSITORY_URL}\" '
            f'--username {REPO_USERNAME} --password {token} {distfiles}')


@task
def docs(ctx):
    """Build the HTML documentation."""
    with ctx.cd("doc"):
        ctx.run(f"{PYTHONBIN} -m sphinx.cmd.build -M html . _build")
    if os.environ.get("DISPLAY"):
        ctx.run("xdg-open docs/_build/html/index.html")


@task
def branch(ctx, name=None):
    """start a new branch, both local and remote tracking."""
    if name:
        ctx.run(f"git checkout -b {name}")
        ctx.run(f"git push -u origin {name}")
    else:
        ctx.run("git --no-pager branch")


@task
def tag(ctx, tag=None, major=False, minor=False, patch=False):
    """Tag or bump release with a semver tag, prefixed with 'v'. Makes a signed tag."""
    latest = None
    if tag is None:
        tags = get_tags()
        if not tags:
            latest = semver.VersionInfo(0, 0, 0)
        else:
            latest = tags[-1]
        if patch:
            nextver = latest.bump_patch()
        elif minor:
            nextver = latest.bump_minor()
        elif major:
            nextver = latest.bump_major()
        else:
            nextver = latest.bump_patch()
    else:
        if tag.startswith("v"):
            tag = tag[1:]
        try:
            nextver = semver.parse_version_info(tag)
        except ValueError:
            raise Exit("Invalid semver tag.", 2)

    print(latest, "->", nextver)
    tagopt = "-s" if CURRENT_USER in SIGNERS else "-a"
    ctx.run(f'git tag {tagopt} -m "Release v{nextver}" v{nextver}')


@task
def tag_delete(ctx, tag=None):
    """Delete a tag, both local and remote."""
    if tag:
        ctx.run(f"git tag -d {tag}")
        ctx.run(f"git push origin :refs/tags/{tag}")


@task
def branch_delete(ctx, name=None):
    """Delete local, remote and tracking branch by name."""
    if name:
        ctx.run(f"git branch -d {name}", warn=True)  # delete local branch
        ctx.run(f"git branch -d -r {name}", warn=True)  # delete local tracking info
        ctx.run(f"git push origin --delete {name}", warn=True)  # delete remote (origin) branch.
    else:
        print("Supply a branch name: --name <name>")


@task
def set_token(ctx):
    """Set the password in the local key ring for the pypi account used as the package repo.
    """
    pw = getpass.getpass(f"token for account on {REPO_HOST}? ")
    if pw:
        keyring.set_password(REPO_HOST, REPO_USERNAME, pw)
    else:
        raise Exit("No token entered.", 3)


# Helper functions follow.

def get_tags():
    rv = run('git tag -l "v*"', hide="out")
    vilist = []
    for line in rv.stdout.split():
        try:
            vi = semver.parse_version_info(line[1:])
        except ValueError:
            pass
        else:
            vilist.append(vi)
    vilist.sort()
    return vilist


def get_repo_token():
    cred = keyring.get_credential(REPO_HOST, REPO_USERNAME)
    if not cred:
        raise Exit("You must set the pypi token first with set-token target.", 1)
    return cred.password


def get_suffix():
    return run(
        f'{PYTHONBIN} -c \'import sysconfig; print(sysconfig.get_config_vars()["EXT_SUFFIX"])\'',
        hide=True,
    ).stdout.strip()  # noqa
