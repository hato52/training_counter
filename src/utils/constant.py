##
# @file     constant.py
# @version  1.0.0
# @author   hato
# @date     2022/04/29
# @brief    定数値定義
# @details  定数値の定義を行う

# Button
BTN_UP          = 1         # ボタンが押されていない
BTN_DOWN        = 0         # ボタンが押されている

# LED
LED_ON          = False     # LED点灯
LED_OFF         = True      # LED消灯

# Atmospheric Pressure Sensor
LPS22HB         = 0x5c      # 気圧センサアドレス
CTRL_REG1       = 0x10      # コントロールレジスタ1

# Humidity and Temperature Sensor
HDC2010         = 0x40      # 温湿度センサアドレス
RESET_AND_DRDY  = 0x0e      # リセット・データレディ設定レジスタ

# 9Axis Sensor
BMX055_ACC      = 0x18      # 加速度センサアドレス
PMU_RANGE       = 0x0F      # レンジ設定レジスタ
PMU_BW          = 0x10      # フィルタ帯域設定レジスタ
PMU_LPW         = 0x11      # パワーモード設定レジスタ
ACC_X           = 0x02      # X軸加速度レジスタ
ACC_Y           = 0x04      # Y軸加速度レジスタ
ACC_Z           = 0x06      # Z軸加速度レジスタ

BMX055_GYR      = 0x68      # ジャイロセンサ
GYR_LPM1        = 0x11      # パワーモード設定レジスタ

BMX055_MAG      = 0x10      # 地磁気センサ
MAG_CTRL        = 0x4B      # パワー設定レジスタ

G_UNIT          = 0.00098;  # 重力加速度係数 1024LSB/g

# State
STATE_SLEEP     = 1         # スリープ状態
STATE_INIT      = 2         # 初期化状態
STATE_ACTIVE    = 3         # アクティブ状態
STATE_ERROR     = 0         # エラー

# Sleep Time
TIME_TO_SLEEP_SLEEP   = 0.1         # スリープ時周期処理待機時間 (s)
TIME_TO_SLEEP_ACTIVE  = 1           # アクティブ時周期処理待機時間 (s)

# Threshold
THRESHOLD       = 2.0       # 加速度センサ 閾値
