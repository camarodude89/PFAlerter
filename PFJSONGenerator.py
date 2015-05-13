#! python3

import sched
import time
import json
import string
import codecs
import random


def getListenerList(data):
    data = json.loads(data)
    return data, data['ListenersContainer']['Listener']
    
def buildTestJSON(fileIn, fileOut, newElementKey=None, newElementValue=None):
    """generates JSON txt file adding the key and values specified by the user
    
    Keyword arguments:
    fileIn -- the file containing JSON data to be read
    fileOut -- the file to direct results to
    """
    
    data = open(fileIn).read()
    data, testList = getListenerList(data)
    newElementKey = newElementKey or 'TimeSinceLastTransaction'
    
    for i, j in zip(testList, range(1, len(testList)+1)):
        newElementValue = newElementValue or '350000'
        i[newElementKey] = int(newElementValue)
    
    data['ListenersContainer']['Listener'] = testList
    jsonToTextFile(data, fileOut)
    return
    
def jsonToTextFile(data, fileName):
    """sends the json data to text file with 'pretty printing'
    
    Keyword arguments:
    data -- the json object to parse
    fileName -- the file to save results to
    """
    
    data = json.dumps(data, sort_keys=True, indent=4)
    with codecs.open(fileName, 'w+', 'utf-8') as save_file:
        save_file.write(str(data))
    return
    
def lastTransactionCounter(fail=None):
    global timeSinceLastTransaction
    if timeSinceLastTransaction < 300000:
        timeSinceLastTransaction += (interval * 1000)
    elif timeSinceLastTransaction >= 300000 and not fail:
        timeSinceLastTransaction = 1000

def runTest():
    fail = False
    if random.randint(0, 10) > 3:
        fail = True
    lastTransactionCounter(fail)
    lastTransactionTime = int(time.time() * 1000 - timeSinceLastTransaction)
    buildTestJSON('tempJSON2.txt', 'testJSON2.txt', newElementValue=timeSinceLastTransaction)
    print(timeSinceLastTransaction, '|', lastTransactionTime)
    
s = sched.scheduler(time.time, time.sleep)
interval = 1
timeSinceLastTransaction = 1000
while(True):
    s.enter(interval, 1, runTest)
    s.run()