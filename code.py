from adafruit_pybadger import pybadger
import time

class State:
    time_length = 50  # Tens of seconds

    def __init__(self):
        pass

    def run(self):
        pass

class QRState(State):
    def run(self):
        pybadger.show_qr_code(
            data='https://anzelpwj.github.io/')

class BCState(State):
    def run(self):
        pybadger.show_business_card(
            image_name='heb.bmp',
            name_string='Paul Anzel',
            name_scale=2,
            email_string_one='Senior Data Scientist',
            email_scale_one=1)

class BadgeState(State):
    def run(self):
        pybadger.show_badge(
            name_string='Paul',
            hello_scale=2,
            my_name_is_scale=2,
            name_scale=3)

states = [BadgeState(), BCState(), QRState()]

state = 0
prev_a = False
prev_b = False
prev_start = False
timer = 50

def change_state(state):
    state %= len(states)
    states[state].run()
    timer = states[state].time_length
    change_timer = True
    return state, timer, change_timer

state, timer, change_timer = change_state(state)

while True:
    state_change = False
    cur_a = pybadger.button.a
    cur_b = pybadger.button.b
    cur_start = pybadger.button.start
    if not cur_a and prev_a:
        state += 1
        state_change = True
    elif not cur_b and prev_b:
        state -= 1
        state_change = True
    elif not cur_start and prev_start:
        change_timer = False
    prev_a = cur_a
    prev_b = cur_b
    prev_start = cur_start
    if change_timer:
        timer -= 1
    if timer <= 0:
        state += 1
        state_change = True
    if state_change:
        state, timer, change_timer = change_state(state)
    time.sleep(0.1)
