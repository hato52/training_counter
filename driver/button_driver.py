import board
from digitalio import DigitalInOut, Direction, Pull

from utils import constant


class ButtonDriver():

    def __init__(self):
        self.button1 = DigitalInOut(board.BUTTON1)
        self.button1.direction = Direction.INPUT
        self.button1.pull = Pull.UP
        self.prev_state = constant.BTN_UP
        

    # @brief ボタン1が押されているかどうかを判定する
    def is_button1_pressed(self):
        res = False
        if self.button1.value == constant.BTN_DOWN:     # ボタンが押されている
            res = True
        return res


    # @brief ボタン1が押されたかどうかを判定する
    def is_button1_hitted(self):
        res = False
        if self.button1.value == constant.BTN_DOWN and self.prev_state == constant.BTN_UP:
            res = True
        self.prev_state = self.button1.value    
        return res


    # @brief ボタン1が離されたかどうかを判定する
    def is_button1_released(self):
        res = False
        if self.button1.value == constant.BTN_UP and self.prev_state == constant.BTN_DOWN:
            res = True
        self.prev_state = self.button1.value    
        return res
