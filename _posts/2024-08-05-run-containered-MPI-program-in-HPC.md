---
layout: article
title: "Run Containered MPI Program in HPC with Slurm and Apptainer"
date: 2024-08-05 09:00:00 +08:00
last_modified_at: 2024-8-5 09:00:00 +08:00
categories: tech
---

This blog is inspired by the blog post [*A New Approach to MPI in Apptainer*](https://ciq.com/blog/a-new-approach-to-mpi-in-apptainer/) written by Dave Godlove from [CIQ, Inc.](https://ciq.com/). This blog post provides a simple and straightforward introduction to the method proposed by Dave Godlove.

## Background


The traditional way of running MPI programs in the HPC environment faces the challenges of complex compiling dependences. The users have to recompile their programs from source code in the HPC environment. This process is time-consuming and error-prone. The compiler version may be too old. The HPC environment may lacks the required third-party libraries. The third-party library version provided by the OS may be imcompatible with the program. The users have to compile and install the third-party libraries manually one by one. New problems may arise during the compilation of third-party libraries.

[Apptainer](https://apptainer.org/) (formerly [Singularity](https://docs.sylabs.io/guides/3.5/user-guide/introduction.html)) provides a lightweight and portable container platform especially optimized for the HPC environment. Compared with other container platforms like Docker and Podman, Apptainer is rootless, does not need any daemon process, mounts the home directory by default, and exposes the host network and hardware devices to the containers. With the help of Apptainer, we can compile the programs in the local environment and packs the environment as a container image. The container image can be run in the HPC environment without any modification.

Apptainer natively provides [two methods to run containered MPI programs in HPC](https://apptainer.org/docs/user/1.0/mpi.html): the hybrid way and the bind way. However, the two methods require the same MPI version installed inside and outside the container. Sometimes, it is difficult to install the other MPI versions in the HPC environment. Dave Godlove provides a new method to run containered MPI programs in HPC with the help of Slurm.


## Prerequisites

1. The HPC environment use Slurm as the job scheduler and Slurm is compiled with PMI support for MPI.
   
    To check whether your HPC environment meets the requirement, you can run the following command:
    ```{bash}
    $ srun --mpi=list
    ```

    The output should contain `pmi2`:

    ```{bash}
    srun: MPI types are...
    srun: none
    srun: openmpi
    srun: pmi2
    ```
2. Install the MPI library with PMI support inside the Apptainer container image. (It is usually enabled by default in popular Linux distros like Debian).

## Workflow

1. Compile the program in the local environment and package the environment as a Apptainer container image (usually a `.sif` image file).
2. Upload the image file to the HPC environment.
3. Submit the MPI job to the HPC environment with the following commands.

   - Method 1: Run with `srun` directly

      ```{bash}
      $ srun --mpi=pmi2 <Resource Allocation Options> apptainer exec <Path to the Apptainer image file> <Path to MPI program inside the container> [Program arguments...]
      ```

      This command will use slurm to start up and manage MPI processes. The slurm will interactive with the processes of the MPI program inside the containers with the PMI2 interface. The MPI processes inside the container will communicate with each other directly. If you use singularity, you can replace `apptainer` with `singularity` in the previous command.

      For example, support we want to run eight processes with two processes per node , we can execute the following command: 

      ```
      $ srun --mpi=pmi2 --ntasks=8 --ntasks-per-node=2 apptainer exec exp_env.sif ./mpi_program [other arguments...]
      ```
  
   - Method2: Run with `sbatch`

     Inside the slurm script, run the MPI program with the `srun` command. A demo slurm script is shown below:

     ```{bash}
     #!/bin/bash
     #SBATCH --job-name=test_par
     #SBATCH -p amd_256
     #SBATCH --error=log/%J.err
     #SBATCH --output=log/%J.out
     # Remember to start the MPI program with srun 
     srun --mpi=pmi2 singularity exec ./expenv20240804.sif ./MPIProgramPath [other arguments...]
     ```

    The `srun` command will start up and manage MPI processes based on the resources allocated for the job.

## What Happened Behind?

The MPI library starts a MPI job with the help of two components:

- Process Manager: Start processes on remote nodes and manage the processes. When we run MPI with `mpirun`, the process manager is provided by the MPI library.  However, in this method, we use slurm as the process manager in MPI to start up and monitor the MPI processes. Therefore, we need to start the MPI job with the `srun` command.
- Communication: The actual communication is handled by the MPI library linked to the program. In this method, the communication is conducted by the MPI library *inside the container*. All the programs are executed inside the container.

The traditional way to start a MPI job is

```
User (mpirun) -> Process Manager -> Rank1
                                 | [System MPI]
                                 -> Rank2
                                 | [System MPI]
                                 -> Rank3
                                 | [System MPI]
                                 -> ...
```

All MPI ranks are run in the OS environment in HPC.

With the method proposed in this blog:

```
User (srun) -> Slurm -> [Container1: Rank1]
                     | [MPI in container]
                     -> [Container2: Rank2]
                     | [MPI in container]
                     -> [Container3: Rank3]
                     | [MPI in container]
                     -> ...
```

### Drawbacks

Due to all programs are run inside the container, the communication between processes contain overheads. The experimental results below show that the bandwidth between two processes ia about 50% lower than the native MPI.

With the apptainer (`srun -np 2 singularity exec ./debian_sid_202408.sif ./osu_bibw`):

```
# OSU MPI Bi-Directional Bandwidth Test v7.4
# Datatype: MPI_CHAR.
# Size      Bandwidth (MB/s)
1                       3.90
2                       8.06
4                      16.13
8                      32.02
16                     64.93
32                    129.97
64                    256.00
128                   302.41
256                   578.48
512                   881.49
1024                 1721.00
2048                 2281.93
4096                 3217.77
8192                 4037.09
16384                5880.22
32768                7714.31
65536                8306.49
131072               9636.22
262144              10280.08
524288              10832.43
1048576             11003.63
2097152             11095.36
4194304             11212.31
```

With the system native MPI library (`mpirun -np 2 ./osu_bibw`):

```
# OSU MPI Bi-Directional Bandwidth Test v7.4
# Datatype: MPI_CHAR.
# Size      Bandwidth (MB/s)
1                      12.08
2                      23.40
4                      48.47
8                      90.66
16                    186.53
32                    345.68
64                    674.01
128                   883.64
256                  1725.95
512                  3028.14
1024                 5173.77
2048                 8234.39
4096                12702.55
8192                18792.05
16384               12307.55
32768               18643.63
65536               22044.42
131072              22781.26
262144              24458.06
524288              24810.75
1048576             24688.00
2097152             24879.01
4194304             24697.29
```
