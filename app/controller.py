from driver import bluetooth_driver, button_driver, led_driver, nine_axis_sensor_driver
from utils import constant


class Controller():

    def __init__(self):
        self._training_cnt = 0
        self._prev_acc_x = 0
        self._prev_acc_y = 0
        self._prev_acc_z = 0
        self.sensor = nine_axis_sensor_driver.NineAxisSensorDriver()
        self.led = led_driver.LEDDriver()
        self.ble = bluetooth_driver.BluetoothDriver()
        self.btn = button_driver.ButtonDriver()

    # @brief データシリアライズ処理
    def serialize(self, data):
        return int(data[0]) << 2 | int(data[1]) << 1 | int(data[2])

    # @brief LED処理
    def led_on(self):
        self.led.LED_red_on()

    def led_off(self):
        self.led.LED_red_off()

    # @brief スイッチ押下判断
    def is_button_pressed(self):
        return self.btn.is_button1_pressed()

    # @brief 接続確立判断
    def is_connected(self):
        return self.ble.is_connected()

    # @brief センサ値取得処理
    def get_sensor_value(self):
        # センサ値取得
        _acc_x = self.sensor.read_filtered_acc(constant.ACC_X, constant.THRESHOLD)
        _acc_y = self.sensor.read_filtered_acc(constant.ACC_Y, constant.THRESHOLD)
        _acc_z = self.sensor.read_filtered_acc(constant.ACC_Z, constant.THRESHOLD)
        return _acc_x, _acc_y, _acc_z

    # @brief スリープ状態時処理
    def sleep(self):
        self.led.LED_red_off()
        self.led.LED_green_off()
        self.ble.stop_advertise()
        self.sensor.sleep()

    # @brief 初期化処理
    def initialize(self):
        self.sensor.initialize()
        self.led.LED_red_on()
        self.ble.start_advertise()

    # @brief アクティブ移行時処理
    def activate(self):
        self.led.LED_red_off()
        self.led.LED_green_on()
        # センサ前回値の初期化
        self.acc_x, self.acc_y, self.acc_z = self.get_sensor_value()
        self._prev_acc_x = self.acc_x
        self._prev_acc_y = self.acc_y
        self._prev_acc_z = self.acc_z

    # @brief 定常処理
    def cyclic(self):
        # センサ値取得
        self.acc_x, self.acc_y, self.acc_z = self.get_sensor_value()
        self.acc = [self.acc_x, self.acc_y, self.acc_z]

        # トレーニング回数計算
        if self.acc_x - self._prev_acc_x == 1 or self.acc_x - self._prev_acc_x == 1 or self.acc_x - self._prev_acc_x == 1:
            self._training_cnt += 1

        # 前回値保存
        self._prev_acc_x = self.acc_x
        self._prev_acc_y = self.acc_y
        self._prev_acc_z = self.acc_z

        # シリアライズ処理
        self._serialized = self.serialize(self.acc)

        return self._serialized

    # @brief データ送信処理
    def data_send(self):
        # print("send : x=" + str(self.acc_x) + " y=" + str(self.acc_y) + " z=" + str(self.acc_z))
        print("count : " + str(self._training_cnt))
        # self.ble.send(self._serialized)
        self.ble.send(self._training_cnt)

    # @brief 通信終了処理
    def disconnect(self):
        self.ble.stop_advertise()
        self.led.LED_red_on()
        self.led.LED_green_on()
