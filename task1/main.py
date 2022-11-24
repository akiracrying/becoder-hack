import os
from git import *

author = 0
message = 1
files = 2

def prob(array, commits):
    prob_guys = {}
    for guy in array:
        for filename in array[guy]:
            error_prob = array[guy][filename][0] / (array[guy][filename][0] + array[guy][filename][1])

            if guy not in prob_guys:
                prob_guys[guy]={}

            prob_guys[guy][filename] = error_prob

    final_prob_with_commit = {}

    for commit in commits:
        sum = 1
        if commit[0] not in prob_guys:
            final_prob_with_commit[commit[3]] = 0
            continue
        for filename in commit[2]:
            try:
                sum *= (1 -(prob_guys[commit[0]][filename]))
            except Exception as exp:
                pass
        final_prob_with_commit[commit[3]] = 1 - sum

    for final in final_prob_with_commit:
        print(final, final_prob_with_commit[final])
        
def load_commits():
    repo = Repo("C:\\Users\\Timon\Desktop\\becoder-hack\\task1\\knockout")
    commits_list = []
    error_guys = {}

    master = repo.head.reference
    commits = list(repo.iter_commits())
    for commit in commits:

        commit_data = [commit.author.email, commit.message.lower(), list(commit.stats.files.keys()), commit]
        commits_list.append(commit_data)

    for isfix in range(0, len(commits_list)-1):
        if (commits_list[isfix][message].find("fix") != -1):

            correctly_detected = []
            fixed_files = commits_list[isfix][files]
            for i in range(isfix+1, len(commits_list)):
                if not fixed_files:
                    break
                error_files = commits_list[i][files]
                correctly_detected = list(set(fixed_files) & set(error_files))
                for item in correctly_detected: 
                    fixed_files.remove(item) 

                if not correctly_detected:
                    continue
                if commits_list[i][author] not in error_guys:
                    error_guys[commits_list[i][author]] = {}
                for filename in correctly_detected:
                    if filename not in error_guys[commits_list[i][author]]:
                        error_guys[commits_list[i][author]][filename] = [1,0]
                    else:
                        error_guys[commits_list[i][author]][filename][0]+=1
        else:
            user_changed_files = commits_list[isfix+1][files]
            if commits_list[isfix+1][author] not in error_guys:
                error_guys[commits_list[isfix+1][author]] = {}
            for filename in user_changed_files:
                if filename not in error_guys[commits_list[isfix+1][author]]:
                    error_guys[commits_list[isfix+1][author]][filename] = [0,1]
                else:
                    error_guys[commits_list[isfix+1][author]][filename][1]+=1

    #for check in error_guys:
    #    print(check, error_guys[check])
    prob(error_guys, commits_list)


if __name__ == "__main__":
    load_commits()   