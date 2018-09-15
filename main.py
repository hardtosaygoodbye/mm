from cnc import CNC
from rgv import RGV
from work import Work
from functools import cmp_to_key
from config import *
from copy import *
import itertools

def get_move_time(position_x, position_y):
    distance = abs(position_x - position_y)
    if distance != 0:
        return k_move_time_arr[distance - 1]
    return 0

def get_has_minus(cnc_arr,rgv):
    has_minus = False
    for cnc in cnc_arr:
        if cnc.work_timer - get_move_time(cnc.position, rgv.position) < 0:
            has_minus = True
            break
    return has_minus

def main(tools = [1] * 8, step = 1, is_error = False):
    cnc_arr = [CNC(i+1, tools[i], is_error) for i in range(0,8)]
    rgv = RGV()
    work_num = 1
    for i in range(0, 28800):
        if rgv.state == 0:
            temp_cnc_arr = []
            for cnc in cnc_arr:
                if rgv.target_work:
                    if rgv.target_work.step + 1 == cnc.tool:
                        temp_cnc_arr.append(cnc)
                else:
                    if cnc.tool == 1:
                        temp_cnc_arr.append(cnc)
            min_time = float('inf')
            best_cnc = None
            if get_has_minus(temp_cnc_arr,rgv):
                # 有负数情况
                for cnc in temp_cnc_arr:
                    if cnc.work_timer - get_move_time(cnc.position, rgv.position) <= 0:
                        place_time = k_even_place_time if cnc.num % 2 == 0 else k_odd_place_time
                        if get_move_time(cnc.position, rgv.position) + place_time < min_time:
                            min_time = get_move_time(cnc.position, rgv.position) + place_time
                            best_cnc = cnc
            else:
                # 全为正数
                for cnc in temp_cnc_arr:
                    place_time = k_even_place_time if cnc.num % 2 == 0 else k_odd_place_time
                    temp_time = cnc.work_timer + place_time
                    if temp_time < min_time:
                        min_time = temp_time
                        best_cnc = cnc
            if not best_cnc:return []
            # 对最佳cnc操作
            if rgv.position == best_cnc.position:
                if best_cnc.work_timer > 0:
                    rgv.wait()
                else:
                    if not rgv.target_work:
                        new_work = Work(work_num, step)
                        work_num = work_num + 1
                        rgv.target_work = new_work
                    rgv.place(best_cnc)
            else:    
                rgv.move_to_position(best_cnc.position)
        for cnc in cnc_arr:cnc.execute()
        rgv.execute()
    return rgv.work_arr

if __name__ == '__main__':
    '''
    max = 0
    max_r = []
    ttt = None
    for i in itertools.product('12', repeat = 8):
        r = main(i,2)
        if len(r) > max:
            max = len(r)
            max_r = r
            ttt = i
    print(max)
    print(max_r)
    print(ttt)
    '''
    r = main(is_error = True)
    print(len(r))
