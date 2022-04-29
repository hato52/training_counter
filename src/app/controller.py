##
# @file     controller.py
# @version  1.0.0
# @author   hato
# @date     2022/04/29
# @brief    制御アプリケーション
# @details  メイン制御処理の定義

from driver import bluetooth_driver, button_driver, led_driver, nine_axis_sensor_driver
from utils import constant


##
# @class    Controller
# @brief    制御アプリケーション
# @details  メイン制御処理の定義
class Controller():

    ##
    # @fn       __init__()
    # @brief    コンストラクタ
    # @param    None 引数なし
    # @return   None 戻り値なし
    # @details  Controllerクラスの初期化を行う
    def __init__(self):
        self._training_cnt = 0
        self._prev_acc_x = 0
        self._prev_acc_y = 0
        self._prev_acc_z = 0
        self.sensor = nine_axis_sensor_driver.NineAxisSensorDriver()
        self.led = led_driver.LEDDriver()
        self.ble = bluetooth_driver.BluetoothDriver()
        self.btn = button_driver.ButtonDriver()


    ##
    # @fn       serialize()
    # @brief    送信データのシリアライズを行う
    # @param    data センサ値配列
    # @return   data シリアライズ済みセンサ値
    # @details  送信データのシリアライズを行う
    def serialize(self, data):
        return int(data[0]) << 2 | int(data[1]) << 1 | int(data[2])


    ##
    # @fn       led_on()
    # @brief    LEDの点灯
    # @param    None 引数なし
    # @return   None 戻り値なし
    # @details  赤色LEDを点灯させる
    def led_on(self):
        self.led.LED_red_on()


    ##
    # @fn       led_off()
    # @brief    LEDの消灯
    # @param    None 引数なし
    # @return   None 戻り値なし
    # @details  赤色LEDを消灯させる
    def led_off(self):
        self.led.LED_red_off()


    ##
    # @fn       is_button_pressed()
    # @brief    ボタン押下判断
    # @param    None 引数なし
    # @return   True: ボタン押下されている, False: ボタン押下されていない
    # @details  中央ボタンが押されているかどうかを判定する
    def is_button_pressed(self):
        return self.btn.is_button1_pressed()


    ##
    # @fn       is_connected()
    # @brief    接続確立判断
    # @param    None 引数なし
    # @return   True: Bluetooth接続が確立されている, False: Bluetooth接続が確立されていない
    # @details  Bluetooth接続が確立されているかどうかを判定する
    def is_connected(self):
        return self.ble.is_connected()


    ##
    # @fn       get_sensor_value()
    # @brief    センサ値取得処理
    # @param    None 引数なし
    # @return   acc_x フィルタリング済みX軸加速度
    # @return   acc_y フィルタリング済みY軸加速度
    # @return   acc_z フィルタリング済みZ軸加速度
    # @details  各軸のフィルタリング済み加速度センサ値を取得する
    def get_sensor_value(self):
        # センサ値取得
        _acc_x = self.sensor.read_filtered_acc(constant.ACC_X, constant.THRESHOLD)
        _acc_y = self.sensor.read_filtered_acc(constant.ACC_Y, constant.THRESHOLD)
        _acc_z = self.sensor.read_filtered_acc(constant.ACC_Z, constant.THRESHOLD)
        return _acc_x, _acc_y, _acc_z


    ##
    # @fn       sleep()
    # @brief    スリープ時処理
    # @param    None 引数なし
    # @return   None 戻り値なし
    # @details  スリープ時処理を行う
    def sleep(self):
        self.led.LED_red_off()
        self.led.LED_green_off()
        self.ble.stop_advertise()
        self.sensor.sleep()


    ##
    # @fn       initialize()
    # @brief    初期化時処理
    # @param    None 引数なし
    # @return   None 戻り値なし
    # @details  初期化時処理を行う
    def initialize(self):
        self.sensor.initialize()
        self.led.LED_red_on()
        self.ble.start_advertise()


    ##
    # @fn       initialize()
    # @brief    アクティブ移行時処理
    # @param    None 引数なし
    # @return   None 戻り値なし
    # @details  定常時処理移行前の初期化処理を行う
    def activate(self):
        self.led.LED_red_off()
        self.led.LED_green_on()
        # センサ前回値の初期化
        self.acc_x, self.acc_y, self.acc_z = self.get_sensor_value()
        self._prev_acc_x = self.acc_x
        self._prev_acc_y = self.acc_y
        self._prev_acc_z = self.acc_z


    ##
    # @fn       cyclic()
    # @brief    定常時周期処理
    # @param    None 引数なし
    # @return   None 戻り値なし
    # @details  定常時周期処理を行う
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


    ##
    # @fn       data_send()
    # @brief    データ送信処理
    # @param    None 引数なし
    # @return   None 戻り値なし
    # @details  データの送信を行う
    def data_send(self):
        # print("send : x=" + str(self.acc_x) + " y=" + str(self.acc_y) + " z=" + str(self.acc_z))
        print("count : " + str(self._training_cnt))
        # self.ble.send(self._serialized)
        self.ble.send(self._training_cnt)


    ##
    # @fn       disconnect()
    # @brief    通信終了時処理
    # @param    None 引数なし
    # @return   None 戻り値なし
    # @details  通信を終了する
    def disconnect(self):
        self.ble.stop_advertise()
        self.led.LED_red_on()
        self.led.LED_green_on()
