---
title:  "Solve the Netty version conflict in a Hadoop + gRPC program"
date:   2017-12-13 11:48:00 +0800
categories: big data 
---

## Background

I use gRPC in a Hadoop application to make the mapper and the driver can communicate with each other.

However, I want to use the latest gRPC v1.8.0 along with an old Hadoop v2.7.2.

## Problem

gRPC and Hadoop rely on conflicting Netty versions. 

The gRPC v1.8.0 is built with Netty v4.1.16.Final while the old Hadoop v2.7.2 is built with Netty v3.6.2.Final.

Hadoop can work with Netty v4.1.16.Final but gRPC cannot work with Netty v3.6.2.Final.

In a word, the problem is to make the Hadoop application run with the new Netty version. 

## Solution

My solution is to make Hadoop application run with the new version Netty. To do so, I first package the new version Netty into my application's assembly jar and then force Hadoop use the new version Netty when launching my application.

My solution has two parts: Maven configuration and Hadoop job configuration.


### Maven configuration

I need to make sure that the Netty in the application's assembly jar is the new version.

**Step 1**: Add the shade plugin in pom.xml to generate the assembly jar.

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

**Step 2**: Avoid packaging Hadoop-related jars into the assembly jar by declaring the Hadoop dependency as in the `provided` scope.

```xml

<dependency>
    <groupId>org.apache.hadoop</groupId>
    <artifactId>hadoop-client</artifactId>
    <version>2.7.2</version>
    <scope>provided</scope>
</dependency>
```

When packaging the assembly jar, Hadoop and its dependencies will be ignored. Only the new Netty brought by gRPC will be packaged into the fat jar.


### Hadoop job configuration

Second, I need to make sure that Hadoop uses the new Netty packaged in the assembly jar when launching my application in Yarn.

Two configurations changes are needed:

1. Before launching the program with `hadoop jar`, set the environment variable:

    ```bash
    export HADOOP_USE_CLIENT_CLASSLOADER=true
    ```

    By setting this environment variable, Hadoop will isolate the classpath of the user program from the hadoop system classpath. This will make the client-side java program use the new Netty packaged in the assembly jar.

2. Set the Hadoop configuration in the program or in the configuration file:

    ``` 
    mapreduce.job.user.classpath.first=true
    mapreduce.job.classloader=true
    ```

    This will make the user jar appear first on the Mapper/Reducer side. The the program is launched, it will load the new Netty packaged in the assembly jar.


Finally, I can use gRPC with a new Netty version in my Hadoop application.
