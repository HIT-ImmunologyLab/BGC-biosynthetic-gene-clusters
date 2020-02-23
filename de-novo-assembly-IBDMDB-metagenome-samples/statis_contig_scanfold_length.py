#!/usr/bin
#-*-coding:utf-8-*-

import os

def statis_length_file(input_file,output_file,header_list):
    fout = open(output_file,'w')
    fout.write('\t'.join(header_list)+'\n')
    with open(input_file,'r')as fin:
        content = fin.read()
        elems = content.split('\n>')
        if '' in elems:
            elems.remove('')
        for elem in elems:
            elem_content = elem.split('\n')
            cur_elem_title = elem_content[0].strip('>')
            cur_elem_len = 0
            for elem_item in elem_content[1:]:
                cur_elem_len = cur_elem_len + len(elem_item)
            fout.write(cur_elem_title+'\t'+str(cur_elem_len)+'\n')
    fout.close()

if __name__=='__main__':
    save_root_dir = '/share/test003/zhoufx/IBDMDB/denovo_assembly'
    dir_name_list = ['denovel_assembly_result_pediatric', 'denovel_assembly_result']
    run_complete_file = 'run_complete_file.txt'
    fout = open(run_complete_file,'w')
    for dir_name_item in dir_name_list[0:1]:
        cur_dir_path = '%s/%s'%(save_root_dir,dir_name_item)
        sample_id_list = os.listdir(cur_dir_path)
        for sample_id_item in sample_id_list:
            cur_sample_dir_path = '%s/%s/%s'%(cur_dir_path,sample_id_item,sample_id_item)
            cur_sample_file_num = len(os.listdir(cur_sample_dir_path))
            if cur_sample_file_num == 23:
                fout.write(sample_id_item+'\n')
                cur_contig_input_file = '%s/%s_denovo_assembly.contig'%(cur_sample_dir_path,sample_id_item)
                cur_contig_outut_file = '%s/%s_denovo_assembly_contig_len_statis.txt'%(cur_sample_dir_path,sample_id_item)
                cur_contig_header_list = ['contig_name','contig_len']
                statis_length_file(cur_contig_input_file, cur_contig_outut_file, cur_contig_header_list)

                cur_scaf_input_file = '%s/%s_denovo_assembly.scafSeq' % (cur_sample_dir_path, sample_id_item)
                cur_scaf_outut_file = '%s/%s_denovo_assembly_scaf_len_statis.txt' % (
                cur_sample_dir_path, sample_id_item)
                cur_scaf_header_list = ['scaf_name', 'scaf_len']
                statis_length_file(cur_scaf_input_file, cur_scaf_outut_file, cur_scaf_header_list)
    fout.close()
