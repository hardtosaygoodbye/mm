from cnc import CNC
from rgv import RGV
from work import Work
from functools import cmp_to_key
from config import *

def get_move_time(position_x,position_y):
    distance = abs(position_x - position_y)
    if distance != 0:
        return k_move_time_arr[distance - 1]
    return 0

def cmpf(a,b,rgv):
    a_distance = abs(a.position - rgv.position)
    b_distance = abs(b.position - rgv.position)
    if (a_distance != b_distance):
        return a_distance - b_distance
    else:
        return a.place_time - b.place_time

def main():
    # 初始化对象
    cnc_arr = []
    for num in range(1,9):
        cnc = CNC(num)
        cnc_arr.append(cnc)
    rgv = RGV()
    for i in range(0,28800):
        if rgv.state == 0:
            # 判断是否有负数
            has_minus = False
            for cnc in cnc_arr:
                if cnc.work_timer - get_move_time(cnc.position, rgv.position) < 0:
                    has_minus = True
                    break
            min_time = float('inf')
            best_cnc = None
            if has_minus:
                # 有负数情况
                temp_cnc_arr = []
                for cnc in cnc_arr:
                    if cnc.work_timer - get_move_time(cnc.position, rgv.position) <= 0:
                        temp_cnc_arr.append(cnc)
                temp_cnc_arr.sort(key=cmp_to_key(lambda a,b:cmpf(a,b,rgv)))
                best_cnc = temp_cnc_arr[0]
            else:
                # 全为正数
                for cnc in cnc_arr:
                    place_time = 0
                    if cnc.num % 2 == 0:
                        place_time = k_even_place_time
                    else:
                        place_time = k_odd_place_time
                    temp_time = cnc.work_timer + place_time
                    if temp_time < min_time:
                        min_time = temp_time
                        best_cnc = cnc
            if rgv.position == best_cnc.position:
                if best_cnc.work_timer > 0:
                    rgv.wait()
                else:
                    rgv.place(best_cnc)
            else:    
                rgv.move_to_position(best_cnc.position)
        for cnc in cnc_arr:
            cnc.execute()
        rgv.execute()
    print(rgv.total_count) 

if __name__ == '__main__':
    main()
