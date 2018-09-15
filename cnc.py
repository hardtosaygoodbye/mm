class CNC:
    # 常量
    num = 1
    place_time = 0
    position = 0
    # 变量
    is_empty = 1
    work_timer = 0
    waste_time = 0

    def __init__(self, num, odd_place_time, even_place_time):
        self.num = num
        if num % 2 == 0:
            self.place_time = even_place_time
        else:
            self.place_time = odd_place_time
        self.position = (num - 1) // 2

    def execute(self):
        if self.work_timer == 0:
            self.waste_time = self.waste_time + 1
        else:
            self.work_timer = self.work_timer - 1

