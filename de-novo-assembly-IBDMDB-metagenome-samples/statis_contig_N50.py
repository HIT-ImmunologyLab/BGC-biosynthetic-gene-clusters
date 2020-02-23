#!/usr/bin
#-*-coding:utf-8-*-

import os

if __name__=='__main__':
    save_root_dir = '/share/test003/zhoufx/IBDMDB/denovo_assembly'
    dir_name_list = ['denovel_assembly_result_pediatric', 'denovel_assembly_result']
    result_file = 'donove_assembly_contig_statis.txt'
    fout = open(result_file,'w')
    header_list = ['sample_id','total_contig_len','average_contig_len','longest_contig_len','contig_N50_len','contig_N90_len']
    fout.write('\t'.join(header_list)+'\n')
    for dir_name_item in dir_name_list:
        cur_dir_path = '%s/%s' % (save_root_dir, dir_name_item)
        sample_id_list = os.listdir(cur_dir_path)
        for sample_id_item in sample_id_list:
            cur_sample_dir_path = '%s/%s/%s' % (cur_dir_path, sample_id_item, sample_id_item)
            cur_sample_file_num = len(os.listdir(cur_sample_dir_path))
            if cur_sample_file_num == 25 or cur_sample_file_num == 23:
                cur_run_log_file = '%s/%s/%s_run.log' % (cur_dir_path, sample_id_item, sample_id_item)
                with open(cur_run_log_file,'r')as fin:
                    contents = fin.read()
                    cur_contig_total_len = contents.split('sum up ')[1].split('bp')[0].strip()
                    cur_contig_avg_len = contents.split('with average length ')[1].split('.')[0]
                    cur_longest_len = contents.split('The longest length is ')[1].split('bp')[0].strip()
                    cur_contig_N50_len = contents.split('contig N50 is ')[1].split('bp')[0].strip()
                    cur_contig_N90_len = contents.split('contig N90 is ')[1].split('bp')[0].strip()
                    strwrite_list = [sample_id_item,cur_contig_total_len,cur_contig_avg_len,cur_longest_len,cur_contig_N50_len,cur_contig_N90_len]
                    fout.write('\t'.join(strwrite_list)+'\n')
    fout.close()
