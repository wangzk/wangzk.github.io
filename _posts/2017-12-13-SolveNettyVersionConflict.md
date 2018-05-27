---
title:  "Solve the Netty version conflict in a Hadoop + gRPC program"
date:   2017-12-13 11:48:00 +0800
categories: big data 
---

## Background

I try to use gRPC in a Hadoop application to make the mapper and the driver can communicate with each other.

However, I want to use the latest gRPC v1.8.0 along with the old Hadoop v2.7.2.

## Problem

gRPC v1.8.0 and Hadoop v2.7.2 rely on the conflicting Netty versions. 

The gRPC v1.8.0 is built with Netty v4.1.16.Final while the old Hadoop v2.7.2 is built with Netty v3.6.2.Final.

Hadoop can work with the new Netty v4.1.16.Final but gRPC cannot work with the old Netty v3.6.2.Final.

In a word, the problem is how to make Hadoop run my application with the new Netty version. 

## Solution

To make Hadoop run the application with the new Netty, the main idea is to package the new Netty in the application's jar and force Hadoop launching the application with the Netty provided in the jar.

The solution has two parts: Configure maven and configure Hadoop job.


### Maven configuration

Firstly, Package the Netty of the new version in the application's assembly jar.

**Step 1**: Use the shade plugin in maven to generate the assembly jar.

```xml
<!-- use maven shade plugin to generate the assembly jar -->
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-shade-plugin</artifactId>
    <version>1.5</version>
    <executions>
        <execution>
            <phase>package</phase>
            <goals>
                <goal>shade</goal>
            </goals>
            <configuration>
                <shadedArtifactAttached>true</shadedArtifactAttached>
                <shadedClassifierName>allinone</shadedClassifierName>
                <artifactSet>
                    <includes>
                        <include>*:*</include>
                    </includes>
                </artifactSet>
                <transformers>
                    <transformer implementation="org.apache.maven.plugins.shade.resource.AppendingTransformer">
                        <resource>reference.conf</resource>
                    </transformer>
                    <transformer implementation="org.apache.maven.plugins.shade.resource.ManifestResourceTransformer"></transformer>
                </transformers>
            </configuration>
        </execution>
    </executions>
</plugin>
 
```

**Step 2**: Avoid packaging Hadoop-related jars in the assembly jar by declaring the Hadoop dependency in the `provided` scope.

```xml
<dependency>
    <groupId>org.apache.hadoop</groupId>
    <artifactId>hadoop-client</artifactId>
    <version>2.7.2</version>
    <scope>provided</scope>
</dependency>
```

After the configuration, maven will not package Hadoop and its dependencies in the assembly jar. Only the new Netty depended by gRPC will be packaged into the assembly jar.


### Hadoop job configuration

Secondly, force Hadoop lauching the application with the new Netty packaged in the assembly jar.

Two configurations are needed:

1. Before launching the application with `hadoop jar`, set the environment variable on the driver side:

    ```bash
    export HADOOP_USE_CLIENT_CLASSLOADER=true
    ```

    By setting this environment variable, Hadoop will isolate the classpath of the user program from the hadoop system classpath. This will make the driver side use the new Netty in the assembly jar.

1. Set the following Hadoop configurations in the program (or you can modify the hadoop configuration file):

    ``` 
    mapreduce.job.user.classpath.first=true
    mapreduce.job.classloader=true
    ```

    This will make the user jar appear first in the classpath on the Mapper/Reducer side, thus the new Netty is used.

Finally, I can use gRPC with a new Netty version in my Hadoop application.
