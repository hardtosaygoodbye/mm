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
    last_work = None
    current_time = 0
    target_work = None
    work_arr = []

    def __init__(self):
        self.work_arr = []

    # 等待中
    def wait(self):
        pass

    # 移动到位置
    def move_to_position(self, position):
        if self.state != 0:
            return
        distance = abs(position - self.position)
        if distance == 0:
            return
        self.state = 1
        self.move_timer = k_move_time_arr[distance - 1]
        self.target_position = position

    # 洗
    def __wash(self):
        if self.state != 0:
            return
        self.state = 1
        self.wash_timer = k_wash_time

    # 投料
    def place(self, cnc):
        if self.state != 0:
            return
        self.state = 1
        if cnc.num % 2 == 0:
            self.place_timer = k_even_place_time
        else:
            self.place_timer = k_odd_place_time
        # 下料
        if cnc.work:
            if cnc.work.step == 1:
                cnc.work.first_place_down = self.current_time
            elif cnc.work.step == 2:
                cnc.work.second_place_down = self.current_time
        # 上料
        if self.target_work.step == 0:
            self.target_work.first_cnc_num = cnc.num
            self.target_work.first_place_up = self.current_time
        elif self.target_work.step == 1:
            self.target_work.second_cnc_num = cnc.num
            self.target_work.second_place_up = self.current_time
        self.target_cnc = cnc

    def log(self,work):
        temp_dict = {
            'num':work.num,
            'first_cnc_num': work.first_cnc_num,
            'first_place_up': work.first_place_up,
            'first_place_down': work.first_place_down,
            'second_cnc_num': work.second_cnc_num,
            'second_place_num': work.second_place_up,
            'second_place_down': work.second_place_down
        }
        self.work_arr.append(work)

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
        self.current_time = self.current_time + 1

    # 投料完成
    def __finish_place(self):
        self.state = 0
        if self.target_work.total_step == 1:
            self.target_cnc.work_timer = k_one_work_time
        elif self.target_work.total_step == 2:
            if self.target_work.step == 0:
                self.target_cnc.work_timer = k_two_work_first_time
            elif self.target_work.step == 1:
                self.target_cnc.work_timer = k_two_work_second_time
        self.target_cnc.work,self.target_work = self.target_work,self.target_cnc.work
        if self.target_work:
            if self.target_work.step == self.target_work.total_step:
                self.__wash()

    # 完成移动
    def __finish_move(self):
        self.state = 0
        self.position = self.target_position

    # 清洗完成
    def __finish_wash(self):
        self.state = 0
        self.total_count = self.total_count + 1
        self.log(self.target_work)
        self.target_work = None

if __name__ == '__main__':
    pass
        
