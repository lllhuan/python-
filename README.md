# 智能停车场识别系统

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-orange.svg)](https://www.mysql.com/)
[![Baidu AI](https://img.shields.io/badge/Baidu%20AI-Plate%20Recognition-green.svg)](https://ai.baidu.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> 桌面应用 + 车牌自动识别 + 停车管理 + 缴费系统 | Python / MySQL / 百度 AI

基于 Python 开发的智能停车场管理系统，通过摄像头实时采集车牌信息，调用百度 AI 车牌识别接口，实现车辆入场登记、自动计费、缴费管理及数据统计分析。适用于小区、商场、园区等停车场场景，可作为毕业设计或小型商超停车管理原型。

## ✨ 主要功能

- **车牌自动识别** – 调用摄像头 + 百度 API，毫秒级识别车牌号码
- **停车管理** – 车辆入场/离场记录、车位状态实时更新
- **缴费支付** – 支持按停车时长计算费用，模拟支付流程
- **数据统计** – 统计车流量、收入、使用频次等，支持可视化
- **用户登录/注册** – 管理员/操作员权限分离，保障系统安全
- **日志追踪** – 完整的操作日志与错误记录，方便调试

## 🛠 技术栈

| 类别       | 技术                                 |
| ---------- | ------------------------------------ |
| 语言       | Python 3.8+                          |
| GUI 框架   | Tkinter / PyQt5（根据实际选择）      |
| 数据库     | MySQL 8.0                            |
| 车牌识别   | 百度 AI 车牌识别 API                  |
| 图像处理   | OpenCV-Python                        |
| 网络请求   | Requests                             |
| 其他       | PyMySQL、Logging、unittest           |

## 📁 项目结构
```
智能停车系统
├── main.py # 程序入口，模块协调与进程控制
├── login.py # 用户登录验证、注册及界面管理
├── BTN.py # 核心业务：车牌识别、停车管理、缴费、统计
├── dbutil.py # 数据库连接管理、SQL操作、数据安全
├── logger.py # 日志记录、错误追踪与调试支持
├── chepai.py # 摄像头控制、图像处理、百度API调用
├── apk.py # API测试与功能验证模块
├── requirements.txt # 项目依赖
├── LICENSE # MIT 许可证
└── README.md
```


## 快速开始

```
git clone https://github.com/yourname/SmartParkingSystem.git
cd SmartParkingSystem
pip install -r requirements.txt
# 配置数据库与百度API密钥
python main.py
```

##📸 界面预览
![登录页面](https://github.com/user-attachments/assets/ffc46536-6cda-418d-9a6e-2bd2a36d0c03)
登录页面

![停车场页面](https://github.com/user-attachments/assets/816cc468-6001-4f3a-a8ef-2f0d4d1d810e)
停车场系统页面

![缴费](https://github.com/user-attachments/assets/4aaed838-c42c-4fff-a433-0a87622b087f)
停车场缴费系统（请勿扫描二维码）

![数据库](https://github.com/user-attachments/assets/8562780b-b1be-4c5e-85e4-9407bd432cfc)
packinfo数据库表

![sjk2](https://github.com/user-attachments/assets/2d35c3f4-b402-4d9b-a2f2-aed53304d86e)
packvehicle表

⚠️ 注意事项

需自行申请百度AI车牌识别接口，并替换 chepai.py 中的 API_KEY 和 SECRET_KEY

缴费模块为模拟流程，不含真实支付

摄像头编号（默认0）请根据实际设备调整

日志文件默认保存在 logs/ 目录

