##
# @file     button_driver.py
# @version  1.0.0
# @author   hato
# @date     2022/04/29
# @brief    ボタン用ドライバ
# @details  ボタン用ドライバの定義

import board
from digitalio import DigitalInOut, Direction, Pull
from utils import constant


##
# @class    ButtonDriver
# @brief    ボタン用ドライバ
# @details  ボタン用ドライバの定義
class ButtonDriver():

    ##
    # @fn       __init__()
    # @brief    コンストラクタ
    # @param    None 引数なし
    # @return   None 戻り値なし
    # @details  ButtonDriverクラスの初期化を行う
    def __init__(self):
        self.button1 = DigitalInOut(board.BUTTON1)
        self.button1.direction = Direction.INPUT
        self.button1.pull = Pull.UP
        self.prev_state = constant.BTN_UP
        

    ##
    # @fn       is_button1_pressed()
    # @brief    ボタン1の押下判定
    # @param    None 引数なし
    # @return   True: ボタン1が押下されている, False: ボタン1が押下されていない
    # @details  ボタン1が押されているかどうかを判定する
    def is_button1_pressed(self):
        res = False
        if self.button1.value == constant.BTN_DOWN:     # ボタンが押されている
            res = True
        return res


    ##
    # @fn       is_button1_hitted()
    # @brief    ボタン1が押下されたタイミングの判定
    # @param    None 引数なし
    # @return   True: ボタン1が押下された, False: ボタン1が押下されていない
    # @details  ボタン1が押されたかどうかを判定する
    def is_button1_hitted(self):
        res = False
        if self.button1.value == constant.BTN_DOWN and self.prev_state == constant.BTN_UP:
            res = True
        self.prev_state = self.button1.value    
        return res


    ##
    # @fn       is_button1_released()
    # @brief    ボタン1が離されたタイミングの判定
    # @param    None 引数なし
    # @return   True: ボタン1が離された, False: ボタン1が離されていない
    # @details  ボタン1が離されたかどうかを判定する
    def is_button1_released(self):
        res = False
        if self.button1.value == constant.BTN_UP and self.prev_state == constant.BTN_DOWN:
            res = True
        self.prev_state = self.button1.value    
        return res
