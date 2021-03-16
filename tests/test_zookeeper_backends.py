# import os
# import json
# import shutil
# import sys,inspect
# currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# parentdir = os.path.dirname(currentdir)
# sys.path.insert(0,parentdir)
# from confo.Backends.ZookeeperBackend import ZookeeperBackend
#
#
#
#
#
# def get_obj():
#     zb = ZookeeperBackend()
#     cred = {"zookeeper_host": "0.0.0.0", "zookeeper_port":2181}
#     zb.load_credentials(credentials=cred)
#     return zb
#
# def setup_function(function):
#     pass
# def teardown_function(function):
#    pass
#
#
# def test_count():
#     fb = get_obj()
#     fb.use_namespace("systemA")
#     assert fb.get_count() == 1
#     fb.use_namespace("systemB")
#     assert fb.get_count() == 3, "Get count failure"
#
# def test_get():
#     fb = get_obj()
#     fb.use_namespace("systemA")
#     print(fb.get("database","host"))
#     assert fb.get("database","host") == "127.0.0.1"
#     assert fb.get("database","port") == 3306
#     assert fb.get("database","user") == "root"
#
# def test_getall():
#     fb = get_obj()
#     fb.use_namespace("systemA")
#     assert fb.get_all() == {'database':
#                                 {'host': '127.0.0.1',
#                                  'port': 3306, 'user': 'root',
#                                  'password': 'newpassword'}}
#
# def test_set():
#     fb = get_obj()
#     fb.use_namespace("systemB")
#     fb.reload()
#     fb.set("database","host","127.0.0.1")
#     assert fb.get("database","host") == "127.0.0.1"
#     assert fb.get_count() == 4
#
# def test_system_swap():
#     fb = get_obj()
#     fb.use_namespace("systemA")
#     assert fb.get_count() == 1
#     fb.use_namespace("systemB")
#
#     assert fb.get_count() == 3
