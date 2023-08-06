<h1 align="center">cutmv</h1>

<p align="center"><img src="https://img.shields.io/badge/Licence-MIT-green.svg?style=for-the-badge" /></p>

### 项目介绍

调用ffmpeg库实现视频剪辑

该库需要依赖ffmpeg软件。所以在调用该库写代码时，请首先确保您的计算机中已安装ffmpeg并将ffmpeg软件路径加入环境变量。

### 计划目标

* [x] 全格式音频文件分段切割
* [x] 全格式视频文件分段切割
* [x] 全格式音频格式转换
* [x] 全格式视频格式转换

### 项目文件参数说明

* s_time ：音视频文件分割起始时间
* e_time ：音视频文件分割截至时间
* files ：需要切割的文件名
* i_format ：输出格式

### 版本修正

* 2020-12-10 [v0.0.3]：修正了代码中的小错误
* 2020-12-10 [v0.0.4]：追加批量压制视频功能

### 代码演示：
* 调用 cutmv 批量剪辑视频
```python
import os
import cutmv

if __name__ == "__main__":
    rootdir = './'
    list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
    for i in range(0, len(list)):
        cutmv.video_cut(0, 480, list[i], '.mp4')
```

* 调用 cutmv 批量压制视频
```python
import cutmv

if __name__ == "__main__":
    cutmv.video_compress('./', './压制/', '600k')
```

### 合作及交流

* 联系邮箱：<gomehome@qq.com>
* QQ ：287000822

