import os
import sys
import argparse
import subprocess

dirname = os.path.dirname(__file__)
repodir = os.path.dirname(dirname)

# Some packages depend on other packages
# having been built first.
order = [
    "rezutils",
    "base",
    "python",
    "core_pipeline",
    "maya",
    "maya_base",
    "pip",
]

parser = argparse.ArgumentParser()
parser.add_argument("--verbose", action="store_true")
opts = parser.parse_args()

print("-" * 30)
print("")
print("Auto-building..")
print("")
print("-" * 30)

count = 0

for root in ("software", "configurations"):
    root = os.path.join(repodir, root)

    for base, dirs, files in os.walk(root):

        # Order relevant packages by above criteria
        for index, name in enumerate(order):
            if name in dirs[:]:
                dirs.remove(name)
                dirs.insert(index, name)

        for fname in files:
            if fname != "package.py":
                continue

            dirs[:] = []  # Stop traversing
            abspath = os.path.join(base, fname)

            name = "unknown"
            version = "0.0.0"

            with open(abspath) as f:
                for line in f:
                    if line.startswith("name"):
                        name = line.split(" = ")[-1]
                        name = name.rstrip()  # newline
                        name = name.replace("\"", "")  # quotes
                    if line.startswith("version"):
                        version = line.split(" = ")[-1]
                        version = version.rstrip()  # newline
                        version = version.replace("\"", "")  # quotes

            print(" - %s-%s" % (name, version))

            exe = sys.executable

            try:
                with open(os.devnull, "w") as devnull:
                    subprocess.check_call(
                        "rez build --install",
                        cwd=base,
                        shell=True,
                        stdout=None if opts.verbose else devnull,
                    )

            except subprocess.CalledProcessError:
                raise

            count += 1

print("-" * 30)
print("Auto-built %d packages for you" % count)