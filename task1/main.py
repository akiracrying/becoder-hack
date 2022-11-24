import os
from git import *

author = 0
message = 1
files = 2

def hypothesis_1_vse(error_guys):
    global file
    avgInOneFile = []
    kbOtk = []
    isAvgByPeople = {}
    for eGuy in error_guys:
        for file in error_guys.get(eGuy):
            trueFiles = error_guys.get(eGuy).get(file)[1]
            falseFiles = error_guys.get(eGuy).get(file)[0]
            if (trueFiles != 0):
                avgInOneFile.append(falseFiles / trueFiles)
            else:
                avgInOneFile.append(0.0)
        sumAvg = 0
        for i in avgInOneFile:
            sumAvg += i
        avg = sumAvg / len(avgInOneFile)
        for i in avgInOneFile:
            kbOtk.append(i - avg)
        isAvgByPeople.update({eGuy: kbOtk})
        avgInOneFile = []
        kbOtk = []
    for avg in isAvgByPeople:
        print(avg, isAvgByPeople[avg])

def hypothesis_1_ne_vse(error_guys):
    global file
    avgInOneFile = []
    moreThanAvg = []
    moreThanAvgByPeople = {}
    for eGuy in error_guys:
        for file in error_guys.get(eGuy):
            trueFiles = error_guys.get(eGuy).get(file)[1]
            falseFiles = error_guys.get(eGuy).get(file)[0]
            if(trueFiles != 0):
                avgInOneFile.append(falseFiles/trueFiles)
            else:
                avgInOneFile.append(0.0)
        sumAvg = 0
        for i in avgInOneFile:
            sumAvg+=i
        avg = sumAvg / len(avgInOneFile)
        for i in avgInOneFile:
            if(i > avg):
                moreThanAvg.append(i)
        moreThanAvgByPeople.update({eGuy:moreThanAvg})
        moreThanAvg = []
        avgInOneFile = []
    for more in moreThanAvgByPeople:
        print(more, moreThanAvgByPeople[more])

def reviewer_choice(prob_guys, commits_list):
    filenames = {}
    for user in prob_guys:
        for filename in prob_guys[user]:
            if filename not in filenames:
                filenames[filename] = [user, prob_guys[user][filename]]
            if filenames[filename][1] > prob_guys[user][filename]:
                filenames[filename][0] = user
                filenames[filename][1] = prob_guys[user][filename]
    #for f in filenames:
    #    print(f, filenames[f])
        
    commits_reviewers = {}
    
    for commit in commits_list:
        if commit[4] == True:
            continue
        reviewers = {}
        rev = ""
        val = 0
        for files in commit[2]:
            try:
                if filenames[files][0] not in reviewers:
                    reviewers[filenames[files][0]] = 1
                else:
                    reviewers[filenames[files][0]] += 1
            except Exception as exp:
                pass
        for reviewer in reviewers:
            if reviewers[reviewer] > val:
                val = reviewers[reviewer]
                rev = reviewer
        commits_reviewers[commit[3]] = rev

    for i in commits_reviewers:
        print(i, commits_reviewers[i])

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
            final_prob_with_commit[commit[3]] = 0.0
            continue
        for filename in commit[2]:
            try:
                sum *= (1 -(prob_guys[commit[0]][filename]))
            except Exception as exp:
                pass
        if commit[4] is True:
            final_prob_with_commit["FIXED_" + commit[3].hexsha] = 1 - sum
        else:
            final_prob_with_commit[commit[3]] = 1 - sum

    for final in final_prob_with_commit:
        print(final, round(final_prob_with_commit[final]* 100, 4), "%")
        
    return prob_guys
        
def load_commits():
    repo = Repo("C:\\Users\\Timon\\Desktop\\becoder-hack\\task1\\knockout")
    commits_list = []
    error_guys = {}

    master = repo.head.reference
    commits = list(repo.iter_commits())
    for commit in commits:

        commit_data = [commit.author.email, commit.message.lower(), list(commit.stats.files.keys()), commit, False]
        commits_list.append(commit_data)
    reviewer_commits_list = commits_list.copy()
    
    for isfix in range(0, len(commits_list)-1):
        if (commits_list[isfix][message].find("fix") != -1):

            correctly_detected = []
            fixed_files = commits_list[isfix][files].copy()
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
                        commits_list[i][4] = True
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
        #print(check, error_guys[check])
    prob_guys = prob(error_guys, commits_list)
    reviewer_choice(prob_guys, reviewer_commits_list)
    hypothesis_1_vse(error_guys)


if __name__ == "__main__":
    load_commits()   