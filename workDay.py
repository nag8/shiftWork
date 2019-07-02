# coding: UTF-8
import datetime

CATEGORY_MORNING_COUNTER   = 1  # 朝窓口
CATEGORY_AFTERNOON_COUNTER = 2  # 昼窓口
CATEGORY_EVENING_COUNTER   = 3  # 夜窓口
CATEGORY_STUDY             = 4  # 研修
CATEGORY_MEETING           = 5  # 会議
CATEGORY_EVENT_KAKOM       = 6  # かこむ主催

categoryDict = {
    '会議'      :  CATEGORY_MEETING,
    'かこむ主催' :  CATEGORY_EVENT_KAKOM
    }

class WorkDay():

    def __init__(self, date, holiday=False):
        self.date       = date
        self.holiday    = holiday
        self.personList = []

    def appendPerson(self, person):
        self.personList.append(person)


class Person():

    def __init__(self, id, name, work):
        self.id    = id
        self.name  = name
        self.work  = work
        self.lucky = False


class Work():

    def __init__(self, startTime, endTime, eventList = []):
        self.startTime = startTime
        self.endTime   = endTime
        self.eventList = eventList

    def appendEvent(self, event):
        self.eventList.append(event)


class Event():

    def __init__(self, startTime, endTime, category, name):
        self.startTime = startTime
        self.endTime   = endTime
        self.category  = category
        self.name      = name
