# coding: UTF-8
import configparser
import workDay
import csv
from dateutil.relativedelta import relativedelta
from datetime import date, timedelta
import datetime as dt
import calendar
import jpholiday
from operator import itemgetter
import copy

iniFile                    = '' # 設定
workDayList                = [] # シフト設定日
luckyCountList             = [] # ラッキーさんリスト


'''
参照
https://www.draw.io/#G1NWr0eZlKIxYNEkeO8e29hx7TYkem8LQk
https://qiita.com/tekitoh/items/fc8e3aeacc1cf0a0616c
'''

def main():

    initialize()

    createShift()

    alertShift()

    manageSheet()


def createShift():

    basicShiftList = getBasicShiftList()
    scheduleDict   = getScheduleDict()

    count3rdSunday = 0

    for wd in workDayList:

        if wd.holiday:
            wd.personList = copy.deepcopy(basicShiftList[6])
        else:
            wd.personList = copy.deepcopy(basicShiftList[wd.date.weekday()])

        if wd.date.weekday() == 6:
            count3rdSunday += 1

        # 第3SUNDAYの場合
        if count3rdSunday == 3 and wd.date.weekday() == 6:
            for person in wd.personList:
                person.work.startTime = getTime('8:30')
                person.work.endTime   = getTime('17:30')
                person.work.eventList = [workDay.Event(getTime('8:30'), getTime('17:30'), workDay.CATEGORY_STUDY, '第3SUNDAY')]

        for schedule in scheduleDict:
            if scheduleDict[schedule][0].day == wd.date.day:
                for person in wd.personList:
                    if person.name in scheduleDict[schedule][1]:
                        person.work.appendEvent(scheduleDict[schedule][2])

def alertShift():

    for wd in workDayList:
        for person in wd.personList:
            checkOverlapTime(wd, person, person.work.eventList)


def checkOverlapTime(wd, person, eventList):

    count = 0

    for event in eventList:

        count += 1

        for i in range(len(eventList) - count):
            starttime1 = event.startTime
            endtime1   = event.endTime
            starttime2 = eventList[i + count].startTime
            endtime2   = eventList[i + count].endTime
            if starttime1 < endtime2 and endtime1 > starttime2:
                print('Overlap:', '{}/{}'.format(wd.date.month, wd.date.day), person.name, event.name, event.startTime, eventList[i + count].name, eventList[i + count].startTime)
                assignOther(wd, person, event)

def assignOther(wd, person, event):

    for otherPerson in wd.personList:

        if person.id != otherPerson.id:

            # TODO 他の人の予定がその時間空いているかの確認
            pass


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

    for searchCategory in {workDay.CATEGORY_MORNING_COUNTER, workDay.CATEGORY_AFTERNOON_COUNTER, workDay.CATEGORY_EVENING_COUNTER}:

        counterFlg = False

        for event in eventList:
            if event.category == searchCategory:
                counterFlg = True
                subList.append(strCounter)
                break

        if not counterFlg:
            subList.append('')

    return subList

def getScheduleDict():

    rows = getCsv(iniFile.get('CSV', 'EVENT'))

    eventDict = {}

    for row in rows:

        date    = dt.datetime.strptime(row[1], '%Y/%m/%d')
        eventId = date.strftime('%m/%d') + '_' + row[0]

        if (eventId in eventDict):
            duplicateList = eventDict[eventId]
            duplicateList[1].append(row[8])

        elif row[5] in workDay.categoryDict:
            startTime = getTime(row[2][:5])
            endTime   = getTime(row[4][:5])
            category  = workDay.categoryDict[row[5]]
            name      = row[6]
            person    = row[8]

            eventDict[eventId] = [date, [person], workDay.Event(startTime, endTime, category, name)]

    return eventDict

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
        if wd.date.weekday() < 5 and not wd.holiday:

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
        eventList.append(workDay.Event(getTime('8:30'), getTime('12:30'), workDay.CATEGORY_MORNING_COUNTER, '窓口'))

    if afternoonCounter:
        eventList.append(workDay.Event(getTime('12:30'), getTime('17:30'), workDay.CATEGORY_AFTERNOON_COUNTER, '窓口'))

    if eveningCounter:
        eventList.append(workDay.Event(getTime('17:30'), getTime('21:30'), workDay.CATEGORY_EVENING_COUNTER, '窓口'))

    personId   = row[0]
    personName = row[1]

    return workDay.Person(personId, personName, workDay.Work(startTime, endTime, eventList))

def getTime(timeStr):

    if timeStr:
        timeList = timeStr.split(':')
        return dt.time(int(timeList[0]), int(timeList[1]), 0, 0)
    else:
        return None

# 開始日から終了日までの日のリストを取得
def date_range(start_date: dt, end_date: dt):
    diff = (end_date - start_date).days + 1
    return (start_date + timedelta(i) for i in range(diff))

def getCsv(csvPath):
    with open(csvPath, 'rt') as fin:
        cin = csv.reader(fin)
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
    startDate = (dt.datetime.today() + relativedelta(months=1)).replace(day=1)
    endDate   = (startDate + relativedelta(months=1)).replace(day=1) - timedelta(days=1)

    global workDayList

    for date in date_range(startDate, endDate):

        if date.weekday() == 6 or jpholiday.is_holiday(date.date()):
            workDayList.append(workDay.WorkDay(date, True))

        else:
            workDayList.append(workDay.WorkDay(date))


if __name__ == '__main__':
    main()
