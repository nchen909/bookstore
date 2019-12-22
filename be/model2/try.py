#from datetime import datetime
# import time
# a=datetime.now()
# time.sleep(1)
# b=datetime.now()
# print(a)
# print(b)
# print((b-a).days)

# import schedule
# import time
#
#
# def job():
#     print("I'm working...")
#
#
#
# schedule.every().second.do(job)

# while True:
#     schedule.run_pending()
#     time.sleep(1)

# import datetime
# import schedule
# import threading
# import time
#
#
# def job1():
#     print("I'm working for job1")
#     time.sleep(2)
#     print("job1:", datetime.datetime.now())
#
#
# def job2():
#     print("I'm working for job2")
#     time.sleep(2)
#     print("job2:", datetime.datetime.now())
#
#
# def job1_task():
#     threading.Thread(target=job1).start()
#
#
# def job2_task():
#     threading.Thread(target=job2).start()
#
#
# def run():
#     schedule.every(5).seconds.do(job1_task)
#     schedule.every(5).seconds.do(job2_task)
#
#     while True:
#         schedule.run_pending()
#         time.sleep(1)
# # run()
# threading.Thread(target=job1).start()
# threading.Thread(target=job2).start()

# import threading
# # import schedule
# # from datetime import datetime
# # import time
# # i=0
# # def thread():
# #     time1=time.time()
# #     a=threading.Thread(target=job1())
# #     a.start()
# #     a.join()
# #     time2 = time.time()
# #     print(time2-time1)
# # def job1():
# #     global i
# #     print("I'm working for job",i)
# #     i+=1
# #     time.sleep(5)
# #
# # def do_every_sec():#每秒运行一次 将超时订单删去
# #     schedule.every().second.do(thread)#每秒开一个线程去auto_cancel,做完的线程自动退出
# #     while True:
# #         time.sleep(1)
# #         schedule.run_pending()
# #
# # timer=threading.Timer(0,do_every_sec)
# # timer.start()#由于开启了多线程 test运行完后会无法结束
# # # do_every_sec()
# # print(timer.isAlive())
# # timer.cancel()

import threading
import time

class TimerClass(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.count = 10

    def run(self):
        while self.count > 0 and not self.event.is_set():
            print (self.count)
            self.count -= 1
            self.event.wait(1)

    def stop(self):
        self.event.set()

tmr = TimerClass()
tmr.start()

time.sleep(3)
def tostop():
    global tmr
    tmr.stop()
tostop()