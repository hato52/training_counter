##
# @file     button_driver.py
# @version  1.0.0
# @author   hato
# @date     2022/04/29
# @brief    9軸センサ用ドライバ
# @details  9軸センサ用ドライバの定義

import board, busio
from adafruit_bus_device.i2c_device import I2CDevice
from utils import constant


##
# @class    NineAxisSensorDriver
# @brief    9軸センサ用ドライバ
# @details  9軸センサ用ドライバの定義
class NineAxisSensorDriver():

    ##
    # @fn       __init__()
    # @brief    コンストラクタ
    # @param    None 引数なし
    # @return   None 戻り値なし
    # @details  NineAxisSensorDriverクラスの初期化を行う
    def __init__(self):
        pass

    ##
    # @fn       initialize()
    # @brief    センサ初期化処理
    # @param    None 引数なし
    # @return   None 戻り値なし
    # @details  センサの初期化を行う
    def initialize(self):
        with busio.I2C(board.SCL, board.SDA) as self.i2c:
            with I2CDevice(self.i2c, constant.BMX055_ACC) as self.device:
                self.device.write(bytes([constant.PMU_RANGE, 0x03]))  # g-range +-2g
                self.device.write(bytes([constant.PMU_BW, 0x08]))     # フィルタ帯域 7.81Hz
                self.device.write(bytes([constant.PMU_LPW, 0x00]))    # 通常モードに移行


    ##
    # @fn       sleep()
    # @brief    センサ停止
    # @param    None 引数なし
    # @return   None 戻り値なし
    # @details  センサを低電力消費モードに移行する
    def sleep(self):
        with busio.I2C(board.SCL, board.SDA) as self.i2c:
            # 加速度センサ
            with I2CDevice(self.i2c, constant.BMX055_ACC) as self.device:
                self.device.write(bytes([constant.PMU_LPW, 0x20]))          # DEEP_SUSPEND mode
            # ジャイロセンサ
            with I2CDevice(self.i2c, constant.BMX055_GYR) as self.device:
                self.device.write(bytes([constant.GYR_LPM1, 0x20]))          # DEEP_SUSPEND mode
            # 地磁気センサ
            with I2CDevice(self.i2c, constant.BMX055_MAG) as self.device:
                self.device.write(bytes([constant.MAG_CTRL, 0x00]))          # Suspend mode
            # 気圧センサ
            with I2CDevice(self.i2c, constant.LPS22HB) as self.device:
                self.device.write(bytes([constant.CTRL_REG1, 0x00]))        # Power-down mode
            # 温湿度センサ
            with I2CDevice(self.i2c, constant.HDC2010) as self.device:
                self.device.write(bytes([constant.RESET_AND_DRDY, 0x80]))    # Soft-Reset


    ##
    # @fn       read_acc()
    # @brief    加速度センサ値の読み取り
    # @param    reg 読み取り対象レジスタ
    # @return   _acc 読み取ったセンサ値
    # @details  加速度センサ値を読み取る
    def read_acc(self, reg):
        with busio.I2C(board.SCL, board.SDA) as self.i2c:
            with I2CDevice(self.i2c, constant.BMX055_ACC) as self.device:
                # レジスタ読み込み
                _res = bytearray(2)
                self.device.write_then_readinto(bytes([reg]), _res)

                # 取得データ変換
                _data = []
                for _r in _res:
                    _data.append(bin(_r))

                # 上位ビット側のデータを8ビット左にシフトしOR演算することで、上位ビットデータと下位ビットデータが繋がった形の1つのshortデータにする
                _acc = bin( ( int(_data[1]) << 8 | int(_data[0]) ) )

                # 16で割ることで無視すべき下位4ビットを切り捨て、その後係数をかける
                _acc = float( (int(_acc) / 16) * constant.G_UNIT)

                return _acc


    ##
    # @fn       read_filtered_acc()
    # @brief    加速度センサ値をバイナリで返す
    # @param    reg 読み取り対象レジスタ
    # @param    filter 加速度センサ閾値
    # @return   0: 閾値以下センサ値, 1: 閾値以上センサ値
    # @details  加速度センサ値を読み取り、与えられたフィルタを閾値としてバイナリで返す
    def read_filtered_acc(self, reg, filter):
        res = self.read_acc(reg)
        if res < filter:
            return 0
        else:
            return 1
