import board, busio
from adafruit_bus_device.i2c_device import I2CDevice

from utils import constant


class NineAxisSensorDriver():

    def __init__(self):
        pass

    # @brief センサ初期化処理
    def initialize(self):
        with busio.I2C(board.SCL, board.SDA) as self.i2c:
            with I2CDevice(self.i2c, constant.BMX055_ACC) as self.device:
                self.device.write(bytes([constant.PMU_RANGE, 0x03]))  # g-range +-2g
                self.device.write(bytes([constant.PMU_BW, 0x08]))     # フィルタ帯域 7.81Hz
                self.device.write(bytes([constant.PMU_LPW, 0x00]))    # 通常モードに移行


    # @brief センサを低電力消費状態に移行する
    def sleep(self):
        with busio.I2C(board.SCL, board.SDA) as self.i2c:
            # 加速度センサ
            with I2CDevice(self.i2c, constant.BMX055_ACC) as self.device:
                self.device.write(bytes([constant.PMU_LPW, 0x20]))          # DEEP_SUSPEND mode
            # ジャイロセンサ
            with I2CDevice(self.i2c, constant.BMX055_GYR) as self.device:
                self.device.write(bytes([constant.GYR_LPM1,0x20]))          # DEEP_SUSPEND mode
            # 地磁気センサ
            with I2CDevice(self.i2c, constant.BMX055_MAG) as self.device:
                self.device.write(bytes([constant.MAG_CTRL,0x00]))          # Suspend mode
            # 気圧センサ
            with I2CDevice(self.i2c, constant.LPS22HB) as self.device:
                self.device.write(bytes([constant.CTRL_REG1, 0x00]))        # Power-down mode
            # 温湿度センサ
            with I2CDevice(self.i2c, constant.HDC2010) as self.device:
                self.device.write(bytes([constant.RESET_AND_DRDY,0x80]))    # Soft-Reset


    # @brief 加速度センサ値の読み込み
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


    # @brief 加速度変化をバイナリで返す
    def read_filtered_acc(self, reg, filter):
        res = self.read_acc(reg)
        if res < filter:
            return 0
        else:
            return 1
