# coding: UTF-8
import configparser
import csv
import workDay


iniFile      = ''  # 設定
nickNameDict = {}  # ニックネーム

def main():

    initialize()

    getData()


def getData():

    rows = getCsv(iniFile.get('CSV', 'EVENT'))

    eventDict = {}

    for row in rows:

        # idと開始日からイベントIDを作成
        eventId = row[0] + '_' + row[1]
        print(row)

        # 既に同じIDが登録されている場合
        if (eventId in eventDict):
            duplicateEvent = eventDict[eventId]
            duplicateEvent.addPerson(row[8])

        # 登録されていない場合、かつカテゴリが登録条件に合致する場合
        elif row[5] in ('会議', 'かこむ主催'):

            # イベント辞書にIDをキーとして設定
            # eventDict[eventId] = event.Event(startTime, endTime, category, name)
            pass

    setNickName(eventDict)

def getCsv(csvPath):
    with open(csvPath, 'rt') as fin:
        cin = csv.reader(fin)
        header = next(cin)
        return [row for row in cin]


def setNickName(eventDict):

    eventList = []
    global nickNameDict

    with open(iniFile.get('CSV', 'NICK_NAME'), newline='') as csvfile:
        nickNameDict = csv.DictReader(csvfile)

    for key in eventDict:
        outerEvent = eventDict[key]

        nickName = getNicknameStr(outerEvent.person)
        eventList.append([outerEvent.startDate, outerEvent.startTime + '-' + outerEvent.endTime, outerEvent.name ])


# 初期化
def initialize():

    global iniFile
    iniFile = configparser.ConfigParser()
    iniFile.read('./IN/config.ini', 'UTF-8')


def getNicknameStr(nameList):

    nickNameStr = ''

    for value in nickNameDict:
        print(nickNameDict[value])

    for name in nameList:

        print(name)

        # 既に名前がある場合
        if name in nickNameDict:
            nickNameStr += ',' + nickNameDict[name]

        # ない場合
        else:
            nickNameStr += ',' +  name

    return nickNameStr


if __name__ == '__main__':
    main()
