import os
import json
import cPickle as pickle


def get_specific_dir(path):
    """
    Gets the directory specified. The path needs to exist in the directory. The get_directories
    function only goes down only one spot in the directory.

    ** Possible addition: make it go down multiple directories.

    Args:
      path (str): folder name given 

    Returns:
      dir_location (str): sends path to the specified directory
    """

    cwd = os.path.dirname(os.path.abspath(__file__))
    dir_location = os.path.join(os.path.split(cwd)[0], path)
    return dir_location


def get_directories():
	"""
	Gets the directory specified. The path needs to exist in the directory. The get_directories
	function only goes down only one spot in the directory.

	** Possible addition: make it go down multiple directories.

	Args:
	  path (str): folder name given 

	Returns:
	  datdir (str): sends path to the specified directory
	"""

	cwd = os.path.dirname(os.path.abspath(__file__))
	root = '/'.join(cwd.split(os.sep)[:-2])
	datadir = os.path.join(root, 'data')
	resultsdir = os.path.join(root, 'results')
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