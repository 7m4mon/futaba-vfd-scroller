"""
Futaba VFD Display Controller
-----------------------------

このスクリプトは、Futaba製 160x36ドットのVFDモジュール（例：AH145AAシリーズ）に対して、
RS-232C経由でビットマップ画像を送信し、テキストスクロールを行うためのツールです。

主な機能:
- 任意の文字列を指定したビットマップフォントでレンダリング
- 18ドットビットマップフォントを縦2倍（36ドット）にスケーリング
- スクリーン幅（160ピクセル）に合わせて画像を右から左にスクロール表示
- Futabaモジュールに対応したバイナリ形式に変換して送信

使用方法:
1. 使用するフォント（.ttf）を指定する
2. 表示したい文字列とシリアルポート名を設定する
3. スクリプトを実行すると、画像生成 → スクロール → シリアル送信を自動で行う

要件:
- Python 3.x
- Pillow ライブラリ（画像処理）
- pyserial ライブラリ（シリアル通信）

例:
    font_path = "JF-Dot-Ayu18.ttf"
    text = "Hello, world!"
    output_file = "output.bmp"
    display = FutabaDisplay(port="COM3")
    display.text_to_bitmap(text, font_path, output_file)
    display.scroll_image(output_file)

対応機種:
- AH145AA / AB / AC / BA / BB / BC （Futaba社製 VFD 160x36ドット）

Author: 7M4MON
Date: 2025-May-1st
"""


import serial
import time
from PIL import Image, ImageDraw, ImageFont

class FutabaDisplay:
    def __init__(self, port="COM3", baudrate=38400):
        self.port = port
        self.baudrate = baudrate

    def send(self, data: bytes):
        with serial.Serial(self.port, self.baudrate, timeout=1) as ser:
            ser.write(data)
            print("送信完了")

    def text_to_bitmap(self, text, font_path, output_file, base_height=18, scale=2, offset_height=-1):
        font = ImageFont.truetype(font_path, base_height)
        dummy_img = Image.new('RGB', (1, 1))
        bbox = ImageDraw.Draw(dummy_img).textbbox((0, 0), text, font)
        text_width = bbox[2] - bbox[0]
        image = Image.new('1', (text_width, base_height), color=0)
        draw = ImageDraw.Draw(image)
        draw.text((0, offset_height), text, font=font, fill=1)
        scaled_image = image.resize((text_width * scale, base_height * scale), Image.NEAREST)
        scaled_image.save(output_file, format="BMP")

    def scroll_image(self, image_path, screen_width=160, speed=0.05, step=10):
        image = Image.open(image_path)
        img_width, img_height = image.size
        screen = Image.new('RGB', (screen_width, img_height), (0, 0, 0))
        for x in range(0, img_width - screen_width, step):
            scroll_part = image.crop((x, 0, x + screen_width, img_height))
            screen.paste(scroll_part, (0, 0))
            binary_data = self.image_to_binary_array(screen)
            self.send(binary_data)
            time.sleep(speed)

    def image_to_binary_array(self, img):
        img = img.convert("1")
        width, height = img.size
        if width < 160 or height < 40:
            padded = Image.new("1", (160, 40), color=0)
            padded.paste(img, (0, 0))
            img = padded
        binary_data = [0x1B, 0x20]
        for x in range(160):
            for y in range(0, 40, 8):
                byte_val = 0
                for bit in range(8):
                    if y + bit < 40:
                        bit_val = 1 if img.getpixel((x, y + bit)) == 255 else 0
                        byte_val = (byte_val << 1) | bit_val
                binary_data.append(byte_val)
        return bytes(binary_data)

if __name__ == "__main__":
    display = FutabaDisplay(port="COM4", baudrate=38400)
    text = "　　　　武器や防具は、装備しないと効果がないよ！　　　　　"
    font_path = "JF-Dot-Ayu18.ttf"
    output_file = "output.bmp"
    display.text_to_bitmap(text, font_path, output_file, base_height=18, scale=2)
    display.scroll_image(output_file, screen_width=160, speed=0.05, step=10)
