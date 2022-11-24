import os
from git import *


def load_commits():
    author = 0
    message = 1
    files = 2

    repo = Repo("C:\\Users\\Timon\Desktop\\becoder-hack\\task1\\knockout")
    commits_list = []

    master = repo.head.reference
    commits = list(repo.iter_commits())
    for commit in commits:

        commit_data = [commit.author.name, commit.message.lower(), list(commit.stats.files.keys())]
        commits_list.append(commit_data)
        #print(commit.author, commit.message, list(commit.stats.files.keys()))
        #print(commits_list)
    
    for isfix in range(0, len(commits_list)):
        if (commits_list[isfix][message].find("fix") != -1):
            error_commit = commits_list[isfix-1]
            print(error_commit)

    #for i in commits_list:
    #    print(i)
if __name__ == "__main__":
    load_commits()   