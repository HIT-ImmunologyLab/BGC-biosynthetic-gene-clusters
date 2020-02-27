## 使用 SPAdes 进行基因组组装
### 1. SPAdes 简介
SPAdes 主要用于进行单细胞测序的细菌基因组组装，当然也能用于非单细胞测序数据。输入数据可以是 Illumina、IonTorrent reads,或 PacBio、Sanger reads，也可以把一些 contigs 序列作为 long reads 进行输入。该软件可以同时接受多组 paired-end、mate-pairs 和 unpaired reads 数据的输入。同时该软件有一个独立的模块用于进行杂合基因组的组装。  

SPAdes 包含多个独立模块

```
BayesHammer： 用于 Illumina reads 的修正
IonHammer： 用于 IonTorrent 数据的修正
SPAdes： 用于基因组组装；K 值是软件自动选择的。
MismatchCorrector： 对组装结果 contigs 或 scaffolds 的 mismatch 和 sort indels 进行修正；此模块需要使用 BWA；默认下此模块是关闭的，但是推荐开启它。
dipSPAdes： 用于组装双倍型高杂合基因组；更多说明：dipSPAdes manual
```

### 2. SPAdes 下载和安装
从网页http://bioinf.spbau.ru/spades下载


```
$ wget http://spades.bioinf.spbau.ru/release3.1.0/SPAdes-3.1.0-Linux.tar.gz
$ tar -xzf SPAdes-3.1.0-Linux.tar.gz -C /opt/biosoft/
# 测试运行
$ /opt/biosoft/SPAdes-3.1.0-Linux/bin/spades.py --test 
```

### 3. SPAdes 的使用
#### 3.1 输入数据
SPAdes 3.0.0 的运行至少需要有以下一种数据：


```
Illumina paired-end/unpaired reads
IonTorrent paired-end/unpaired reads
PacBio CCS reads
```

并且，值得注意的是：Illumina 数据和 Ionorrent 数据不能同时用于组装； 仅有 mate-paired，PacBio CLR reads, Sanger reads 或 additional contigs 数据时，不应该使用 SPAdes 进行组装。
SPAdes 支持的 Paired-end 和 Mate-Paired 的数据，其数据需要为 fastq 格式，软件需要对其进行 reads 的 error correction 。同时， SPAdes 也支持使用 Sanger 或 PacBio CCS 的 reads 数据，但软件不能对此数据进行 error correction。

##### 3.1.1 READ-PAIR 数据
Read-pair 数据输入到程序中有 3 种方式：
1. left 和 right 的 reads 分别在两个 fastq 文件中。
2. left 和 right 的 reads 交叉融合在一个 fastq 文件中。
3. 将所有的输入数据信息整合在一个 YAML 格式的文本文件中。

使用非 YAML 方式输入数据，这种方式最多能使用 5 组 paired-end 数据 和 5 组 mate-paired 数据。
仅有一个 library 数据时：

```
--12 file_name
12 表示后面接的文件是交叉融合的 paired 数据，下同。
-1 file_name
1 表示 left 数据
-2 file_name
2 表示 right 数据
-s file_name
s 表示 single 数据, 也用于输入 PacBio CCS reads。
```
有多个 paired-end library 数据时：

```
--pe{int}-12 编号为 int 的 library 的交叉融合后的 paired 数据。int 取值只能是 1,2,3,4,5 。下同。
--pe{int}-1  编号为 int 的 library 的 left 数据
--pe{int}-2  编号为 int 的 library 的 right 数据
--pe{int}-s  编号为 int 的 library 的 single 数据
--pe{int}-{fr|rf|ff} 编号为 int 的 library 的数据的方向，默认为 --pe{int}-fr 。
```
有多个 mate-paired library 数据时：

```
--mp{int}-12 编号为 int 的 library 的交叉融合后的 paired 数据
--mp{int}-1  编号为 int 的 library 的 left 数据
--mp{int}-2  编号为 int 的 library 的 right 数据
--mp{int}-s  编号为 int 的 library 的 single 数据
--mp{int}-{fr|rf|ff} 编号为 int 的 library 的数据的方向，默认为 --mp{int}-rf 。
```
##### 3.1.2 PACBIO 数据
PacBio 数据有两种： CCS (circular consensus sequence) 和 CLR (continuous long read)。PacBio CLR 数据有利于杂合基因组的组装。
数据输入参数：

```
--pacbio  输入 PacBio CLR reads
--sanger  输入 sanger reads
```
##### 3.1.3 ADDITIONAL CONTIGS

