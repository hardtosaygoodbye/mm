from cnc import CNC
from rgv import RGV
from work import Work
from functools import cmp_to_key
from config import *
from copy import *
import itertools
import pandas as pd
from datetime import datetime


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
    for i in range(0, 8*60*60):
        if rgv.state == 0:
            # 检查是否持有物料
            if rgv.target_work == None:
                rgv.target_work = Work(work_num,step)
                work_num = work_num + 1
            # 筛选故障cnc和不同加工工序的cnc
            temp_cnc_arr = []
            for cnc in cnc_arr:
                if cnc.trouble_time != 0:
                    continue
                if rgv.target_work.step + 1 == cnc.tool:
                    temp_cnc_arr.append(cnc)
            # 打擂找出最佳目标cnc
            min_time = float('inf')
            best_cnc = None
            if get_has_minus(temp_cnc_arr,rgv):
                # 有负数情况
                for cnc in temp_cnc_arr:
                    # 去除所有正数
                    if cnc.work_timer - get_move_time(cnc.position, rgv.position) > 0:
                        continue
                    # 求出放置移动时间加上下料时间最小的数
                    place_time = k_even_place_time if cnc.num % 2 == 0 else k_odd_place_time
                    if get_move_time(cnc.position, rgv.position) + place_time < min_time:
                        min_time = get_move_time(cnc.position, rgv.position) + place_time
                        best_cnc = cnc
            else:
                # 全为正数
                # 求出剩余工作时间加上上下料时间最短
                for cnc in temp_cnc_arr:
                    place_time = k_even_place_time if cnc.num % 2 == 0 else k_odd_place_time
                    temp_time = cnc.work_timer + place_time
                    if temp_time < min_time:
                        min_time = temp_time
                        best_cnc = cnc
            # 未找到最佳cnc则退出
            if not best_cnc:return (rgv,cnc_arr)
            # 对rgv下达指令
            rgv.move_to_position(best_cnc.position)
            if best_cnc.work_timer > 0:
                rgv.wait()
            else:
                rgv.place(best_cnc)
        # cnc,rgv 执行指令
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
    # 空载日志
    cnc_num = []
    cnc_waste_time = []
    for cnc in cnc_arr:
        cnc_num.append(cnc.num)
        cnc_waste_time.append(cnc.waste_time)
    excel_path = 'log/' + str(step) + '步工序' + ('错误' if is_error else '无错误') + '-'  + ','.join(tools) + '空载日志.xlsx' 
    df = pd.DataFrame({'cnc_num':cnc_num, 'cnc_waste_time':cnc_waste_time})
    df[['cnc_num','cnc_waste_time']].to_excel(excel_path,index=False)

        
            

def output_all():
    print('正在玩命计算中，请稍后')
    output(**no_err_one_step())
    output(**err_one_step())
    output(**no_err_two_step())
    output(**err_two_step())
    print('success! please see in log folder')

if __name__ == '__main__':
    start = datetime.now() 
    output_all()
    end = datetime.now() 
    print((end-start).seconds)

