# -*- coding: utf-8 -*-
from turing_machine import TuringMachine
from test_turing_machine_example1 import print_states

#create the Turing machine
transitions = {
    # q0: پیدا کردن نماد 1 بعدی از عدد اول برای شروع یک چرخه ضرب
    ('q0', '1'): ('find_0', 'X', 'R'),
    ('q0', '0'): ('clean_X', '', 'L'),  # عدد اول تمام شد، رفتن به فاز پاک‌سازی نوار

    # find_0: حرکت به راست و عبور از عدد اول تا رسیدن به جداکننده 0
    ('find_0', '1'): ('find_0', '1', 'R'),
    ('find_0', '0'): ('find_1', '0', 'R'),

    # find_1: پیدا کردن نماد 1 بعدی در عدد دوم که هنوز پردازش نشده (با Y علامت نخورده)
    ('find_1', 'Y'): ('find_1', 'Y', 'R'),
    ('find_1', '1'): ('move_end', 'Y', 'R'),   # یک 1 پیدا شد، رفتن به انتهای نوار برای نوشتن در پاسخ
    ('find_1', ''): ('reset_Y', '', 'L'),     # چرخه عدد دوم برای این X تمام شد، بازگشت برای ریست کردن Yها
    ('find_1', 'A'): ('reset_Y', 'A', 'L'),

    # move_end: حرکت به انتهای سمت راست نوار برای اضافه کردن یک نماد A (پاسخ موقت)
    ('move_end', '1'): ('move_end', '1', 'R'),
    ('move_end', 'Y'): ('move_end', 'Y', 'R'),
    ('move_end', '0'): ('move_end', '0', 'R'),
    ('move_end', 'A'): ('move_end', 'A', 'R'),
    ('move_end', ''): ('back_to_second', 'A', 'L'), # نوشتن A در اولین خانه خالی و بازگشت

    # back_to_second: بازگشت به چپ تا رسیدن به آخرین Y که تغییر داده بودیم
    ('back_to_second', '1'): ('back_to_second', '1', 'L'),
    ('back_to_second', 'Y'): ('find_1', 'Y', 'R'), # پیدا کردن Y، تغییر جهت به راست برای ادامه عدد دوم
    ('back_to_second', '0'): ('back_to_second', '0', 'L'),
    ('back_to_second', 'A'): ('back_to_second', 'A', 'L'),
    ('back_to_second', 'X'): ('back_to_second', 'X', 'L'),

    # reset_Y: تبدیل تمام Yها به 1 برای آمادگی چرخه بعدی ضرب
    ('reset_Y', 'Y'): ('reset_Y', '1', 'L'),
    ('reset_Y', '1'): ('reset_Y', '1', 'L'),
    ('reset_Y', '0'): ('back_to_first', '0', 'L'),

    # back_to_first: بازگشت به عدد اول برای پیدا کردن ۱ بعدی
    ('back_to_first', '1'): ('back_to_first', '1', 'L'),
    ('back_to_first', 'X'): ('q0', 'X', 'R'), # رسیدن به آخرین X و حرکت به راست برای انتخاب 1 بعدی

    # ==== فاز پاک‌سازی نوار (Cleanup) ====
    # clean_X: پاک کردن تمام علامت‌های X در سمت چپ نوار
    ('clean_X', 'X'): ('clean_X', '', 'L'),
    ('clean_X', ''): ('clean_rest', '', 'R'), # رسیدن به مرز ابتدای نوار و شروع حرکت به راست

    # clean_rest: عبور از جاهای خالی و پاک کردن بقیه علائم
    ('clean_rest', ''): ('clean_rest', '', 'R'),
    ('clean_rest', '0'): ('clean_rest', '', 'R'),
    ('clean_rest', '1'): ('clean_second', '', 'R'), # ورود به عدد دوم برای پاک کردن آن

    # clean_second: پاک کردن 1های عدد دوم
    ('clean_second', '1'): ('clean_second', '', 'R'),
    ('clean_second', 'A'): ('make_1', '1', 'R'),    # رسیدن به پاسخ (A)؛ تبدیل آن به 1 واقعی
    ('clean_second', ''): ('qa', '', 'R'),          # اگر پاسخی وجود نداشت (ضرب در صفر مثل 01111)

    # make_1: تبدیل تمام Aها به 1 و اتمام کار ماشین
    ('make_1', 'A'): ('make_1', '1', 'R'),
    ('make_1', ''): ('qa', '', 'R')                 # رفتن به حالت پذیرش نهایی
}

if __name__ == "__main__":
    print_states(transitions)
    machine = TuringMachine(transitions)

    def run(input_):
        w = input_
        print("Input:",w)
        print("Accepted" if machine.accepts(w) else "Rejected")
        machine.debug(w, step_limit=1000)

        print()

    # SHOULD ACCEPT
    run("110111")
    # outputs 111111

    # SHOULD ACCEPT
    run("11101111")
    # outputs 111111111111

    run("01111")
