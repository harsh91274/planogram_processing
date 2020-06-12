# Code for comparison of changes within the same store and location
"""
Created on Mon Jun  1 09:16:43 2020

@author: Harsh
"""

#%%
import pandas as pd
import numpy as np
#import os
import xlsxwriter 
#import openpyxl as xl
#from openpyxl import load_workbook
import warnings
from datetime import datetime
import glob
#import pdb

warnings.filterwarnings('ignore');
#%%
#get inputs
store=input("Enter Store (Lowes|Home-Depot|*): ");
loc=input("Enter Location (Fisher|Hurst|*): ");

#output file name
if store=="*" and loc=="*":
    outfil="store_comparison_all.xlsx";
elif store=="*":
    outfil="store_comparison_"+loc+".xlsx";
elif loc=="*":
    outfil="store_comparison_"+store+".xlsx";
else:
    outfil="store_comparison_"+store+"_"+loc+".xlsx";
outfile=pd.ExcelWriter(outfil,engine='xlsxwriter');

#headers for empty input pages 
files=pd.DataFrame (columns=['Filename','Month', 'Year', 'Month Year','Datetime', 'Store', 'Location']); 

file_count=0; #number of files processed - important variable
for file in glob.glob("processed_*"+store+"*"+loc+"*.xlsx"):    #for loop gets file details and stores them in dataframe files2
    file_count=file_count+1;
    fs=file.split("_");    
    files.loc[file_count,"Filename"]=file;
    files.loc[file_count,"Month"]=fs[1].split(" ")[0];
    files.loc[file_count,"Year"]=fs[1].split(" ")[1];
    files.loc[file_count,"Month Year"]=fs[1].split(" ")[0]+" "+fs[1].split(" ")[1];
    files.loc[file_count,"Datetime"]= datetime.strptime(fs[1].split(" ")[0]+","+fs[1].split(" ")[1], "%B,%Y"); 
    files.loc[file_count,"Store"]=fs[1].split(" ")[4];
    fs2=fs[1].split(".");
    files.loc[file_count,"Location"]=fs2[0].split(" ")[5];
    
files2=files.sort_values(by=['Datetime','Store','Location'],ascending=False);    #sort files
files2=files2.reset_index(drop=True);
print("Number of files:"+str(file_count));  #outputs
print ("Files:\n"+files2.Filename.to_string(index=False))    #outputs

#%%
#columns to read
fields0=["Brand / Appliance","Model #", "MSRP"];
fields_m=['Model #'];
fields1=['Sale Price','Assigned Value']
#fields2=["Occurrences", "Planogram_row","Planogram_column"];
fields2=["Occurrences", 'Planogram_row','Planogram_column'];
fields=fields1+fields2;
#%%
# Washers-Dryers
df0=pd.read_excel(files2.loc[0,'Filename'], sheet_name="Washers-Dryers");
m_check=[col for col in df0.columns if 'MRSP' in col];
if m_check:
    df0.rename(columns={m_check[0]:"MSRP"},inplace=True);

df_wd=df0[fields0];

for i in range (file_count):
    ifile=files2.loc[i,"Filename"]; #filename
    df=pd.read_excel(ifile, sheet_name="Washers-Dryers");   #read excel page
    #OUTPUT
    sl=files2.astype(str).loc[i,"Store"]+"_"+files2.astype(str).loc[i,"Location"];    #get store, location strings
    my=files2.astype(str).loc[i,"Month Year"];    #get month year string
    out_fields1=[sl+" "+s+" "+my for s in fields1]; #create labels 1 for output columns
    out_fields2=[sl+" "+s+" "+my for s in fields2]; #create labels 2 for output columns
    out_fields=fields_m+out_fields2+out_fields1;    
    df_wd1=pd.DataFrame(columns=out_fields);    #creating iteration output dataframe 
    df_wd1[fields_m]=df[fields_m];  #copying model#   
    df_wd1[out_fields2]=df[fields2];    #copying occurences, row, column
    if df.empty==False:
        df_wd1[out_fields1[0]]=df.loc[:,df.columns.str.contains('Sale Price')]; #Copying sale price
        df_wd1[out_fields1[1]]=df.loc[:,df.columns.str.contains('Assigned Value')];   #copying assigned value
        df_wd=pd.merge(left=df_wd, right=df_wd1, how='outer',left_on='Model #', right_on=str(fields_m[0])); #outer merge of datasets             

if df_wd.empty==False:    
    df_wd.to_excel(outfile,'Washers-Dryers', index=False);
#outfile.save();     
#%%
# Dishwashers
df0=pd.read_excel(files2.loc[0,'Filename'], sheet_name="Dishwashers");
m_check=[col for col in df0.columns if 'MRSP' in col];
if m_check:
    df0.rename(columns={m_check[0]:"MSRP"},inplace=True);

df_dw=df0[fields0];

