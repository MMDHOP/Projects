# -*- coding: utf-8 -*-
"""A Turing machine simulator skeleton.

    Accepting '#'
    =============

    >>> from turing_machine import TuringMachine

    Instantiate the machine with particular transitions.

    >>> one_hash = TuringMachine(
    ...     {
    ...         ('q0', '#'): ('saw_#', '#', 'R'),
    ...         ('saw_#', ''): ('qa', '', 'R'),
    ...     }
    ... )

    Check whether it accepts a string:

    >>> one_hash.accepts('#')
    True

    >>> one_hash.accepts('##')
    False

    Check whether it rejects a string:

    >>> one_hash.rejects('#')
    False

    >>> one_hash.rejects('##')
    True

"""

import logging
from itertools import islice


# -*- coding: utf-8 -*-

class TuringMachine:
    def __init__(self, transitions, start_state='q0', accept_state='qa', reject_state='qr', blank_symbol=''):
        self.transitions = transitions
        self.start_state = start_state
        self.accept_state = accept_state
        self.reject_state = reject_state
        self.blank_symbol = blank_symbol

    def run(self, input_):
        # نوار به صورت دو لیست مجزا (برای پشتیبانی از نوار نامتناهی دو طرفه)
        # در ابتدا فقط بخش سمت راست مقداردهی می‌شود
        tape_left = []
        tape_right = list(input_) if input_ else []
        current_symbol = tape_right.pop(0) if tape_right else self.blank_symbol
        current_state = self.start_state

        while True:
            # تعیین وضعیت ماشین
            if current_state == self.accept_state:
                action = 'Accept'
            elif current_state == self.reject_state:
                action = 'Reject'
            else:
                action = None

            # ساخت دیکشنری پیکربندی طبق مستندات
            configuration = {
                'state': current_state,
                'left_hand_side': list(tape_left),
                'symbol': current_symbol,
                'right_hand_side': list(tape_right)
            }

            yield (action, configuration)

            if action in ('Accept', 'Reject'):
                break

            # خواندن قوانین انتقال
            transition_key = (current_state, current_symbol)
            if transition_key in self.transitions:
                next_state, write_symbol, direction = self.transitions[transition_key]
                
                # نوشتن روی نوار
                current_symbol = write_symbol
                current_state = next_state

                # حرکت هد و گسترش داینامیک نوار (نوار دو طرفه)
                if direction == 'R':
                    tape_left.append(current_symbol)
                    current_symbol = tape_right.pop(0) if tape_right else self.blank_symbol
                elif direction == 'L':
                    tape_right.insert(0, current_symbol)
                    current_symbol = tape_left.pop() if tape_left else self.blank_symbol
            else:
                current_state = self.reject_state

    def accepts(self, input_, step_limit=100):
        from itertools import islice
        generator = self.run(input_)
        steps = list(islice(generator, step_limit))
        if not steps: return None
        last_action, _ = steps[-1]
        return True if last_action == 'Accept' else False if last_action == 'Reject' else None

    def rejects(self, input_, **kwargs):
        res = self.accepts(input_, **kwargs)
        return not res if res is not None else None

    def debug(self, input_, step_limit=100, colored=False):
        from itertools import islice
        for _, config in islice(self.run(input_), step_limit):
            left = "".join(config['left_hand_side'])
            right = "".join(config['right_hand_side'])
            symbol = config['symbol']
            print(f"{config['state']}\t{left}[{symbol}]{right}")
            if config['state'] in (self.accept_state, self.reject_state):
                break