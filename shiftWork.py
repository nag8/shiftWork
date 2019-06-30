# coding: UTF-8
import configparser
import workDay
import csv
import datetime
from dateutil.relativedelta import relativedelta
from datetime import datetime, date, timedelta
import calendar
import jpholiday
from operator import itemgetter



iniFile     = '' # 設定
workDayList = [] # シフト設定日
luckyList   = [] # ラッキーさんリスト
yobi = {0:"月",1:"火",2:"水",3:"木",4:"金",5:"土",6:"日"}

'''
参照
https://www.draw.io/#G1NWr0eZlKIxYNEkeO8e29hx7TYkem8LQk
'''

# メイン処理
def main():

    # 初期化
    initialize()

    # シフト作成
    createShift()


# シフト作成
def createShift():

    # 基本シフトを取得
    basicShiftList = getBasicShift()

    count3rdSunday = 0

    # 1日ごと
    for workDay in workDayList:

        if workDay.date.weekday() == 6:
            count3rdSunday += 1

        # 人ごと
        for basicShift in  basicShiftList:

            # 第3SUNDAYの場合
            if count3rdSunday == 3:

                shift = basicShift[workDay.date.weekday()]
                # TODO うまくいっていないので治す
                # shift.startTime      = '08:30'
                # shift.endTime        = '17:30'
                # shift.morningShift   = ''
                # shift.afternoonShift = ''
                # shift.eveningShift   = ''
                workDay.setShift(shift)


            else:
                workDay.setShift(basicShift[workDay.date.weekday()])


    manageSheet()





    '''
    やりたいこと
    - 基本シフトから各日に当てはめ
    - 窓口
    -
    -
    -

    最終目標
    ◯◯
    7/1 8:30　〜 17:30。 朝窓口　昼会議（〜）
    〜
    7/31 8:30　〜 17:30。 会議（全体会議）

    シフトclass
    窓口◯名。
    '''

# 表を編集して出力
def manageSheet():

    # 出力リスト
    printList  = []
    dayList    = ['名']
    personList = []

    # 日付行
    for workDay in workDayList:

        # 日付
        day = workDay.date
        day = "{}/{}".format(day.month, day.day)

        dayList.append('朝' + day)
        dayList.append('昼' + day)
        dayList.append('夜' + day)
        dayList.append('始' + day)
        dayList.append('終' + day)
        dayList.append('ラ' + day)

    printList.append(dayList)

    yobiList = ['']
    # 曜日
    for workDay in workDayList:

        for i in range(6):
            yobiList.append(yobi[workDay.date.weekday()])

    printList.append(yobiList)

    # 名前列
    for shift in workDayList[0].shift:
        printList.append([shift.person.name])

    for workDay in workDayList:
        for i, shift in enumerate(workDay.shift):

            printList[i + 2].append(shift.morningShift)
            printList[i + 2].append(shift.afternoonShift)
            printList[i + 2].append(shift.eveningShift)
            printList[i + 2].append(shift.startTime)
            printList[i + 2].append(shift.endTime)
            printList[i + 2].append('')

    lotteryLucky()
    writeCsv(printList)

# ラッキーさん抽選
def lotteryLucky():

    maxNum = 999

    global workDayList
    global luckyList

    # ラッキーさんリストが空の場合
    if not luckyList:

        # 人情報を設定
        for shift in workDayList[0].shift:
            luckyList.append([0, shift.person])

    print(luckyList)

    for workDay in workDayList:

        lotteryList = luckyList

        for shift in workDay.shift:
            minNum = 0

            for lottery in lotteryList:
                if shift.startTime != '08:30':
                    lottery = maxNum

        sorted(lotteryList, key=itemgetter(0))
        lotteryList[0]
        print(lotteryList)



            # 土日祝の場合
            # if workDay.date.weekday() >= 5 and workDay.date.holiday:
            #     printList[i + 1].append('')
            # else:
            #
            #     printList[i + 1].append('')



# 基本シフト情報を取得
def getBasicShift():

    # 基本シフト情報を取得
    rows = getCsv(iniFile.get('CSV', 'BASIC'))

    basicShiftList = []

    for row in rows:
        person = workDay.Person(int(row[0]),row[1])
        week = {}

        # 1週間分のシフトを設定
        num = 0
        for i in range(7):

            if not row[2 + num]:
                shift = workDay.Shift(i, person, None, None, None, None, None)
            else:
                shift = workDay.Shift(i, person, row[2 + num], row[3 + num], row[4 + num], row[5 + num], row[6 + num])

            num += 5
            week[shift.weekday] = shift


        basicShiftList.append(week)

    return basicShiftList

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

# 初期化
def initialize():

    global iniFile
    iniFile = configparser.ConfigParser()
    iniFile.read('./IN/config.ini', 'UTF-8')


    # 翌月初日と末日を取得
    startDay = (datetime.today() + relativedelta(months=1)).replace(day=1)
    endDay   = (startDay + relativedelta(months=1)).replace(day=1) - timedelta(days=1)

    global workDayList

    for day in date_range(startDay, endDay):
        workDayList.append(workDay.WorkDay(day))

        # TODO 祝日設定


if __name__ == '__main__':
    main()
