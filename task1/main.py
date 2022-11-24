import os
from git import *


def load_commits():
    author = 0
    message = 1
    files = 2

    repo = Repo("C:\\Users\\Timon\Desktop\\becoder-hack\\task1\\knockout")
    commits_list = []
    error_guys = {}

    master = repo.head.reference
    commits = list(repo.iter_commits())
    for commit in commits:

        commit_data = [commit.author.email, commit.message.lower(), list(commit.stats.files.keys())]
        commits_list.append(commit_data)
        #print(commit.author, commit.message, list(commit.stats.files.keys()))
        #print(commits_list)
    
    for isfix in range(0, len(commits_list)):
        if (commits_list[isfix][message].find("fix") != -1):

            fixed_files = commits_list[isfix][files]
            error_files = commits_list[isfix-1][files]

            correctly_detected = list(set(fixed_files) & set(error_files))
            if not correctly_detected:
                continue
            if commits_list[isfix-1][author] not in error_guys:
                error_guys[commits_list[isfix-1][author]] = {}
            for filename in correctly_detected:
                if filename not in error_guys[commits_list[isfix-1][author]]:
                    error_guys[commits_list[isfix-1][author]][filename] = 1
                else:
                    error_guys[commits_list[isfix-1][author]][filename]+=1
                    
    for check in error_guys:
        print(check, error_guys[check])
    #for i in commits_list:
    #    print(i)
if __name__ == "__main__":
    load_commits()   