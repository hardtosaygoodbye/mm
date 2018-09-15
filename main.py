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

def main():
    # 初始化对象
    cnc_arr = []
    for num in range(1, 9):
        cnc = CNC(num)
        cnc_arr.append(cnc)
    rgv = RGV()
    work_num = 1
    for i in range(0, 28800):
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
                for cnc in cnc_arr:
                    if cnc.work_timer - get_move_time(cnc.position, rgv.position) <= 0:
                        place_time = 0
                        if cnc.num % 2 == 0:
                            place_time = k_even_place_time
                        else:
                            place_time = k_odd_place_time
                        if get_move_time(cnc.position, rgv.position) + place_time < min_time:
                            min_time = get_move_time(cnc.position, rgv.position) + place_time
                            best_cnc = cnc
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
            # 对最佳cnc操作
            if rgv.position == best_cnc.position:
                if best_cnc.work_timer > 0:
                    rgv.wait()
                else:
                    new_work = Work(work_num)
                    work_num = work_num + 1
                    rgv.place(best_cnc, new_work)
            else:    
                rgv.move_to_position(best_cnc.position)
        for cnc in cnc_arr:
            cnc.execute()
        rgv.execute()
    print(rgv.work_arr)
    print(rgv.total_count) 

if __name__ == '__main__':
    main()
