import struct
import adafruit_ble
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService


class BluetoothDriver():

    def __init__(self):
        self.ble = adafruit_ble.BLERadio()
        self.uart_service = UARTService()
        self.advertisement = ProvideServicesAdvertisement(self.uart_service)
        self.scan_response = adafruit_ble.Advertisement()
        self.scan_response.complete_name = "Smart Dumbbell"


    # @brief Advertiseの開始
    def start_advertise(self):
        self.ble.start_advertising(self.advertisement, self.scan_response)


    # @brief Advertiseの停止
    def stop_advertise(self):
        self.ble.stop_advertising()

    
    # @brief 接続確立の判定
    def is_connected(self):
        if self.ble.connected:
            return True
        else:
            return False


    # @brief データの送信
    def send(self, data):
        self.uart_service.write(struct.pack("@B", data))
