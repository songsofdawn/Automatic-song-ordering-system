# 代码运行说明

### 功能
可以实现：

* 在局域网内点歌
* 任一用户点歌按时间顺序产生列表，按照列表逐一放歌

### Guides
script目录下放置了运行所必须的bat脚本、chrome浏览器驱动和python脚本

* auto_music.py下有三个路径需要自定义：
* * chrome_path：你的chrome浏览器exe文件路径
* * driver_path：你的chrome驱动器路径
* * user_data_di：你的chrome个人信息路径，用以保存登录信息

* bat脚本中路径为auto_music.py的路径
* 请务必修改java代码中bat脚本的路径
