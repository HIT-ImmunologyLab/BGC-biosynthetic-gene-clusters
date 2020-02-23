## Overview
In this exercise we will try to perform de novo assembly of **Illumina Paired end reads**. The data is from a Vibrio cholerae strain isolated in Nepal. You will try to:

1. Run FastQC, adaptor and quality trimming reads
2. Count k-mers and estimate genome size
3. Correct reads using Musket
4. Determine insert size of paired end reads
5. Run de novo assembly using SOAPdenovo
6. Calculate assembly statistics
7. Plot coverage and length histograms of the assembly
9. Visualize assembly using Circoletto
10. Try to assemble the genome using SPAdes

## FastQC and trimming
1. Running fastqc on the reads

```
mkdir fastqc
fastqc -o fastqc *.txt.gz
```
2. Trim the reads using **AdapterRemoval**. In the command below the most frequent adapter/primer sequence is already pasted in - don't worry about the others in our case they are just variations of that one. Also we use minimum of 40nt and trim to quality 20 (~3 mins) and note that we write qualitybase 64 (Q1). The "--basename" option gives the base name of the output files and we want it to be compressed using gzip "--gzip". When it is done take a look at "Vchol-001_6.settings" for some statistics on how many reads were trimmed etc.

```
AdapterRemoval --file1 Vchol-001_6_1_sequence.txt.gz --file2 Vchol-001_6_2_sequence.txt.gz \
--adapter1 GATCGGAAGAGCACACGTCTGAACTCCAGTCACATCACGATATCGTATGC \
--adapter2 GATCGGAAGAGCGTCGTGTAGGGAAAGAGGGTAGATCTCGGTGGTCGCCG \
--qualitybase 64 --basename Vchol-001_6 --gzip --trimqualities --minquality 20 --minlength 40
```
## Genome size estimation
Count the occurence of k-mers in the data - a k-mer is simply a string of nucleotides of a certain length. Lets say we count all the 15-mers that are in the read data we have - we do this using a program called Jellyfish. Here we tell Jellyfish to count 15-mers and also add counts from the complementary strand. Afterwards we tell it to create a histogram that we will plot using R. "/dev/fd/0" in the command below means that it should take input from "STDIN", eg. from the gzip program.

```
gzip -dc Vchol-001_6.pair*.truncated.gz | jellyfish count -t 2 -m 15 -s 1000000000 -o Vchol-001 -C /dev/fd/0
jellyfish histo Vchol-001 > Vchol-001.histo
```

```
# R
dat=read.table("Vchol-001.histo")
barplot(dat[,2], xlim=c(0,150), ylim=c(0,5e5), ylab="No of kmers", xlab="Counts of a k-mer", names.arg=dat[,1], cex.names=0.8)
dev.print("Vchol-001.histo.pdf", device=pdf)
```
The plot shows how many times a k-mer is found (x-axis) and the number of kmers with this count (y-axis). The bars in the lower end are the k-mers that only occur very few times, these are probably sequencing errors, whereas the k-mers that occurs many times are "real" k-mers. We can use the information from the "real" k-mers to correct similar "error k-mers". In this way we can increase the performance of our assembly (this also works for SNP calling as well).
## Error correction
Correct the reads using Musket. First we need to know how many k-mers that will be in the data, this is rather easy to get becasue we already counted kmers using jellyfish. Use this command to output the number of "distinct" k-mers in the dataset:

jellyfish stats Vchol-001
This is needed for musket to setupt the bloom filters and hash tables for memory consumption. Then we area ready to run the correction. Finally we will rename the outputfiles to sensible names.

```
musket -k 15 8423098 -p 1 -omulti Vchol-001_6.cor -inorder Vchol-001_6.pair1.truncated.gz Vchol-001_6.pair2.truncated.gz -zlib 1
mv Vchol-001_6.cor.0 Vchol-001_6.pair1.cor.truncated.gz
mv Vchol-001_6.cor.1 Vchol-001_6.pair2.cor.truncated.gz
```
## de novo assembly
Now the reads are ready for de novo assembly. We are going to use SOAPdenovo as the assembler, it uses the de bruijn approach. When running denovo assemblies one should try different k-mer sizes - the k-mer size is what is being used for building the de bruijn graph and is therefore very important. There is currently no way to estimate what will be the optimal k before running, the best k-size may change between different dataset and may change between different assemblers for the same dataset.

