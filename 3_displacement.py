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
from store_comparison2 import *
import l2c

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
