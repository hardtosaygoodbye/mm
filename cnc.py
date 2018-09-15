from random import randint
class CNC:
    num = 1
    position = 0
    work_timer = 0
    work = None
    tool = 1
    waste_time = 0
    trouble_time = 0

    def __init__(self, num, tool = 1):
        self.num = num
        self.position = (num - 1) // 2
        self.tool = int(tool)

    def execute(self):
        if self.trouble_time > 0:
            self.trouble_time = self.trouble_time - 1
            return
        if self.work_timer >  0:
            #if randint(0,100) == 0:
                # 发生故障
                #self.trouble_time = randint(10*60,21*60)
            self.work_timer = self.work_timer - 1
            if self.work_timer == 0:
                self.__finish_process()
        else:
            self.waste_time = self.waste_time + 1
            
    def __finish_process(self):
        self.work.step = self.tool
