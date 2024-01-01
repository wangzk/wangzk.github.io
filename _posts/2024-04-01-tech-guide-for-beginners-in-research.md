---
layout: article
title: "本科毕业设计/大学生创新训练计划技术指导"
date: 2024-01-01 16:00:00 +08:00
last_modified_at: 2024-01-01 16:30:00 +08:00
categories: tech
---

在进行本科毕业设计、大学生创新训练计划时，需要提前学习和掌握部分课堂中不会教、但对于后续研究工作开展非常必要的技术知识。目前包括Linux虚拟机安装、Docker容器安装与使用、Anaconda安装等。

<!--more-->

## Linux虚拟机安装

部分项目的后续实验需要在Linux开发服务器或学校的高性能计算平台上完成，目标操作系统均为Linux系统，因此需要熟悉Linux系统命令行的使用方式。如果本地电脑是Windows环境，需要安装Linux虚拟机。

为了适应学校的高性能计算平台的操作系统环境（CentOS 7），本地安装CentOS 7的虚拟机。

- Linux发行版：CentOS 7。安装光盘iso下载链接：[南京大学开源软件镜像站CentOS7安装光盘](https://mirror.nju.edu.cn/centos/7/isos/x86_64/CentOS-7-x86_64-DVD-2207-02.iso)。
- 虚拟机：使用VMWare或VirtualBox，安装指导视频：[如何使用VMware安装centos7_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1Kh4y1m767/)

## Docker容器安装与使用

在Linux虚拟机中，安装docker容器环境。部分软件（例如GraphScope）的安装与使用都在Docker环境中完成。

参考教程： [2小时搞定Docker 全程干货 基于CentOS7](https://www.bilibili.com/video/BV1vP4y1m76P/)

在实际的系统中，因为docker的运行需要root权限，但很多的系统不支持向第三方用户提供root权限（例如学校与商业的高性能计算平台）。因此，实际工作中更多的会用docker的无root权限版平替品podman。可以通过这个视频了解两者的区别[Docker vs Podman 两者的区别是什么？](https://www.bilibili.com/video/BV1YU4y1p7jG)。因为docker和podman的命令行是完全兼容的，因此可以先用docker学习，后期再用podman实际运行与实验。

## Anaconda安装

对于需要在CentOS 7中使用新版Python环境的同学，可以借助anaconda安装新Python环境。

- Anaconda可以使用国内镜像源（使用说明）：[Anaconda 软件仓库镜像使用帮助 - MirrorZ Help](https://mirror.nju.edu.cn/mirrorz-help/anaconda/?mirror=NJU)
- Anaconda的安装包（国内镜像）：[南京大学开源镜像站Anaconda3-2023.09-0-Linux-x86_64.sh](https://mirror.nju.edu.cn/anaconda/archive/Anaconda3-2023.09-0-Linux-x86_64.sh)
- Anaconda安装说明（官方文档）：https://docs.anaconda.com/free/anaconda/install/linux/，其中下载Anaconda安装包的步骤可以不从官方网站下载，而是从上面的国内镜像下载速度快。

