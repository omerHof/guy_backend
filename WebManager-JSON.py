import logging
import os
import pickle
import json
import csv
import PreProccesing
import Index
import ParseOutputFile
import shutil

import numpy as np
from flask import Flask, request, render_template, jsonify, Response, make_response
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
    # CORS(app, origins="*", allow_headers=[
    # "Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
    # supports_credentials=True, intercept_exceptions=False)


states = dict()

# Classification process and output page
@app.route('/upload', methods=['GET', 'POST'])
def uploaded_file():
    if request.method == 'POST':
        data_set_name = request.form['data_set_name']
        username = request.form['username']
        if data_set_name != 'undefined' and username != 'undefined':
            path = 'DataSets/' + data_set_name
            if 'old_data_set_name' not in request.form.keys():
                if not os.path.exists(path):
                    os.mkdir(path)
                else:
                    return jsonify(
                        {'errMsg': 'DataSet Already Exist'}), 416
            else:   #edit mode
                old_data_set_name = request.form['old_data_set_name']
                if old_data_set_name != data_set_name:
                    os.rename('DataSets/' + old_data_set_name, path)

        else:
            if data_set_name == 'undefined' and username == 'undefined':
                return jsonify(
                    {'errMsg': 'No DataSet Name and UserName Provided'}), 416
            if data_set_name == 'undefined':
                return jsonify(
                    {'errMsg': 'No DataSet Name Provided'}), 416
            else:
                return jsonify(
                     {'errMsg': 'No UserName Provided'}), 416
        class_name = request.form['className']
        if class_name == 'undefined':
            class_name = ''
        second_class_name = request.form['secondclassName']
        if second_class_name == 'undefined':
            second_class_name = ''
        comments = request.form['comments']
        if comments == 'undefined':
            comments = ''
        # files
        if 'output' in request.files.keys():
            output = request.files['output']
            output_file_name = output.filename
            output.save(path + "/KLOutput")
            if os.path.exists(path + '/chunks'):
                shutil.rmtree(path + '/chunks', ignore_errors=True)
            os.mkdir(path + '/chunks')
            PreProccesing.create_index_files(path + "/KLOutput", path + '/chunks')
        else:
            output_file_name = 'File does not exist'
        if 'states' in request.files.keys():
            states_arr = []
            states_file = request.files['states']
            states_file_name = states_file.filename
            states_file.save(path + "/states.csv")
            with open(path + "/states.csv",encoding='utf-8-sig') as csvFile:
                csvReader = csv.DictReader(csvFile)
                for csvRow in csvReader:
                    states_arr.append(csvRow)
            # write the data to a json file
            os.remove(path + "/states.csv")
            with open(path + "/states.json", "w") as jsonFile:
                jsonFile.write(json.dumps(states_arr, indent=4))
        else:
            states_file_name = 'File does not exist'
        if 'entities' in request.files.keys():
            arr = []
            entities = request.files['entities']
            entities_file_name = entities.filename
            entities.save(path + "/entities.csv")
            with open(path + "/entities.csv") as csvFile:
                csvReader = csv.DictReader(csvFile)
                for csvRow in csvReader:
                    arr.append(csvRow)
            # write the data to a json file
            os.remove(path + "/entities.csv")
            with open(path + "/entities.json", "w") as jsonFile:
                jsonFile.write(json.dumps(arr, indent=4))
        else:
            entities_file_name = 'File does not exist'
        if 'rawData' in request.files.keys():
            raw_data = request.files['rawData']
            raw_data_file_name = raw_data.filename
            raw_data.save(path + "/rawData")
        else:
            raw_data_file_name = 'File does not exist'
        if 'secondClassOutput' in request.files.keys():
            second_class_output = request.files['secondClassOutput']
            second_class_output_file_name = second_class_output.filename
            second_class_output.save(path + "/secondClassOutput")
        else:
            second_class_output_file_name = 'File does not exist'

        settings = {
            'data_set_name': data_set_name,
            'username': username,
            'class_name': class_name,
            'second_class_name': second_class_name,
            'comments': comments,
            'output_file_name': output_file_name,
            'states_file_name': states_file_name,
            'entities_file_name': entities_file_name,
            'raw_data_file_name': raw_data_file_name,
            'second_class_output_file_name': second_class_output_file_name,
        }
        with open(path + '/settings.json', 'w') as outfile:
            json.dump(settings, outfile)
        data = {'status': 'ok'}
        js = json.dumps(data)
        resp = Response(js, status=200, mimetype='application/json')
        resp.headers['Access-Control-Allow-Origin'] = '*'
        # resp = jsonify(data)
        # resp.
        # resp.status_code = 200
        return resp


@app.route('/getDataSets', methods=['GET'])
def get_dataSets():
    data_sets_names = os.listdir("./DataSets")
    data_sets_details = list()
    for name in data_sets_names:
        settings_path = "./DataSets/" + name + "/settings.json"
        with open(settings_path, 'r') as fs:
            settings = json.load(fs)
        data_sets_details.append(settings)
    return jsonify(
        {'DataSets': data_sets_details})


@app.route('/getEntities', methods=['POST'])
def get_entities():
    if request.method == 'POST':
        data_set_name = request.form['data_set_name']
        path = 'DataSets/' + data_set_name + '/entities.json'
        with open(path, 'r') as fs:
            entities = json.load(fs)
    # js = json.dumps(entities, indent=4)
    # resp = Response(js, status=200, mimetype='application/json')
    # resp.headers['Access-Control-Allow-Origin'] = '*'
    # # resp = jsonify(data)
    # # resp.
    # # resp.status_code = 200
    # return resp
    return jsonify({'Entities': entities})

@app.route('/getStates', methods=['POST'])
def get_states():
    if request.method == 'POST':
        data_set_name = request.form['data_set_name']
        path = 'DataSets/' + data_set_name + '/states.json'
        with open(path, 'r') as fs:
            states_from_file = json.load(fs)
    return jsonify({'States': states_from_file})

@app.route('/initiateTirps', methods=['POST'])
def initiate_tirps():
    data_set_name = request.form['data_set_name']
    path = 'DataSets/' + data_set_name
    global states
    states = ParseOutputFile.parse_states_file(path + '/states.json')
    root_elements = Index.parse_main_index(path + '/chunks', states)
    # json_root_elements = json.dumps([ob.__dict__ for ob in root_elements])
    response = make_response(jsonify({'Root': root_elements}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/getSubTree', methods=['POST'])
def get_sub_tree():
    data_set_name = request.form['data_set_name']
    TIRP = request.form['TIRP']
    path = 'DataSets/' + data_set_name + '/chunks'
    tirps = Index.get_sub_tree(TIRP, states, path)
    return jsonify({'TIRPs': tirps})




if __name__ == '__main__':
    handler = logging.FileHandler('./log.log')
    handler.setLevel(logging.ERROR)
    app.debug = True  # allows for changes to be enacted without rerunning server
    app.logger.addHandler(handler)
    app.config["JSON_SORT_KEYS"] = False
    app.run()
