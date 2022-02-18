# 配置文件说明

* 配置文件位于`gar`文件夹内，包含`config.json`、`server_config.json`、`client_config.json`。
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