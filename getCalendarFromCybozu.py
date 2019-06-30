# coding: UTF-8
import configparser
import event
import csv


iniFile      = ''  # 設定
nickNameDict = {}  # ニックネーム

# メイン処理
def main():

    print('処理開始！')

    # 初期化
    initialize()

    # 表の変換
    manageSheet()

    print('処理終了！')

# シートの集計
def manageSheet():

    # csvファイルを取得
    rows = getCsv(iniFile.get('settings', 'CSV'))

    eventDict = {}

    for row in rows:

        # idと開始日からイベントIDを作成
        eventId = row[0] + row[1]

        # 既に同じIDが登録されている場合
        if (eventId in eventDict):
            duplicateEvent = eventDict[eventId]
            duplicateEvent.addPerson(row[8])

        # 登録されていない場合、かつカテゴリが登録条件に合致する場合
        elif row[5] in ('会議', 'かこむ主催'):

            # イベント辞書にIDをキーとして設定
            eventDict[eventId] = event.event(row)

    writeCsv(eventDict)


# csvファイルを読み取りで開く
def getCsv(csvPath):
    with open(csvPath, 'rt') as fin:
        cin = csv.reader(fin)
        header = next(cin)
        return [row for row in cin]

# csvファイルに情報を編集して出力
def writeCsv(eventDict):

    eventList = []
    global nickNameDict

    with open(iniFile.get('settings', 'CSV_NICK'), newline='') as csvfile:
        nickNameDict = csv.DictReader(csvfile)

    for key in eventDict:
        outerEvent = eventDict[key]

        nickName = getNicknameStr(outerEvent.person)
        eventList.append([outerEvent.startDate, outerEvent.startTime + '-' + outerEvent.endTime, outerEvent.name ])

    # csvファイルに出力
    with open(iniFile.get('settings', 'CSV_OUT'), 'wt') as fout:
        csvout = csv.writer(fout)
        csvout.writerows(eventList)

# 初期化
def initialize():

    global iniFile
    iniFile = configparser.ConfigParser()
    iniFile.read('./config.ini', 'UTF-8')


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
