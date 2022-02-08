[![genshin_achievement_recognition](https://socialify.git.ci/Aminor-z/genshin_achievement_recognition/image?forks=1&issues=1&language=1&name=1&pulls=1&stargazers=1&theme=Dark)](https://github.com/Aminor-z/genshin_achievement_recognition)


# <center>✧*｡ (ˊᗜˋ*) ✧*｡</center>
<center>你好呀，这是一个通过OCR识别原神成就的项目</center>
<center>Hi, this is a project to identify Genshin Impact through OCR.</center>
&nbsp;

# <center>快速使用</center>

1. 环境配置：运行`setup_requeiment.cmd`。
2. 启动`原神`。
3. 将`原神`的分辨率调整至`1280×720`（必须）。
4. 切换至成就页面并进入某个成就分类中，例如`天地万象`。
5. 不要最小化原神窗口（可切至后台）。
6. 启动`start_server.exe`（该程序强制服务以管理员模式启动`GenshinAchievementRecognitionServer.py`）（必须），等待其显示如下内容：

```
Loading Resource[GenshinAchievementRecognition]: 100%|███████████████████████████████████| 1/1 [xx:xx<xx:xx,  x.xxs/it]
xxxx-xx-xx xx:xx:xx INFO: Resources loading finish.
```
7. 启动`start_client.exe`（该程序强制服务以管理员模式启动`GenshinAchievementRecognitionClient.py`）。（必须）
8. 默认按`q`开始识别，按任意其他键取消。
9. 识别期间尽量不要进行操作，识别完成时会显示如下内容：

```
xxxx-xx-xx xx:xx:xx INFO: [xxxx]:[1005]: Start to save achievement record.
xxxx-xx-xx xx:xx:xx INFO: [xxxx]:[1006]: Achievement record saved. [path=gar/record/xxxx.guiar]
xxxx-xx-xx xx:xx:xx INFO: [xxxx]:[1004]: Task finish.
```

10. 您可以切换至其他成就分页重复`7~9`的操作步骤进行识别。
11. 格式转化：
> `csv`：运行`Guiar2Csv.py`，输入游戏uid后可在`gar/record/csv`目录下找到输出结果。（推荐）  
> `json`：运行`Guiar2Json.py`，输入游戏uid后可在`gar/record/json`目录下找到输出结果。

&nbsp;

# <center>输出示例</center>
* `{uid}.csv`识别成就一览  

| GroupId | Id | 成就名称   | 状态 | 当前进度 | 目标进度 | 总计 | 完成日期 |
| ------- | -- | -------------- | ------ | -------- | -------- | ---- | --------- |
| 1       | 1  | 风与异乡人 | 已完成 |          |          | 0    | 2020/xx/xx |
| 1       | 2  | 千嶂万仞   | 已完成 |          |          | 0    | 2020/xx/xx |
| 1       | 3  | 流水叮咛   | 已完成 |          |          | 0    | 2020/xx/xx |
| 1       | 4  | 神戟狂言凌云霄 | 已完成 |          |          | 0    | 2020/xx/xx |


* `{uid}_incomplete.csv`未完成成就

| GroupId | Id  | 成就名称         | 当前进度 | 目标进度 |
| ------- | --- | -------------------- | -------- | -------- |
| 0       | 92  | 妖鬼狂言百物语 |          |          |
| 0       | 127 | 「是想要驯服我吗？」 | 0        | 1        |
| 0       | 128 | 天赐的猎人之手 |          |          |
| 0       | 129 | 动物园大亨      |          |          |

* 另有`json`格式输出，见 [json格式输出](doc/json_output.md)

&nbsp;

# <center>配置文件</center>

* 位于`gar`文件夹内。
* 配置文件不存在时生成默认配置文件。

* `config.json`：
> * `window_name`: 原神窗口名称，一般为`原神`或`Genshin Impact`。
> * `enable_gpu`: 是否启用GPU，默认为False。
> * 其他参数基本已经调整至最优水平（可能），不建议修改。

* `server_config.json`：
> * `host`: 服务地址。
> * `port`: 服务端口。
> * `enable_gamt`: 是否启用gamt。
> * `gamt_file_path`: gamt文件路径。
> * `enable_title_fix`: 是否启用标题修复。
> * `title_fix_file_path`: 标题修复文件路径。
> * `save_record`: 是否保存识别记录。
> * `save_record_path`: 识别记录保存位置的文件夹路径。
> * `save_record_backup`: 是否保存备份识别记录。
> * `save_record_backup_path`: 识别记录备份位置的文件夹路径。
> * `record_type`: 暂无作用。

* `client_config.json`：
> * `host`: 服务地址，应与`server.config.json`中的`host`相同。
> * `port`: 服务端口，应与`server.config.json`中的`port`相同。
> * `start_key`: 开始键，字符串类型，仅支持单个字母。

&nbsp;

# <center>guiar文件</center>

* `guiar`文件使用protobuf进行编码，由`GuiarBlock`和`GuiarItem`组成，其大致格式如下所示：

```
{length of the next GuiarBlock}{GuiarBlock{uid,group_id,[GuiarItem,GuiarItem,GuiarItem]}}
```
* `GuiarBlock`
> * `uid`: 游戏内的uid
> * `group_id`: 成就所属类别
> * `items`: 一个或多个`GuiarItem`

* `GuiarItem`
> * `id`: 成就id，同名成就仅取id最大的
> * `state`: 成就完成状态，True为已完成，False为未完成
> * `data_a`: 当成就完成时，该项目表示总计完成次数；当成就未完成时，该项目表示当前进度
> * `data_b`: 当成就完成时，该项目表示`guiar_date`（见下方对应条目）；当成就未完成时，该项目表示目标进度

* `guiar_date`
> * 该日期格式对year,month,day三个变量进行了编码。
> * 编码公式：  
> `(year - 2020) * 384 + ((month - 1) << 5) + (day - 1)`
> * 解码公式：  
> ```python
>        t = int(guiar_date / 384)
>        year = t + 2020
>        md = guiar_date - t * 384
>        month = (md >> 5) + 1
>        day = md % 32 + 1
>        return year, month, day
> ```
>

* 变量具体类型请参考`proto/Guiar.proto`

&nbsp;

# <center>gamt文件</center>

* 该文件为原神成就映射表(Genshin Impact Achievement Mapping Table)
* 格式：
> {去除空白字符、标点符号的成就标题},{成就标题},{成就id},{成就group_id}

&nbsp;

# <center>title_fix文件</center>

* 该文件为标题修复文件。由于OCR对相似中文字符难以辨别，如`迁`和`迂`、`土`和`士`等，外加原神游戏内字体笔画较粗，造成个别字符识别出错或失败。
* 格式：
> {去除空白符、标点符号的错误标题},{去除空白符、标点符号的正确标题}


&nbsp;

# <center>API文档</center>
* API文档会在日后完善  

&nbsp;

# <center>友情链接</center>
* [Snap.Genshin](https://github.com/DGP-Studio/Snap.Genshin)