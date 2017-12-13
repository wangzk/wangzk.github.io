---
layout: post
title:  "Solve the Netty version conflict in a Hadoop + gRPC program"
date:   2017-12-13 11:48:00 +0800
categories: bigdata 
---

## Background

I use gRPC in a Hadoop application to make the mapper and the driver can communicate with each other.

However, I want to use a new gRPC version (1.8.0) with a old Hadoop version (2.7.2).

## Problem

gRPC and Hadoop relies on conflicting Netty versions. The new gRPC 1.8.0 is built on Netty 4.1.16.Final while the old Hadoop 2.7.2 is built on Netty 3.6.2.Final.

I need to use the newer Netty version to make the program work, but I cannot change the netty jar version in the Hadoop installation as the Hadoop environment is maintained by other guys.

## Solution
