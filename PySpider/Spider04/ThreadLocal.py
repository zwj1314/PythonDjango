import threading

"""
局部线程变量
"""

local_school = threading.local()#每个线程独用，线程间不共享

def process_student():
    std = local_school.student
    print('Hello %s (%s)\n' % (std, threading.current_thread().name))

def process_thread(name):
    local_school.student = name
    process_student()

t1 = threading.Thread(target=process_thread, args=('Tom', ), name='TA') #name对应线程的名称
t2 = threading.Thread(target=process_thread, args=('Jack', ), name='TB')
t1.start()
t2.start()
t1.join()
t2.join()
