# -*- coding: utf-8 -*-
from turing_machine import TuringMachine
from test_turing_machine_example1 import print_states

#create the Turing machine
transitions = {
    # ۱. حرکت به راست و رد شدن از 1های عدد اول
    ('q0', '1'): ('q0', '1', 'R'),
    
    # ۲. تبدیل صفر جداکننده به 1 و تغییر حالت برای رفتن به انتهای نوار
    ('q0', '0'): ('replace_zero', '1', 'R'),
    
    # ۳. حرکت به راست و رد شدن از 1های عدد دوم تا رسیدن به انتهای نوار (بلنک)
    ('replace_zero', '1'): ('replace_zero', '1', 'R'),
    
    # ۴. برخورد با انتهای نوار (رشته خالی) و حرکت به چپ برای پاک کردن آخرین 1
    ('replace_zero', ''): ('clear_last_one', '', 'L'),
    
    # ۵. پاک کردن آخرین 1 اضافه (تبدیل به رشته خالی) و رفتن به حالت پذیرش qa
    ('clear_last_one', '1'): ('qa', '', 'R')
}

if __name__ == "__main__":
    print_states(transitions)
    machine = TuringMachine(transitions)

    def run(input_):
        w = input_
        print("Input:",w)
        print("Accepted" if machine.accepts(w) else "Rejected")
        machine.debug(w)
        print()

    # SHOULD ACCEPT
    run("110111")
    # outputs 11111

    # SHOULD ACCEPT
    run("11101111")
    #     # outputs 1111111
    run("0111")
    # outputs 111