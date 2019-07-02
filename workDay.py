# coding: UTF-8
import datetime

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
