# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 16:04:12 2020

@author: harshv
"""
#fields3=["L1_distance", "L2_distance"];
#fields2=["Occurrences", 'Planogram_row','Planogram_column'];
#fields1=['Sale Price','Assigned Value']

import numpy
import pdb
from openpyxl.utils.cell import column_index_from_string

def distances (df, file_count, files2, fields1, fields2, fields3):
    df=df.fillna(0);
    for i in range (file_count):
        sl=files2.astype(str).loc[i,"Store"]+"_"+files2.astype(str).loc[i,"Location"];
        my=files2.astype(str).loc[i,"Month Year"];    #get month year string
        out_fields3=[sl+" "+s+" "+my for s in fields3];
        out_fields2=[sl+" "+s+" "+my for s in fields2];
        out_fields1=[sl+" "+s+" "+my for s in fields1]; #create labels 1 for output columns
        
        if i==0:
            df[out_fields3[0]]=0; df[out_fields3[1]]=0; df[out_fields3[2]]=0; 
            x_ref=df[out_fields2[1]]; y_ref0=df[out_fields2[2]]; p_ref=df[out_fields1[0]];
            #y_ref=[0 for x in range (y_ref0)];
            y_ref=[0]*y_ref0.shape[0];
            for j in range(y_ref0.shape[0]):
                if y_ref0[j]!=0:
                    y_ref[j]=column_index_from_string(y_ref0[j]);
                else:
                    y_ref[j]=0;
                        
                
        else: 
            x=df[out_fields2[1]]; y0=df[out_fields2[2]]; p=df[out_fields1[0]];
            y=[0]*y0.shape[0];
            for j in range(y0.shape[0]):
                if y0[j]!=0:
                    y[j]=column_index_from_string(y0[j]);
                else:
                    y[j]=0;
            
            #df[out_fields3[0]]=abs(numpy.subtract(x,x_ref))+abs(numpy.subtract(y,y_ref));
            #df[out_fields3[1]]=(numpy.square(numpy.subtract(x,x_ref))+numpy.square(numpy.subtract(y,y_ref)))**0.5;
            for j in range (y0.shape[0]):
                if x[j]!=0 and y[j]!=0 and x_ref[j]!=0 and y_ref[j]!=0:
                    df.loc[j,out_fields3[0]]=abs(x[j]-x_ref[j])+abs(y[j]-y_ref[j]);
                    df.loc[j,out_fields3[1]]=((x[j]-x_ref[j])**2+(y[j]-y_ref[j])**2)**0.5;
                    df.loc[j,out_fields3[2]]=p[j]-p_ref[j];
                else:
                    df.loc[j,out_fields3[0]]=0;
                    df.loc[j,out_fields3[1]]=0;
                    df.loc[j,out_fields3[2]]=0;
            
            x_ref=x;
            y_ref=y;
            p_ref=p;
        
    return df