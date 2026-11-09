# Sandstorm V1

2026-11-09 冻结版本 / Frozen release.

- [GitHub Repository](https://github.com/QzQ99999/sandstorm-v1)
- [GitHub Pages — 在线运行](https://qzq99999.github.io/sandstorm-v1/)
- [Releases — 完整离线游戏与源码归档](https://github.com/QzQ99999/sandstorm-v1/releases)

独立的 Sandstorm V1，包含碎片行走、战斗性能优化及人物射击补光。
人物移动边缘限制已取消；敌人生成/检测距离20米，7米内奔跑，射击冷却0.3秒。
保留完整工作台和59个控件。平均帧率超过100不代表最低100；本版本仍有短时慢帧。

使用支持WebGPU的桌面Chrome或Edge。完整内嵌HTML约166MB，首次加载需要时间。

操作：`1`进入/退出游戏；`W A S D`移动；`Shift`疾跑；按住右键瞄准；单击左键射击；`2`隐藏/显示提示与帧数；普通模式`Tab`打开编辑器。

## 版本冻结

未经用户明确确认，不得修改源码、资源、HTML、工作台、启动器或归档，不得重建或再次发布。当前冻结要求覆盖之前全部优化授权。详见[AGENTS.md](AGENTS.md)。

Frozen standalone HTML SHA-256:

`5a656c3a80d3c34bddcd880588a55b7f4660da5321c7c20cb1bc6ae4a0b3e7be`

## 逐字节发布

仓库使用不超过32MiB的UTF-8分片。GitHub Pages通过Jekyll原样拼接为index.html，不重新编译游戏，不修改内嵌资产。完整生产源码、离线HTML和启动器在Release归档中。

只读验证：`python verify-parts.py`

还原离线HTML（拒绝覆盖已有文件）：`python verify-parts.py --output "Sandstorm V1.html"`

将`Launch Sandstorm V1.cmd`放在HTML旁边启动。完整场景预设见`initial-workbench.json`，Three.js许可见`THREE-LICENSE.txt`。
