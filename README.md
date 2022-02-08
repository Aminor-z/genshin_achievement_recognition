[![genshin_achievement_recognition](https://socialify.git.ci/Aminor-z/genshin_achievement_recognition/image?forks=1&issues=1&language=1&name=1&pulls=1&stargazers=1&theme=Dark)](https://github.com/Aminor-z/genshin_achievement_recognition)

# Genshin Achievement Recognition
## ✧*｡ (ˊᗜˋ*) ✧*｡
你好呀，这是一个通过OCR识别原神成就的项目  
Hello, this is a project to identify Genshin Impact through OCR.  

Readme 文件会在日后完善  
Readme files will be gradually improved in the future

# 快速使用

1. 环境配置：运行`setup_requeiment.cmd`。
2. 启动`原神`。
3. 将`原神`的分辨率调整至`1280×720`（必须）。
4. 切换至成就页面并进入某个成就分类中，例如`天地万象`。
5. 不要最小化原神窗口（可切至后台）。
6. 启动`start_server.exe`（该程序强制服务以管理员模式启动`GenshinAchievementRecognitionServer.py`）（必须）等待其显示如下内容：

```
Loading Resource[GenshinAchievementRecognition]: 100%|███████████████████████████████████| 1/1 [xx:xx<xx:xx,  x.xxs/it]
20xx-xx-xx xx:xx:xx INFO: Resources loading finish.
```
7. 启动`start_server.exe`（该程序强制服务以管理员模式启动`GenshinAchievementRecognitionClient.py`）（必须）
8. 默认按`q`开始识别，按任意其他键取消。
9. 识别期间尽量不要进行操作，识别完成时会显示如下内容：

```
xxxx-xx-xx xx:xx:xx INFO: [xxxx]:[1005]: Start to save achievement record.
xxxx-xx-xx xx:xx:xx INFO: [xxxx]:[1006]: Achievement record saved. [path=gar/record/xxxx.guiar]
xxxx-xx-xx xx:xx:xx INFO: [xxxx]:[1004]: Task finish.
```

10. 您可以切换至其他成就分页重复`7~9`的操作步骤进行识别
11. 可视化：
> `csv`：运行`Guiar2Csv.py`，输入游戏uid后可在`gar/record/csv`目录下找到输出结果。（推荐）  
> `json`：运行`Guiar2Json.py`，输入游戏uid后可在`gar/record/json`目录下找到输出结果。

# 配置文件

位于`gar/*.json`