---
title: '英文论文翻译指导'
date: 2024-01-01 09:51:00 +08:00
categories: teaching
---

在将一篇英文论文翻译成中文时，需要注意专业术语的使用、规范的书面语写作，以及格式与排版问题。同时给出翻译过程中常见问题的对策。

<!--more-->

## 英文论文翻译的过程和注意重点

在确定好需要翻译的英文论文之后，就可以开始对经典的英文论文进行翻译了。翻译英文论文的过程，也是学习如下内容的过程：

1. 毕业论文题目所涉及的背景知识与专业术语。（专业术语不能搞错，这是体现毕业论文工作专业度的地方。）
2. 论文结构。（所翻译的论文均是毕业设计涉及领域的经典文献，其论文结构和表达经过相关领域专家的思考与打磨。通过翻译经典范文，可以学习到一篇论文的写作结构与说理方式。）翻译论文过程中请留意以下内容，体会论文是如何通过行文逻辑来表达科学观点，在毕业论文中借鉴相关的写作技巧与思路：
    - 论文的章节划分与章节之间的关系。
    - 章节内每个段落的主旨句，以及段落之间的逻辑关系。
3. 正规书面语的论文写作。在翻译过程中请尤其注意以下几点：
    - 请使用严肃正式的书面语来翻译文献，避免口语化表达。
    - 对于英文的长句、多重嵌套从句，请手动拆分成多个中文短句来表达；中文中较少使用嵌套的从句。
    - 相关科学术语的翻译。对于专业的英文术语，在该术语第一次出现的地方，以“术语翻译（英文原文）”的形式标出，这样读者就知道你对该术语的翻译，例如“子图匹配（subgraph matching）”。如果不确定一个英文术语该怎样翻译比较合适，可以借助[CNKI翻译助手](https://dict.cnki.net)进行专业术语的翻译选择。
4. 格式与排版。（在翻译论文的过程中，学习如何正确地使用LaTeX或Word版排出规范、好看的论文。）关于格式与排版，有以下的注意事项。
    - 可以使用LaTeX或Word，优先推荐LaTeX。
    - 如果使用LaTeX，推荐用XeLaTeX配合xeCJK使用，任意文档模板均可。
    - 如果使用Word，则请使用提供的模板“英文论文翻译模板.docx”出发，请将该模板文件下载到本地，在本地的WPS/Word中进行编辑。使用Word编辑的过程中，请注意以下注意事项。
        1. 请使用Word/WPS提供的“样式”功能规范所有的排版格式。模板中的样式已经全部设置好了，请不要修改。如果不清楚什么是“样式”，请看在线视频（[【Word小技巧】1 标题样式，排版时永远的捷径_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1W84y1F7YD) ）。模板中已经对图、表、正文、标题排版的要求进行了解释。建议在模板的基础上进行修改。
        2. 所有的正文选择“正文”样式，论文的大标题（1级标题）选择“标题1”，论文的节标题（2级标题）选择“标题2”，论文的小节标题（3级标题）选择“标题3”。(5)公式请使用Word/WPS自带的公式，不用MathType。
        3. 从外部向Word文档中粘贴时，图像和文字请分别粘贴。
            - 从外部向Word文档中粘贴文字时，请选择"只粘贴文本”方式（“粘贴” -> “只粘贴/保留文本”，或右键菜单里粘贴选项下的“只粘贴/保留文本”）。
            - 从外部向Word文档中粘贴图片时，请选择“粘贴” -> “选择性粘贴”，然后选择“图片（PNG格式图片）”或“位图”。
    - 论文的插图和插表请按照模板中的范例格式整理。

为了保证翻译质量过关，请先试翻译论文的摘要和第一节的前5个段落，将试翻译好的论文通过邮件发给导师审阅。通过第一轮反馈之后，根据反馈意见，继续完成论文第一节（Introduction）的翻译工作，再邮件发给我审阅。再根据审阅意见，完成论文后续所有内容的翻译。全文翻译完毕后，请通过邮件发送给我审阅、修改，最终定稿。

## 英文论文翻译中的常见问题与对策

**Q：英文翻译成中文的原则是？逐句翻译还是以流畅为主？**

英文论文翻译在保持原意不变的情况下，应优先尊重汉语的写作习惯，因此以流畅为先。不需要严格遵循英语的语序和分局。即根据汉语的习惯，可以将一句长英文句拆分成多个短中文句，对于英语中常用的倒装句应该恢复成汉语的语序。

**Q：英文中经常出现修饰语（从句、to短语）倒装在名词后面（修饰指的是描述前面名词的细节），在翻译成中文时需要恢复。**

英文原文：Recently there emerge many distributed algorithms that aim at solving subgraph matching at scale.

错误翻译：近期出现许多分布式算法以解决大规模子图匹配问题。(翻译时修饰词倒装了）

更好的翻译：近期出现了许多面向大规模子图匹配的分布式算法。（修饰词提前）

**Q：如果一个从句主要用于描述前面做法的效果，该从句应该单独拆出来，并通过“以”来描述这样做的效果。**

英文原文：We want to provide eﬃcient mechanisms to ensure correctness and completeness (to be deﬁned shortly) of range selection queries.（注意这里的to表示mechanism所能达到的效果）

错误的翻译：我们为了保证范围选择查询的正确性和完备性，提出了高效的机制。

更好的翻译：我们提出了一组高效的新机制，以保证范围选择查询的正确性和完备性。

**Q：英语中的倒装成分（例如从句、分句）在翻译成中文时，应该恢复成正常的语序（中文习惯修饰词在前，名词在后），或者将从句拆分成单独一句话（中文中较少使用单独的、无主语的从句）。**

英文原文：Existing algorithm-level comparisons failed to provide a systematic view of distributed subgraph matching mainly due to the intertwining of strategy and optimization.

错误翻译：现有的算法水平比较未能提供关于分布式子图匹配的系统观点，主要是由于策略和优化的相互交织。

更好的翻译：由于算法策略与优化交织在一起，导致现有关注分布式子图匹配算法的比较性研究工作不能提供一个系统性的视点。

**Q：英语中需要较长的修饰成分（从句、括号里的话）在翻译的过程中可以拆分成若干中文短句，这样表述更清晰。**

英文原文：We speciﬁcally do not address queries that involve data aggregation (exempliﬁed by arithmetic operations, such as SUM or AVERAGE) which usually return a single value as the answer to the posed query.（注意本文中有一个长的从句、一个长的括号里的话）

更好的翻译：我们的研究不涉及聚集（aggregation）查询，例如带有算术计算的求和（SUM）和平均（AVERAGE）查询，这类查询通常只返回单个值作为查询结果。（注意句子被拆分成了若干短句）

**Q：正文中第一次出现的专有名词、特殊的翻译词汇，应该在翻译时在括号中标出英文原文。**

英文原文：In the Outsourced Database (ODB) Model, a third-party database service provider oﬀers adequate software, hardware and network resources to host its clients’ databases as well as mechanisms to eﬃciently create, update and access outsourced data.

更好的翻译：在外包数据库（outsourced database，ODB）模式中，第三方数据库服务提供商提供足够的软件、硬件和网络资源来托管其客户的数据库，并提供高效创建、更新和访问外包数据的机制。

**Q：英文原文中斜体、加粗的字词，在翻译的文章中应该以加粗表示。**

**Q: 论文中插图应该放多大比较合适？**

插图中字体的常见大小（即大部分文字的字号）与正文字号相当或略小。