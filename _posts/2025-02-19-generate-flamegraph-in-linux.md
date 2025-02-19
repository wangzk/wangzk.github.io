---
title: '在Linux下生成程序性能分析火焰图'
date: 2025-02-19 18:16:00 +08:00
categories: linux
---

本博文简单记录如何在 Linux下 生成程序性能分析的火焰图（Flame Graph），用于分析
程序执行的性能瓶颈。

相关软件：
- 火焰图生成工具 [FlameGraph](https://github.com/brendangregg/FlameGraph)
- 性能分析工具[perf: Linux profiling with performance counters](https://perfwiki.github.io/main/)

## 准备可执行程序

因为perf工具依赖程序中的栈信息分析性能瓶颈，因此在编译C/C++程序时建议开启调试
编译选项 `-g` 并关闭栈帧指针优化 `-fno-omit-frame-pointer`。

例如：

```
$ gcc -g -fno-omit-frame-pointer hello.c
```

## 设置用户进行性能分析的权限

如果需要以*普通用户*的身份利用perf进行性能分析，需要以root权限调整 /proc/sys/kernel/perf_event_paranoid
的设置。

**注意：该操作有安全风险**

```
切换到root
$ sudo su
开启与普通性能分析相关的权限
# echo 0 > /proc/sys/kernel/perf_event_paranoid
```

## 使用perf工具进行性能采样

通过perf命令启动程序，获得程序性能采样的Profile信息。

```
$ perf record -F 100 -g --call-graph dwarf 可执行程序 [程序运行参数]
```

该命令将会以100Hz的频率进行性能采样，并使用dwarf工具获得程序栈帧信息，为生成火焰图
做准备。

性能采样的结果将输出在当前目录下的perf.data文件中。

## 将pref采样结果转换为Firefox Profiler工具的格式

在当前目录下（即perf.data文件存在的目录下），执行下面的命令，将性能分析结果利用
Firefox Profiler工具打开。

```
$ perf script report gecko
```

该命令执行后将在默认浏览器中打开Firefox Profiler页面，在该页面中可以观察程序运行
过程中的性能火焰图，找出性能瓶颈所在之处。





