---
title: 'Review of "Set Similarity Joins on MapReduce: An Experimental Survey"'
date: 2018-10-24 21:30:00 +0800
categories: review 
---

* content
{:toc}

This blog is my review of [a recent experimental survey [1]](http://dl.acm.org/citation.cfm?doid=3231751.3242932) on distributed set similarity join algorithms.





## Summary

Many distributed algorithms for set similarity join (SSJ) have been proposed recently. They claim that they have achieved significant performance improvement over the previous methods. However, the comparisons presented in the existing work are incomplete, missing neither related competitors or datasets. There lacks a comprehensive comparison of the existing distributed SSJ algorithms to examine the progress that the research community has actually achieved these years.

In this paper, the authors systematically summarize the existing distributed SSJ algorithms under a unified notation system. They elaborate on the map and reduce phases in each algorithm and analyze the sizes of intermediate results theoretically. They evaluate the performance of 10 distributed SSJ algorithms comprehensively by conducting extensive experiments on 12 datasets (10 real-world + 2 synthetic). The evaluation reveals a severe defect of the existing algorithms. The algorithms cannot balance the workloads evenly among machines and an individual machine will become the straggler in execution. The defect is intrinsic that cannot be fixed by adding more machines. This finding inspires future research directions on the problem.

The authors review the recent literature on the distributed SSJ problem and pick 10 algorithms as evaluation subjects. The 10 algorithms all use sets (aka sparse binary vectors) as the input records and use Jaccard-like scores as the similarity measurement. The theoretic upper bounds of intermediate results of each algorithm are analyzed. To compare the algorithms fairly, the authors re-implement the algorithms with a common code base to eliminate the effects of code quality on performance. Twelve datasets (10 real-world + 2 synthetic) are used in the evaluation. The datasets come from the previous non-distributed experimental research and expose different characteristics in element universe and record lengths.

The authors first evaluate and compare the execution time of the algorithms on all the datasets with the similarity threshold ranging from 0.6 to 0.95. They present the quickest algorithm for each test case in Table 3 and counts the winning times for each algorithm. The results show that VJ [2] is the clear winner. It is the quickest algorithm in 45% of the test cases. GJ [3] and FS [4] are the second and third quickest algorithms. The robustness analysis further indicates that VJ [2] is also the most robust algorithm. Its execution time is at most 1.67 times larger than the quickest one among all the test cases. The second most robust algorithm is MG [5].

To justify the need for MapReduce in SSJ problem, the authors further evaluate the scalability of the algorithms. On data scalability, VJ [2], MJ [6] and MG [5] scale better when enlarging the datasets. On machine scalability, the execution time of most algorithms decreases as the number of reducers increases. However, they are all far from the near-linear scalability (up to 1.4x speedup with 2x reducers). VJ [2] and MJ [6] show a better machine scalability than the others. Under the 10Gbps network, the compression technique provided by Hadoop has little impacts on the performance as the bottleneck is the bandwidth of disks.

After getting the overview of all the algorithms, the authors further analyze the cluster utilization and data replication of each algorithm independently. They find the existing algorithms mainly have three defects:

1. **Unbalanced workload among groups/partitions**. Related algorithms are VJ, GJ, MG, MJ, FF, and VS. These algorithms are sensitive to long records and frequent tokens. These algorithms construct an inverted index for each token/signature and conduct join on the inverted indexes in parallel. The computation and space costs of processing an inverted index are usually quadratic to the length of the inverted index. The token frequency distributions in real-world datasets are highly skewed. It makes the sizes of the inverted indexes greatly vary and thus the workloads of different machines vary greatly. Moreover, the algorithms process a complete inverted index on a single machine. This design limits both the data and machine scalability. The memory of a single machine limits the maximal size of the inverted index that the algorithm can handle. As the sizes of the inverted indexes increase when the datasets grow larger, it further limits the data scalability of the algorithms. The machine that processes the longest inverted index is the slowest and becomes the straggler in the execution. Adding more machines cannot eliminate the straggler, thus it limits the machine scalability of the algorithms.
2. **High level of data replication**. Related algorithms are GJ, CJ, and MR. These algorithms are often sensitive to small thresholds. They replicate records either according to signatures or partitions. When the threshold is small, the level of replication is very high, making the algorithms inefficient.
3. **Large in-memory data structures**. Related algorithms are FS and V2. These algorithms need to load external data into memory to construct the utility data structures (Prefix list in FS and residual file in V2). The memory available in a single machine limits the data scalability of the algorithms.

The authors finally show their efforts on reproducing the previous results. They succeed in reproducing the results of VJ and S2 but fail in MJ and FS. They carefully discuss the potential reasons.

**Conclusion**: In this paper, the authors compare the 10 recent Hadoop-based SSJ algorithms in a fair environment. Contrary to the previous studies, the fastest algorithm is VJ with GJ and FS as the second and third fastest. None of the existing algorithms can scale to large datasets in the experiments. The authors analyze the existing algorithms one by one and find the most severe defect is workload balancing. The slowest machines become stragglers in execution because the existing algorithms fail to distribute the workloads related to frequent tokens/signatures evenly among multiple machines. The finding inspires the authors finding more efficient and balanced way to group and replicate intermediate data.

## Critique

I mainly have two critiques on the evaluation.

First, the datasets used in evaluation is small for distributed computation. The datasets that the authors use come from the evaluation of the serial SSJ algorithms. The datasets are all small. All of the datasets are less than 3Gbytes and have less than 10M records. Though the authors enlarge the datasets up to 10 times when evaluating the scalability, the maximal dataset is still less than 30Gbytes which can be stored totally in-memory by modern servers. The enlarged datasets may not expose the real characteristics of real-world large datasets like FriendSter and Twitter-mpi. Moreover, the authors only test the performance with a high threshold (0.95) on the 10x enlarged datasets. The experiments do not show the performance on large datasets with small thresholds.

Second, the evaluation lacks specialized analysis on threshold-dependent steps. In the evaluation, the authors focus on the execution time of the join phases in the algorithms. In some algorithms, the join phases contain MapReduce jobs to get the GTF (global token frequency) and reorder the tokens according to the GTF. These jobs are independent of similarity thresholds. In practice, users can conduct these threshold-independent jobs for each dataset only once and reuse the results of these jobs for many different thresholds. It is better to isolate the preprocessing time from the total join time during the evaluation. According to Figure 23, VJ and MG all spend non-trivial time on threshold-independent jobs. Removing them from the execution time may better reflect the advantages of MG over GJ and FS.

## Synthesis

To further improve the evaluation, I consider evaluating the RF-SetJoin algorithm [7]. RF-SetJoin is a distributed SSJ algorithm that builds upon both MapReduce and NoSQL database. It adopts the extended prefix filter technique which shows a strong filtering power. Though the network communication is larger than the prefix filter-based algorithms, the reduction in the number of candidates makes the time spent on verification much less. It has the potential to beat the VJ algorithm.

I also want to compare the algorithms on larger datasets (>1Gbytes and >1M records) and smaller thresholds (<0.5). Smaller thresholds may bring extra challenges to the existing algorithms. 

## References

[1] F. Fier, N. Augsten, P. Bouros, U. Leser, and J.-C. Freytag, “Set similarity joins on mapreduce: an experimental survey,” *Proc. VLDB Endow.*, vol. 11, no. 10, pp. 1110–1122, Jun. 2018.

[2] VernicaJoin: R. Vernica, M. J. Carey, and C. Li, “Efficient parallel set-similarity joins using MapReduce,” in *Proceedings of the 2010 international conference on Management of data - SIGMOD ’10*, 2010, p. 495.

[3] MRGroupJoin: D. Deng, G. Li, H. Wen, and J. Feng, “An efficient partition based method for exact set similarity joins,” *Proc. VLDB Endow.*, vol. 9, no. 4, pp. 360–371, Dec. 2015.

[4] FS-Join: C. Rong, C. Lin, Y. N. Silva, J. Wang, W. Lu, and X. Du, “Fast and Scalable Distributed Set Similarity Joins for Big Data Analytics,” in *2017 IEEE 33rd International Conference on Data Engineering (ICDE)*, 2017, pp. 1059–1070.

[5] MGJoin: C. Rong, W. Lu, X. Wang, X. Du, Y. Chen, and A. K. H. Tung, “Efficient and Scalable Processing of String Similarity Join,” *IEEE Trans. Knowl. Data Eng.*, vol. 25, no. 10, pp. 2217–2230, Oct. 2013.

[6] MassJoin: D. Deng, G. Li, S. Hao, J. Wang, and J. Feng, “MassJoin: A mapreduce-based method for scalable string similarity joins,” in *2014 IEEE 30th International Conference on Data Engineering*, 2014, pp. 340–351.

[7] RF-SetJoin: C. Kim and K. Shim, “Supporting set-valued joins in NoSQL using MapReduce,” *Inf. Syst.*, vol. 49, pp. 52–64, Apr. 2015.