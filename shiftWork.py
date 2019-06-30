# coding: UTF-8
import configparser
import workDay
import csv
import datetime
from dateutil.relativedelta import relativedelta
from datetime import datetime, date, timedelta
import calendar
import jpholiday



iniFile     = '' # 設定
workDayList = [] # シフト設定日

'''
参照
https://qiita.com/calderarie/items/0ef921b476911a55148d
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

    # 出力リスト
    printList = []
    dayList   = []
    for workDay in workDayList:
        day = workDay.date
        dayList.append("{}/{}".format(day.month, day.day))

    printList.append(dayList)

    for workDay in workDayList:
        for shift in workDay.shift:
            # print(workDay.date, shift.person.name, shift.startTime)
            printList.append([shift.person.name, shift.startTime])

    writeCsv(printList)




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


if __name__ == '__main__':
    main()
