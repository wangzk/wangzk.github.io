---
layout: article
title: "本科毕业设计/大学生创新训练计划技术指导"
date: 2024-01-01 16:00:00 +08:00
last_modified_at: 2024-01-23 16:42:00 +08:00
categories: tech
---

在进行本科毕业设计、大学生创新训练计划时，需要提前学习和掌握部分课堂中不会教、但对于后续研究工作开展非常必要的技术知识。目前包括Linux编程环境配置、C/C++语言系列、Java语言系列、分布式计算、图计算、大数据技术等。

<!--more-->

## Linux编程环境

### Linux虚拟机安装

部分项目的后续实验需要在Linux开发服务器或学校的高性能计算平台上完成，目标操作系统均为Linux系统，因此需要熟悉Linux系统命令行的使用方式。如果本地电脑是Windows环境，需要安装Linux虚拟机。

为了适应学校的高性能计算平台的操作系统环境（CentOS 7），本地安装CentOS 7的虚拟机。

- Linux发行版：CentOS 7。安装光盘iso下载链接：[南京大学开源软件镜像站CentOS7安装光盘](https://mirror.nju.edu.cn/centos/7/isos/x86_64/CentOS-7-x86_64-DVD-2207-02.iso)。
- 虚拟机：使用VMWare或VirtualBox，安装指导视频：[如何使用VMware安装centos7\_哔哩哔哩\_bilibili](https://www.bilibili.com/video/BV1Kh4y1m767/)

也可以根据需要安装Ubuntu 22.04。Ubuntu 22.04的镜像也可以在南京大学开源软件镜像站下载到。

### Linux基础工具使用

下面使用来自MIT的[_The Missing Semester of Your CS Education_](https://missing.csail.mit.edu)（计算机教育中缺失的一课）作为参考资料。该课程提供了详细的技术指导与视频，方便学习。目前国内已经有了对应的中文版网站[“计算机教育中缺失的一课”](https://missing-semester-cn.github.io)。与Linux基础工具使用相关的课程章节包括：

- 课程概览与shell。
- Shell工具和脚本。

关于Linux系统的常用命令，可以参考书籍：

[1] 《Linux命令行与shell脚本编程大全（第3版）(图灵出品)》([美]布鲁姆（Richard Blum）,布雷斯纳汉（Christine Bresnahan）)-[京东图书(jd.com)](https://item.jd.com/12010266.html)

### Docker容器安装与使用

在Linux虚拟机中，安装docker容器环境。部分软件（例如GraphScope）的安装与使用都在Docker环境中完成。

参考教程： [2小时搞定Docker 全程干货 基于CentOS7](https://www.bilibili.com/video/BV1vP4y1m76P/)

在实际的系统中，因为docker的运行需要root权限，但很多的系统不支持向第三方用户提供root权限（例如学校与商业的高性能计算平台）。因此，实际工作中更多的会用docker的无root权限版平替品podman。可以通过这个视频了解两者的区别[Docker vs Podman 两者的区别是什么？](https://www.bilibili.com/video/BV1YU4y1p7jG)。因为docker和podman的命令行是完全兼容的，因此可以先用docker学习，后期再用podman实际运行与实验。

### Anaconda安装

对于需要在CentOS 7中使用新版Python环境的同学，可以借助anaconda安装新Python环境。

- Anaconda可以使用国内镜像源（使用说明）：[Anaconda 软件仓库镜像使用帮助 - MirrorZ Help](https://mirror.nju.edu.cn/mirrorz-help/anaconda/?mirror=NJU)
- Anaconda的安装包（国内镜像）：[南京大学开源镜像站Anaconda3-2023.09-0-Linux-x86_64.sh](https://mirror.nju.edu.cn/anaconda/archive/Anaconda3-2023.09-0-Linux-x86_64.sh)
- Anaconda安装说明（官方文档）：https://docs.anaconda.com/free/anaconda/install/linux/，其中下载Anaconda安装包的步骤可以不从官方网站下载，而是从上面的国内镜像下载速度快。

### 使用Git进行代码版本管理

Git是目前使用广泛的一种管理大型软件项目代码版本的工具。当一个软件项目是由多人共同开发时，更加需要使用版本管理工具在多人直接协调。关于Git的介绍与基础使用，可以参考[“计算机教育中缺失的一课”](https://missing-semester-cn.github.io)中“版本控制（Git）”一节的内容。

## C/C++语言系列

### xmake构建系统

虽然CMake是C/C++语言事实上的软件构建系统，但CMake的语法以及编译依赖管理繁琐，对新手并不友好。在大创或毕业设计阶段，我们并不需要十分复杂的软件构建工具，因此目前推荐采用[xmake](https://github.com/xmake-io/xmake/blob/master/README_zh.md)作为C语言项目的构建工具。

xmake具有项目配置简单、依赖管理方便的特点，很容易就可以搭建起一个有效的C语言工程，并且支持VS Code等开发环境。

学习xmake可以阅读官方文档中的[“快速入门”部分](https://xmake.io/#/zh-cn/guide/installation)。

### C++编程规则（有争议，可改进）

为了避免在做大创或毕业设计时，被C++众多的内存问题以及各种构造函数陷阱所困扰而无法自拔、怀疑自我，在使用C++编写程序时，**尽量**遵守以下规则。如果实在没办法，可以找指导老师确认是否有必要使用高级特性：

1. 【指针】不要使用任何指针（包括智能指针等）。
2. 【数据容器】如有可能，全部用std::vector和std::map作为基础数据容器。
3. 【函数】不要将std::vector和std::map作为函数的返回值。
4. 【函数】函数参数不要使用指针，全部使用引用。
5. 【函数】当需要向函数传入或从函数中传出std::vector/std::map参数时，**务必使用引用**。
6. 【函数】函数的所有传入参数一律使用`const`修饰，所有传出参数不修饰。
7. 【类】只使用`struct`定义类，避免使用继承、多态、重载等面向对象特性。
8. 【类】所有基础类型（例如int, double等）的类成员变量，一定要显式给出一个默认值。
9. 【类】不要包含引用类型成员变量。
10. 【类】所有需要对一个类重载赋值运算符的场景，都转换成对应类的set成员函数调用；所有需要拷贝构造函数的地方，都转换为先创建一个默认初始化的对象，再调用set成员函数。
11. 【语言标准】采用C++11标准，可以使用`auto`关键字。

经验表明，对于大学生创新项目以及毕业设计，上述规则限制足够用了！

### 程序调试与性能分析

对于C/C++程序进行调试时，需要确保C/C++程序采用“调试模式”编译（即启用-g编译选项），以保证程序中的关键符号（例如变量名、函数名等）是被包含在可执行程序里。

关于调试和性能分析相关技术的介绍，可以参考[“计算机教育中缺失的一课”](https://missing-semester-cn.github.io)中“调试及性能分析”一节的内容。

## Java语言系列

部分研究项目（尤其是与分布式计算）需要使用到Java语言进行编程，根据需要学习Java语言的相关特性。

### Java语言基础

- 书籍教程：[《Java语言程序设计（基础篇）》](https://find.nuaa.edu.cn/#/searchList/bookDetails/209357)，在校内网中访问该页面后可以点击“电子馆藏”->“馆藏电子书”下载到扫描版书籍。
  - Java语言的基本编程概念（选择、循环等）与C/C++是相通的，可以触类旁通，学习时重点关注Java语言的语法特性即可。
  - Java语言的面向对象特性是它的一个特点，在实际编程中会经常用到。面向对象程序设计的基本概念与C/C++是一样的，但Java中的实现方法和语法特性与C++有较大区别，需要专门关注。
  - 学习建议：第1章-第13章，第17章（二进制IO）。JavaFX的内容可以跳过。
  - IDE建议：不要使用Netbeans，教材中是Eclipse，推荐使用IntelliJ IDEA Community Edition。**建议直接在Linux系统下编程。**
    - Windows版安装教程：[IntelliJ IDEA社区版下载安装及项目创建](https://www.bilibili.com/video/BV1Qr4y1F7rH)
    - Linux系统下操作类似。
- 视频教程：[黑马程序员Java零基础视频教程\_上部](https://www.bilibili.com/video/BV17F411T7Ao)

### Maven

[Maven](https://maven.apache.org)是管理Java程序工程的事实标准，在学习Java语言的同时需要学习Maven的使用。

- 官方教程：[Maven Getting Started Guide](https://maven.apache.org/guides/getting-started/index.html)
- 视频教程： [黑马程序员Maven全套教程，maven项目管理从基础到高级，Java项目开发必会管理工具maven](https://www.bilibili.com/video/BV1Ah411S7ZE)
  - 推荐内容：P1到P14（Maven基础）。
- [Apache Maven Assembly Plugin](https://maven.apache.org/plugins/maven-assembly-plugin/)：在利用Maven生成Jar包时，为了简化Jar包结构，通常会选择将一个工程的所有代码以及该工程所依赖的所有软件包，联合打包成一个fat jar（即带有所有依赖库的jar包），这个过程需要使用到Apache Maven Assembly Plugin。学习该插件的使用，掌握生成fat jar的方法。
  - [官方介绍](https://maven.apache.org/plugins/maven-assembly-plugin/index.html)
  - [官方文档](https://maven.apache.org/plugins/maven-assembly-plugin/usage.html)

### Java语言并行程序设计

对于涉及到并行计算的研究项目，有可能需要使用Java语言进行多线程并行编程。对于这部分知识的学习建议是：“根据项目需求驱动的学习模式”。当项目中需要用到一个特性时，去学习该特性的使用；如果在学习的过程中遇到了陌生的概念或不懂的知识，再去按图索骥的学习相关内容。

- 书籍教程：[《Java 9并发编程实战》](https://find.nuaa.edu.cn/#/searchList/bookDetails/239156)。在校园网中访问时，可以通过该页面的“馆藏电子书”链接下载扫描版书籍。
  - Java语言的多线程并行编程与操作系统中多线程并发的机制密切相关，许多基础概念（例如互斥锁等）是相通的。
  - 学习建议：第1章、第2章、第5章、第6章、第7章做基础了解，其他章节按需学习。
  - 书籍内容更详细、背景知识介绍更全面。
- 视频教程：[Dating Java8 系列视频](https://www.cnblogs.com/lingyejun/p/12130179.html)
  - 相关视频：E04-E06（Java流），E07（fork-join框架）。
  - 特点：实战向。

## 分布式计算

### 序列化与反序列化

序列和与反序列化是进程之间通信、交换对象的基本方式，其基本概念以及在互联网中的应用可以参看[《序列化和反序列化》](https://tech.meituan.com/2015/02/26/serialization-vs-deserialization.html)一文。

目前一个被广泛应用的跨编程语言的序列化框架是由Google开发的[Protocol Buffer](https://protobuf.dev/)。

- 请根据Protobuf提供的官方教程[《Protocol Buffer Basics: Java》](https://protobuf.dev/getting-started/javatutorial/)，学习如何使用Protobuf序列化一个对象到文件中，并从文件中将该对象反序列化出来。
- [Maven Protocol Buffers Plugin](https://www.xolstice.org/protobuf-maven-plugin/)：该插件可以让maven在编译Java工程时自动调用Protocol Buffer的相关工具链生成代码，替代了人工调用的麻烦。请学习[官方教程](https://www.xolstice.org/protobuf-maven-plugin/index.html)，使Maven工程可以自动编译Protocol Buffer定义文件。

### 远程过程调用框架gRPC

[gRPC](https://grpc.io/)是一个由Google开发的高性能远程过程调用框架。关于远程过程调用的概念，可以观看视频[《第1.3节：远程过程调用（Remote Procedure Call，RPC）》](https://www.bilibili.com/video/BV1LL411y7Xx)。请根据gRPC官方提供的以下教学，学习gRPC框架的基础使用：

- [Quick start](https://grpc.io/docs/languages/java/quickstart/)
- [Basics tutorial](https://grpc.io/docs/languages/java/basics/)

在自己的机器上尝试使用gRPC编写一个最简单的ping-pong程序。

## 图计算

如果研究工作涉及图计算，则可能需要掌握以下知识。

### 图数据库

通过阅读中文技术报告《人工智能之图数据库》，初步了解图数据库的基本概念与数据模型。

> [1] 清华大学人工智能研究院, 北京智源人工智能研究院, 清华—中国工程院知识智能联合研究中心. 人工智能之图数据库: 2020年第4期[R/OL]. AMiner, 2020[2023-08-01]. https://static.aminer.cn/misc/pdf/graphDB.pdf.

与图数据库相关概念的更宏观全景、更详细的解释可以参考下列综合调研论文：

> [2] BESTA M, GERSTENBERGER R, PETER E, 等. Demystifying Graph Databases: Analysis and Taxonomy of Data Organization, System Designs, and Graph Queries[J/OL]. ACM Computing Surveys, 2023, 56(2): 31:1-31:40. https://doi.org/10.1145/3604932.

参考书籍：《图数据库》（Neo4j数据库的介绍与使用），按需阅读。

> [3] IAN ROBINSON, JIM WEBBER, EMIL EIFREM. 图数据库[M]. 刘璐, 梁越, 译. 2 版. 北京: 人民邮电出版社, 2016.

## 大数据技术

### 大数据技术概览

了解大数据处理的概念以及基础知识。参考书籍：

> [1] 黄宜华主编. 深入理解大数据 : 大数据处理与编程实践[M]. 北京: 机械工业出版社, 2014.

- 第1章：大数据处理技术简介

### MapReduce编程模型

了解大数据处理的经典编程模型MapReduce的概念，及其执行流程。

参考书籍：

> [1] 黄宜华主编. 深入理解大数据 : 大数据处理与编程实践[M]. 北京: 机械工业出版社, 2014.

- 第4.1节：MapReduce基本编程模型和框架
- 第4.2节：Hadoop MapReduce基本构架与工作过程

### YARN资源调度框架

通过学习YARN资源调度框架，了解分布式环境中任务与资源调度的常见做法与流程。

参考书籍：

> [1] WHITE TOM. Hadoop权威指南 : 大数据的存储与分析[M]. 王海, 译. 北京:清华大学出版社, 2017.

- 第1章 初识Hadoop
- 第4章 关于YARN
