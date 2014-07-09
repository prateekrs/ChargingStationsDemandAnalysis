import os
import json
import cPickle as pickle

def get_directories():
    cwd = os.path.dirname(os.path.abspath(__file__))
    datadir = os.path.join(os.path.split(cwd)[0], 'data')
    resultsdir = os.path.join(os.path.split(cwd)[0], 'results')
    return datadir, resultsdir


def serialize_object(obj,filename):
    pkl_file = open(filename, 'wb')
    pickle.dump(obj, pkl_file)
    pkl_file.close()


def load_json(json_filename):
    # print "loading json"
    json_data = open(json_filename).read()
    data = json.loads(json_data)
    return data


def render_file_style(frase):
    return frase.replace("/", "").replace(" ", "").replace(".", "").replace(",", "")


def write_json(filename, dictionary):
    print "writing file: ", filename
    with open(filename, 'wb') as fp:
        json.dump(dictionary, fp, indent=4, sort_keys=True)


def make_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)   