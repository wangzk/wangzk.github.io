---
title: '研究生新生编程能力提升培训教程'
date: 2022-07-06 09:30:00 +0800
categories: teaching 
--- 

本文主要为我的新入学研究生准备，用于培养与提升研究生新生的编程能力。本文内容将持续更新。

*最后更新日期：2022年8月1日*

## 培训目标

1. 【编程环境】熟悉Linux环境下编程环境，能够使用IDE开发程序，能在Linux环境下编译运行与调试。
2. 【编程环境】掌握基本的Linux Shell环境使用方法，适应Linux的命令行界面。
3. 【编程环境】掌握使用git进行源代码版本控制与协作的方法。
4. 【编程环境】了解Linux下性能Profile工具的使用。
5. 【编程能力】熟练掌握常用数据结构实现方法。
6. 【编程能力】熟练掌握常用算法实现方法。

## 培训任务

### 任务1：Linux Shell环境入门

利用阿里云开发者发社区提供的[“Linux基础知识”在线课程](https://developer.aliyun.com/graph/linux/point/229?spm=a2c6h.21254954.graph.4.67e64fe0dXrbhC)，完成以下学习任务：

1. 完成基础知识下的学习和所有体验实验室的体验活动。
2. 在本地笔记本安装Linux虚拟机（Ubuntu 22.04），学习Ubuntu 22.04使用，并熟悉在Ubuntu 22.04下进行命令行操作。
3. 虚拟机里的Ubuntu 22.04能够连接外网，并且与本机进行文件共享（VMware虚拟机[3]或VirtualBox虚拟机[4]）。


参考资料：

[1] 上海交通大学并行与分布式系统研究所, "上海交通大学IPADS新人培训第一讲：Shell", 2021. [Bilibili视频](https://www.bilibili.com/video/BV1y44y1v7c3/?spm_id_from=333.788&vd_source=351076ebef83681ea73f45ba5a858412)

[2] 富国王，"Ubuntu22.04安装教程 实战无跳过超详细", 2022. [Bilibili视频](https://www.bilibili.com/video/BV1Ru411y7n9?vd_source=351076ebef83681ea73f45ba5a858412)

[3] QQ两个人, "图解VMware+Linux开启共享文件", 2021. [CSDN博客链接](https://blog.csdn.net/qq_44938451/article/details/119104928)

[4] 苏格拉一地, "Windows系统与VirtualBox中Ubuntu系统文件夹共享", 2022. [Bilibili视频](https://www.bilibili.com/read/cv16973605/)

### 任务2：Linux下C语言编程入门

利用上海交通大学IPADS研究所的新人培训教程，学习Linux下C++编程的入门知识，并利用CMake构建C语言编程环境。

- 视频指导1(Linux命令行使用进阶): [IPADS新人培训第一讲：Shell](https://www.bilibili.com/video/BV1y44y1v7c3/?spm_id_from=333.788)
- 视频指导2(Linux下C语言大型工程编译工具入门): [IPADS新人培训第二讲：CMake](https://www.bilibili.com/video/BV14h41187FZ/?spm_id_from=333.788)
- 可以使用Ubuntu操作系统提供的apt命令安装cmake程序[2]。

完成以下学习任务: 

- 在Linux虚拟机中,完成视频指导2中[样例程序代码](https://github.com/richardchien/modern-cmake-by-example)程序的本地编译。
- 在Linux虚拟机中，编写一个Hello，World的程序，并创建一个cmake工程编译该Hello，World程序。

参考资料：

[1] Linux命令行与shell脚本编程大全（第3版）(图灵出品) [京东购买链接](https://item.jd.com/12010266.html#crumb-wrap)

[2] 菜鸟教程, "Linux apt命令", https://www.runoob.com/linux/linux-comm-apt.html.


### 任务3：Git代码管理入门

利用上海交通大学IPDAS研究所的新人培训教程，学习Linux下利用git管理源代码并进行协作开发的知识，并将本地代码上传到[Gitee](https://gitee.com)的教师指定代码仓库中。Git用于管理源代码的不同版本，并上传到远程仓库以在多位开发者之间同步与协作。Vim是Linux下的一个文本编辑器，可以运行在命令行界面里，常用于在命令行环境内编辑文件内容使用。

- 视频指导1 (Git使用入门): [IPADS新人培训第三讲：Git](https://www.bilibili.com/video/BV1YR4y1E7LX/?spm_id_from=333.788)
- 视频指导2（Vim使用入门）：[IPADS新人培训第四讲：Vim](https://www.bilibili.com/video/BV1PL411M7bg/?spm_id_from=333.788) 

完成以下学习任务：

- 注册一个Gitee网站的账号。联系老师在Gitee网站开通一个代码仓库，用于编程练习。老师会提供Gitee代码仓库的地址以及remote地址。
- 将Gitee上的远程仓库拉取（Pull）到本地。将之前创建的Hello，World的CMake工程添加到git代码仓库里。
- 将本地更新后的代码仓库推送到Gitee网站的远程仓库，并在网站上查看。
- 尝试使用vim编辑Hello, World源代码，将其中的"Hello, Wolrd!"变成"Hello, NUAA!"。将更新后的源代码进行提交(commit)，并推送到远程的Gitee仓库。

参考资料：

[1] 菜鸟教程, "Git教程", https://www.runoob.com/git/git-tutorial.html.

[2] 利用vim自带的vimtutor程序学习vim的基本使用。使用apt命令`apt install vim-gtk`安装vim，然后在命令行里执行命令`vimtutor`开始vim学习。

### 任务4：利用LeetCode提升数据结构的编程能力

利用[力扣（LeetCode中文站）](https://leetcode.cn/)提供的学习教程和题库，完成常用数据结构的编程练习，以提升编程能力。首先需要在力扣网站注册会员，用会员登录后就可以看到左上角的“学习”和“题库”。在力扣的“学习”版块，依次完成以下课程内容的学习与编程任务：

1. [数组和字符串-LeetBook](https://leetcode.cn/leetbook/detail/array-and-string/)
2. [链表-LeetBook](https://leetcode.cn/leetbook/detail/linked-list/)
3. [二叉树-LeetBook](https://leetcode.cn/leetbook/detail/data-structure-binary-tree/)
4. [队列&栈-LeetBook](https://leetcode.cn/leetbook/detail/queue-stack/)
5. [二分查找-LeetBook](https://leetcode.cn/leetbook/detail/binary-search/)
6. [哈希表-LeetBook](https://leetcode.cn/leetbook/detail/hash-table/)

学习小提示：

1. 关于力扣网站的使用方法可以参见官方的[入门指南](https://support.leetcode.cn/hc/kb/category/1018381/)，或者在网络上搜索相关资料。力扣网站是提升编程能力的常用网站，互联网上有很多经验分享帖子:)
2. 在课程中的做题页面（例如[“寻找数组的中心索引”](https://leetcode.cn/leetbook/read/array-and-string/yf47s/)）时，注意页面下方类似如下说明的提示：

    ![LeetCode Tips](/img/2022-07-06-prepare-for-graduate-study/leetcode-tip.png)

    该提示中的链接将引导到主站对应的题目页面。在主站的题目页面可以看到完整的题目描述、评论以及题解。**建议先自己尝试独立思考和解题。当遇到不会的题目时，先查询数据结构教材或其他的在线资料，实在搞不懂时再去看网站提供的题解**。即使看了题解获得了解题思路，也要在关闭题解的状态下重新独立作答一次，**直到自己独立写出的程序也能通过测试**。

3. 编写代码时需遵循[Google C++ 风格指南](https://zh-google-styleguide.readthedocs.io/en/latest/)。需要先阅读该风格指南的“注释”和“格式”两部分，其他的部分在用到相应C++语言特性时阅读。

**源代码上传**：学习过程中各题目的解题答案源代码文件，需要上传到上一个任务中创建的git仓库中。每一个题目对应一个源代码文件（*源代码文件名为该题目在LeetCode上的编号*），且每个文件至少应提交（commit）一次。避免一次性同时提交多个源代码文件。同一个源代码文件可以commit多次，形成不同的文件版本（version）。

### 任务5：单元测试与测试驱动的开发

软件测试是保证软件开发质量的重要手段。在我们学习的过程中，也需要编写大量的程序，程序的正确性及质量直接影响计算机研究中的各类实验的正确性与实验结果。当我们编写的程序因为bug而不能产生预期的结果时（例如程序的预测精度或计算性能低于预期），可能并不是因为我们自己的idea有问题，而是软件中的bug使得我们提出的idea并不能正确发挥作用。因此，学习基本的软件测试知识，是编写正确程序的基础。本次任务中请依次完成以下的任务：

1. 学习["2021版南京大学软件测试公开课"](https://www.bilibili.com/video/BV1v3411v785)的第5部分["1.3 测试术语"](https://www.bilibili.com/video/BV1v3411v785?p=5)，了解软件测试中的基本概念。
2. 单元测试（Unit Test）是软件测试中的一种基础测试方法，也是最常用的测试方法。利用["同济大学-软件测试方法和技术实践"](https://www.bilibili.com/video/BV1wW411j7rN)在线课程，学习从第8部分"1.0单元测试引言"到第17部分"1.9还有哪些单元测试工具"的内容，了解单元测试的概念以及方法。
3. 测试驱动开发（Test-Driven Development）是一种测试先于实现的软件开发理念，通过以单元测试为先导，督促程序员写出高质量的程序。学习["C++中的测试驱动开发 Test-Driven Development in C++"](https://www.bilibili.com/video/BV1Yb411v73C)的在线课程，了解测试驱动开发的理解以及实践方法。
   - [《Google Test用户指南》](https://google.github.io/googletest/)，介绍了Google Test框架的安装与使用方法。
4. 编写程序时，遵循良好的编码风格能够提升源代码的易读性，并避免一些常见的编码错误。不同语言有不同的常用编码风格，主流大厂会公开发布其代码编码规范：
   - [《Google C++ 风格指南》](https://zh-google-styleguide.readthedocs.io/en/latest/)，需要先阅读该风格指南的“注释”和“格式”两部分，其他的部分在用到相应C++语言特性时阅读。
   - [《阿里巴巴Java开发手册》](https://developer.aliyun.com/special/tech-java)，来自国内Java大厂的一线实践经验。
   - 将编码规范当做**工具书**使用，即用即查。

在后续的程序编写与开发过程中，遵循与实践测试驱动开发的理念，并利用编码风格规范代码。

🎬本任务的在线培训PPT[下载链接](/assets/任务5培训大纲ppt.pdf)