class CNC:
    num = 1
    last_time = 0
    load_time = 0
    one_work_time = 0
    two_work_first_time = 0
    two_work_second_time = 0
    position = 0
    is_empty = 1
    waste_time = 0

    def __init__(self,num,odd_load_time,even_load_time,one_work_time,two_work_first_time,two_work_second_time):
        self.num = num
        if num % 2 == 0:
            self.load_time = even_load_time
        else:
            self.load_time = odd_load_time
        self.position = (num - 1) // 2
        self.one_work_time = one_work_time
        self.two_work_first_time = two_work_first_time
        self.two_work_second_time = two_work_second_time
    def work(self,real_time):
        self.last_time = self.last_time - real_time
        if self.last_time < 0:
            self.waste_time = self.waste_time - self.last_time
            self.last_time = 0