**SOAPdenovo requires a configuration file with different information, a sample file is the Vchol-001.soap.conf. You need to open it and change the path to your file.** To open it write "gedit Vchol-001.soap.conf" and then navigate to "q1" and "q2", here paste in the path and filename of your two files. Note that we have written "avg_ins=200" even though we do not know the average insert size. We will run an initial assembly to create contigs and then extract the information and then rerun the full assembly again. When you have changed the paths save the file (Ctrl-S) then start the assembler. We will try first with a k of 35.

```
SOAPdenovo2-127mer pregraph -s Vchol-001.soap.conf -K 35 -p 2 -o initial
SOAPdenovo2-127mer contig -g initial
```
Now you should have a file called "initial.contig", we need to map our reads back to the contigs to identify the insert size, just as we did in the alignment exercise. Lets only map the first 100.000 reads - this should be enough.

```
zcat Vchol-001_6.pair1.cor.truncated.gz | head -n 400000 > Vchol_sample_1.fastq
zcat Vchol-001_6.pair2.cor.truncated.gz | head -n 400000 > Vchol_sample_2.fastq

bwa index initial.contig
bwa mem initial.contig Vchol_sample_1.fastq Vchol_sample_2.fastq | samtools view -Sb - > initial.sample.bam

samtools view initial.sample.bam | cut -f9 > initial.insertsizes.txt
```

```
R
a = read.table("initial.insertsizes.txt")
a.v = a[a[,1]>0,1]
mn = quantile(a.v, seq(0,1,0.05))[4]
mx = quantile(a.v, seq(0,1,0.05))[18]
mean(a.v[a.v >= mn & a.v <= mx])       # mean
sd(a.v[a.v >= mn & a.v <= mx])         # sd
```
## Coverage of assembly
Lets calculate coverage and length for each sequence and plot it as a histogram in R. We also plot the lengths of the scaffolds.

```
fastx_soapcov.py --i Vchol-001.best.fa > Vchol-001.best.cov
```

```
# R
library(plotrix)
dat=read.table("Vchol-001.best.cov", sep="\t")
par(mfrow=c(1,2))
weighted.hist(w=dat[,2], x=dat[,1], breaks=seq(0,100, 1), main="Weighted coverage", xlab="Contig coverage")
hist(dat[,1], xlim=c(0,100), breaks=seq(0,1000,1), main="Raw coverage", xlab="Contig coverage")
dev.print("best.coverage.pdf", device=pdf)

# Lengths
par(mfrow=c(1,1))
barplot(rev(sort(dat[,2])), xlab="# Scaffold", ylab="Length", main="Scaffold Lengths")
dev.print("scaffold.lengths.pdf", device=pdf)
q()

evince best.coverage.pdf &
evince scaffold.lengths.pdf &
```
The left plot shows the length-weighted coverage (of k-mers) of the contigs/scaffolds - this means that long sequences has a larger weight compared to short sequences. The plot on the right side shows a normal histogram of contig coverage. By comparing the two plots we see that the majority of the assembly has a k-mer coverage around 20-30X, and that remaining assembly are short sequences. NB: The contig coverage is dependent on the size of the K you chose - larger K gives smaller coverage. Looking at the plot with the lengths you see that the majority of the assembly are in quite long scaffolds.
## Assembly evaluation
First we will use Quast to evaluate the assembly using different metrics, see here. You can run it with our without a reference genome and we will try to evaluate our assembly vs. the Vibrio cholerae reference genome:

```
python /home/27626/bin/quast-4.0/quast.py Vchol-001.best.fa --scaffolds -R vibrio_cholerae_O1_N16961.fa
firefox quast_results/latest/report.html & 
```
## Visualization using circoletto
Lets try to visualize the assembly. Because we know that the data is from a Vibrio cholerae we can try to compare our assembly with the a V.cholerae reference genome. First lets filter the assembly to minimum 500bp.

```
fastx_filterfasta.py --i Vchol-001.best.fa --min 500
```
## Try to assemble the genome using SPAdes
There is a lot of discussion on which assembler is better than others. SPAdes is defintely one of the best ones. SPAdes will run error correction and use multiple k-mers at the same time when it is doing the assembly. Try it out, it is in the bin folder - try to figure out the commands you need to write to run it and compare with the output from SOAPdenovo2 (hint: you can use Quast for the comparison).

```
spades.py -h
```
## Reference
http://www.cbs.dtu.dk/courses/27626/Exercises/denovo_exercise.php