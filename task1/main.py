import os
from git import *


def load_commits():

    repo = Repo("C:\\Users\\Timon\Desktop\\becoder-hack\\task1\\knockout")
    o = repo.remotes.origin
    o.pull()

    master = repo.head.reference
    commits = list(repo.iter_commits())
    for commit in commits:
        print(commit.author, commit.message)
    

if __name__ == "__main__":
    load_commits()   