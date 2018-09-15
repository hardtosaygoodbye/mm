from random import randint
from config import *
class CNC:
    num = 1
    position = 0
    work_timer = 0
    work = None
    tool = 1
    waste_time = 0
    trouble_time = 0
    is_error = False

    def __init__(self, num, tool = 1, is_error = False):
        self.num = num
        self.position = (num - 1) // 2
        self.tool = int(tool)
        self.is_error = is_error

    def execute(self):
        if self.trouble_time > 0:
            self.trouble_time = self.trouble_time - 1
            return
        if self.work_timer >  0:
            if self.is_error:
                process_total_time = 0
                if self.work.total_step == 1:
                    process_total_time = k_one_work_time
                elif self.work.total_step == 2:
                    if self.work.step == 0:
                        process_total_time = k_two_work_first_time
                    elif self.work.step == 1:
                        process_total_time = k_two_work_second_time
                if randint(0,100*process_total_time) == 0:
                    # 发生故障
                    self.trouble_time = randint(10*60,21*60)
                    self.work = None
                    self.work_timer = 0
                    return
            self.work_timer = self.work_timer - 1
            if self.work_timer == 0:
                self.__finish_process()
        else:
            self.waste_time = self.waste_time + 1
            
    def __finish_process(self):
        self.work.step = self.tool
