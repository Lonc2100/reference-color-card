---
name: reference-color-card
description: 从指定电影帧、照片或环境图提取真实颜色，制作白底色块网格及HEX编号的独立PNG色卡参考图，附可追溯取色JSON。用于“提取色卡”“做这种色卡参考图”“给生成模型一张配色图”；不代替洗图综合色块图、LUT或最终调色，不凭印象编造颜色。
metadata:
  version: "0.1.0"
  owner: Lonc2100
  maturity: personal-pilot
---

# 参考图提取为独立色卡

先查看原图及本人样式参考，明确谁提供颜色、谁只提供排版。默认交1920×1080白底、两行六列等宽色块、每块下方HEX；本人的参考图不是所有项目的颜色来源。

1. 使用原分辨率图片；截图先指定有效图像范围，排除浏览器、白边/黑边、字幕、水印。不能靠亮度阈值自动删掉真实暗部。
2. 运行[scripts/extract_card.py](scripts/extract_card.py)，从该图实际像素选代表色，输出`color-card.png`和`palette.json`。脚本只分析源图，不改变源图。颜色不足12种时交实际种数，不编造梯度凑数。
3. 先看主色是否有代表性，再检查需要保留的小面积灯光、植被等。自动提取不理解物体；遗漏时根据原图明确取样位置，用`--points`提供真实像素坐标，重新生成新目录版本，不能手填“更好看”的HEX。
4. 验证每块中心像素、HEX、JSON一致，取样坐标能回查源图。等宽网格是展示方式，不表示各色面积占比；不是影片官方色卡。
5. 展示独立色卡PNG，再给来源JSON与局限。作为生成输入时明确它只管颜色，不提供场景结构或人物身份。不承诺必然复现色调。

```powershell
python <skill>/scripts/extract_card.py --image '<原图>' --out '<新的输出目录>'
# 可选：--crop '左,上,右,下'（原图像素）；--count 12；--points 'x,y;x,y'。
```

依赖Pillow、numpy；全部本地运行，不上传、不自动安装、不联网、不覆盖已有输出。空间锁交scene-spatial-lock，洗图的综合色块交character-asset-cleanup。方法、来源和测试边界见[README](README.md)。
