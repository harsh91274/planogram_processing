#Evolution in same store/same location
#code to plot up store comparison data
#%matplotlib inline

import statistics as stats
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import numpy as np
import pandas as pd
import pdb
import os
import seaborn as sns
from pathlib import Path
#from mpltools import color

large = 22; med = 16; small = 12
params = {'axes.titlesize': large,
          'legend.fontsize': med,
          'figure.figsize': (16, 10),
          'axes.labelsize': med,
          'axes.titlesize': med,
          'xtick.labelsize': med,
          'ytick.labelsize': med,
          'figure.titlesize': large}
plt.rcParams.update(params)
plt.style.use('seaborn-whitegrid')
sns.set_style("white")

patha=store+"_"+loc;
Path("figures/"+patha).mkdir(parents=True, exist_ok=True)
path_plot=os.path.join(os.getcwd(),"figures/"+patha);
#%%
#dishwashers
drop_cols = [col for col in df_dw.columns if 'Planogram' in col];
df_dw_plot_master=df_dw.dropna(subset=drop_cols, how='all').reset_index(drop=True);
df_dw_plot_master["Brand / Appliance"]=df_dw_plot_master["Brand / Appliance"].str.strip();
no_times=len(files2);
symbols=["o","s","*","P","^","v"];

#figure 1: price vs assigned value
fig = plt.figure(figsize = (12, 6))
ax = fig.add_subplot(1,1,1,)

for i in range (no_times):
    search_str=files2.get_value(i,"Month Year");
    for cat in sorted(list(df_dw_plot_master["Brand / Appliance"].unique())):
        xcols=[col for col in df_dw_plot_master.columns if "Sale Price "+search_str in col]
        ycols=[col for col in df_dw_plot_master.columns if "Assigned Value "+search_str in col]
        
        price=df_dw_plot_master[df_dw_plot_master["Brand / Appliance"]==cat][xcols];
        assign_val=df_dw_plot_master[df_dw_plot_master["Brand / Appliance"]==cat][ycols];
        
        mean_price=np.around(np.mean(price.values),decimals=1);
        std_price=np.around(np.std(price.values),decimals=1);
        mean_av=np.around(np.mean(assign_val.values),decimals=1);
        cata=cat+" "+"mean: "+str(mean_price)+"$ , avg_pos: "+str(mean_av);
        
        ax.scatter(price, assign_val, label = cata, s = 50, marker=symbols[i],edgecolors='k', alpha=0.55);
        
ax.set_xlabel("Price ($)") 
ax.set_ylabel("Assigned Value");
ax.set_title("Scatter plot of Price vs Assigned Value")
ax.grid();
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
ax.legend(by_label.values(), by_label.keys(), loc = "best", fontsize = 10, frameon=True)
fname1=os.path.join(path_plot,"wash_dryer_price_vs_value.jpg");
fname2=os.path.join(path_plot,"wash_dryer_price_vs_value.pdf");
plt.savefig(fname1, facecolor='w', edgecolor='k'); 
plt.savefig(fname2, facecolor='w', edgecolor='k'); 
#%%
#figure 2: price variation over time
fig2=plt.figure(figsize = (9, 9))
ax2=fig2.add_subplot(1,1,1)

ycols=df_dw_plot_master["Model #"];
xcols=[col for col in df_dw_plot_master.columns if "Sale Price " in col];
price2=df_dw_plot_master[xcols];
colormap=cm.rainbow(np.linspace(0,1,len(price2)))

for i in df_dw_plot_master.index:
    for j in range (price2.shape[1]):
        ax2.plot(price2.iloc[i,j],i,alpha=0.5,color=colormap[i,:],marker=symbols[j],linestyle=':');
    
    if i==0:
        plt.legend(xcols, fontsize="small",loc="best", frameon=True, facecolor="white");
    
ax2.grid(which='both',axis='y');
ax2.set_yticks(np.arange(len(df_dw_plot_master)));
ax2.set_yticklabels(df_dw_plot_master["Model #"],fontsize="medium"); 
ax2.set_xlabel("Price ($)") 
ax2.set_title("Price Change over time")      
#ax2.legend(symbols[0:price2.shape[1]],xcols); #plt.show();

fname1=os.path.join(path_plot,"wash_dryer_price_changes.jpg");
fname2=os.path.join(path_plot,"wash_dryer_price_changes.pdf");
plt.savefig(fname1, facecolor='w', edgecolor='k'); 
plt.savefig(fname2, facecolor='w', edgecolor='k');         

#%%
#figure 3: position variation over time
fig3=plt.figure(figsize = (9, 9))
ax3=fig3.add_subplot(1,1,1);

ycols=df_dw_plot_master["Model #"];
xcols=[col for col in df_dw_plot_master.columns if "Assigned Value " in col];
av2=df_dw_plot_master[xcols];
colormap=cm.rainbow(np.linspace(0,1,len(av2)))

for i in df_dw_plot_master.index:
    for j in range (price2.shape[1]):
        ax3.plot(av2.iloc[i,j],i,alpha=0.5,color=colormap[i,:],marker=symbols[j],linestyle=':');
    
    if i==0:
        plt.legend(xcols, fontsize="small",loc="best",frameon=True,facecolor="white");
    
ax3.grid(which='both',axis='y');
ax3.set_yticks(np.arange(len(df_dw_plot_master)));
ax3.set_yticklabels(df_dw_plot_master["Model #"],fontsize="medium"); 
ax3.set_xlabel("Analyst Assigned Value") 
ax3.set_title("Assigned Value Change over time")      
#ax2.legend(symbols[0:price2.shape[1]],xcols); #plt.show();

fname1=os.path.join(path_plot,"wash_dryer_assigned_value_change.jpg");
fname2=os.path.join(path_plot,"wash_dryer_assigned_value_change.pdf");
plt.savefig(fname1, facecolor='w', edgecolor='k'); 
plt.savefig(fname2, facecolor='w', edgecolor='k'); 

#%%
#pairwise plot

fig4=plt.figure(figsize=(12,12));sns.set(style="ticks", color_codes=True);

cols=[];
for i in range(price2.shape[1]):
    cols0=[col for col in df_dw_plot_master.columns if "Brand / Appliance" in col];
    cols1=[col for col in df_dw_plot_master.columns if "Occurrences "+files2.iloc[i,3] in col];
    cols2=[col for col in df_dw_plot_master.columns if "Sale Price "+files2.iloc[i,3] in col];
    cols3=[col for col in df_dw_plot_master.columns if "Assigned Value "+files2.iloc[i,3] in col];
        
    #df_pairplot1=df_dw_plot_master[[cols0[0],cols1[0],cols2[0],cols3[0]]];
    df_pairplot1=pd.DataFrame({'Brand / Appliance':df_dw_plot_master[cols0[0]], 'Occurences': df_dw_plot_master[cols1[0]], 'Sale Price ($)': df_dw_plot_master[cols2[0]], 'Assigned Value': df_dw_plot_master[cols3[0]]});
    
    pp=sns.pairplot(df_pairplot1, markers=symbols[i],size=5, hue="Brand / Appliance", plot_kws = {'alpha': 0.7, 's': 80, 'edgecolor': 'k'}, palette="husl");

pp.fig.suptitle("pairwise_correlation");          
fname1=os.path.join(path_plot,"wash_dryer_correlation_matrix.jpg");
fname2=os.path.join(path_plot,"wash_dryer_correlation_matrix.pdf");
pp.savefig(fname1);
pp.savefig(fname2);
   
    
    
    
    
    
    
    
    
    
    
    
    

        
