# 从原图提取真实色卡

`reference-color-card` v0.1.0。公开试用版，保留既有方法与功能边界。

## 用途与输入

本地脚本需要Python 3、Pillow、numpy。Windows当前使用C:/Windows/Fonts/arial.ttf；其他系统需自行适配显式字体配置。自动提取不理解物体，也不是LUT；不能保证生成模型复现配色。

## 安装

```sh
npx skills add Lonc2100/reference-color-card --skill reference-color-card
```

也可在 Releases 下载同版本ZIP，解压后将整个`reference-color-card`目录放入客户端实际支持的Skill目录。安装后确认客户端识别该名称，再提供自己的输入；复制成功不等于已完成实际调用。

## 前置条件

- [ ] 客户端支持读取本地SKILL.md和相对引用文件。
- [ ] 提供自己有权使用的参考图及明确设定。
- [ ] 若执行脚本或生图，已具备相应运行环境及授权。

## 你可以直接这样说

> 请使用 reference-color-card，从这张原图提取独立PNG色卡，附HEX和可追溯取样JSON，排除浏览器边框。

## 验证与边界

包内测试可运行`python -m unittest discover -s tests`。开发者如使用技能工厂，可用其`validate_skill.py <本目录>`做结构检查；该工厂不是本包运行依赖。触发报告仅为关键词边界冒烟检查，不代表模型真实选择能力。

## Troubleshooting

未识别Skill时，检查目录中是否直接含SKILL.md，并重新加载客户端；不能运行脚本时先检查Python及依赖。生图结果漂移时比较同一部位，保留原图并拒绝不合格候选，不用更锐代替身份验收。

## 许可证

MIT，见[LICENSE](LICENSE)。包内不含原片、私人图片、密钥、字体文件或模型权重；输入素材权利由使用者自行确认。

## 原有详细说明

# reference-color-card 0.1.0

个人试行Skill：白底网格PNG＋HEX＋逐色源坐标，默认12色。它解决可交给生成模型的实际色卡文件，不只返回文字色值或视频内色条。

参考pascalorg/image-analysis（原图像素→结构化颜色），Color Thief（代表色提取机制），Pillow官方quantize文档。借鉴机制，未复制第三方代码，也不自动安装它们的依赖。

- 设计优势：排版与取色分离；不由图像生成模型猜HEX或伪造颜色。
- 实测优势：本期原图的输出中心像素、源取样、标签JSON逐项一致；不等于所有画面都自动选得好。
- 局限：RGB代表色筛选不是专业感知聚类；自动算法可能遗漏小面积关键色，需看原图并补真实取样点。等宽色块不是面积统计，未经验证不宣称模型控制效果。

来源核查于2026-11-04：
https://raw.githubusercontent.com/pascalorg/skills/main/image-analysis/SKILL.md
https://github.com/lokesh/color-thief
https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.quantize

不采纳：UI专用面积→主辅色角色的自动推断；自动联网安装；无明确许可的第三方代码复制。当前为本地个人版，不发布、无跨客户端热加载保证。

适配目标只表示SKILL.md格式面向这些客户端，不代表所有客户端已实际运行通过。
