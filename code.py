from adafruit_pybadger import pybadger
import time

BLACK = (0, 0, 0)
COLOR1 = (255, 0, 0)
COLOR2 = (255, 255, 0)
COLOR3 = (0, 255, 0)
COLOR4 = (0, 255, 255)
COLOR5 = (0, 0, 255)

class State:
    time_length = 50  # Tens of seconds

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

print('first')

print('second')

def pixel_display(timer, max_timer):
    # Times look backwards due to timer decrementing
    time5 = timer < int(max_timer/5)
    time4 = int(max_timer/5) <= timer < int(2*max_timer/5)
    time3 = int(2*max_timer/5) <= timer < int(3*max_timer/5)
    time2 = int(3*max_timer/5) <= timer < int(4*max_timer/5)
    time1 = int(4*max_timer/5) <= timer
    clr1 = COLOR1 if time1 else BLACK
    clr2 = COLOR2 if time2 else BLACK
    clr3 = COLOR3 if time3 else BLACK
    clr4 = COLOR4 if time4 else BLACK
    clr5 = COLOR5 if time5 else BLACK

    pybadger.pixels[0] = clr1
    pybadger.pixels[1] = clr2
    pybadger.pixels[2] = clr3
    pybadger.pixels[3] = clr4
    pybadger.pixels[4] = clr5
    pybadger.pixels.brightness = 0.1


def change_state(state):
    state %= len(states)
    states[state].run()
    timer = states[state].time_length
    change_timer = True
    return state, timer, change_timer

state, timer, change_timer = change_state(state)

#Main loop
while True:
    state_change = False
    pixel_display(timer, states[state].time_length)
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