for i in range (file_count):
    ifile=files2.loc[i,"Filename"]; #filename
    df=pd.read_excel(ifile, sheet_name="Dishwashers");   #read excel page
    #OUTPUT
    sl=files2.astype(str).loc[i,"Store"]+"_"+files2.astype(str).loc[i,"Location"];    #get store, location strings
    my=files2.astype(str).loc[i,"Month Year"];    #get month year string
    out_fields1=[sl+" "+s+" "+my for s in fields1]; #create labels 1 for output columns
    out_fields2=[sl+" "+s+" "+my for s in fields2]; #create labels 2 for output columns
    out_fields=fields_m+out_fields2+out_fields1;    
    df_dw1=pd.DataFrame(columns=out_fields);    #creating iteration output dataframe 
    df_dw1[fields_m]=df[fields_m];  #copying model#   
    df_dw1[out_fields2]=df[fields2];    #copying occurences, row, column
    if df.empty==False:
        df_dw1[out_fields1[0]]=df.loc[:,df.columns.str.contains('Sale Price')]; #Copying sale price
        df_dw1[out_fields1[1]]=df.loc[:,df.columns.str.contains('Assigned Value')];   #copying assigned value
        df_dw=pd.merge(left=df_dw, right=df_dw1, how='outer',left_on='Model #', right_on=str(fields_m[0])); #outer merge of datasets             

if df_dw.empty==False:    
    df_dw.to_excel(outfile,'Dishwashers', index=False);
#outfile.save();

#%%
# Refrigerators
df0=pd.read_excel(files2.loc[0,'Filename'], sheet_name="Refrigerators");
m_check=[col for col in df0.columns if 'MRSP' in col];
if m_check:
    df0.rename(columns={m_check[0]:"MSRP"},inplace=True);

df_ref=df0[fields0];

for i in range (file_count):
    ifile=files2.loc[i,"Filename"]; #filename
    df=pd.read_excel(ifile, sheet_name="Refrigerators");   #read excel page
    #OUTPUT
    sl=files2.astype(str).loc[i,"Store"]+"_"+files2.astype(str).loc[i,"Location"];    #get store, location strings
    my=files2.astype(str).loc[i,"Month Year"];    #get month year string
    out_fields1=[sl+" "+s+" "+my for s in fields1]; #create labels 1 for output columns
    out_fields2=[sl+" "+s+" "+my for s in fields2]; #create labels 2 for output columns
    out_fields=fields_m+out_fields2+out_fields1;    
    df_ref1=pd.DataFrame(columns=out_fields);    #creating iteration output dataframe 
    df_ref1[fields_m]=df[fields_m];  #copying model#   
    df_ref1[out_fields2]=df[fields2];    #copying occurences, row, column
    if df.empty==False:
        df_ref1[out_fields1[0]]=df.loc[:,df.columns.str.contains('Sale Price')]; #Copying sale price
        df_ref1[out_fields1[1]]=df.loc[:,df.columns.str.contains('Assigned Value')];   #copying assigned value
        df_ref=pd.merge(left=df_ref, right=df_ref1, how='outer',left_on='Model #', right_on=str(fields_m[0])); #outer merge of datasets             

if df_ref.empty==False:    
    df_ref.to_excel(outfile,'Refrigerators', index=False);
#outfile.save();
#%%
# Cooking Products
df0=pd.read_excel(files2.loc[0,'Filename'], sheet_name="Cooking Products");
m_check=[col for col in df0.columns if 'MRSP' in col];
if m_check:
    df0.rename(columns={m_check[0]:"MSRP"},inplace=True);

df_cookp=df0[fields0];

for i in range (file_count):
    ifile=files2.loc[i,"Filename"]; #filename
    df=pd.read_excel(ifile, sheet_name="Cooking Products");   #read excel page
    #OUTPUT
    sl=files2.astype(str).loc[i,"Store"]+"_"+files2.astype(str).loc[i,"Location"];    #get store, location strings
    my=files2.astype(str).loc[i,"Month Year"];    #get month year string
    out_fields1=[sl+" "+s+" "+my for s in fields1]; #create labels 1 for output columns
    out_fields2=[sl+" "+s+" "+my for s in fields2]; #create labels 2 for output columns
    out_fields=fields_m+out_fields2+out_fields1;    
    df_cookp1=pd.DataFrame(columns=out_fields);    #creating iteration output dataframe 
    df_cookp1[fields_m]=df[fields_m];  #copying model#   
    df_cookp1[out_fields2]=df[fields2];    #copying occurences, row, column
    if df.empty==False:
        df_cookp1[out_fields1[0]]=df.loc[:,df.columns.str.contains('Sale Price')]; #Copying sale price
        df_cookp1[out_fields1[1]]=df.loc[:,df.columns.str.contains('Assigned Value')];   #copying assigned value
        df_cookp=pd.merge(left=df_cookp, right=df_cookp1, how='outer',left_on='Model #', right_on=str(fields_m[0])); #outer merge of datasets             

if df_cookp.empty==False:    
    df_cookp.to_excel(outfile,'Cooking Products', index=False);

outfile.save();
print("Requested store comparison data can be found in file: "+outfil);
