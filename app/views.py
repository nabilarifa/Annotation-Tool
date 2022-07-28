from flask import render_template, request, redirect, session
from app import app
import json
from datetime import datetime
from app import helper as FD
import pandas as pd


@app.route('/')
@app.route('/index', methods=['POST'])
def index():
    total_tasks = FD.get_total_tasks()
    completed_tasks = FD.get_completed_tasks()
    # print(completed_tasks)
    remaining = total_tasks-completed_tasks
    return render_template('layouts/index.html', completed=completed_tasks, remaining=remaining, total=total_tasks)


@app.route('/annotate', methods=['POST'])
def annotate():
    passcode = request.form['passcode_text'].strip()

    if(FD.is_passcode_present(passcode) == True):
        print('valid passcode')
        sentence = FD.get_next_sentence(passcode)
        if len(sentence) == 0:
            return render_template("finish.html", message='Thank You!')
        return render_template("layouts/test.html", annotator_id=passcode, eval_data=sentence)

    print("invalid passcode")
    return render_template("finish.html", message='Invalid Passcode!')


@app.route('/next_page', methods=['POST'])
def next_page():

    DUMP_PATH = 'results_dump/'

    print('next_page')
    result = request.form.to_dict(flat=False)

    annotator_id = result['annotator_id'][0]
    sentence_id = result['sentence_id'][0]

    FD.add_annotator(sentence_id, annotator_id)

    (sentence, tokens) = FD.get_sentence_data(sentence_id)

    print(sentence, tokens)

    json_data = {}

    json_data['id'] = sentence_id
    json_data['annotator_id'] = annotator_id
    json_data['text'] = sentence
    json_data['tokenized'] = tokens

    lid_list = []
    ner_list = []

    form_lid = result['LID']
    form_ner = result['NER']

    for token, lid, ner in zip(tokens, form_lid, form_ner):
        temp1 = {}
        temp2 = {}
        temp1[token] = lid
        temp2[token] = ner
        lid_list.append(temp1)
        ner_list.append(temp2)

    json_data['lid'] = lid_list
    json_data['ner'] = ner_list

    json_data['sentiment'] = result['sentiment_analysis'][0]
    json_data['humor'] = result['humor_detection'][0]
    json_data['abusive'] = result['abusive_sentence'][0]
    json_data['abusive_target'] = result['abusive_target'][0]

    with open(DUMP_PATH + annotator_id + '#' + sentence_id + '.json', 'w') as wf:
        json.dump(json_data, wf)
        wf.close()

    sentence = FD.get_next_sentence(annotator_id)

    if(len(sentence) > 0):
        return render_template("layouts/test.html", annotator_id=annotator_id, eval_data=sentence)

    return render_template("finish.html", message='Thank You!')


@app.route('/finish/<sentence_id>', methods=['GET'])
def finish(sentence_id):
    print(sentence_id)
    return render_template("finish.html", message='Thank You!')