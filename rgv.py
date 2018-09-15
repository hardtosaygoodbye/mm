from copy import copy
from config import *

class RGV:
    position = 0
    # 用于判断是否被指令占用
    state = 0
    # move
    target_position = 0
    move_timer = 0
    # wash
    wash_timer = 0
    total_count = 0
    # place
    place_timer = 0
    target_cnc = None

    # 等待中
    def wait(self):
        pass

    # 移动到位置
    def move_to_position(self, position):
        if self.state != 0:
            raise
        distance = abs(position - self.position)
        if distance == 0:
            return
        self.state = 1
        self.move_timer = k_move_time_arr[distance - 1]
        self.target_position = position

    # 洗
    def __wash(self):
        if self.state != 0:
            raise
        self.state = 1
        self.wash_timer = k_wash_time

    # 投料
    def place(self, cnc):
        if self.state != 0:
            raise
        self.state = 1
        if cnc.num % 2 == 0:
            self.place_timer = k_even_place_time
        else:
            self.place_timer = k_odd_place_time
        self.target_cnc = cnc

    # 执行
    def execute(self):
        if self.move_timer > 0:
            self.move_timer = self.move_timer - 1
            if self.move_timer == 0:
                self.__finish_move()
        if self.wash_timer > 0:
            self.wash_timer = self.wash_timer - 1
            if self.wash_timer == 0:
                self.__finish_wash()
        if self.place_timer > 0:
            self.place_timer = self.place_timer - 1
            if self.place_timer == 0:
                self.__finish_place()

    # 完成移动
    def __finish_move(self):
        self.state = 0
        self.position = self.target_position

    # 清洗完成
    def __finish_wash(self):
        self.state = 0
        self.total_count = self.total_count + 1

    # 投料完成
    def __finish_place(self):
        self.state = 0
        if self.target_cnc.is_full == 1:
            self.__wash()
        self.target_cnc.is_full = 1
        self.target_cnc.work_timer = k_one_work_time

if __name__ == '__main__':
    pass
        
