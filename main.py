import time

from app import controller


def main():
    ctr = controller.Controller()

    while True:
        # センサスリープ
        print("1 sensor sleep")
        ctr.sleep()
    
        # ボタン押下待機
        print("2 wait for button press")
        while ctr.is_button_pressed():         # ボタン押しっぱなしによる処理飛ばしの防止
            time.sleep(0.1)

        while not ctr.is_button_pressed():
            time.sleep(0.1)

        # 初期化処理
        print("3 initialize")
        ctr.initialize()

        # 接続待機
        print("4 wait for connected")
        timer = 0
        while not ctr.is_connected():
            timer = timer + 1
            if timer > 30:      # 接続タイムアウト(30秒)
                break
            ctr.led_on()
            time.sleep(0.5)
            ctr.led_off()
            time.sleep(0.5)

        if ctr.is_connected():
            while ctr.is_button_pressed():         # ボタン押しっぱなしによる処理飛ばしの防止
                time.sleep(0.1)

            # アクティブ移行時処理
            print("5 activate")
            ctr.activate()

            # 定常処理
            print("6 cyclic process")
            cnt = 0
            while not ctr.is_button_pressed() and ctr.is_connected():
                ctr.cyclic()
                if cnt > 10:
                    ctr.data_send()
                    cnt = 0
                cnt = cnt + 1
                time.sleep(0.1)

            # 通信終了処理
            print("7 disconnect")
            ctr.disconnect()
            time.sleep(1)


if __name__ == "__main__":
    main()
