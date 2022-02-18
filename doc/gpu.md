# GPU启用说明

> 启用GPU能显著地提高运行速度，但配置GPU环境操作较为复杂，不适合普通用户。

## GPU启用步骤

1. 配置CUDA环境。
> 您需要查看显卡的CUDA支持版本，前往官网下载对应版本CUDA环境并将其配置好。

2. 配置GPU版本的PyTorch。
> 您需要前往[PyTorch官网](https://pytorch.org/get-started/locally/)，寻找低于或等于您显卡CUDA支持版本的PyTorch版本，下载完成后通过pip等方式将其配置好。

3. 在本程序包中的`gar`目录下，找到`config.json`，将`config.json`中的`enable_gpu`设置为`true`。