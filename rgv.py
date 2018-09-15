from copy import copy

class RGV:
    # 常量
    move_time_arr = [0,0,0]
    wash_time = 0
    position = 0
    # 用于判断是否被指令占用
    state = 0
    # 移动计数器
    move_timer = 0
    # 清洗计时器
    wash_timer = 0
    # 投料计时器
    place_timer = 0
    # 持有工作
    work = None
    # 总数
    total_count = 0
    # cnc
    current_cnc = None

    def __init__(self,move_time_arr,wash_time):
        self.wash_time = wash_time
        self.move_time_arr = move_time_arr

    # 等待中
    def wait(self):
        pass

    # 移动到位置
    def move_to_position(self, position):
        if self.state != 0:
            raise
        distance = abs(position - self.position)
        if distance != 0:
            self.state = 1
            self.move_timer = self.move_time_arr[distance - 1]
            self.position = position

    # 洗
    def __wash(self):
        self.state = 1
        self.wash_timer = self.wash_time
        self.work = None

    # 投料
    def place(self, cnc):
        if self.state != 0:
            raise
        self.state = 1
        self.place_timer = cnc.place_time
        cnc.work = copy(self.work)
        self.current_cnc = cnc
        if cnc.is_empty == 1:
            pass 
        else:
            self.__wash()
        cnc.is_empty = 0
        self.work = None

    # 执行
    def execute(self):
        once_token = 1
        if self.move_timer > 0 and once_token:
            once_token = 0
            self.move_timer = self.move_timer - 1
            if self.move_timer == 0:
                self.state = 0
        if self.wash_timer > 0 and once_token:
            once_token = 0
            self.wash_timer = self.wash_timer - 1
            if self.wash_timer == 0:
                self.state = 0
                self.total_count = self.total_count + 1
        if self.place_timer > 0 and once_token:
            once_token = 0
            self.place_timer = self.place_timer - 1
            if self.place_timer == 0:
                self.current_cnc.work_timer = self.current_cnc.work.one_work_time
                self.state = 0

if __name__ == '__main__':
    pass
        
