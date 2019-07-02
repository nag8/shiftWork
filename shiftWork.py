# coding: UTF-8
import configparser
import workDay
import csv
from dateutil.relativedelta import relativedelta
from datetime import date, timedelta
import datetime
import calendar
import jpholiday
from operator import itemgetter
import copy


iniFile                    = '' # 設定
workDayList                = [] # シフト設定日
luckyCountList             = [] # ラッキーさんリスト
CATEGORY_MORNING_COUNTER   = 1  # 朝窓口
CATEGORY_AFTERNOON_COUNTER = 2  # 昼窓口
CATEGORY_EVENING_COUNTER   = 3  # 夜窓口
CATEGORY_STUDY             = 4  # 研修
CATEGORY_MEETING           = 5  # 会議
CATEGORY_EVENT_KAKOM       = 6  # かこむ主催


'''
参照
https://www.draw.io/#G1NWr0eZlKIxYNEkeO8e29hx7TYkem8LQk
'''

def main():

    initialize()

    createShift()

    manageSheet()


def createShift():

    basicShiftList = getBasicShiftList()

    count3rdSunday = 0

    for wd in workDayList:

        if wd.date.weekday() == 6:
            count3rdSunday += 1

        wd.personList = copy.deepcopy(basicShiftList[wd.date.weekday()])

        # 第3SUNDAYの場合
        if count3rdSunday == 3:
            for person in wd.personList:
                person.startTime = getTime('8:30')
                person.endTime   = getTime('17:30')
                person.eventList = [workDay.Event(getTime('8:30'), getTime('17:30'), CATEGORY_STUDY, '第3SUNDAY')]

# 表を編集して出力
def manageSheet():

    yobi = {
        0 : "月",
        1 : "火",
        2 : "水",
        3 : "木",
        4 : "金",
        5 : "土",
        6 : "日"}
    printList = [['日付'],['曜日']]

    for person in workDayList[0].personList:
        printList.append([person.name])

    lotteryLucky()

    # 日付行
    for wd in workDayList:

        # 日付
        day = wd.date
        dayStr = '{}/{}'.format(day.month, day.day)

        printList[0].append('朝' + dayStr)
        printList[0].append('昼' + dayStr)
        printList[0].append('夜' + dayStr)
        printList[0].append('始' + dayStr)
        printList[0].append('終' + dayStr)
        printList[0].append('ラ' + dayStr)

        yobiStr = yobi[day.weekday()]

        for i in range(6):
            printList[1].append(yobiStr)

        for i, person in enumerate(wd.personList):

            printList[i + 2].extend(getCounterList(person.work.eventList))
            printList[i + 2].append(person.work.startTime)
            printList[i + 2].append(person.work.endTime)
            if person.lucky:
                printList[i + 2].append('ラッキー')
            else:
                printList[i + 2].append('')

    writeCsv(printList)

def getCounterList(eventList):

    subList = []
    strCounter = '窓口'

    for searchCategory in {CATEGORY_MORNING_COUNTER, CATEGORY_AFTERNOON_COUNTER, CATEGORY_EVENING_COUNTER}:

        counterFlg = False

        for event in eventList:
            if event.category == searchCategory:
                counterFlg = True
                subList.append(strCounter)
                break

        if not counterFlg:
            subList.append('')

    return subList

# ラッキーさん抽選
def lotteryLucky():

    maxNum = 999

    global workDayList
    global luckyCountList

    # ラッキーさんリストが空の場合
    if not luckyCountList:
        for person in workDayList[0].personList:
            luckyCountList.append([0, person])

    for wd in workDayList:

        # 平日の場合
        if wd.date.weekday() < 5:

            lotteryList = copy.deepcopy(luckyCountList)

            for i, person in enumerate(wd.personList):

                if not person.work.startTime or person.work.startTime.hour != 8:
                    lotteryList[i][0] = maxNum

            lotteryList.sort(key=lambda x:x[0])

            for lucky in luckyCountList:
                if lucky[1].id == lotteryList[0][1].id:
                    lucky[0] += 1

                    for person in wd.personList:

                        if person.id == lucky[1].id:
                            person.lucky = True
                            break

                    break

# 基本シフト情報を取得
def getBasicShiftList():

    rows = getCsv(iniFile.get('CSV', 'BASIC'))

    basicShiftList = []

    for row in rows:
        weekList = []

        # 一週間分
        for i in range(7):
            weekList.append(getBasicPerson(row, i))

        basicShiftList.append(weekList)

    # 転置
    return [list(x) for x in zip(*basicShiftList)]

def getBasicPerson(row, num):

    eventList = []

    # 一旦時刻も文字列で格納
    startTime        = getTime(row[2 + num * 5])
    endTime          = getTime(row[3 + num * 5])
    morningCounter   = row[4 + num * 5]
    afternoonCounter = row[5 + num * 5]
    eveningCounter   = row[6 + num * 5]

    if morningCounter:
        eventList.append(workDay.Event(getTime('8:30'), getTime('12:30'), CATEGORY_MORNING_COUNTER, '窓口'))

    if afternoonCounter:
        eventList.append(workDay.Event(getTime('12:30'), getTime('17:30'), CATEGORY_AFTERNOON_COUNTER, '窓口'))

    if eveningCounter:
        eventList.append(workDay.Event(getTime('17:30'), getTime('21:30'), CATEGORY_EVENING_COUNTER, '窓口'))

    personId   = row[0]
    personName = row[1]

    return workDay.Person(personId, personName, workDay.Work(startTime, endTime, eventList))

def getTime(timeStr):

    if timeStr:
        timeList = timeStr.split(':')
        return datetime.time(int(timeList[0]), int(timeList[1]), 0, 0)
    else:
        return None

def getCategory(str):

    categoryDict = {
        '窓口': 1,
        'test':   'Kevin Ford Mench',
        'test2':  'Brooks Litchfield Conrad'
    }

    return categoryDict[str]

# 開始日から終了日までの日のリストを取得
def date_range(start_date: datetime, end_date: datetime):
    diff = (end_date - start_date).days + 1
    return (start_date + timedelta(i) for i in range(diff))

# csvファイルをリスト形式で開く（読み取り専用）
def getCsv(csvPath):
    with open(csvPath, 'rt') as fin:
        cin = csv.reader(fin)
        # 1行目を飛ばす
        next(cin)
        return [row for row in cin]

# csvファイルに出力
def writeCsv(strList):

    # csvファイルに出力
    with open(iniFile.get('CSV', 'OUT'), 'wt', encoding='shift_jis') as fout:
        csvout = csv.writer(fout)
        csvout.writerows(strList)

def initialize():

    global iniFile
    iniFile = configparser.ConfigParser()
    iniFile.read('./IN/config.ini', 'UTF-8')


    # 翌月初日と末日を取得
    startDate = (datetime.datetime.today() + relativedelta(months=1)).replace(day=1)
    endDate   = (startDate + relativedelta(months=1)).replace(day=1) - timedelta(days=1)

    global workDayList

    for date in date_range(startDate, endDate):

        # TODO 祝日設定も追加
        if date.weekday() == 6:
            workDayList.append(workDay.WorkDay(date, True))

        else:
            workDayList.append(workDay.WorkDay(date))

if __name__ == '__main__':
    main()
