import time
import random

def mysleep(max):
    '''
    睡眠 [max-1,max+1] 内的随机数
    :param max:
    :return:
    '''
    sleeptime = float(format(random.randint(max - 1, max + 1) + random.random(), '1.2f'))
    time.sleep(sleeptime)


def print_and_log(msg):
    '''
    打印日志并输出在屏幕上，非线程安全
    :param msg:
    :return:
    '''
    now = time.strftime("%Y-%m-%d %X", time.localtime())
    msg = now + "  " + msg
    print(msg)
    with open(f'log.txt', 'a', encoding='utf-8') as f:
        f.write('\n' + msg)