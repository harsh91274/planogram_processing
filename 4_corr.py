# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 11:29:56 2020

@author: harshv
"""
import numpy as np
from openpyxl.utils.cell import column_index_from_string as cifs
import pdb 
#fields_corr=[ 'Planogram_row','Planogram_column'];

def correlation (df, file_count, files2, fields_corr):
   for i in range (file_count):
        l1_mat = np.zeros(shape=(len(df),len(df)));
        l2_mat = np.zeros(shape=(len(df),len(df)));
        
        sl=files2.astype(str).loc[i,"Store"]+"_"+files2.astype(str).loc[i,"Location"];
        my=files2.astype(str).loc[i,"Month Year"];    #get month year string
        out_fields_corr=[sl+" "+s+" "+my for s in fields_corr];
        
        for j in range (len(df)):
            for k in range(len(df)):
                if df.loc[i,out_fields_corr[1]]!=0 and df.loc[j,out_fields_corr[1]]!=0:
                    l1_mat[i,j]=abs(df.loc[i,out_feilds_corr[0]]-df.loc[j,out_feilds_corr[0]])+abs(cifs(df.loc[i,out_feilds_corr[1]])-cifs(df.loc[j,out_feilds_corr[1]]));
                    l2_mat[i,j]=((df.loc[i,out_feilds_corr[0]]-df.loc[j,out_feilds_corr[0]])**2+(cifs(df.loc[i,out_feilds_corr[1]])-cifs(df.loc[j,out_feilds_corr[1]]))**2)**0.5;
                    
       pdb.set_trace();
