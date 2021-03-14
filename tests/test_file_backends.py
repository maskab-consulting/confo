import os
import json
import shutil
import sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from confo.Backends.FileBackend import FileBackend




def get_mock():
    main_path = os.path.dirname(os.path.realpath(__file__))
    mock = main_path+"/configurations/"
    return mock
def get_obj():
    mock = get_mock()
    fb = FileBackend()
    cred = {"config_path": mock}
    fb.load_credentials(credentials=cred)
    return fb

def setup_function(function):
    mock = get_mock()
    systemA = mock+"/systemA"
    systemB = mock+"/systemB"
    confA1 = systemA+"/confA1.json"
    confA2 = systemA+"/confA2.json"
    confB1 = systemB+"/confB1.json"
    os.mkdir(mock)
    os.mkdir(systemA)
    os.mkdir(systemB)

    with open(confA1,"w+") as f:
        f.write(json.dumps({"name":"confA1","version":1}))

    with open(confA2,"w+") as f:
        f.write(json.dumps({"name":"confA2","version":1}))

    with open(confB1,"w+") as f:
        f.write(json.dumps({"name":"confB1","version":1}))


def teardown_function(function):
    mock = get_mock()
    shutil.rmtree(mock)


def test_count():
    fb = get_obj()
    fb.use_namespace("systemA")
    assert fb.get_count() == 2
    fb.use_namespace("systemB")
    assert fb.get_count() == 1, "Get count failure"

def test_get():
    fb = get_obj()
    fb.use_namespace("systemA")
    assert fb.get("confA1","name") == "confA1"
    assert fb.get("confA2","name") == "confA2"
    assert fb.get("confA2","version") == 1

def test_getall():
    fb = get_obj()
    fb.use_namespace("systemB")
    assert fb.get_all() == {"confB1":{"name":"confB1","version":1}}

def test_set():
    fb = get_obj()
    fb.use_namespace("systemA")
    fb.reload()
    fb.set("database","host","127.0.0.1")
    assert fb.get("database","host") == "127.0.0.1"
    assert fb.get_count() == 3

def test_system_swap():
    fb = get_obj()
    fb.use_namespace("systemA")
    assert fb.get_count() == 2
    fb.use_namespace("systemB")

    assert fb.get_count() == 1
