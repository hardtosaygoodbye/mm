class CNC:
    num = 1
    position = 0
    work_timer = 0
    work = None
    tool = 1

    def __init__(self, num, tool = 1):
        self.num = num
        self.position = (num - 1) // 2
        self.tool = int(tool)

    def execute(self):
        if self.work_timer >  0:
            self.work_timer = self.work_timer - 1
            if self.work_timer == 0:
                self.work.step = self.tool
