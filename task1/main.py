import os
from git import *


def load_commits():

    repo = Repo("C:\\Users\\Timon\Desktop\\becoder-hack\\task1\\knockout")
    commits_list = []

    master = repo.head.reference
    commits = list(repo.iter_commits())
    for commit in commits:
        cur_files = commit.stats.files.keys()
        commit_data = [commit.author, commit.message, list(commit.stats.files.keys())]
        commits_list.append(commit_data)
        #print(commit.author, commit.message, list(commit.stats.files.keys()))
        #print(commits_list)
    
    for i in commits_list:
        print(i)
if __name__ == "__main__":
    load_commits()   