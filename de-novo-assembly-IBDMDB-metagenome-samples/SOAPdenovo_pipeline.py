#!/usr/bin
#-*-coding:utf-8-*-

import os
import multiprocessing

def mkdir(dirPath):
    cmd_mkdir = 'mkdir -p %s'%dirPath
    os.system(cmd_mkdir)

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

def assembly_sequence(config_file_path,result_prefix,cur_run_log):
    cmd_soapdenovo_assembly = '/share/test003/software/soapdenovo/SOAPdenovo2-r241/SOAPdenovo-63mer all -s %s -R -p 20 -o %s > %s 2>&1'%(config_file_path,result_prefix,cur_run_log)
    print(cmd_soapdenovo_assembly)
    os.system(cmd_soapdenovo_assembly)

def assembly_pipeline(config_file_path,read1_file_path, read2_file_path,result_prefix,cur_run_log):
    create_config_file(config_file_path, read1_file_path, read2_file_path)
    assembly_sequence(config_file_path, result_prefix,cur_run_log)

def get_need_denoveassembly_id_list():
    cur_need_run_id_list = []
    file_name = 'need_to_denove_assembly.txt'
    with open(file_name,'r')as fin:
        lines = fin.readlines()
        for line in lines[1:]:
            cur_need_run_id = line.strip('\n').split('\t')[0]
            if cur_need_run_id not in cur_need_run_id_list:
                cur_need_run_id_list.append(cur_need_run_id)
    return cur_need_run_id_list

if __name__=='__main__':
    sample_save_dir = '/share/test003/data/IBDMDB/IBDMDB_Metagenomes'
    sample_phenotype_file = 'IBDMDB_metagenome_sample_phenotype_adult.txt'
    result_save_dir = '/share/test003/zhoufx/IBDMDB/denovo_assembly/denovel_assembly_result'
    need_denovo_assembly_id_list = get_need_denoveassembly_id_list()
    pool = multiprocessing.Pool(processes=5)
    with open(sample_phenotype_file,'r')as fin:
        lines = fin.readlines()
        for line in lines[1:]:
            content = line.strip('\n').split('\t')
            cur_sample_id = content[0]
            if cur_sample_id not in need_denovo_assembly_id_list:
                continue
            cur_phenotype = content[1]
            cur_read1_file = '%s/%s/%s_R1.fastq.gz'%(sample_save_dir,cur_sample_id,cur_sample_id)
            cur_read2_file = '%s/%s/%s_R2.fastq.gz'%(sample_save_dir,cur_sample_id,cur_sample_id)
            cur_result_dir = '%s/%s/%s'%(result_save_dir,cur_sample_id,cur_sample_id)
            mkdir(cur_result_dir)
            cur_config_file = '%s/%s/%s_config.txt'%(result_save_dir,cur_sample_id,cur_sample_id)
            cur_result_file = '%s/%s_denovo_assembly'%(cur_result_dir,cur_sample_id)
            cur_run_log = '%s/%s/%s_run.log'%(result_save_dir,cur_sample_id,cur_sample_id)
            # assembly_pipeline(cur_config_file, cur_read1_file, cur_read2_file, cur_result_file)
            pool.apply_async(assembly_pipeline,(cur_config_file, cur_read1_file, cur_read2_file, cur_result_file,cur_run_log,))
    pool.close()
    pool.join()
