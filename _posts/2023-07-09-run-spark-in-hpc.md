---
title: '在超算（HPC）集群中运行Spark作业'
date: 2023-07-09 18:00:00 +08:00
categories: linux
---

高性能计算（HPC）中经常需要使用到超算集群。超算集群多采用[Slurm](https://slurm.schedmd.com/sbatch.html)作为集群资源管理器，对用户提交的计算作业（job）统筹分配计算节点并在远程节点上启动计算进程。
但Spark官方仅支持Standalone、YARN、Mesos、K8s等部署方式，其不适应HPC集群中基于Slurm的以作业为单位的管理方式。

为了在HPC环境下利用大数据软件栈，劳伦斯利物浦国家实验室（LLNL）开发的[Magpie项目](https://github.com/LLNL/magpie)提供了在HPC环境下通过Slurm、Moab等集群管理器运行大数据系统的脚本。
Magpie项目的官方文档精确而简洁，适合对HPC环境很了解的专业用户阅读与使用，但对于初学者上手有难度。
本教程的目标是面向初学者介绍如何利用Magpie项目在HPC环境中启动和运行Spark作业。

## 基本原理

Magpie项目的脚本主要完成以下几个功能：

1. 提供Slurm等管理框架支持的作业执行脚本，向Slurm申请计算节点。
2. 当Slurm分配完计算节点后，脚本利用Slurm提供的环境变量、srun命令整理集群动态分配的节点列表，并根据节点列表生成大数据系统的配置文件目录（例如Hadoop配置文件、Spark集群的masters、workers以及其他的配置文件）。
3. 对大数据系统的集群启动脚本打补丁，使其支持HPC环境和自定义配置文件目录。
4. 借助大数据系统原有的启动脚本，在HPC分配的计算节点上启动相应的进程。
5. 对大数据系统作业进程进行监控，当进程退出时，通知Slurm系统结束相关的计算作业。

## 安装步骤

### 安装前检查

1. HPC集群的$HOME目录是挂载的网络文件系统目录，在集群的所有节点上可以以相同的路径访问。
2. HPC集群可以连接互联网，如果不能联网则需要手动下载安装包并上传到集群的特定目录下。

### 大数据系统安装

1. 将[Magpie项目](https://github.com/LLNL/magpie)的源代码clone到集群的登录节点上，或从Github的主页下载源代码zip文件，并在集群登录节点上解压。将Magpie源代码解压后的根目录记为MAGPIE_HOME。
2. 关于利用Magpie运行Spark作业的文档是`MAGPIE_HOME/doc/README.spark`，技术细节可查询该文档。
3. 如果集群登录节点可以连接互联网：
   1. 按以下要求修改MAGPIE_HOME/misc/magpie-download-and-setup.sh脚本。
   2. 将脚本开头的SPARK_DOWNLOAD设置为"Y"。
   3. 修改INSTALL_PATH为你期望安装的目录，将该目录记为`INSTALL_PATH`。
   4. 如果是通过module load的方式加载的Java环境，更新JAVA_DEFAULT_PATH环境变量，并取消注释。
   5. 检查SPARK_PACKAGE的版本，确保该版本被Magpie所支持（检查Magpie项目[README文件](https://github.com/LLNL/magpie)中Suppported Packages & Versions部分），而且可以从[TUNA的Apache Spark镜像源](https://mirrors.tuna.tsinghua.edu.cn/apache/spark/)下载。截止文档更新时，可支持版本是3.3.2。
   6. 修改SPARK_HADOOP_PACKAGE的版本，变更为当前[TUNA的Apache Hadoop镜像源](https://mirrors.tuna.tsinghua.edu.cn/apache/hadoop/common/)可以提供的，并且和对应Spark版本兼容的版本。截止文档更新时，可用版本是hadoop-3.2.3。
   7. 修改APACHE_DOWNLOAD_BASE变量为TUNA的Apache镜像地址，国内下载速度更快：`APACHE_DOWNLOAD_BASE="https://mirrors.tuna.tsinghua.edu.cn/apache"`。
   8. 修改`__download_apache_package ()`函数中`DOWNLOAD_URL=${APACHE_DOWNLOAD_BASE}/${package}`，这样直接从特定镜像源下载软件包。
   9. 保存脚本并退出。
4. 如果集群的登录节点不能连接互联网：
   1. 重复上面可以联网的步骤修改MAGPIE_HOME/misc/magpie-download-and-setup.sh脚本。
   2. 修改`__download_apache_package ()`函数，不再调用wget来下载软件包，而是提前下载好Spark和Hadoop的压缩包，并将压缩包放置在`INSTALL_PATH/PACKAGE_BASENAME位置（例如`INSTALL_PATH/spark-3.3.2-bin-hadoop3.tgz`和`$INSTALL_PATH/hadoop-3.2.3.tar.gz`）。
5. 在MAGPIE_HOME目录下运行misc/magpie-download-and-setup.sh脚本，该脚本会自动解压缩Spark和Hadoop的安装包并对启动脚本打补丁。

### Spark作业运行

假设集群的作业通过sbatch命令提交，而且sbatch内支持srun命令。

Magpie项目提供的Spark作业运行脚本路径在`MAGPIE_HOME/submission-scripts/script-sbatch-srun/magpie.sbatch-srun-spark`（不使用HDFS）。

在实际运行自己的作业之前，需要将该脚本拷贝出来一份，放到自己喜欢的目录下，后文假设脚本文件是run.sh。

使用文本编辑器编辑run.sh文件，留意和修改以下中文注释的地方：

```bash
#!/bin/sh
#############################################################################
#  Copyright (C) 2013-2015 Lawrence Livermore National Security, LLC.
#  Produced at Lawrence Livermore National Laboratory (cf, DISCLAIMER).
#  Written by Albert Chu <chu11@llnl.gov>
#  LLNL-CODE-644248
#
#  This file is part of Magpie, scripts for running Hadoop on
#  traditional HPC systems.  For details, see https://github.com/llnl/magpie.
#
#  Magpie is free software; you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  Magpie is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Magpie.  If not, see <http://www.gnu.org/licenses/>.
#############################################################################

############################################################################
# SLURM Customizations
############################################################################

# Node count.  Node count should include one node for the
# head/management/master node.  For example, if you want 8 compute
# nodes to process data, specify 9 nodes below.
#
# If including Zookeeper, include expected Zookeeper nodes.  For
# example, if you want 8 Hadoop compute nodes and 3 Zookeeper nodes,
# specify 12 nodes (1 master, 8 Hadoop, 3 Zookeeper)
#
# Also take into account additional nodes needed for other services.
#
# Many of the below can be configured on the command line.  If you are
# more comfortable specifying these on the command line, feel free to
# delete the customizations below.

### 修改位置，设置使用的节点数量<my_node_count>（即master + worker总节点数量，如果是2个worker,则这里设置为3）
#SBATCH --nodes=<my_node_count>
### 修改位置：输出日志文件路径
#SBATCH --output="slurm-%j.out"
#SBATCH --error="slurm-%j.err"

### 修改位置：作业的最长执行时间（分钟）
# Note defaults of MAGPIE_STARTUP_TIME & MAGPIE_SHUTDOWN_TIME, this
# timelimit should be a fair amount larger than them combined.
#SBATCH --time=<my_time_in_minutes>

### 修改位置：作业名称，需人工设置
# Job name.  This will be used in naming directories for the job.
#SBATCH --job-name=<my_job_name>

### 修改位置：调度分区名，需人工设置
# Partition to launch job in
#SBATCH --partition=<my_partition>

## SLURM Values
# Generally speaking, don't touch the following, misc other configuration

#SBATCH --ntasks-per-node=1
#SBATCH --exclusive
#SBATCH --no-kill

# Need to tell Magpie how you are submitting this job
export MAGPIE_SUBMISSION_TYPE="sbatchsrun"


############################################################################
# Magpie Configurations
############################################################################

# Directory your launching scripts/files are stored
#
# Normally an NFS mount, someplace magpie can be reached on all nodes.
# 修改位置：改为Magpie项目的安装目录的路径MAGPIE_HOME
export MAGPIE_SCRIPTS_HOME="${HOME}/magpie"

# 修改位置：存储本地数据的位置（适用于允许写入/tmp或其他本地目录的场景。如果不提供/tmp写入的支持，则阅读 magpie/doc/README.no-local-dir的说明，打开相应的补丁，具体操作见后面的说明。）
# If your cluster does not have any node-local storage available (or
# an extremely small amount of it) for small config files, log files,
# and other temporary scratch space, set the following to yes and see
# the README for patching requirements to projects.
#
# This option applies to all LOCAL_DIR environment variables, such as
# MAGPIE_LOCAL_DIR, HADOOP_LOCAL_DIR, HBASE_LOCAL_DIR, etc.
#
# Defaults to no.
#
export MAGPIE_NO_LOCAL_DIR="yes"

# Path to store data local to each cluster node, typically something
# in /tmp.  This will store local conf files and log files for your
# job.  If local scratch space is not available, consider using the
# MAGPIE_NO_LOCAL_DIR option.  See README for more details.
# 这里应该已经变成在template中设置的本地工作目录
export MAGPIE_LOCAL_DIR="/public3/home/scb9801/performance-bottleneck-analysis-for-subgraph-matching-based-aggregation/spark_install/local_dir/magpie"

# Magpie job type
#
# "spark" - Run a job according to the settings of SPARK_JOB.
#
# "testall" - Run a job that runs all basic sanity tests for all
#             software that is configured to be setup.  This is a good
#             way to sanity check that everything has been setup
#             correctly and the way you like.
#
#             For Spark, testall will run sparkpi
#
# "script" - Run arbitraty script, as specified by MAGPIE_JOB_SCRIPT.
#            You can find example job scripts in examples/.
#
# "interactive" - manually interact with job run to submit jobs,
#                 peruse data (e.g. HDFS), move data, etc.  See job
#                 output for instructions to access your job
#                 allocation.
#
# "setuponly" - do not launch any daemons or services, only setup
#               configuration files.  Useful for debugging or
#               development.
# 修改位置：推荐interactive，手动启动spark作业与停止作业。如果需要自动化运行脚本，则选择script，需进一步阅读script模式的说明
export MAGPIE_JOB_TYPE="interactive"

# Specify script and arguments to execute for "script" mode in
# MAGPIE_JOB_TYPE
#
# export MAGPIE_JOB_SCRIPT="${HOME}/my-job-script"

# Specify script startup / shutdown time window
#
# Specifies the amount of time to give startup / shutdown activities a
# chance to succeed before Magpie will give up (or in the case of
# shutdown, when the resource manager/scheduler may kill the running
# job).  Defaults to 30 minutes for startup, 30 minutes for shutdown.
#
# The startup time in particular may need to be increased if you have
# a large amount of data.  As an example, HDFS may need to spend a
# significant amount of time determine all of the blocks in HDFS
# before leaving safemode.
#
# The stop time in particular may need to be increased if you have a
# large amount of cleanup to be done.  HDFS will save its NameSpace
# before shutting down.  Hbase will do a compaction before shutting
# down.
#
# The startup & shutdown window must together be smaller than the
# timelimit specified for the job.
#
# MAGPIE_STARTUP_TIME and MAGPIE_SHUTDOWN_TIME at minimum must be 5
# minutes.  If MAGPIE_POST_JOB_RUN is specified below,
# MAGPIE_SHUTDOWN_TIME must be at minimum 10 minutes.
#
# export MAGPIE_STARTUP_TIME=30
# export MAGPIE_SHUTDOWN_TIME=30

# Magpie One Time Run
#
# Normally, Magpie assumes that when a user runs a job, data created
# and stored within that job will be desired to be accessed again.  For
# example, data created and stored within HDFS will be accessed again.
#
# Under a number of scenarios, this may not be desired.  For example
# during testing.
#
# To improve useability and performance, setting MAGPIE_ONE_TIME_RUN
# below to yes will have two effects on the Magpie job.
#
# 1) A number of data paths (such as for HDFS) will be put into unique
#    paths for this job.  Therefore, no other job should be able to
#    access the data again.  This is particularly useful if you wish
#    to run performance tests with this job script over and over
#    again.
#
#    Magpie will not remove data that was written, so be sure to clean up
#    your directories later.
#
# 2) In order to improve job throughout, Magpie will take shortcuts by
#    not properly tearing down the job.  As data corruption should not be
#    a concern on job teardown, the job can complete more quickly.
#
# export MAGPIE_ONE_TIME_RUN=yes

# Convenience Scripts
#
# Specify script to be executed to before / after your job.  It is run
# on all nodes.
#
# Typically the pre-job script is used to set something up or get
# debugging info.  It can also be used to determine if system
# conditions meet the expectations of your job.  The primary job
# running script (magpie-run) will not be executed if the
# MAGPIE_PRE_JOB_RUN exits with a non-zero exit code.
#
# The post-job script is typically used for cleaning up something or
# gathering info (such as logs) for post-debugging/analysis.  If it is
# set, MAGPIE_SHUTDOWN_TIME above must be > 5.
#
# See example magpie-example-pre-job-script and
# magpie-example-post-job-script for ideas of what you can do w/ these
# scripts
#
# Multiple scripts can be specified separated by comma.  Arguments can
# be passed to scripts as well.
#
# A number of convenient scripts are available in the
# ${MAGPIE_SCRIPTS_HOME}/scripts directory.
#
# export MAGPIE_PRE_JOB_RUN="${MAGPIE_SCRIPTS_HOME}/scripts/pre-job-run-scripts/my-pre-job-script"
# export MAGPIE_POST_JOB_RUN="${MAGPIE_SCRIPTS_HOME}/scripts/post-job-run-scripts/my-post-job-script"
#
# Similar to the MAGPIE_PRE_JOB_RUN and MAGPIE_POST_JOB_RUN, scripts can be
# run after the stack is setup but prior to the script or interactive mode
# begins. This enables frontends and other processes that depend on the stack
# to be started up and torn down. In similar fashion the cleanup will be done
# immediately after the script or interactive mode exits before the stack is
# shutdown.
#
# export MAGPIE_PRE_EXECUTE_RUN="${MAGPIE_SCRIPTS_HOME}/scripts/pre-job-run-scripts/my-pre-job-script"
# export MAGPIE_POST_EXECUTE_RUN="${MAGPIE_SCRIPTS_HOME}/scripts/post-job-run-scripts/my-post-job-script"

# Environment Variable Script
#
# When working with Magpie interactively by logging into the master
# node of your job allocation, many environment variables may need to
# be set.  For example, environment variables for config file
# directories (e.g. HADOOP_CONF_DIR, HBASE_CONF_DIR, etc.) and home
# directories (e.g. HADOOP_HOME, HBASE_HOME, etc.) and more general
# environment variables (e.g. JAVA_HOME) may need to be set before you
# begin interacting with your big data setup.
#
# The standard job output from Magpie provides instructions on all the
# environment variables typically needed to interact with your job.
# However, this can be tedious if done by hand.
#
# If the environment variable specified below is set, Magpie will
# create the file and put into it every environment variable that
# would be useful when running your job interactively.  That way, it
# can be sourced easily if you will be running your job interactively.
# It can also be loaded or used by other job scripts.
#
# export MAGPIE_ENVIRONMENT_VARIABLE_SCRIPT="${HOME}/my-job-env"

# Environment Variable Shell Type
#
# Magpie outputs environment variables in help output and
# MAGPIE_ENVIRONMENT_VARIABLE_SCRIPT based on your SHELL environment
# variable.
#
# If you would like to output in a different shell type (perhaps you
# have programmed scripts in a different shell), specify that shell
# here.
#
# export MAGPIE_ENVIRONMENT_VARIABLE_SCRIPT_SHELL="/bin/bash"

# 修改位置：需要根据集群的情况进行调整。如果运行报错，则分别尝试将MAGPIE_HOSTNAME_CMD增加参数-s或-f。
# Hostname config
#
# Magpie internally assumes that the nodenames provided by the
# scheduler/resource manager are the addresses that should be used for
# configuration AND they are identical to the output of the `hostname`
# command, which is used by Magpie to determine what nodes individual
# services should run on.
#
# If this is not true in your environment, you can provide an alternate
# hostname command below to correct this.  Very often, users may need to
# set:
#
# MAGPIE_HOSTNAME_CMD="hostname -s" // use short hostname
# or
# MAGPIE_HOSTNAME_CMD="hostname -f" // use FQDN
#
# If you have a more complex situation, see README.hostname for more
# advanced options.
#
export MAGPIE_HOSTNAME_CMD="hostname -f"

# Remote Shell
#
# Magpie requires a passwordless remote shell command to launch
# necessary daemons across your job allocation.  Magpie defaults to
# ssh, but it may be an alternate command in some environments.  An
# alternate ssh-equivalent remote command can be specified by setting
# MAGPIE_REMOTE_CMD below.
#
# If using ssh, Magpie requires keys to be setup ahead of time so it
# can be executed without passwords.
#
# Specify options to the remote shell command if necessary.
#
# export MAGPIE_REMOTE_CMD="ssh"
# export MAGPIE_REMOTE_CMD_OPTS=""

############################################################################
# General Configuration
############################################################################

# 修改位置：如果是通过module load的机制使用java,则需要在此增加命令module load加载java环境并配置相应的JAVA_HOME
# Necessary for most projects
module load java/1.8.0_221-public3
export JAVA_HOME="/public3/soft/java/1.8.0_221"

# 修改位置：如果是通过module load的机制使用python,则需要在此增加命令module load加载python环境并配置相应的MAGPIE_PYTHON即可
# MAGPIE_PYTHON path used for:
# - Spark PySpark path
# - Launching tensorflow tasks
module load anaconda/3-Python3.7.4-fenggl-public3
export MAGPIE_PYTHON="/public3/soft/anaconda/anaconda3/bin/python3"

############################################################################
# Spark Core Configurations
############################################################################

# Should Spark be run
#
# Specify yes or no.  Defaults to no.
#
export SPARK_SETUP=yes

# Set Spark Setup Type
#
# Will inform scripts on how to setup config files and what daemons to
# launch/setup.
#
# STANDALONE - Launch Spark stand alone scheduler
# YARN - do not setup stand alone scheduler, use Yarn scheduler
#
# For most users, the stand alone scheduler is likely preferred.
# Resources do not need to be competed for in a Magpie environment
# (you the user have all the resources allocated via the
# scheduler/resource manager of your cluster).
#
# However, portability and integration with other services may require
# Spark to work with Yarn instead.  If SPARK_SETUP_TYPE is set to
# YARN:
#
# - The Spark standalone scheduler will not be launched
# - The default Spark master will be set to 'yarn-client' (Spark 1.X)
#   or 'yarn' (Spark [2-3].X) in all appropriate locations
#   (e.g. spark-defaults.conf)
# - All situations that would otherwise use the standalone scheduler
#   (e.g. SPARK_JOB="sparkpi") will now use Yarn instead.
#
# Make sure that HADOOP_SETUP_TYPE is set to MR or YARN for the
# SPARK_SETUP_TYPE="YARN".
#
export SPARK_SETUP_TYPE="STANDALONE"

# Version
#
export SPARK_VERSION="3.3.2-bin-hadoop3"

# 修改位置：需要修改成安装的具体的SPARK_HOME
# Path to your Spark build/binaries
#
# This should be accessible on all nodes in your allocation. Typically
# this is in an NFS mount.
#
# Ensure the build matches the Hadoop/HDFS version this will run against.
#
export SPARK_HOME="${HOME}/spark-${SPARK_VERSION}"

# Path to store data local to each cluster node, typically something
# in /tmp.  This will store local conf files and log files for your
# job.  If local scratch space is not available, consider using the
# MAGPIE_NO_LOCAL_DIR option.  See README for more details.
#
export SPARK_LOCAL_DIR="/public3/home/scb9801/performance-bottleneck-analysis-for-subgraph-matching-based-aggregation/spark_install/local_dir/spark"

# 修改位置：如果不需要设置conf文件目录，则不调整
# Directory where alternate Spark configuration templates are stored
#
# If you wish to tweak the configuration files used by Magpie, set
# SPARK_CONF_FILES below, copy configuration templates from
# $MAGPIE_SCRIPTS_HOME/conf/spark into SPARK_CONF_FILES, and modify as
# you desire.  Magpie will still use configuration files in
# $MAGPIE_SCRIPTS_HOME/conf/spark if any of the files it needs are not
# found in SPARK_CONF_FILES.
#
# export SPARK_CONF_FILES="${HOME}/myconf"

# 修改位置：默认使用CPU核数，如果也可以手动调整
# Worker Cores per Node
#
# If not specified, a reasonable estimate will be calculated based on
# number of CPUs on the system.
#
# Be aware of the number of tasks and the amount of memory that may be
# needed by other software.
#
# export SPARK_WORKER_CORES_PER_NODE=8

# 修改位置：指定每个Worker使用的内存容量（MB）
# Worker Memory
#
# Specified in M.  If not specified, a reasonable estimate will be
# calculated based on total memory available and number of CPUs on the
# system.
#
# Be aware of the number of tasks and the amount of memory that may be
# needed by other software.
#
export SPARK_WORKER_MEMORY_PER_NODE=225280

# Worker Directory
#
# Directory to run applications in, which will include both logs and
# scratch space for local jars.  If not specified, defaults to
# SPARK_LOCAL_DIR/work.
#
# Generally speaking, this is best if this is a tmp directory such as
# in /tmp
#
# export SPARK_WORKER_DIRECTORY=/public3/home/scb9801/performance-bottleneck-analysis-for-subgraph-matching-based-aggregation/spark_install/local_dir/spark/work

# SPARK_JOB_MEMORY
#
# Memory for spark jobs.  Defaults to being set equal to
# SPARK_WORKER_MEMORY_PER_NODE, but users may wish to lower it if
# multiple Spark jobs will be submitted at the same time.
#
# In Spark parlance, this will set both the executor and driver memory
# for Spark.
#
# export SPARK_JOB_MEMORY="2048"

# 修改位置：根据情况可以调整大一些Driver的内存
# SPARK_DRIVER_MEMORY
#
# Beginning in Spark 1.0, driver memory could be configured separately
# from executor memory.  If SPARK_DRIVER_MEMORY is set below, driver
# memory will be configured differently than the executor memory
# indicated above with SPARK_JOB_MEMORY.
#
# If running Spark < 1.0, this option does nothing.
#
export SPARK_DRIVER_MEMORY="225280"

# Daemon Heap Max
#
# Heap maximum for Spark daemons, specified in megs.
#
# If not specified, defaults to 1000
#
# May need to be increased if you are scaling large, get OutofMemory
# errors, or perhaps have a lot of cores on a node.
#
# export SPARK_DAEMON_HEAP_MAX=2000

# Environment Extra
#
# Specify extra environment information that should be passed into
# Spark.  This file will simply be appended into the spark-env.sh.
#
# By default, a reasonable estimate for max user processes and open
# file descriptors will be calculated and put into spark-env.sh.
# However, it's always possible they may need to be set
# differently. Everyone's cluster/situation can be slightly different.
#
# See the example example-environment-extra for examples on
# what you can/should do with adding extra environment settings.
#
# export SPARK_ENVIRONMENT_EXTRA_PATH="${HOME}/spark-my-environment"

############################################################################
# Spark Job/Run Configurations
############################################################################

# Set spark job for MAGPIE_JOB_TYPE = spark
#
# "sparkpi" - run sparkpi example. Useful for making sure things are
#             setup the way you like.
#
#             There are additional configuration options for this
#             example listed below.
#
# "sparkwordcount" - run wordcount example.  Useful for making sure
#                    things are setup the way you like.
#
#                    See below for additional required configuration
#                    for this example.
#
export SPARK_JOB="sparkpi"

# 修改位置：根据情况按需要调整
# SPARK_DEFAULT_PARALLELISM
#
# Default number of tasks to use across the cluster for distributed
# shuffle operations (groupByKey, reduceByKey, etc) when not set by
# user.
#
# For Spark versions < 1.3.0.  Defaults to number compute nodes
# (i.e. 1 per node) This is something you (the user) almost definitely
# want to set as this is non-optimal for most jobs.
#
# For Spark versions >= 1.3.0, will not be set by Magpie if the below
# is commented out.  Internally, Spark defaults this to the largest
# number of partitions in a parent RDD.  Or for operations without a
# parent, defaults to nodes X cores.
#
# export SPARK_DEFAULT_PARALLELISM=8

# SPARK_MEMORY_FRACTION
#
# Fraction of heap space used for execution and storage. The lower
# this is, the more frequently spills and cached data eviction occur.
#
# This configuration only works for Spark versions >= 1.6.0.  See
# SPARK_STORAGE_MEMORY_FRACTION and SPARK_SHUFFLE_MEMORY_FRACTION for
# older versions.
#
# Defaults to 0.6
#
# export SPARK_MEMORY_FRACTION=0.6

# SPARK_MEMORY_STORAGE_FRACTION
#
# Amount of storage memory immune to eviction, expressed as a fraction
# of the size of the region set aside by SPARK_MEMORY_FRACTION.  The
# higher this is, the less working memory may be available to
# executiona nd tasks may spill to disk more often.
#
# This configuration only works for Spark versions >= 1.6.0.  See
# SPARK_STORAGE_MEMORY_FRACTION and SPARK_SHUFFLE_MEMORY_FRACTION for
# older versions.
#
# Defaults to 0.5
#
# export SPARK_MEMORY_STORAGE_FRACTION=0.5

# SPARK_STORAGE_MEMORY_FRACTION
#
# Configure fraction of Java heap to use for Spark's memory cache.
# This should not be larger than the "old" generation of objects in
# the JVM.  This can highly affect performance due to interruption due
# to JVM garbage collection.  If a large amount of time is spent in
# garbage collection, consider shrinking this value, such as to 0.5 or
# 0.4.
#
# This configuration only works for Spark versions < 1.6.0.  Starting
# with 1.6.0, see SPARK_MEMORY_FRACTION and
# SPARK_MEMORY_STORAGE_FRACTION.
#
# Defaults to 0.6
#
# export SPARK_STORAGE_MEMORY_FRACTION=0.6

# SPARK_SHUFFLE_MEMORY_FRACTION
#
# Fraction of Java heap to use for aggregation and cogroups during
# shuffles.  At any given time, the collective size of all in-memory
# maps used for shuffles is bounded by this limit, beyond which the
# contents will begin to spill to disk.  If spills are often, consider
# increasing this value at the expense of storage memory fraction
# (SPARK_STORAGE_MEMORY_FRACTION above).
#
# This configuration only works for Spark versions < 1.6.0.  Starting
# with 1.6.0, see SPARK_MEMORY_FRACTION and
# SPARK_MEMORY_STORAGE_FRACTION.
#
# Defaults to 0.2
#
# export SPARK_SHUFFLE_MEMORY_FRACTION=0.2

# SPARK_RDD_COMPRESS
#
# Should RDD's be compressed by default?  Defaults to true.  In HPC
# environments with parallel file systems or local storage, the cost
# of compressing / decompressing RDDs is likely a be a net win over
# writing data to a parallel file system or using up the limited
# amount of local storage space available.  However, for some users
# this cost may not be worthwhile and should be disabled.
#
# Note that only serialized RDDs are compressed, such as with storage
# level MEMORY_ONLY_SER or MEMORY_AND_DISK_SER.  All python RDDs are
# serialized by default.
#
# Defaults to true.
#
# export SPARK_RDD_COMPRESS=true

# SPARK_IO_COMPRESSION_CODEC
#
# Defaults to lz4, can specify snappy, lz4, lzf, snappy, or zstd
#
# export SPARK_IO_COMPRESSION_CODEC=lz4

# SPARK_DEPLOY_SPREADOUT
#
# Per Spark documentation, "Whether the standalone cluster manager
# should spread applications out across nodes or try to consolidate
# them onto as few nodes as possible. Spreading out is usually better
# for data locality in HDFS, but consolidating is more efficient for
# compute-intensive workloads."
#
# If you are hard coding parallelism in certain parts of your
# application because those individual actions do not scale well, it
# may be beneficial to disable this.
#
# Defaults to true
#
# export SPARK_DEPLOY_SPREADOUT=true

# 修改设置：需要根据情况改成本地目录或者是共享目录（例如${SPARK_LOCAL_DIR}/scratch）
# SPARK_LOCAL_SCRATCH_DIR
#
# By default, if Hadoop is setup with a file system, the Spark local
# scratch directory, where scratch data is placed, will automatically
# be calculated and configured.  If Hadoop is not setup, the following
# must be specified.
#
# If you have local SSDs or NVRAM stored on the nodes of your system,
# it may be in your interest to set this to a local drive.  It can
# improve performance of both shuffling and disk based RDD
# persistence.  If you want to specify multiple paths (such as
# multiple drives), make them comma separated
# (e.g. /dir1,/dir2,/dir3).
#
# Note that this field will not work if SPARK_SETUP_TYPE="YARN".
# Please set HADOOP_LOCALSTORE to inform Yarn to set a local SSD for
# Yarn to use for local scratch.
#
export SPARK_LOCAL_SCRATCH_DIR="${SPARK_LOCAL_DIR}/scratch"

# 修改设置：推荐设置为yes
# SPARK_LOCAL_SCRATCH_DIR_CLEAR
#
# After your job has completed, if SPARK_LOCAL_SCRATCH_DIR_CLEAR is
# set to yes, Magpie will do a rm -rf on all directories in
# SPARK_LOCAL_SCRATCH_DIR.  This is particularly useful if the local
# scratch directory is on local storage and you want to clean up your
# work before the next user uses the node.
#
export SPARK_LOCAL_SCRATCH_DIR_CLEAR="yes"

# SPARK_NETWORK_TIMEOUT
#
# This will configure many network timeout configurations within
# Spark.  If you see that your jobs are regularly failing with timeout
# issues, try increasing this value.  On large HPC systems, timeouts
# may occur more often, such as on loaded parallel file systems or
# busy networks.
#
# As of this version, this will configure:
#
# spark.network.timeout
# spark.files.fetchTimeout
# spark.rpc.askTimeout
# spark.rpc.lookupTimeout
# spark.core.connection.ack.wait.timeout
# spark.shuffle.registration.timeout
# spark.network.auth.rpcTimeout
# spark.shuffle.sasl.timeout
#
# Note that some of this fields will only effect newer spark versions.
#
# Specified in seconds, by default 120.
#
# export SPARK_NETWORK_TIMEOUT=120

# SPARK_YARN_STAGING_DIR
#
# By default, Spark w/ Yarn will use your home directory for staging
# files for a job.  This home directory must be accessible by all
# nodes.
#
# This may pose a problem if you are not using HDFS and your home
# directory is not NFS or network mounted.  Set this value to a
# network location as your staging directory.  Be sure to prefix this
# path the appropriate scheme, such as file://.
#
# This option is only available beginning in Spark 2.0.
#
# export SPARK_YARN_STAGING_DIR="file:///lustre/${USER}/sparkStaging/"

############################################################################
# Spark SparkPi Configuration
############################################################################

# SparkPi Slices
#
# Number of "slices" to parallelize in Pi estimation.  Generally
# speaking, more should lead to more accurate estimates.
#
# If not specified, equals number of nodes.
#
# export SPARK_SPARKPI_SLICES=4

############################################################################
# Spark SparkWordCount Configuration
############################################################################

# SparkWordCount File
#
# Specify the file to do the word count on.  Specify the scheme, such
# as hdfs://, alluxio:// or file://, appropriately.
#
# export SPARK_SPARKWORDCOUNT_FILE="file:///path/mywordcountfile"

# SparkWordCount Copy In File
#
# In some cases, a file must be copied in before it can be used.  Most
# notably, this can be the case if the file is not yet in HDFS or Alluxio.
#
# If specified below, the file will be copied to the location
# specified by SPARK_SPARKWORDCOUNT_FILE before the word count is
# executed.
#
# Specify the scheme appropriately.  At this moment, the schemes of
# file://, alluxio://, and hdfs:// are recognized for this option.
#
# Note that this is not required.  The file could be copied in any
# number of other ways, such as through a previous job or through a
# script specified via MAGPIE_PRE_JOB_RUN.
#
# export SPARK_SPARKWORDCOUNT_COPY_IN_FILE="file:///mywordcountinfile"

############################################################################
# Run Job
############################################################################

srun --no-kill -W 0 $MAGPIE_SCRIPTS_HOME/magpie-check-inputs
if [ $? -ne 0 ]
then
    exit 1
fi
srun --no-kill -W 0 $MAGPIE_SCRIPTS_HOME/magpie-setup-core
if [ $? -ne 0 ]
then
    exit 1
fi
srun --no-kill -W 0 $MAGPIE_SCRIPTS_HOME/magpie-setup-projects
if [ $? -ne 0 ]
then
    exit 1
fi
srun --no-kill -W 0 $MAGPIE_SCRIPTS_HOME/magpie-setup-post
if [ $? -ne 0 ]
then
    exit 1
fi
srun --no-kill -W 0 $MAGPIE_SCRIPTS_HOME/magpie-pre-run
if [ $? -ne 0 ]
then
    exit 1
fi
srun --no-kill -W 0 $MAGPIE_SCRIPTS_HOME/magpie-run
srun --no-kill -W 0 $MAGPIE_SCRIPTS_HOME/magpie-cleanup
srun --no-kill -W 0 $MAGPIE_SCRIPTS_HOME/magpie-post-run
```

### 应用No Local Dir的patch

如果HPC集群不支持向/tmp目录写入大量文件，则需要启用Magpie脚本的no-local-dir的机制。
打Patch的原理参见[README文档说明](https://github.com/LLNL/magpie/blob/master/doc/README)。
如何启用no-local-dir的说明见[README.no-local-dir文档](https://github.com/LLNL/magpie/blob/master/doc/README.no-local-dir)。

1. cd $SPARK_HOME。 进入SPARK的安装目录
2. patch -p1 < ../../magpie-master/patches/spark/spark-3.3.2-bin-hadoop3-alternate.patch。注意Spark版本号跟着改变。如果提示已经patch过，则选择y，重新应用patch。
3. patch -p1 < MAGPIE_HOME/patches/spark/spark-3.3.2-bin-hadoop3-no-local-dir.patch。注意Spark版本号跟着改变。如果提示已经patch过，则选择y，重新应用patch。 
4. cd MAGPIE_HOME/submission-scripts/script-templates。
5. 编辑Makefile文件，将其中的MAGPIE_NO_LOCAL_DIR设置为'y'；修改LOCAL_DIR_PREFIX指向本地文件系统路径。
6. make。

### 使用自定义Python环境

如果想使PySpark不使用系统标准的Python环境，而是使用第三方环境（例如通过module load加载的Anaconda），需要修改Spark的配置目录，使其使用自定义的Python解释器。

1. 修改MAGPIE_HOME/conf/spark/spark-env-2.X.sh和MAGPIE_HOME/conf/spark/spark-env-1.X.sh脚本，在最后的export PYSPARK_PYTHON前面增加对应的module load命令，并修改PYSPARK_PYTHON为对应的python解释器路径。