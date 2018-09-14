from cnc import CNC
from rgv import RGV
from work import Work

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

if __name__ == '__main__':
    # 初始化对象
    cnc_arr = []
    for num in range(1,9):
        cnc_config['num'] = num
        cnc = CNC(**cnc_config)
        cnc_arr.append(cnc)
    rgv = RGV(**rgv_config)
    for i in range(0,100):
        if rgv.state == 0:
            # 进行测算，执行指令
            # 回收加工信息
            has_minus = False
            for cnc in cnc_arr:
                if cnc.work_timer <= 0:
                    has_minus = True
            min_time = float('inf')
            best_cnc = None
            if has_minus:
                # 有负数情况
                for cnc in cnc_arr:
                    distance = abs(cnc.position - rgv.position)
                    move_time = rgv.move_time_arr[distance - 1]
                    temp_time = cnc.work_timer - move_time + cnc.place_time
                    if temp_time < min_time:
                        min_time = temp_time
                        best_cnc = cnc
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
        cnc.execute()
        rgv.execute()
        
