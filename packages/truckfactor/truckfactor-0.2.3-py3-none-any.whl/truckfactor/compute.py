"""
This program computes the truck factor (also called bus factor) for a given 
Git repository.

It can be called like:

truckfactor <path_to_git_repository>

python -m truckfactor.run 

The truck factor specifies "...the number of people on your team that have to 
be hit by a truck (or quit) before the project is in serious trouble..."" 
L. Williams and R. Kessler, Pair Programming Illuminated

Note, do not call it from within a Git repository.

More on the truck factor:
  * https://legacy.python.org/search/hypermail/python-1994q2/1040.html
  * https://en.wikipedia.org/wiki/Bus_factor
"""
import os
import sys
import uuid
import tempfile
import subprocess
from pathlib import Path
from shutil import which
from urllib.parse import urlparse
from truckfactor.evo_log_to_csv import convert
from truckfactor.repair_git_move import repair
import pandas as pd


TMP = tempfile.gettempdir()


def write_git_log_to_file(path_to_repo):
    p = Path(path_to_repo)
    outfile = os.path.join(TMP, p.name + "_evo.log")

    cmd = f"""git -C {path_to_repo} log --pretty=format:'"%h","%an","%ad"' \
    --date=short \
    --numstat > \
    {outfile}"""

    subprocess.run(cmd, shell=True)

    return outfile


def preprocess_git_log_data(path_to_repo):
    evo_log = write_git_log_to_file(path_to_repo)
    evo_log_csv = convert(evo_log)
    evo_log_csv = repair(evo_log_csv)
    return evo_log_csv


def create_file_owner_data(df):
    new_rows = []

    for fname in set(df.current.values):
        view = df[df.current == fname]
        sum_series = view.groupby(["author"]).added.sum()
        view_df = sum_series.reset_index(name="sum_added")
        total_added = view_df.sum_added.sum()

        if total_added > 0:  # For binaries there are no lines counted
            view_df["owning_percent"] = view_df.sum_added / total_added
            owning_author = view_df.loc[view_df.owning_percent.idxmax()]
            new_rows.append(
                (
                    fname,
                    owning_author.author,
                    owning_author.sum_added,
                    total_added,
                    owning_author.owning_percent,
                )
            )
        # All binaries are silently skipped in this report...

    owner_df = pd.DataFrame(
        new_rows,
        columns=["artifact", "main_dev", "added", "total_added", "owner_rate"],
    )

    owner_freq_series = owner_df.groupby(["main_dev"]).artifact.count()
    owner_freq_df = owner_freq_series.reset_index(name="owns_no_artifacts")
    owner_freq_df.sort_values(by="owns_no_artifacts", inplace=True)

    return owner_df, owner_freq_df


def compute_truck_factor(df, freq_df):
    """Similar to G. Avelino et al.
    [*A novel approach for estimating Truck Factors*](https://ieeexplore.ieee.org/stamp)/stamp.jsp?arnumber=7503718)
    we remove low-contributing authors from the dataset as long as still more 
    than half of the files have an owner. The amount of remaining owners is the 
    bus-factor of that project.
    """
    no_artifacts = len(df.artifact)

    half_no_artifacts = no_artifacts // 2
    count = 0

    for owner, freq in freq_df.values:
        no_artifacts -= freq
        if no_artifacts < half_no_artifacts:
            break
        else:
            count += 1

    truckfactor = len(freq_df.main_dev) - count
    return truckfactor


def main(path_to_repo, is_url=False):
    if is_url:
        path_to_repo = clone_to_tmp(path_to_repo)
    evo_log_csv = preprocess_git_log_data(path_to_repo)
    complete_df = pd.read_csv(evo_log_csv)
    owner_df, owner_freq_df = create_file_owner_data(complete_df)
    truckfactor = compute_truck_factor(owner_df, owner_freq_df)
    return truckfactor


def git_is_available():
    """Check whether `git` is on PATH"""
    if which("git"):
        return True
    else:
        return False


def is_git_url(potential_url):
    result = urlparse(potential_url)
    is_complete_url = all((result.scheme, result.netloc, result.path))
    is_git = result.path.endswith(".git")
    is_git_user = result.path.startswith("git@")
    if is_complete_url:
        return True
    elif is_git_user and is_git:
        return True
    else:
        return False


def clone_to_tmp(url):
    path = Path(urlparse(url).path)
    outdir = path.name.removesuffix(path.suffix)
    git_repo_dir = os.path.join(TMP, outdir + str(uuid.uuid4()))
    cmd = f"git clone {url} {git_repo_dir}"
    print(cmd)
    subprocess.run(cmd, shell=True)

    return git_repo_dir


def run():
    if not git_is_available():
        print(
            "Truckfactor requires `git` to be installed and accessible on path"
        )
        sys.exit(1)

    if len(sys.argv) <= 1:
        print(__doc__)
        sys.exit(1)

    if is_git_url(sys.argv[1]) or Path(sys.argv[1]).is_dir():
        path_to_repo = sys.argv[1]
        truckfactor = main(path_to_repo, is_url=is_git_url(sys.argv[1]))
        print(f"The truck factor of {path_to_repo} is: {truckfactor}")
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    run()
