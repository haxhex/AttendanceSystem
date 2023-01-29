import datetime
x = datetime.datetime.now()
y =  "2023-01-29"
yy = datetime.datetime.strptime(y, "%Y-%m-%d")

print(x.date() < yy.date())


#Iliyaxxx----2022-12-24 03:26:06+00:00----2022-12-24 04:26:06+00:00
#Iliyaxxx----2022-12-25 03:27:03+00:00----2022-12-25 03:45:03+00:00
#Iliyaxxx----2022-12-25 03:36:56+00:00----2022-12-25 05:36:56+00:00
#Iliyaxxx----2022-12-25 06:37:20+00:00----2022-12-25 08:37:20+00:00

dt_string1 = "2022-12-24 03:26:06"
dt_object1 = datetime.datetime.strptime(dt_string1, "%Y-%m-%d %H:%M:%S") 

dt_string2 = "2022-12-25 03:27:03"
dt_object2 = datetime.datetime.strptime(dt_string2, "%Y-%m-%d %H:%M:%S") 

dt_string3 = "2022-12-25 03:36:56"
dt_object3 = datetime.datetime.strptime(dt_string3, "%Y-%m-%d %H:%M:%S")

dt_string4 = "2022-12-25 06:37:20"
dt_object4 = datetime.datetime.strptime(dt_string4, "%Y-%m-%d %H:%M:%S")


dt_string5 = "2022-12-24 04:26:06"
dt_object5 = datetime.datetime.strptime(dt_string5, "%Y-%m-%d %H:%M:%S") 

dt_string6 = "2022-12-25 03:45:03"
dt_object6 = datetime.datetime.strptime(dt_string6, "%Y-%m-%d %H:%M:%S") 

dt_string7 = "2022-12-25 05:36:56"
dt_object7 = datetime.datetime.strptime(dt_string7, "%Y-%m-%d %H:%M:%S")

dt_string8 = "2022-12-25 08:37:20"
dt_object8 = datetime.datetime.strptime(dt_string8, "%Y-%m-%d %H:%M:%S")


timeList = [str(dt_object1.time()), str(dt_object2.time()), str(dt_object3.time()), str(dt_object4.time())]

timeList1 = [str(dt_object5.time()), str(dt_object6.time()), str(dt_object7.time()), str(dt_object8.time())]


mysum1 = datetime.timedelta()
for i in timeList:
    (h, m, s) = i.split(':')
    d = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
    mysum1 += d
print(str(mysum1))
mysum2 = datetime.timedelta()
for i in timeList1:
    (h, m, s) = i.split(':')
    d = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
    mysum2 += d
    
print(str(mysum2))

time = mysum2 - mysum1
print(time)

