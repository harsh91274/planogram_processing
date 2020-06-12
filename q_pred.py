#initialization 
from pulp import *
import numpy as np
import pandas as pd
import re
import pdb
import matplotlib.pyplot as plt
from sklearn import preprocessing

#%%
#this is the function to develop a basic model for predicting quantity sold of each item 
#fields_q=['Occurrences','Assigned Value', 'Sale Price'];

def qmodel (df, file_count, files2, fields_q, patha, fields_pred):
    for i in range (file_count):
        l1_mat = np.zeros(shape=(len(df),1));
        
        sl=files2.astype(str).loc[i,"Store"]+"_"+files2.astype(str).loc[i,"Location"];
        my=files2.astype(str).loc[i,"Month Year"];    #get month year string
        out_fields_q=[sl+" "+s+" "+my for s in fields_q];
        
        out_fields_pred=[s+" "+my for s in fields_pred];
        df_pred=pd.DataFrame(columns=out_fields_pred); 
        
        ri=preprocessing.minmax_scale(df[out_fields_q[0]]*df[out_fields_q[1]]);
        
        #define pulp maximization problem
        prob = pulp.LpProblem("Volume Prediction"+my,pulp.LpMaximize);
        total_allowable_units=100; #total units for distribution computation - 100 gives SKU volumes as percentages 
        
        #define the SKU volumes variables
        q=[];  #creating the for sales volume variables, one variable for each SKU (Model #)
        for j in range (df.shape[0]):
            variable_str=str('q'+str(j));
            variable=pulp.LpVariable(str(variable_str), lowBound=0, upBound=(total_allowable_units/2), cat='Continuous'); #minimum of 5 unit sales, max of 50 unit sales for each SKU
            q.append(variable);
        print("Total Number of model decision variables: "+str(len(q)));
        
        #define the optimization function for total sales
        dolla_dolla="";
        for j in range (df.shape[0]):
            formula=q[j]*df.loc[j,out_fields_q[2]]*ri[j];
            dolla_dolla+=formula;
        
        prob+=dolla_dolla;
        print("Optimization function: ", str(dolla_dolla));
        
        #define total SKU volume constraint
                        
        total_unit_constraint="";
        for j in range (df.shape[0]):
            total_unit_constraint+=q[j];
            
        prob+=(total_unit_constraint==total_allowable_units);
        
        #define individual SKU volume constraint
        factor=0.25; #factor range is 0 to 1 [0 means no constraint on min sales, 1 means min sales must be proportional to occurences]; 
        total_occ=df[out_fields_q[0]].sum(); rel_occ=df[out_fields_q[0]].divide(total_occ);
        rel_occ_fac=round(rel_occ*factor*total_allowable_units); #minimum occurence matrix for each SKU
        
        for j in range (df.shape[0]):
            if rel_occ_fac[j]==0:
                prob+=(q[j]==0);
            else: 
                prob+=(q[j]>=rel_occ_fac[j]);
        
        print('Prediction for '+sl+my);        
        print(prob);
        prob.writeLP(sl+'prediction_'+my.replace(" ","_")+'.lp');
        
        opt_result=prob.solve();
        assert opt_result==pulp.LpStatusOptimal;
        print("Status:",LpStatus[prob.status]);
        print("Total $ Sales from 100 units:", value(prob.objective),"$");
        print("Individual Decision Variables:");
        
        j=0;
        for v in prob.variables():
            print(v.name,"=",v.varValue);
            df_pred.loc[j,out_fields_pred]=v.varValue;
            j+=1;
        
        df=pd.concat([df, df_pred], axis=1).reindex(df_pred.index)
        
    return df; 
        #df[out_fields_pred]=prob.variables;
        
        
       
         
        
            
        