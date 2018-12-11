---
title:  "Popularity Survey of Graph Processing Frameworks"
date:   2018-12-11 16:21:00 +0800
categories: graph-processing-systems
---

* content
{:toc}

Recently, a survey [^1] comprehensivelly summarizes the existing graph processing frameworks. It reviews the techniques of the frameworks, but it lacks a popularity survey. Which is the most popular or influencial framework among all of them?. In this blog, I want to add more data on the popularity perspective of the existing graph processing frameworks.



## Popularity Definition

There are many kinds of definitions on popularity. In this survey, I mainly concern on **citation popularity**. The citation popularity of a graph processing framework is defined as the number of citations of the related paper on Google Scholar.

As the older papers tend to have more citations than the newer paper, I also provide the **normalized citation popularity**, i.e. dividing the number of citations by the age of the framework. The age of the framework is defined as the pasted years since the publication of the related paper. A framework published in 2018 has the age of 1.

## Results

I use the citation notation provided in [^1]. The following table is based on the Table 3 in [^1].

The data was collected on Dec. 11, 2018.

| Year | System                                    | Citation Count      | Normalized Citation Count |
| ---- | ----------------------------------------- | ------------------- | ------------------------- |
| 2009 | PEGASUS (Kang et al. 2009)                | 736                 |                           |
| 2010 | Pregel (Malewics et al. 2010)             | 3135                |                           |
| 2010 | Signal/Collect (Stutz et al. 2010)        |                     |
| 2010 | Surfur (Chen et al. 2010)                 | 93                  |
| 2010 | JPregel (Prakasam and Chandrasekhar 2010) | NA (no publication) |                           |
| 2010 | GraphLab (Low et al. 2010)                | 907                 |
| 2010 | Piccolo (Power and Li 2010)               | 231                 |
| 2011 | GoldenOrb (Cao 2011)                      | NA (no publication) |                           |
| 2011 | GBase (Kang et al. 2011                   | 112                 |                           |


[^1]: Heidari, S., Simmhan, Y., Calheiros, R. N., & Buyya, R. (2018). Scalable Graph Processing Frameworks: A Taxonomy and Open Challenges. ACM Computing Surveys, 51(3), 1–53. https://doi.org/10.1145/3199523.