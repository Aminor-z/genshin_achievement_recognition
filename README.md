[![genshin_achievement_recognition](https://socialify.git.ci/Aminor-z/genshin_achievement_recognition/image?forks=1&issues=1&language=1&name=1&pulls=1&stargazers=1&theme=Dark)](https://github.com/Aminor-z/genshin_achievement_recognition)


# ✧*｡ (ˊᗜˋ*) ✧*｡
你好呀，这是一个通过OCR识别原神成就的项目  
Hi, this is a project to recognize Genshin achievements through OCR.

* 可识别成就名称，成就类型，完成状态，完成次数，完成日期。  
* 支持导出`csv`、`json`格式
* 高准确率：

| 标题识别准确率 | 完成状态识别准确率 | 完成次数识别准确率 | 日期识别准确率 |
| -------------- | ------------------ | ------------------ | -------------- |
| 100%           | 100%               | 100%               | 99%            |

* QQ交流群：`573247616`
* 当前原神匹配版本为`2.5`。（若原神高于这一版本，部分成就可能无法识别，有余力的大佬可通过发Issue等方式催更）
&nbsp;

# 快速使用
1. clone本项目或下载源码
2. 环境配置：运行`setup_requeiment.cmd`（`python`版本推荐`3.6+`）。
3. 启动原神，并将原神的分辨率调整至`1280×720`（必须）。
4. 切换至成就页面并进入某个成就分类中，例如`天地万象`。
5. 不要最小化原神窗口（可切至后台）。
6. 启动`start_server.exe`，等待其显示如下内容：

```
Loading Resource[GenshinAchievementRecognition]: 100%|███████████████████████████████████| 1/1 [xx:xx<xx:xx,  x.xxs/it]
xxxx-xx-xx xx:xx:xx INFO: Resources loading finish.
```
7. 启动`start_client.exe`。
8. 默认按`q`开始识别，按任意其他键取消。
9. 识别期间尽量不要进行操作，识别完成时会显示如下内容：

```
xxxx-xx-xx xx:xx:xx INFO: [xxxx]:[1005]: Start to save achievement record.
xxxx-xx-xx xx:xx:xx INFO: [xxxx]:[1006]: Achievement record saved. [path=gar/record/xxxx.guiar]
xxxx-xx-xx xx:xx:xx INFO: [xxxx]:[1004]: Task finish.
```

10. 您可以切换至其他成就分页重复`8~9`的操作步骤进行识别。
11. 格式转化：
> `csv`：运行`Guiar2Csv.py`，输入游戏uid后可在`gar/record/csv`目录下找到输出结果。（推荐）  
> `json`：运行`Guiar2Json.py`，输入游戏uid后可在`gar/record/json`目录下找到输出结果。

&nbsp;

# 输出示例
* `{uid}.csv`识别成就一览(包含识别到的所有成就)   

| GroupId | Id   | 成就名称 | 状态 | 当前进度 | 目标进度 | 总计 | 完成日期 |
| ------- | ---- | ---------- | ------ | -------- | -------- | ------ | ---------- |
| 0       | 1000 | 俯瞰风景 | 已完成 |          |          | 1      | xxxx/xx/xx |
| 0       | 1032 | 见习勇者 | 已完成 |          |          | 126    | xxxx/xx/xx |
| 0       | 2043 | 摧枯拉朽 | 已完成 |          |          | 404772 | xxxx/xx/xx |
| 0       | 4036 | 过量的思念 | 未完成 | 0        | 5        |        |            |


* `{uid}_incomplete.csv`未完成成就

| GroupId | Id  | 成就名称         | 当前进度 | 目标进度 |
| ------- | --- | -------------------- | -------- | -------- |
| 0       | 92  | 妖鬼狂言百物语 |          |          |
| 0       | 127 | 「是想要驯服我吗？」 | 0        | 1        |
| 0       | 128 | 天赐的猎人之手 |          |          |
| 0       | 129 | 动物园大亨      |          |          |

* 另有`json`格式输出，见 [json格式输出](doc/json_output.md)

&nbsp;

# 目录

* [常见错误解决方案](doc/CES.md)
* [管理员权限说明](doc/admin.md)
* [exe文件说明](doc/exe.md)
* [配置文件说明](doc/config.md)
* [GPU启用说明](doc/gpu.md)
* [guiar文件类型](doc/guiar.md)
* [gamt文件说明](doc/gamt.md)
* [title_fix文件说明](doc/title_fix.md)


&nbsp;