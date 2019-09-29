import datetime

for i in range(27):
    today = datetime.date.today()
    new_day = today + datetime.timedelta(days=i)
    if i % 3 == 0:
        print('_'*3)
    print("* " + str(new_day.month) + "月" + str(new_day.day) + "日: ")
    print()

new_day = today + datetime.timedelta(days=i)
