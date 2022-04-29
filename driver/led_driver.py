import board
from digitalio import DigitalInOut, Direction

from utils import constant


class LEDDriver():

    def __init__(self):
        self.led_red = DigitalInOut(board.LED1)
        self.led_green = DigitalInOut(board.LED2)
        self.led_red.direction = Direction.OUTPUT
        self.led_green.direction = Direction.OUTPUT
        self.led_red.value = constant.LED_OFF
        self.led_green.value = constant.LED_OFF


    # @brief 赤色LEDを点灯させる
    def LED_red_on(self):
        self.led_red.value = constant.LED_ON
    

    # @brief 赤色LEDを消灯させる
    def LED_red_off(self):
        self.led_red.value = constant.LED_OFF


    # @brief 緑色LEDを点灯させる
    def LED_green_on(self):
        self.led_green.value = constant.LED_ON
    

    # @brief 緑色LEDを消灯させる
    def LED_green_off(self):
        self.led_green.value = constant.LED_OFF
