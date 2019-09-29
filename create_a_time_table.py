import datetime

task_num = 0
for i in range(27):
    today = datetime.date.today()
    new_day = today + datetime.timedelta(days=i)
    if i % 3 == 0:
        print('_'*3)
        print()
        task_num += 1
        print(f"### Task{task_num}: ")
        print()
    print("" + str(new_day.month) + "月" + str(new_day.day) + "日: ")
    print("* yingshaoxo: ")
    print("* 孙雅斌: ")
    print("* 刘露: ")
    print()

new_day = today + datetime.timedelta(days=i)
