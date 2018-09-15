from cnc import CNC
from rgv import RGV
from work import Work
from copy import copy
from functools import cmp_to_key

cnc_config = {
    'odd_place_time':28,
    'even_place_time':31
}

rgv_config = {
    'move_time_arr': [20,30,46],
    'wash_time': 25
}

work_config = {
    'one_work_time':560,
    'two_work_first_time':400,
    'two_work_second_time':378
}

def cmpf(a,b,rgv):
    a_distance = abs(a.position - rgv.position)
    a_move_time = 0
    if a_distance != 0:
        a_move_time = rgv.move_time_arr[a_distance - 1]
    b_distance = abs(b.position - rgv.position)
    b_move_time = 0
    if b_distance != 0:
        b_move_time = rgv.move_time_arr[b_distance - 1]
    if (a_distance != b_distance):
        return a_distance - b_distance
    else:
        return a.place_time - b.place_time

if __name__ == '__main__':
    # 初始化对象
    cnc_arr = []
    for num in range(1,9):
        cnc_config['num'] = num
        cnc = CNC(**cnc_config)
        cnc_arr.append(cnc)
    rgv = RGV(**rgv_config)
    for i in range(0,28800):
        if rgv.state == 0:
            # 进行测算，执行指令
            # 回收加工信息
            has_minus = False
            for cnc in cnc_arr:
                distance = abs(cnc.position - rgv.position)
                move_time = 0
                if distance != 0:
                    move_time = rgv.move_time_arr[distance - 1]
                if cnc.work_timer - move_time < 0:
                    has_minus = True
            min_time = float('inf')
            best_cnc = None
            if has_minus:
                # 有负数情况
                temp_cnc_arr = []
                for cnc in cnc_arr:
                    distance = abs(cnc.position - rgv.position)
                    move_time = 0
                    if distance != 0:
                        move_time = rgv.move_time_arr[distance - 1]
                    if cnc.work_timer - move_time <= 0:
                        temp_cnc_arr.append(cnc)
                temp_cnc_arr = sorted(temp_cnc_arr, key=cmp_to_key(lambda a,b:cmpf(a,b,rgv)))
                best_cnc = temp_cnc_arr[0]
            else:
                # 全为正数
                for cnc in cnc_arr:
                    temp_time = cnc.work_timer + cnc.place_time
                    if temp_time < min_time:
                        min_time = temp_time
                        best_cnc = cnc
            if rgv.position == best_cnc.position:
                if best_cnc.work_timer > 0:
                    rgv.wait()
                else:
                    work = Work(**work_config)
                    rgv.work = work
                    rgv.place(best_cnc)
            else:    
                rgv.move_to_position(best_cnc.position)
        for cnc in cnc_arr:
            cnc.execute()
        rgv.execute()
    print(rgv.total_count) 
    for cnc in cnc_arr:
        print(cnc.waste_time)
