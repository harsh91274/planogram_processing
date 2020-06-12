# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 11:29:56 2020

@author: harshv
"""
import numpy as np
from openpyxl.utils.cell import column_index_from_string as cifs
import pdb 
#fields_corr=[ 'Planogram_row','Planogram_column'];
import seaborn as sns
import matplotlib.pyplot as plt
import os
from pathlib import Path

def correlation (df, file_count, files2, fields_corr, patha):
   for i in range (file_count):
        l1_mat = np.zeros(shape=(len(df),len(df)));
        l1_del = np.zeros(shape=(len(df),len(df)));
        l2_mat = np.zeros(shape=(len(df),len(df)));
        l2_del = np.zeros(shape=(len(df),len(df)));
        
        sl=files2.astype(str).loc[i,"Store"]+"_"+files2.astype(str).loc[i,"Location"];
        my=files2.astype(str).loc[i,"Month Year"];    #get month year string
        out_fields_corr=[sl+" "+s+" "+my for s in fields_corr];
        
        for j in range (len(df)):
            for k in range(len(df)):
                if df.loc[j,out_fields_corr[1]]!=0 and df.loc[k,out_fields_corr[1]]!=0:
                    l1_mat[j,k]=abs(df.loc[j,out_fields_corr[0]]-df.loc[k,out_fields_corr[0]])+abs(cifs(df.loc[j,out_fields_corr[1]])-cifs(df.loc[k,out_fields_corr[1]]));
                    l2_mat[j,k]=((df.loc[j,out_fields_corr[0]]-df.loc[k,out_fields_corr[0]])**2+(cifs(df.loc[j,out_fields_corr[1]])-cifs(df.loc[k,out_fields_corr[1]]))**2)**0.5;
        
        if i!=0:
            l1_del=l1_mat-l1_mat_ref;
            l2_del=l1_mat-l2_mat_ref;
                   
        fig=plt.figure(figsize = (9, 9));
        ax1=fig.add_subplot(2,2,1); ax1a=sns.heatmap(l1_mat,cmap="OrRd"); ax1a.set_yticklabels(df["Model #"],fontsize="x-small"); ax1a.set_xticklabels(df["Model #"],fontsize="x-small"); ax1a.set_title('L1');
        ax2=fig.add_subplot(2,2,2); ax2a=sns.heatmap(l2_del,cmap="coolwarm"); ax2a.set_yticklabels(df["Model #"],fontsize="x-small"); ax2a.set_xticklabels(df["Model #"],fontsize="x-small"); ax2a.set_title('\u0394L1');
        ax3=fig.add_subplot(2,2,3); ax3a=sns.heatmap(l2_mat,cmap="OrRd"); ax3a.set_yticklabels(df["Model #"],fontsize="x-small"); ax3a.set_xticklabels(df["Model #"],fontsize="x-small"); ax3a.set_title('L2');
        ax4=fig.add_subplot(2,2,4); ax4a=sns.heatmap(l2_del,cmap="coolwarm"); ax4a.set_yticklabels(df["Model #"],fontsize="x-small"); ax4a.set_xticklabels(df["Model #"],fontsize="x-small"); ax4a.set_title('\u0394L2');
        figname=os.path.join(patha,"pairwise_"+my.replace(" ","_")+".jpg");
        plt.savefig(figname, facecolor='w', edgecolor='k'); 
        
        np.savetxt(os.path.join(patha,"pairwise_L1_"+my.replace(" ","_")+".txt"),l1_mat,fmt='%10.2f');
        np.savetxt(os.path.join(patha,"pairwise_delta_L1_"+my.replace(" ","_")+".txt"),l1_del,fmt='%10.2f');
        np.savetxt(os.path.join(patha,"pairwise_L2_"+my.replace(" ","_")+".txt"),l2_mat,fmt='%10.2f');
        np.savetxt(os.path.join(patha,"pairwise_delta_L2_"+my.replace(" ","_")+".txt"),l2_del,fmt='%10.2f');
        
        l1_mat_ref=l1_mat;
        l2_mat_ref=l2_mat;        
        
        plt.close(fig);
       # pdb.set_trace()
        
        
        
