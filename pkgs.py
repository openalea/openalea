import subprocess
import pathlib
import sys

COMMIT=False

SUBMODULE_DIR = pathlib.Path("packages")

pkgs="""
core
grapheditor
oalab
visualea
plantgl
mtg
lpy
scipack
rsml
oawidgets
weberpenn
astk
caribu
adel
spice
hydroroot
hydroshoot
phenomenal
pyratp
""".split()

def run(cmd, cwd=None, capture=False):
    print(">>>", " ".join(cmd))
    if capture:
        return subprocess.check_output(cmd, cwd=cwd).decode().strip()
    else:
        subprocess.check_call(cmd, cwd=cwd)



def latest_tag(repo_path):
    """Return latest tag sorted by version"""
    tags = run(
        ["git", "tag", "--sort=-v:refname"],
        cwd=repo_path,
        capture=True
    ).splitlines()

    print(tags)
    if not tags:
        raise RuntimeError(f"No tag found in {repo_path}")
    return tags[0]


def repo_name(name='core'):
    return f"https://github.com/openalea/{name}"

def submodules():
    for pkg in pkgs:
        print(f"Processing {pkg}...")
        pkgdir = SUBMODULE_DIR / pkg

        url = repo_name(pkg)
        if not pkgdir.exists():
            print(f"Submodule {url} into {pkgdir}...")
            run(["git", "submodule", "add", url, str(pkgdir)])
        else:
            print(f"Submodule {pkgdir} already exists, skipping clone.")


def update_latest_tag(commit=COMMIT):
    for pkg in pkgs:
        print(f"Processing {pkg}...")
        pkgdir = SUBMODULE_DIR / pkg
        if not pkgdir.exists():
            print(f"Submodule {pkgdir} does not exist, skipping.")
            continue

        # ---- fetch tags ----
        run(["git", "fetch", "--tags"], cwd=pkgdir)

        # ---- latest tags ----
        tag = latest_tag(pkgdir)
        print(f"Latest tag for {pkg}: {tag}")

        # ---- checkout tags ----
        run(["git", "checkout", tag], cwd=pkgdir)


        # ---- stage submodule pointer ----
        if commit: 
            run(["git", "add", str(pkgdir)])


