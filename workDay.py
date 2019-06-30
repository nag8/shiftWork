# coding: UTF-8
import datetime

class WorkDay():

    # 初期化
    def __init__(self, date, holiday=False):
        self.date           = date
        self.holiday        = holiday
        self.shift          = []

    # 祝日を設定
    def setHoliday(self, holiday):
        self.holiday = holiday

    # シフトリストを設定
    def setShift(self, shift):
        self.shift.append(shift)
        # self.afternoonShift = shiftList[1]
        # self.eveningShift   = shiftList[2]

    # イベントを設定
    def setEvent(self, event):
        self.event = event

    def setLucky(self, person):
        self.lucky = person


class Shift():

    # 初期化
    def __init__(self, weekday, person, startTime, endTime, morningShift, afternoonShift, eveningShift):
        self.weekday        = weekday
        self.person         = person
        self.startTime      = startTime
        self.endTime        = endTime
        self.morningShift   = morningShift
        self.afternoonShift = afternoonShift
        self.eveningShift   = eveningShift

    # def setTime(self, startTime, endTime, morningShift='', afternoonShift='', eveningShift=''):
    #     self.startTime      = startTime
    #     self.endTime        = endTime
    #     self.morningShift   = morningShift
    #     self.afternoonShift = afternoonShift
    #     self.eveningShift   = eveningShift

class Person():


    # 初期化
    def __init__(self, id, name):
        self.id   = id
        self.name = name
