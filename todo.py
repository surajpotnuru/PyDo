__author__ = "suraj"

import sys, argparse, json, subprocess,math
from pprint import pprint
STR_TO_NUM = dict(first=1, last=-1)
def to_int(x):
    try:
        return int(x)
    except ValueError:
        return int(-1)

argParser = argparse.ArgumentParser(description='simple todo cli')

# avaliable arguments
argParser.add_argument('-a', '--add', help='add note', nargs='+')
argParser.add_argument('-r', '--remove', help='remove note',nargs='+')
argParser.add_argument('-s', '--show', help='show all notes',nargs='+')

args = argParser.parse_args()
with open('todo-data.json', 'r') as dataFile:
    data = dataFile.read()
    dataJsonAccept = data.replace("'", "\"")
    dataJson = json.loads(dataJsonAccept)

if args.add is None and args.remove is None and args.show is None:
    print("enter todo.py -h ")
elif isinstance(args.add, list) and args.remove is None and args.show is None:
    if type(args.add) == list:
        noteData = ' '.join(args.add)
    dataJson['num'] += 1
    temp = {
        'id': dataJson['num'],
        'note': noteData
    }
    writer = open("todo-data.json", "w")
    dataJson['notes'].append(temp)
    writer.write(json.dumps(dataJson))
    writer.close()
    print('Added')
elif args.add is None and isinstance(args.remove, list) and args.show is None:
    showData = dataJson["notes"]
    num = dataJson["num"]
    if "all" in args.remove:
        temp = dataJson
        temp["notes"] = []
        temp["num"] = 0
        writer = open("todo-data.json", "w")
        writer.write(json.dumps(temp))
        writer.close()
        print('All Notes Removed')
    else:
        enumList = enumerate(args.remove)
        removeListNum = []
        for i,x in enumList:
            if type(x) is str and x in STR_TO_NUM.keys():
                removeListNum.append(num) if x == "last" else removeListNum.append(STR_TO_NUM[x])
            if to_int(x) != -1 and to_int(x) in range(1,num+1):
                removeListNum.append(to_int(x))
        removeListNum.sort()
        removeListNum = list(set(removeListNum))
        temp = []
        uploadData = {
            "notes": [],
            "num": 0
        }
        print(removeListNum)
        tempNum = num
        enumList = enumerate(showData)
        idCount = 1
        for i, x in enumList:
            if i+1 in removeListNum:
                tempNum -= 1
            else:
                x = showData[i]
                x["id"] = idCount
                idCount += 1
                temp.append(showData[i])
        uploadData["notes"] = temp
        uploadData["num"] = tempNum
        writer = open("todo-data.json", "w")
        writer.write(json.dumps(uploadData))
        writer.close()
        print("Selected Notes Removed")
elif args.add is None and args.remove is None and isinstance(args.show, list):
    showData = dataJson['notes']
    if "all" in args.show:
        showNote = ""
        for note in showData:
            showNote += str(note['id']) + '. ' + note['note'] + '\n'
        print(showNote)
    else:
        enumList = enumerate(args.show)
        showListNum = []
        num = dataJson['num']
        for i,x in enumList:
            if type(x) is str and x in STR_TO_NUM.keys():
                showListNum.append(num) if x == "last" else showListNum.append(STR_TO_NUM[x])
            if to_int(x) != -1 and to_int(x) in range(1,num+1):
                showListNum.append(to_int(x))
        showListNum.sort()
        showListNum = list(set(showListNum))
        showNote = ""
        for i,x in enumerate(showData):
            if i+1 in showListNum:
                showNote += str(x['id'])+'. '+x['note']+'\n'
        print(showNote)