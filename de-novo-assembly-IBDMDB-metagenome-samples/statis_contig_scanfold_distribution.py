#!/usr/bin
#-*-coding:utf-8-*-

import os

def get_len_dict(len_file,len_dict):
    with open(len_file,'r')as fin:
        lines = fin.readlines()
        for line in lines[1:]:
            cur_len = line.strip('\n').split('\t')[1]
            if cur_len not in len_dict:
                len_dict[cur_len] = 1
            else:
                len_dict[cur_len] = len_dict[cur_len] + 1

def write_len_file(len_info_dict,output_file):
    fout = open(output_file,'w')
    for key in len_info_dict:
        strwrite = key+'\t'+str(len_info_dict[key])+'\n'
        fout.write(strwrite)
    fout.close()

if __name__=='__main__':
    save_root_dir = '/share/test003/zhoufx/IBDMDB/denovo_assembly'
    dir_name_list = ['denovel_assembly_result_pediatric', 'denovel_assembly_result']
    contig_dict = {}
    scanf_dict = {}
    for dir_name_item in dir_name_list[0:1]:
        cur_dir_path = '%s/%s'%(save_root_dir,dir_name_item)
        sample_id_list = os.listdir(cur_dir_path)
        for sample_id_item in sample_id_list:
            cur_sample_dir_path = '%s/%s/%s' % (cur_dir_path, sample_id_item, sample_id_item)
            cur_sample_file_num = len(os.listdir(cur_sample_dir_path))
            if cur_sample_file_num == 25:
                cur_contig_outut_file = '%s/%s_denovo_assembly_contig_len_statis.txt' % (
                cur_sample_dir_path, sample_id_item)
                get_len_dict(cur_contig_outut_file, contig_dict)
                cur_scaf_outut_file = '%s/%s_denovo_assembly_scaf_len_statis.txt' % (
                    cur_sample_dir_path, sample_id_item)
                get_len_dict(cur_scaf_outut_file, scanf_dict)
    contig_distribution_file = 'contig_len_distribution.txt'
    write_len_file(contig_dict, contig_distribution_file)
    scanf_distribution_file = 'scanf_len_distribution.txt'
    write_len_file(scanf_dict, scanf_distribution_file)
