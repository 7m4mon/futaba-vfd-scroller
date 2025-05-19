# Futaba VFD Scroller / フタバ VFD スクローラー

A Python tool for rendering and scrolling bitmap text on Futaba's 160x36 dot Vacuum Fluorescent Display (VFD) modules over RS-232C.

Futaba製160×36ドット VFDモジュール（AH145シリーズなど）に、RS232C経由でビットマップ文字を描画・スクロール表示するPythonツールです。

[![](https://img.youtube.com/vi/sQdYXVcq03k/0.jpg)](https://www.youtube.com/watch?v=sQdYXVcq03k)

---

## Features / 特徴
- 18ドットのビットマップフォントを縦2倍（36ドット）にスケール
- 160ピクセル幅の画面上を右から左にスクロール表示
- Futabaモジュール用のバイナリデータに自動変換
- RS232C経由で送信

## Supported Hardware / 対応機種
- Futaba AH145シリーズ（AH145AA / AB / AC / BA / BB / BC）

## Requirements / 必要な環境
- Python 3.x
- Pillow
- pyserial

```bash
pip install pillow pyserial
```

## Usage / 使い方

```python
from futaba_display import FutabaDisplay

display = FutabaDisplay(port="COM3", baudrate=38400)
text = "　　　　武器や防具は、装備しないと効果がないよ！　　　　　"
font_path = "JF-Dot-Ayu18.ttf"
output_file = "output.bmp"

# Generate scaled bitmap / ビットマップ生成
display.text_to_bitmap(text, font_path, output_file, base_height=18, scale=2)

# Scroll image on display / スクロール表示
display.scroll_image(output_file, screen_width=160, speed=0.05, step=10)
```

## License / ライセンス
MIT License

---

Made with ❤️ by 7M4MON