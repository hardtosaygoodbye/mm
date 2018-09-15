class CNC:
    num = 1
    position = 0
    is_full = 0
    work_timer = 0
    work = None

    def __init__(self, num):
        self.num = num
        self.position = (num - 1) // 2

    def execute(self):
        if self.work_timer >  0:
            self.work_timer = self.work_timer - 1

