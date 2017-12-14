---
layout: post
title:  "Solve the Netty version conflict in a Hadoop + gRPC program"
date:   2017-12-13 11:48:00 +0800
categories: bigdata 
---

## Background

I use gRPC in a Hadoop application to make the mapper and the driver can communicate with each other.

However, I want to use the latest gRPC version (1.8.0) along with a old Hadoop version (2.7.2).

## Problem

gRPC and Hadoop relies on conflicting Netty versions. 

The gRPC 1.8.0 is built on Netty 4.1.16.Final while the old Hadoop 2.7.2 is built on Netty 3.6.2.Final.

Hadoop can work with Netty 4.1.16.Final but gRPC cannot work with Netty 3.6.2.Final.

In a word, the problem is to make my Hadoop application run with the new Netty version. 

## Solution

My solution has two parts: Maven configuration and Hadoop job configuration.

### Maven configuration

First of all, I need to make sure that the Netty in the application's fat jar is the new version.

However, the default behaviour of Maven dependency version conflict resolving follows a nearest wins strategy. It does not guarantee using the latest version in the fat jar. Saurabh jainMore explain the details in [this post](http://techidiocy.com/maven-dependency-version-conflict-problem-and-resolution/). He gives a simple solution (solution 2) in the post. The user can tell Maven to use the specific version when resolving version conflicts by adding the following section in the pom file:

```xml
    <!-- solve jar version conflicts -->
    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>com.google.guava</groupId>
                <artifactId>guava</artifactId>
                <version>19.0</version>
            </dependency>
        </dependencies>
    </dependencyManagement>
```

Users can use the Maven enforcer plugin to check the version conflicts by adding the following code in the build section of the pom file:

```xml
<plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-enforcer-plugin</artifactId>
                <version>1.4.1</version>
                <executions>
                    <execution>
                        <id>enforce</id>
                        <goals>
                            <goal>enforce</goal>
                        </goals>
                        <configuration>
                            <rules>
                                <requireUpperBoundDeps/>
                            </rules>
                        </configuration>
                    </execution>
                </executions>
</plugin>
```

It will check the dependency tree with Upper Bound dependency rule.

This section tells Maven use Guava 19.0 when in the final fat jar.

In my case, I can avoid adding Hadoop-related jars into my fat package by declaring the Hadoop dependency in the `provided` scope.

```xml
<dependency>
    <groupId>org.apache.hadoop</groupId>
    <artifactId>hadoop-client</artifactId>
    <version>2.7.2</version>
    <scope>provided</scope>
</dependency>
```

When packaging the fat jar, Hadoop and its dependencies will be ignored. Only the new Netty brought by gRPC will be packaged into the fat jar.


### Hadoop job configuration
