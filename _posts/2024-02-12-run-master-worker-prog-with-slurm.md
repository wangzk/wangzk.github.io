---
title: "在Slurm中以Master和Worker模式运行自定义程序"
date: 2024-02-12 10:28:00 +08:00
categories: tech
---

超算集群采用的Slurm集群资源管理器默认是为MPI应用设计，但当需要以Master-Worker主从模式运行自定义的分布式计算程序时，需要利用一些技巧进行处理。本文提供了两个适用于主从模式的通用Slurm作业脚本，可以分别启动自定义的主节点程序与从节点程序。

该脚本由两个子脚本slurm-job-script.sh以及driver-script.py组成，其中slurm-job-script.sh是一个bash脚本，用于让Slurm管理器启动作业，driver-script.py是一个Python脚本，用于具体的启动分布式计算作业。

## 使用方法

将slurm-job-script.sh和driver-script.py两个脚本文件放到同一个目录下。

### slurm-job-script.sh脚本

脚本中需要自定义的部分包括：

1. `[]`包围的内容。
2. 第一部分的环境配置（包括载入其他module以及配置环境变量）。
3. 第二部分中NETWORK_INTERFACE变量对应的网络通信用网卡（例如指定网络通信通过Infiniband网卡进行）。

```bash
#!/bin/bash
#SBATCH --job-name=[作业名称]
#SBATCH -p [slurm调度队列名]
#SBATCH --error=log/%J.err
# 作业运行的标准错误输出将写到文件log/[JOB ID].err文件中
#SBATCH --output=log/%J.out
# 作业运行的标准输出将写到文件log/[JOB ID].out文件中
#SBATCH --time=[hh:mm:ss格式]
# 指定作业最大运行时间

#### 第一部分：环境配置（可选） ####
# 1. 使用module指令载入所需的软件环境 #
# 2. 配置其他必要的环境变量 #

#### 第二部分：获取主节点（即编号为0的slurm task）所在机器的网卡IP地址

NETWORK_INTERFACE=ib0
master_ip=$(srun --ntasks=1 --nodes=1 bash -c "ip -4 addr show $NETWORK_INTERFACE | grep -oP '(?<=inet ).*(?=/)'")
echo "The IP address of the master task is" $master_ip
random_port=$(($RANDOM + 10000))

#### 第二部分：执行具体的程序 ####
### 使用driver-script.py脚本来具体启动与运行程序，将主进程所在机器的IP地址、一个随机端口号作为启动脚本的参数
srun python3 driver-script.py $master_ip $random_port
```

### driver-script.py脚本

该脚本用于具体的启动主节点和从节点的程序。脚本中需要自定义的是第二部分，需要通过os.system函数或subprocess.run函数启动具体的计算程序。在脚本中，可以使用预先获取好的若干关键变量辅助程序启动：

1. master_ip，主节点的IP地址（字符串类型）。
2. master_port，主节点上随机生成的一个端口号（int类型）。
3. proc_id，当前进程的编号（从0~N-1连续编号）。
4. num_proc，整个计算作业所启动的总进程数。

```python
import os
import sys
import subprocess
import time

## 第一部分：获得关键变量（本部分代码不要修改）
# 主进程所在机器的IP地址
master_ip = sys.argv[1]
# 主进程用于监听的一个随机端口号
master_port = int(sys.argv[2])
# 当前进程编号
proc_id = int(os.environ["SLURM_PROCID"])
# 本次计算参与的总进程数
num_proc = int(os.environ["SLURM_NTASKS"])

## 第二部分：启动计算所业（需要修改）

if proc_id == 0:
    # 启动主进程
    print("Start the master process...")
    # 通过os.system函数或subprocess.run函数调用其他程序，启动主进程(修改这里)
    os.system("uname -a")
    print("The main process finishes.")
else:
    # 启动从进程
    time.sleep(1)  # 等待1s，等待主进程启动
    print("Start the worker process {}...".format(proc_id))
    # 通过os.system函数或subprocess.run函数调用其他程序，启动从进程(修改这里)
    os.system("uname -a")
    print("The worker process {} finishes.".format(proc_id))
```
