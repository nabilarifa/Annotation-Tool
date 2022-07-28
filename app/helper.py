import pandas as pd
import json
import csv
import os
# change the url here
BASE_URL = 'C:/git/bangla-code-switching/Text_Annotation_Tool/'


def is_passcode_present(input_code):
    url = BASE_URL + 'passcodes.csv'
    df = pd.read_csv(url, sep=',', dtype=str)

    if input_code in list(df['code']):
        return True

    return False


def get_total_tasks():
    fl = open('total_sentences.txt', "r")
    for line in fl:
        return (int(line.strip('\n')))


def get_completed_tasks():
    url = BASE_URL + 'results_dump/'
    paths, dirs, files = next(os.walk(url))
    print(len(files))
    return len(files)


def str_to_list(data):
    if data[0] == '#':
        return []
    return list(data.split('#'))


def get_next_sentence(annotator_id):
    url = BASE_URL + 'Roman21.csv'

    df = pd.read_csv(url, sep=',', dtype={
                     'annotators': 'string'}, encoding='latin-1')

    data = {}
    found = False

    for id, sentence, tokens, annotators in zip(df['sent_id'], df['sentences'], df['tokens'], df['annotators']):
        annotators = str_to_list(annotators)
        if annotator_id in annotators:
            continue
        found = True
        data['sent_id'] = id
        data['sentences'] = sentence
        tokens = tokens.strip('][').split(', ')
        data['tokens'] = tokens
        break

    if found == False:
        return []

    return [data]


def get_sentence_data(sentence_id):
    url = BASE_URL + 'Roman21.csv'
    r = csv.reader(open(url, errors='ignore'))
    lines = list(r)
    sentence = ""
    tokens = ""

    for i in range(len(lines)):
        if lines[i][0] == sentence_id:
            sentence = lines[i][1]
            tokens = lines[i][2]
            tokens = tokens.strip('][').split(', ')
            break

    return (sentence, tokens)


def add_annotator(sentence_id, annotator_id):
    url = BASE_URL + 'Roman21.csv'
    r = csv.reader(open(url, errors='ignore'))
    lines = list(r)

    for i in range(len(lines)):
        if lines[i][0] == sentence_id:
            annotators = str_to_list(lines[i][3])
            annotators.append(annotator_id)
            lines[i][3] = '#'.join(annotators)

    writer = csv.writer(open(url, 'w'), lineterminator='\n')
    writer.writerows(lines)

    return True