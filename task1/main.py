import matplotlib.pyplot as plt
import numpy as np
from git import *

author = 0
message = 1
files = 2

f_probability = open("stats_probability.txt", "w")
f_deviation = open("stats_deviation.txt", "w")
f_start = open("stats_start.txt", "w")
f_reviewers = open("stats_reviewers.txt", "w")


def hypothesis_1_vse(error_guys):
    avg_in_one_file = []
    kb_otk = []
    is_avg_by_people = {}
    avg_array = []
    fail_rate = {}
    more_avg_count = 0
    all_avg_count = 0
    for eGuy in error_guys:
        for file in error_guys.get(eGuy):
            true_files = error_guys.get(eGuy).get(file)[1]
            false_files = error_guys.get(eGuy).get(file)[0]
            try:
                avg_in_one_file.append(false_files / (true_files + false_files))
            except Exception as exp:
                print(exp)
                pass
        sum_avg = 0
        for i in avg_in_one_file:
            sum_avg += i
        avg = sum_avg / len(avg_in_one_file)
        avg_array.append(avg)
        for i in avg_in_one_file:
            kb_otk.append(i - avg)
            if i > avg:
                more_avg_count += 1
            all_avg_count += 1
        fail_rate.update({eGuy: more_avg_count / all_avg_count})
        is_avg_by_people.update({eGuy: kb_otk})
        avg_in_one_file = []
        kb_otk = []
        more_avg_count = 0
        all_avg_count = 0
    f_deviation.write("Deviation stats:\n\n")
    for human in is_avg_by_people:
        f_deviation.write("\n$\n")
        f_deviation.write(str(human) + " " + str(is_avg_by_people.get(human)) + "\n")
        f_deviation.write("\n\t@Fail rate: " + str(fail_rate.get(human)) + "\n")
    f_deviation.close()
    number = 1
    while number != 0:
        print("Enter number of developer to view graph between 1 and ", len(list(is_avg_by_people.keys())) - 1, ":")
        print("Enter 0 code to exit program")
        try:
            number_input = input()
            int(number_input)
            number = int(number_input)
            if 0 < number < len(list(is_avg_by_people.keys())):
                x = np.arange(0, len(is_avg_by_people.get(list(is_avg_by_people.keys())[number - 1])), 1)
                y = np.array(is_avg_by_people.get(list(is_avg_by_people.keys())[number - 1]))
                y_1 = np.array(
                    [avg_array[number - 1] for _ in range(0,
                                                          len(is_avg_by_people.get(
                                                              list(is_avg_by_people.keys())[number - 1])))])
                plt.figure(figsize=(12, 7))
                plt.plot(x, y, marker='.')
                plt.plot(x, y_1)
                plt.title(list(is_avg_by_people.keys())[number - 1])
                plt.grid(True)
                plt.show()
        except Exception as exp:
            print(exp)
            pass


def reviewer_choice(prob_guys, commits_list):
    filenames = {}
    for user in prob_guys:
        for filename in prob_guys[user]:
            if filename not in filenames:
                filenames[filename] = [user, prob_guys[user][filename]]
            if filenames[filename][1] > prob_guys[user][filename]:
                filenames[filename][0] = user
                filenames[filename][1] = prob_guys[user][filename]
    commits_reviewers = {}
    for single_commit in commits_list:
        if single_commit[4]:
            continue
        reviewers = {}
        rev = ""
        val = 0
        for files_commit in single_commit[2]:
            try:
                if filenames[files_commit][0] not in reviewers:
                    reviewers[filenames[files_commit][0]] = 1
                else:
                    reviewers[filenames[files_commit][0]] += 1
            except Exception as exp:
                print(exp)
                pass
        for reviewer in reviewers:
            if reviewers[reviewer] > val:
                val = reviewers[reviewer]
                rev = reviewer
        commits_reviewers[single_commit[3]] = rev
    f_reviewers.write("Reviewers stats:\n\n")
    for i in commits_reviewers:
        f_reviewers.write(str(i) + " " + str(commits_reviewers[i]) + "\n")
    f_reviewers.close()


def prob(array, commits):
    prob_guys = {}
    for guy in array:
        for filename in array[guy]:
            error_prob = array[guy][filename][0] / (array[guy][filename][0] + array[guy][filename][1])
            if guy not in prob_guys:
                prob_guys[guy] = {}
            prob_guys[guy][filename] = error_prob
    final_prob_with_commit = {}
    for single_commit in commits:
        multiplier = 1
        if single_commit[0] not in prob_guys:
            final_prob_with_commit[single_commit[3]] = 0.0
            continue
        for filename in single_commit[2]:
            try:
                multiplier *= (1 - (prob_guys[single_commit[0]][filename]))
            except Exception as exp:
                print(exp)
                pass
        if single_commit[4] is True:
            final_prob_with_commit[single_commit[3].hexsha + " FIXED"] = 1 - multiplier
        else:
            final_prob_with_commit[single_commit[3]] = 1 - multiplier
    f_probability.write("Probability stats:\n\n")
    for final in final_prob_with_commit:
        gap_prefix = " "
        if final_prob_with_commit[final] * 100 > 9:
            gap_prefix = ""
        f_probability.write(gap_prefix + str("{0:2.3f}".format((round(final_prob_with_commit[final] * 100, 4))))
                            + "% " + str(final) + "\n")
    f_probability.close()
    return prob_guys


def load_commits():
    rep = Repo("D:\\selfPro\\becoder-repos\\knockout")
    commits_list = []
    error_guys = {}
    commits = list(rep.iter_commits())
    for single_commit in commits:
        commit_data = [single_commit.author.email, single_commit.message.lower(),
                       list(single_commit.stats.files.keys()), single_commit, False]
        commits_list.append(commit_data)
    reviewer_commits_list = commits_list.copy()

    for is_fix in range(0, len(commits_list) - 1):
        if commits_list[is_fix][message].find("fix") != -1:
            fixed_files = commits_list[is_fix][files].copy()
            for i in range(is_fix + 1, len(commits_list)):
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
                        error_guys[commits_list[i][author]][filename] = [1, 0]
                    else:
                        error_guys[commits_list[i][author]][filename][0] += 1
        else:
            user_changed_files = commits_list[is_fix + 1][files]
            if commits_list[is_fix + 1][author] not in error_guys:
                error_guys[commits_list[is_fix + 1][author]] = {}
            for filename in user_changed_files:
                if filename not in error_guys[commits_list[is_fix + 1][author]]:
                    error_guys[commits_list[is_fix + 1][author]][filename] = [0, 1]
                else:
                    error_guys[commits_list[is_fix + 1][author]][filename][1] += 1
    f_start.write("Start stats:\n\n")
    for check in error_guys:
        f_start.write("--------------------------------------------\n")
        f_start.write(str(check) + " " + str(error_guys[check]) + "\n")
    f_start.close()
    prob_guys = prob(error_guys, commits_list)
    reviewer_choice(prob_guys, reviewer_commits_list)
    hypothesis_1_vse(error_guys)


if __name__ == "__main__":
    load_commits()
