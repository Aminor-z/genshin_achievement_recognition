# guiar文件类型

* `guiar`文件使用protobuf进行编码，由`GuiarBlock`和`GuiarItem`组成，其大致格式如下所示：

```
{length of the next GuiarBlock}{GuiarBlock{uid,group_id,[GuiarItem,GuiarItem,GuiarItem...]}}
```
* `GuiarBlock`
> * `uid`: 游戏内的uid
> * `group_id`: 成就所属类别
> * `items`: 一个或多个`GuiarItem`

* `GuiarItem`
> * `id`: 成就id，同名成就仅取id最大的
> * `state`: 成就完成状态，True为已完成，False为未完成
> * `data_a`: 当成就完成时，该项目表示`guiar_date`（见下方对应条目）；当成就未完成时，该项目表示当前进度
> * `data_b`: 当成就完成时，该项目表示总计完成次数；当成就未完成时，该项目表示目标进度

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