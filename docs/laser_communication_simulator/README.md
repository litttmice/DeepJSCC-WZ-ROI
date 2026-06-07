# 激光通信模拟器框架图

本目录提供按参考图重新绘制的激光通信模拟器框架图，内容覆盖“姿轨与环境模拟—激光远场模拟—通信性能测试”的完整验证闭环。

## 文件说明

- `laser_communication_simulator_framework.vdx`：**Visio 可编辑源文件**（Visio XML Drawing）。在 Microsoft Visio 中打开后，文本框、功能模块和连接线均可分别编辑；如需新版格式，可使用“另存为”保存成 `.vsdx`。
- `laser_communication_simulator_framework.svg`：高清矢量预览，也可直接插入 Visio、PowerPoint 或论文文档。
- `generate_diagram.py`：零第三方依赖的生成脚本，用于统一更新 VDX 与 SVG。

## 图示结构

1. **姿轨与环境模拟组件**：六自由度运动、微振动谱与轨道相对运动、冷黑真空热环境。
2. **激光远场模拟组件**：离轴抛物面镜平行光管、程控光强衰减、波前畸变加载、指向抖动和等效远场光斑。
3. **激光通信性能测试组件**：误码率、跟瞄精度、通信速率的自动测试。
4. 底部闭环表示三者协同完成“终端状态 → 远场传输 → 性能评估”。

## 重新生成

```bash
python docs/laser_communication_simulator/generate_diagram.py
```
