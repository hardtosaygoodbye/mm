from cnc import CNC
from rgv import RGV
from work import Work
from functools import cmp_to_key
from config import *
from copy import *
import itertools
import pandas as pd

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
                if cnc.trouble_time == 0:
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
            if not best_cnc:return (rgv,cnc_arr)
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
    return (rgv,cnc_arr)

def no_err_one_step():
    rgv,cnc_arr =  main()
    return {'rgv':rgv,'cnc_arr':cnc_arr,'is_error':False,'step':1}

def err_one_step():
    rgv,cnc_arr = main(is_error = True)
    return {'rgv':rgv,'cnc_arr':cnc_arr, 'is_error':True,'step':1}

def no_err_two_step():
    max_num_work = 0
    best_rgv = None
    best_cnc_arr = None
    best_tools = None
    for i in itertools.product('12', repeat = 8):
        rgv,cnc_arr = main(i,2)
        if len(rgv.work_arr) > max_num_work:
            max_num_work = len(rgv.work_arr)
            best_rgv = rgv
            best_cnc_arr = cnc_arr
            best_tools = i
    return {'rgv':best_rgv,'cnc_arr': best_cnc_arr, 'tools':best_tools,'is_error':False,'step':2}

def err_two_step():
    max_num_work = 0
    best_rgv = None
    best_cnc_arr = None
    best_tools = None
    for i in itertools.product('12', repeat = 8):
        rgv,cnc_arr = main(i,2,is_error = True)
        if len(rgv.work_arr) > max_num_work:
            max_num_work = len(rgv.work_arr)
            best_rgv = rgv
            best_cnc_arr = cnc_arr
            best_tools = i
    return {'rgv':best_rgv,'cnc_arr': best_cnc_arr, 'tools':best_tools,'is_error':True,'step':2}

def output(rgv, cnc_arr, tools = ['1']*8, is_error = False, step = 1):
    first_cnc=[]
    first_place_up=[]
    first_place_down=[]
    second_cnc=[]
    second_place_up=[]
    second_place_down=[]
    num=[]
    for work in rgv.work_arr:
        first_cnc.append(work.first_cnc_num)
        first_place_up.append(work.first_place_up)
        first_place_down.append(work.first_place_down)
        second_cnc.append(work.second_cnc_num)
        second_place_up.append(work.second_place_up)
        second_place_down.append(work.second_place_down)
        num.append(work.num)
    df=pd.DataFrame({'num':num,'first_cnc':first_cnc,'first_place_up':first_place_up,'first_place_down':first_place_down,
                      'second_cnc':second_cnc,'second_place_up':second_place_up,'second_place_down':second_place_down})
    excel_path = 'log/' + str(step) + '步工序' + ('错误' if is_error else '无错误') + '-'  + ','.join(tools) + '加工日志.xlsx' 
    # 判断类型
    if step == 1:
        # 一步工序
        df[['num','first_cnc','first_place_up','first_place_down']].to_excel(excel_path,index=False)
    elif step == 2:
        # 两步工序
        df[['num','first_cnc','first_place_up','first_place_down','second_cnc','second_place_up','second_place_down']].to_excel(excel_path,index=False)
    # 判断是否错误
    if is_error:
        excel_path = 'log/' + str(step) + '步工序' + ('错误' if is_error else '无错误') + '-'  + ','.join(tools) + '错误日志.xlsx' 
        err_cnc_num = []
        err_begin = []
        err_end = []
        for cnc in cnc_arr:
            for err_dict in cnc.err_log:
                err_cnc_num.append(err_dict['err_cnc_num'])
                err_begin.append(err_dict['err_begin'])
                err_end.append(err_dict['err_end'])
        df = pd.DataFrame({'err_cnc_num':err_cnc_num, 'err_begin':err_begin, 'err_end':err_end})
        df[['err_cnc_num','err_begin','err_end']].to_excel(excel_path,index=False)

if __name__ == '__main__':
    output(**no_err_one_step())
    output(**err_one_step())
    output(**no_err_two_step())
    output(**err_two_step())

