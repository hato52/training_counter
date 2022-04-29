##
# @file     bluetooth_driver.py
# @version  1.0.0
# @author   hato
# @date     2022/04/29
# @brief    Bluetooth通信用ドライバ
# @details  Bluetooth通信用ドライバの定義

import struct
import adafruit_ble
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService


##
# @class    BluetoothDriver
# @brief    Bluetooth通信用ドライバ
# @details  Bluetooth通信用ドライバの定義
class BluetoothDriver():
    
    ##
    # @fn       __init__()
    # @brief    コンストラクタ
    # @param    None 引数なし
    # @return   None 戻り値なし
    # @details  BluetoothDriverクラスの初期化を行う
    def __init__(self):
        self.ble = adafruit_ble.BLERadio()
        self.uart_service = UARTService()
        self.advertisement = ProvideServicesAdvertisement(self.uart_service)
        self.scan_response = adafruit_ble.Advertisement()
        self.scan_response.complete_name = "Smart Dumbbell"


    ##
    # @fn       start_advertise()
    # @brief    Advertiseの開始
    # @param    None 引数なし
    # @return   None 戻り値なし
    # @details  Advertiseを開始する
    def start_advertise(self):
        self.ble.start_advertising(self.advertisement, self.scan_response)


    ##
    # @fn       stop_advertise()
    # @brief    Advertiseの停止
    # @param    None 引数なし
    # @return   None 戻り値なし
    # @details  Advertiseを停止する
    def stop_advertise(self):
        self.ble.stop_advertising()

    
    ##
    # @fn       is_connected()
    # @brief    接続確立の判断
    # @param    None 引数なし
    # @return   True: 接続確立済み, False: 接続未確立
    # @details  接続確立を判定する
    def is_connected(self):
        if self.ble.connected:
            return True
        else:
            return False


    ##
    # @fn       send()
    # @brief    送信処理
    # @param    data 送信データ
    # @return   None 戻り値なし
    # @details  データを送信する
    def send(self, data):
        self.uart_service.write(struct.pack("@B", data))
