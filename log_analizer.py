import json
import pandas as pd
import os
# import numpy as np

PYTHON_CMD = "python"
PYTHON_PATH = os.path.dirname(os.getcwd())


def search_log(keywords):

    number_of_key_words = 0
    mis_number_of_key_words = 0
    found_at = []
    found_at_err = []
    calc_time_over_limit = []
    nav_errors = []
    mis_found_at_err = []
    mis_errors = []
    mis_found_at = []

    errors = keywords["Errors"]
    calculations = keywords["Calculations"]
    missions = keywords["Missions"]

    logfile = os.path.join(PYTHON_PATH, "cs_navigator",
                           "logs", "navigator.log")

    mission_logfile = os.path.join(PYTHON_PATH, "cs_mission_generator",
                                   "logs", "automatic-missions.log")

    # colNames = ['Line#', 'Error', 'Path',
    #             'Time of path calculation', 'Not completed mission']

    try:
        with open(logfile, 'r') as readlog:
            test_pass = 0
            for num, line in enumerate(readlog, 1):
                log = json.loads(line)
                if log["levelname"] == "ERROR":
                    test_pass += 1
                    print("In line # {} of navigator Error occupared: {}".format(
                        num, log["message"]))
                    miss_error = log["message"]
                    found_at_err.append(num)
                    nav_errors.append(miss_error)
                    continue
                else:
                    for error in errors:
                        if error in log["message"]:
                            number_of_key_words += 1
                            found_at.append(num)
                            # break
                    for calc in calculations:
                        if calc in log["message"]:
                            # time_path_calculation.append(line)
                            result = log["message"]
                            # result = [
                            #     y for x in time_path_calculation for y in x.split(',')]
                            # result = result[-1]
                            # result = [
                            #     y for x in time_path_calculation for y in x.split(':')]
                            calc_time = float(result.split(':')[-1])
                            if calc_time > 15:
                                # print(calc_time)
                                calc_time_over_limit.append(calc_time)
                                print(
                                    f"In line # {num} time of path calculation was: {calc_time}")
    except OSError as e:
        print("Error: loading log failed: ", e.filename, "doesn't exist")
        return False

    try:
        with open(mission_logfile, 'r') as mis_readlog:
            miss_test_pass = 0
            for mis_num, line in enumerate(mis_readlog, 1):
                mis_log = json.loads(line)
                if mis_log["levelname"] == "ERROR":
                    miss_test_pass += 1
                    print("In line # {} of mission generator Error occupared: {}".format(
                        mis_num, mis_log["message"]))
                    mis_error = mis_log["message"]
                    mis_found_at_err.append(mis_num)
                    mis_errors.append(mis_error)
                    continue
                else:
                    for error in missions:
                        if error in mis_log["message"]:
                            mis_number_of_key_words += 1
                            mis_found_at.append(num)
                            # break
    except OSError as e:
        print("Error: loading log failed: ", e.filename, "doesn't exist")
        return False

    if number_of_key_words > 0:
        print("Number of incompleted missions ", number_of_key_words)
        # print("Incompleted missions found in lines: ", *found_at, sep='\n')
    if mis_number_of_key_words > 0:
        print("Number of missions weren't sent ", mis_number_of_key_words)
        # print("Incompleted missions found in lines: ", *mis_found_at, sep='\n')
    if test_pass > 0 or miss_test_pass > 0:
        print("Test Failed!!!!!")
    else:
        print("Test Passed!")

    df_nav_errors = pd.DataFrame(list(zip(found_at_err, nav_errors)),
                                 columns=['Line#', 'Error'])
    df_mis_errors = pd.DataFrame(list(zip(mis_found_at_err, mis_errors)),
                                 columns=['Line#', 'Error'])

    # df_errors = pd.concat([df_nav_errors, df_mis_errors], axis=1, join="inner")
    df_nav_errors.append(df_mis_errors)
    # print(df_nav_errors)
    html = df_nav_errors.to_html()
    # print(html)
    error_file = open("errors.html", "w")
    error_file.write(html)
    error_file.close()


if __name__ == '__main__':

    try:
        # with open(r"C:\Git\CS\cs_main\config\keywords.json") as key:
        with open(os.path.join(os.getcwd(), 'config', 'keywords.json')) as key:
            keywords = json.load(key)
            search_log(keywords)
    except OSError as e:
        print("File", e.filename, "doesn't exist")
        exit()