```
--trusted-contigs
输入可信度高的 contigs，用于 graph construction, gap closure 和 repeat resolution。
--untrusted-contigs
输入可信度较低的 contigs, 用于gap closure 和 repeat resolution。
```
这两个参数不能输入其它邻近物种的基因组序列。仅用于输入同一个物种的基因组的 contigs 。

##### 3.1.4 YAML 方式输入数据

```
--dataset
YAML 格式的文件
```

```
 [
      {
        orientation: "fr",
        type: "paired-end",
        right reads: [
          "/FULL_PATH_TO_DATASET/lib_pe1_right_1.fastq",
          "/FULL_PATH_TO_DATASET/lib_pe1_right_2.fastq"
        ],
        left reads: [
          "/FULL_PATH_TO_DATASET/lib_pe1_left_1.fastq",
          "/FULL_PATH_TO_DATASET/lib_pe1_left_2.fastq"
        ]
      },
      {
        orientation: "rf",
        type: "mate-pairs",
        right reads: [
          "/FULL_PATH_TO_DATASET/lib_mp1_right.fastq"
        ],
        left reads: [
          "/FULL_PATH_TO_DATASET/lib_mp1_left.fastq"
        ]
      },
      {
        type: "single",
        single reads: [
          "/FULL_PATH_TO_DATASET/pacbio_ccs.fastq"
        ]
      },
      {
        type: "pacbio",
        single reads: [
          "/FULL_PATH_TO_DATASET/pacbio_clr.fastq"
        ]
      }
    ]
```

#### 3.2 参数
使用 spades.py 运行 SPAdes 程序：

```
$ /opt/biosoft/SPAdes-3.0.0-Linux/bin/spades.py [options] -o output_dir
```
参数：

```
-o output_dir
指定输出的文件夹
--sc
此 flag 用于 MDA (single-cell) 数据
--iontorrent
此 flag 用于 IonTorrent 数据的组装
--test
使用 test 数据运行 SPAdes，用于检测软件是否正确安装
-h | --help
打印帮助信息
--only-error-correction
仅仅执行 reads error correction 步骤
--only-assembler
仅仅运行组装模块
--careful
通过运行 MismatchCorrector 模块进行基因组上 mismatches 和 short indels 的修正。推荐使用此参数。
--continue
从上一次终止处继续运行程序。
--restart-from
从指定的位置重新开始运行程序。和上一个参数相比，此参数可以用于改变一些组装参数。可选的值有：

ec 从 error correction 处开始
as 从 assembly module 处开始
k{int} 从指定的 k 值处开始
mc 从 mismatch correction 处开始

--disable-gzip-output
使用此参数来设定不对 corrected reads 进行压缩。默认下 corrected reads 是 .fastq.gz 格式的
-t int
使用的线程数，默认为16
-m int
设定内存的限制，单位为 Gb。如果程序使用的内存达到此值，则程序会终止运行。默认值是 250 。
--tmp-dir dir_name
设置 reads error correction 的临时文件存放路径。默认为 output_dir/corrected/tmp 。
-k int,int,...
由逗号分隔的 k-mer sizes。这些数值必须为奇数，要小于 128，且按升序排列。如果使用了 --sc 参数，则默认值为 21,33,55 。 若没有 --sc 参数，则程序会根据 reads 长度自动选择 k-mer 参数。
--phred-offset
碱基质量格式， 33 或 64
```
#### 3.3 常用例子
单个 illumina paired-end 文库：

```
$ spades.py -o output_dir -1 reads1.fastq -2 reads2.fastq
```
多个 illumina paired-end 和 mate-paired 文库，以及 Pcabio sanger contigs 数据：

```
$ spades.py -o output_dir\
 --pe1-1 pe1_1.fq --pe1-2 pe1_2.fq --pe2-1 pe2_1.fq --pe2-2 pe2_2.fq\
 --mp1-1 mp1_1.fq --mp1-2 mp1_2.fq --mp2-1 mp2_1.fq --mp2-2 mp2_2.fq\
 -s pacibo_ccs.fastq --pacbio pacbio_clr.fastq\
 --sanger sanger.fa\
 --trusted-contigs trusted_contig.fa\
 --untrusted-contigs untrusted_contig.fa\
 --careful -t 16 --phred-offset 33 -m 250 -k 21,33,55 [--sc]
```


### Reference:

1. SPAdes: a new genome assembly algorithm and its applications to single-cell sequencing (https://dx.doi.org/10.1089%2Fcmb.2012.0021)
2. 软件说明文档： http://spades.bioinf.spbau.ru/release3.0.0/manual.html#sec2.1
3.  http://www.chenlianfu.com/?p=2116