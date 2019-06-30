# coding: UTF-8

class event():

    def __init__(self, row):
        self.id        = row[0]
        self.startDate = row[1]
        self.startTime = row[2][:-3]
        self.endDate   = row[3]
        self.endTime   = row[4][:-3]
        self.category  = row[5]
        self.name      = row[6]
        self.memo      = row[7]
        self.person    = [row[8]]
        self.place     = row[9]

    def about(self):
        print('event名 :', self.name)

    def addPerson(self, newPerson):
        self.person.append(newPerson)
