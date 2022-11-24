import matplotlib.pyplot as plt
import numpy as np
from git import *

author = 0
message = 1
files = 2

f_probability = open("stats_probability.txt", "w")
f_deviation = open("stats_deviation.txt", "w")
f_start = open("stats_start.txt", "w")


def hypothesis_1_vse(error_guys):
    global file
    avg_in_one_file = []
    kb_otk = []
    is_avg_by_people = {}
    avg_array = []
    for eGuy in error_guys:
        for file in error_guys.get(eGuy):
            true_files = error_guys.get(eGuy).get(file)[1]
            false_files = error_guys.get(eGuy).get(file)[0]
            if true_files != 0:
                avg_in_one_file.append(false_files / true_files)
            else:
                avg_in_one_file.append(0.0)
        sum_avg = 0
        for i in avg_in_one_file:
            sum_avg += i
        avg = sum_avg / len(avg_in_one_file)
        avg_array.append(avg)
        for i in avg_in_one_file:
            kb_otk.append(i - avg)
        is_avg_by_people.update({eGuy: kb_otk})
        avg_in_one_file = []
        kb_otk = []
    f_deviation.write("Deviation stats:\n\n")
    for human in is_avg_by_people:
        f_deviation.write(str(human) + " " + str(is_avg_by_people.get(human)))
    for i in range(0, len(list(is_avg_by_people.keys()))):
        x = np.arange(0, len(is_avg_by_people.get(list(is_avg_by_people.keys())[i])), 1)
        y = np.array(is_avg_by_people.get(list(is_avg_by_people.keys())[i]))
        y_1 = np.array([avg_array[i] for _ in range(0, len(is_avg_by_people.get(list(is_avg_by_people.keys())[i])))])
        plt.figure(figsize=(12, 7))
        plt.plot(x, y, marker='.')
        plt.plot(x, y_1)
        plt.title(str(i + 1) + "-ый разработчик")
        plt.grid(True)
        plt.show()


def hypothesis_1_ne_vse(error_guys):
    global file
    avg_in_one_file = []
    more_than_avg = []
    more_than_avg_by_people = {}
    for eGuy in error_guys:
        for file in error_guys.get(eGuy):
            true_files = error_guys.get(eGuy).get(file)[1]
            false_files = error_guys.get(eGuy).get(file)[0]
            if true_files != 0:
                avg_in_one_file.append(false_files / true_files)
            else:
                avg_in_one_file.append(0.0)
        sum_avg = 0
        for i in avg_in_one_file:
            sum_avg += i
        avg = sum_avg / len(avg_in_one_file)
        for i in avg_in_one_file:
            if i > avg:
                more_than_avg.append(i)
        more_than_avg_by_people.update({eGuy: more_than_avg})
        more_than_avg = []
        avg_in_one_file = []
    print(more_than_avg_by_people)

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
                prob_guys[guy] = {}

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
    f_probability.write("Probability stats:\n\n")
    for final in final_prob_with_commit:
        f_probability.write(str(final) + " " + str(round(final_prob_with_commit[final] * 100, 4)) + "%\n")        
    return prob_guys
        
def load_commits():
    repo = Repo("D:\\selfPro\\becoder-hack\\rep2\\memos")
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
    f_start.write("Start stats:\n\n")
    for check in error_guys:
        f_start.write(str(check) + " " + str(error_guys[check]))
    prob_guys = prob(error_guys, commits_list)
    reviewer_choice(prob_guys, reviewer_commits_list)
    hypothesis_1_vse(error_guys)


if __name__ == "__main__":
    load_commits()
    f_probability.close()
    f_deviation.close()
    f_start.close()
