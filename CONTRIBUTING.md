## 怎么参与进来

### Pull Requests
===
* 欢迎Pull Requests，如果你想要添加新功能或对代码进行大面积修改，请先提一个issue进行讨论
* 请尽可能遵循PEP8规范

### Issues
===
* 请多多提bug和new feature，请不要吝啬
* 英语和中文都是可以的，请不要介意


### 快速熟悉项目
1. 目前的文档还不够完善，测试的模块也几乎没有，很抱歉，想要快速地了解项目，可以借助运行过程中输出的调试信息（不要依赖这些信息，将来我会删掉的），在src/tools/config.py中将debug = False改为debug=True可以参考运行过程中的调试信息，如果debug=False，只能看到Debug.logger.info()输出的信息。
2. 项目根目录下的idea_test.py用来测试正则表达式和bs表达式的正确性的，将来可能会移除。再加一个说明：还有几个细枝末节是没有处理的，比如评论数，赞的数量，更新日期等，这些信息目前对我来说作用不大，所以没有写，将来心血来潮可能会补上，也有可能很久都不会补上。