## SOAPdenoovo 简介
SOAPdenovo是一个适用于组装短reads的方法，能组装出类似人类基因组大小的de novo草图。

该软件特地设计用来组装Illumina GA short reads，新的版本减少了在图创建时的内存消耗，解决了contig组装时的重复区域的问题，增加了scaffold组装时的覆盖度和长度，改进了gap closing，更加适用于大型基因组组装。

（SOAPdenovo是为了组装大型植物和动物基因组而设计的，同样也适用于组装细菌和真菌，组装大型基因组大小如人类时，可能需要150G内存。）
## 1.配置文件
一般大型基因组组装项目都会有多个文库，配置文件包含文库的位置信息 以及 其他信息。

配置文件包含 全局信息 和 多个文库部分信息。

全局信息：max_rd_len：任何比它大的read会被切到这个长度。

文库部分由[LIB]开始，并包含如下信息：

**avg_ins**  
文库的平均插入长度，或者是插入长度分布图的峰值。（理论上插入片段长度是成正态分布的，并不是严格控制的） 

**reverse_seq**  
这个选项有 0 或 1 两个选项，它告诉组装器read序列是否需要被完全反转。Illumima GA 产生两种 paired-end文库：一是forward-reverse；另一个是 reverse-forward。"reverse_seq"参数应该如下设置：0，forward-reverse（由典型的插入长度少于500bp的DNA末端片段生成）；1，reverse-forward（由环状文库，典型的2 kb以上的文库生成）。  
序列是否需要被反转，目前的测序技术，插入片段大于等于2k的采用了环化，所以对于插入长度大于等    于2k文库，序列需要反转，reverse_seq＝1，小片段设为0

**asm_flags**  
决定reads哪一段会被利用，1（仅进行contig组装）；2（仅进行scaffold组装）；3（contig和scaffold都组装）；4（只进行gap closure）。 

**rd_len_cutof**  
组装器会过滤掉当前文库中到这个长度之间的reads。 

**rank**  
为整数值，它决定在scaffold组装时reads被利用的顺序。文库中具有同样rank值的会被同时使用（在组装scaffold时）。  

**pair_num_cutoff**  
该参数是成对number的 cutoff value，为了得到两条contigs的可靠的连接 或  pre-scaffolds。paired-end reads and mate-pair reads 的最小数量分别是 3 和 5. 

**map_len**  
这个参数在“map”阶段生效，它是read 和 contig 的最小比对长度，用来建立一个可靠的read定位。

paired-end reads and mate-pair reads 的最小的长度分别是 32 和 35.

组装器接受三种read格式：FASTA, FASTQ and BAM。

Mate-pair关系：fastq中两个文件的同行序列；fasta中的邻行序列，bam文件比较特殊。

配置文件中，单端文件用"f=/path/filename" or "q=/pah/filename" 表示 fasta or fastq 格式。

双端reads被放在两个fasta文件中，分别为"f1=" and "f2="。fastq文件由"q1=" and "q2="表示。

双端reads如果全在一个fasta文件中，则用"p=" 选项；reads在bam文件中则用"b=".选项。
## 2.命令及参数
常用的一站式运行方式：

```
${bin} all -s config_file -K 63 -R -o graph_prefix 1>ass.log 2>ass.err
```
分四步运行：

```
${bin} pregraph -s config_file -K 63 -R -o graph_prefix 1>pregraph.log 2>pregraph.err
OR
${bin} sparse_pregraph -s config_file -K 63 -z 5000000000 -R -o graph_prefix 1>pregraph.log 2>pregraph.err
```

```
${bin} contig -g graph_prefix -R 1>contig.log 2>contig.err
```

```
${bin} map -s config_file -g graph_prefix 1>map.log 2>map.err
```

```
${bin} scaff -g graph_prefix -F 1>scaff.log 2>scaff.err
```

## Reference
1. http://soap.genomics.org.cn/soapdenovo.html
2. https://www.cnblogs.com/leezx/p/5606373.html
3. http://blog.sina.com.cn/s/blog_959d22480102v2fi.html