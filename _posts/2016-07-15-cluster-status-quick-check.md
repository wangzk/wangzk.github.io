---
layout: post
title:  "Quick Check Cluster Status"
date:   2016-07-15 20:00:00 +0800
categories: linux 
---

## Description
Sometimes we need to quickly check the cluster status to make sure that the cluster is OK to run a task. Therefore I wrote a shell script to do the quick check. The script will check the free memory, load and file system performance of every node in the cluster. 

## Prerequests
1. The program `pssh` is installed. `pssh` is a tool to conduct parallel ssh tasks.
2. SSH passwordless login is properly configured.
3. Prepare a text file with cluster node IPs/hostnames. One node per line.

## Shell script
Suppose that the script file is named `check_cluster_status.sh`.

```bash
#!/bin/bash
SLAVE_FILE=$1
run_on_every_node() {
pssh -t $1 -h $SLAVE_FILE -i $2
echo "---> Master:"
bash -c "$2"
}
echo "======== FREE MEMORY =========="
run_on_every_node 2 'free -h | grep +'
echo "======== CHECK LOAD ==========="
run_on_every_node 10 ' top -bn3 | egrep "Cpu|load" | tail -n2'
#~/pssh-2.3.1/bin/pssh -p 1 -t 3 -h node_list -i "free -h | grep +"
echo "======== CHECK SEQUENTIAL DISK WRITE ========="
run_on_every_node 60 'dd if=/dev/zero of=speedtest bs=512M count=4 oflag=direct'
echo "======== CHECK SEQUENTIAL DISK READ ========="
run_on_every_node 60 'dd if=speedtest of=/dev/null bs=512M count=4'
run_on_every_node 10 'rm speedtest'
```

## Usage
Under the shell promote, run the script as:

```bash
$ bash check_cluster_status.sh path-to-node-file
```

The script will check the status of the current node running the script and nodes listed in the node file.

## Output Explain
The output of the script will be diveided into four parts:
1. Free Memory;
2. Load;
3. Sequential disk write;
4. Sequential disk read.

### Free Memory
In the following output, the node `slave002` uses 3.1G memory and has 59G free memory.

```
======== FREE MEMORY ==========
[1] 20:28:05 [SUCCESS] slave002
-/+ buffers/cache:       3.1G        59G
...
```

### Load
In the following output, the system load avg over the last 1, 5 and 15 minutes of `slave007` is 0.15, 0.09, 0.07. The user CPU usage of the last few seconds is 0.1%. 

```
======== CHECK LOAD ===========
[1] 20:28:12 [SUCCESS] slave007
top - 20:24:15 up 41 days, 10:23,  0 users,  load average: 0.15, 0.09, 0.07
%Cpu(s):  0.1 us,  0.1 sy,  0.0 ni, 97.3 id,  2.5 wa,  0.0 hi,  0.0 si,  0.0 st
```

### Disk Performance
In the following output, the sequential write and read performance of `slave007` are 215MB/s and 228MB/s respectively.

```
======== CHECK SEQUENTIAL DISK WRITE =========
[1] 20:28:29 [SUCCESS] slave007
Stderr: 4+0 records in
4+0 records out
2147483648 bytes (2.1 GB) copied, 9.9958 s, 215 MB/s
...
======== CHECK SEQUENTIAL DISK READ =========
[1] 20:28:51 [SUCCESS] slave007
Stderr: 4+0 records in
4+0 records out
2147483648 bytes (2.1 GB) copied, 9.43487 s, 228 MB/s
[2] 20:28:51 [SUCCESS] slave011
```