## Analysis Pipeline

![image](https://github.com/fengxiaZhou/BGC/raw/master/images/workflow.png)

## De novo assembly
### 核心代码
此处显示的为De novo拼接的核心代码，详细代码见： SOAPdenovo_pipeline.py
#### 生成用于Denovo
```
 assembly拼接的配置文件
## max_rd_len=101
## avg_ins=300
## reverse_seq=0
## asm_flags=3
## rank=1
def create_config_file(config_file_path,read1_file_path,read2_file_path):
    fout = open(config_file_path,'w')
    strwrite_list = ['#maximal read length','max_rd_len=101','[LIB]','#average insert size','avg_ins=300','#if sequence needs to be reversed',
                     'reverse_seq=0','#in which part(s) the reads are used','asm_flags=3','#in which order the reads are used while scaffolding',
                     'rank=1','# cutoff of pair number for a reliable connection (at least 3 for short insert size)','pair_num_cutoff=3',
                     '#minimum aligned length to contigs for a reliable read location (at least 32 for short insert size)','map_len=32','# path to genes']
    cur_read1_path_str = 'q1=%s'%read1_file_path
    cur_read2_path_str = 'q2=%s'%read2_file_path

    fout.write('\n'.join(strwrite_list+[cur_read1_path_str,cur_read2_path_str]))
    fout.close()
```
#### denove 拼接
```
## 使用工具： SOAPdenovo
## 参数设置：使用默认参数
def assembly_sequence(config_file_path,result_prefix,cur_run_log):
    cmd_soapdenovo_assembly = '/share/test003/software/soapdenovo/SOAPdenovo2-r241/SOAPdenovo-63mer all -s %s -R -p 20 -o %s > %s 2>&1'%(config_file_path,result_prefix,cur_run_log)
    print(cmd_soapdenovo_assembly)
    os.system(cmd_soapdenovo_assembly)
```
## Quality Control
### 统计Contig长度分布
#### 步骤
1. 统计每个样本的Contig，Scaffold长度文件
2. 统计所有样本的Contig，Scaffold长度分布
3. 绘制样本的Contig，Scaffold长度长度分布直方图  

具体的代码详见：statis_contig_scanfold_length.py, statis_contig_scanfold_distribution.py
生成的结果文件：
contig_len_distribution.txt，scanf_len_distribution.txt

#### 结果
Contig长度分布直方图

![image](https://github.com/fengxiaZhou/BGC/raw/master/images/contig_len_distribution.png)

Scaffold长度分布直方图
![image](https://github.com/fengxiaZhou/BGC/raw/master/images/scaf_len_distribution.png)

### 统计Contig N50
#### 步骤：
1. 统计每个样本Contig N50 分布
2. 绘制Contig N50 分布直方图
具体的代码详见：
statis_contig_N50.py
生成的结果文件： 
donove_assembly_contig_N50_statis.txt

#### 结果
Contig N50 分布直方图

![image](https://github.com/fengxiaZhou/BGC/raw/master/images/Contig_N50_len_distribution.png)

### 统计结果分析：
拼接得到的Contig长度，Contig N50长度较短，需要进一步参考其他文献标准调整拼接的参数