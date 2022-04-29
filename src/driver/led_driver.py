##
# @file     led_driver.py
# @version  1.0.0
# @author   hato
# @date     2022/04/29
# @brief    LED用ドライバ
# @details  LED用ドライバの定義

import board
from digitalio import DigitalInOut, Direction
from utils import constant


##
# @class    LEDDriver
# @brief    LED用ドライバ
# @details  LED用ドライバの定義
class LEDDriver():

    ##
    # @fn       __init__()
    # @brief    コンストラクタ
    # @param    None 引数なし
    # @return   None 戻り値なし
    # @details  LEDDriverクラスの初期化を行う
    def __init__(self):
        self.led_red = DigitalInOut(board.LED1)
        self.led_green = DigitalInOut(board.LED2)
        self.led_red.direction = Direction.OUTPUT
        self.led_green.direction = Direction.OUTPUT
        self.led_red.value = constant.LED_OFF
        self.led_green.value = constant.LED_OFF


    ##
    # @fn       LED_red_on()
    # @brief    赤色LED点灯
    # @param    None 引数なし
    # @return   None 戻り値なし
    # @details  赤色LEDを点灯させる
    def LED_red_on(self):
        self.led_red.value = constant.LED_ON
    

    ##
    # @fn       LED_red_on()
    # @brief    赤色LED消灯
    # @param    None 引数なし
    # @return   None 戻り値なし
    # @details  赤色LEDを消灯させる
    def LED_red_off(self):
        self.led_red.value = constant.LED_OFF


    ##
    # @fn       LED_red_on()
    # @brief    緑色LED点灯
    # @param    None 引数なし
    # @return   None 戻り値なし
    # @details  緑色LEDを点灯させる
    def LED_green_on(self):
        self.led_green.value = constant.LED_ON
    

    ##
    # @fn       LED_red_on()
    # @brief    緑色LED消灯
    # @param    None 引数なし
    # @return   None 戻り値なし
    # @details  緑色LEDを消灯させる
    def LED_green_off(self):
        self.led_green.value = constant.LED_OFF
