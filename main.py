from cnc import CNC
from rgv import RGV

cnc_config = {
    'one_work_time':560,
    'two_work_first_time':400,
    'two_work_second_time':378,
    'odd_load_time':28,
    'even_load_time':31
}

rgv_config = {
    'move_time_arr': [20,30,46],
    'wash_time': 25
}

def predict_time_of_work(cnc,rgv):
    distance = abs(cnc.position - rgv.position)
    move_time = rgv.move_time_arr[distance-1]
    wash_time = 0 if cnc.is_empty == 1 else rgv.wash_time
    return move_time + cnc.last_time + wash_time + cnc.load_time

def time_of_work(cnc,rgv):
    #print(cnc.position,end = '->')
    real_time = predict_time_of_work(cnc,rgv)
    rgv.position = cnc.position
    cnc.is_empty = 0
    cnc.last_time = cnc.one_work_time
    return real_time

def main():
    cnc_arr = []
    for num in range(1,9):
        cnc_config['num'] = num
        cnc = CNC(**cnc_config)
        cnc_arr.append(cnc)
    rgv = RGV(**rgv_config)
    total_time = 0.0
    works = 0
    while total_time < 28800:
        predict_min_time = 10000000000
        predict_cnc = None
        # 预测所有时间
        for cnc in cnc_arr:
            predict_time = predict_time_of_work(cnc,rgv)
            if predict_time < predict_min_time:
                predict_min_time = predict_time
                predict_cnc = cnc
        # 执行最小方案
        real_time = time_of_work(predict_cnc,rgv)
        # 该时间段机器加工
        for cnc in cnc_arr:
            cnc.work(real_time)
        total_time = total_time + real_time
        works  = works + 1
    return works

if __name__ == '__main__':
    works = main()
    print(works)

