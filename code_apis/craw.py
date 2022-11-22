# Code creator/owner GitHub: JustRedTTG
# Original repository name: softuni-judge-web-crawer
# links: https://github.com/JustRedTTG
# links: https://github.com/JustRedTTG/softuni-judge-web-crawer
# CTRL+Click on link*

# License: MIT LICENSE
############################## LICENSE DESCRIPTION ############################
'''
MIT License

Copyright (c) 2022 RedTTG

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''


import requests
import traceback
import ast
from hexicapi import save
from typing import *

judge_url: str = "https://judge.softuni.org/"
login_url: str = "https://judge.softuni.org/Account/Login"
contests_category_url: str = "191/Python-Fundamentals"
exercise_result_page_size = 10


def get_verification_token() -> Tuple[str, dict]:
    resp = requests.get(login_url)
    html = resp.content.decode('utf-8')
    element = html.split('<input name="__RequestVerificationToken" ')[1].split('>')[0]
    value = element.split('value=')[1].split('"')[1]
    return value, resp.cookies


def get_login_data(username: str, password: str) -> dict:
    verification_token, cookies = get_verification_token()
    resp = requests.post(login_url, {
        '__RequestVerificationToken': verification_token,
        'UserName': username,
        'Password': password,
        'RememberMe': False,
    },cookies=cookies, allow_redirects=False)
    if resp.status_code == 302:
        login = dict(resp.cookies)
        login['__RequestVerificationToken'] = verification_token
        return login
    else: return None


def yes_or_no(msg: str) -> bool:
    return input(f'{msg} [Y/n]').lower() != 'n' or False


def get_contest_type(ending_words: str) -> str:
    ending_words = ending_words.lower()
    if ending_words[0] == 'l': return 'practice'
    elif ending_words.endswith('es'): return 'practice'
    elif ending_words.startswith('ex'): return 'compete'
    return 'unknown'


def get_contests(login: dict, category_url: str) -> Tuple[list[dict], int]:
    contests: list[dict] = []
    for i in range(1,21):
        resp = requests.get(judge_url+f'Contests/List/ByCategory/{category_url}?page={i}', cookies=login)
        if 'The selected category is empty.' in resp.text: break
        for line in resp.text.splitlines(False):
            if line.startswith('<a href="    /Contests/'):
                identifier, url_name = line.split('Contests/')[1].split('/')
                name = resp.text.split(f'<a href="    /Contests/{identifier}/{url_name}\r\n">')[1].split('</a>')[0]
                contests.append({
                    'identifier': int(identifier),
                    'name': name,
                    'url_name': url_name,
                    'type': get_contest_type(url_name.split('-')[-1])
                })
    return contests, i-1


def get_exercise_information(login: dict, exercise_url: str, clickable_url: str):
    exercise = {
        'url': exercise_url,
        'clickable_url': clickable_url
    }

    resp = requests.get(judge_url+exercise_url.lstrip('/'), cookies=login)
    exercise['full_name'] = resp.text.split('\n<h2>\n')[1].split('\n')[0]
    number, name = exercise['full_name'].split(maxsplit=1)
    exercise['number'] = int(''.join([n for n in number if n.isdecimal()]))
    exercise['name'] = name
    # TODO: get results
    resp = requests.post(judge_url + exercise_url.lstrip('/').replace('Problem','ReadSubmissionResults'), {
        'sort': "SubmissionDate-desc",
        'page': 1,
        'pageSize': exercise_result_page_size,
        'group': '',
        'filter': ''
    }, cookies=login,)
    dict_text: str = resp.text
    dict_text = dict_text.replace('null','None')
    dict_text = dict_text.replace('true','True')
    dict_text = dict_text.replace('false','False')
    try:
        exercise['submission_data'] = ast.literal_eval(dict_text)
    except:
        print(f"Can't text to dict the following: \n{dict_text}\n")


    return exercise


def get_exercises(login: dict, contest: dict):
    resp = requests.get(judge_url+f'Contests/{contest["type"].capitalize()}/Index/{contest["identifier"]}#0', cookies=login)
    exercises: list[dict] = []
    #print(resp.text)
    exercise_urls: list[str] = resp.text.split('"contentUrls":[')[1].split(']')[0].split(',')
    for i, exercise_url in enumerate(exercise_urls):
        exercises.append(get_exercise_information(login, exercise_url.strip('"'),
                        judge_url+f'Contests/{contest["type"].capitalize()}/Index/{contest["identifier"]}#{i}'))
    return exercises



def login_to_judge() -> dict:
    try:
        username, password = save.load('login.sav')
        used_saved = True
    except:
        username, password = input("username: "), input("password: ")
        used_saved = False

    login = get_login_data(username, password)
    while login is None:
        print("Wrong login!")
        username, password = input("username: "), input("password: ")
        used_saved = False
        login = get_login_data(username, password)

    if (not used_saved) and yes_or_no('Save?'):
        save.save('login.sav', username, password)
    return login


login_details: dict = login_to_judge()

# TODO: list[dict] : int
contests_list, number_of_pages = get_contests(login_details.copy(), contests_category_url)
#print("Got contests!\n", *[contest['name'] for contest in contests_list], sep='\n')
print(f"Got {len(contests_list)} contests!")
exercise_list: list[dict] = []
for contest_dict in contests_list:
    if contest_dict['type'] == 'unknown': continue
    try:
        exercise_list += get_exercises(login_details.copy(), contest_dict)
    except:
        exercise_list += get_exercises(login_details.copy(), contest_dict)
    print(f"Scanned contest \"{contest_dict['name']}\"")
print(f"Got {len(exercise_list)} exercises!")
#print("Got exercises!\n", *[exercise['name'] for exercise in exercise_list], sep='\n')

contests_list = [contest for contest in contests_list if contest['type'] != 'unknown']

save.save('exercises.sav', contests_list, exercise_list)

# print("Please use the evaluate.py to get your evaluation")

import evaluate

input("Press enter to exit ")