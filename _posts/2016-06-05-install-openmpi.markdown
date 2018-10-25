---
layout: post
title:  "Brief Guide on Installing OpenMPI from Source Code"
date:   2016-06-05 11:11:00 +0800
categories: linux mpi
---

A brief guide on installing OpenMPI from source code.

## Download OpenMPI source code

Download the Open MPI release with the suffix `.tar.gz` from Open MPI's [Download page](https://www.open-mpi.org/software/ompi/v1.10/).

As far as the guide is written, the current stable release is [openmpi-1.10.2.tar.gz](https://www.open-mpi.org/software/ompi/v1.10/downloads/openmpi-1.10.2.tar.gz).

## Compile OpenMPI

1. Uncompress the source code tar package. You may need to change the version part in `openmpi-1.10.2` to the version you have downloaded just now.

        $ tar xvzf openmpi-1.10.2.tar.gz
        $ cd openmpi-1.10.2
    
2. Compile Open MPI from source code.

        # use flag --enable-static to enable .a file for Open MPI library
        $ ./configure --prefix=/absolute/path/to/install --enable-static
        $ make
3. Install Open MPI.
    
        $ make install

4. Modify shell environment variables. We need to add the following environment variables to the shell environment setup script (`/etc/profile` for global install and `~/.bashrc` for local install):
    
        export OMPI=/absolute/path/to/install
        export PATH=$PATH:$OMPI/bin
        export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$OMPI/bin

5. Copy all files of `/absolute/path/to/install` and `/etc/profile` or `~/.bashrc` to every node in the cluster.

6. Done!
