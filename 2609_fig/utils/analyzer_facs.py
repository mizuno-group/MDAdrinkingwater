# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 14:53:20 2023

@author: I.Azuma (improvement: T.Iwasaka)
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random

def sampling(filein, targets):
    """
    extract targets (cells) population information from the samples (experiments).
    ----------
    filein : str
        'path/to/Flowjo/output/csv/file/csv'
                    Depth                     Name  Statistic  #Cells
            0     NaN  Specimen_001_C1_001.fcs        NaN  100000
            1      >                CD45+dump-       46.6   46585
            2    > >              Single Cells       98.1   45686
        
    targets : list
        e.g. ["main_population","abT","gdT","NKT","NK"]
    samples : list
        e.g. ["Ctrl_1","Ctrl_2","Ctrl_3","Ctrl_4"]

    Returns
    -------
    df : dataframe
                  Ctrl_1    Ctrl_2    Ctrl_3    Ctrl_4
    abT         0.144218  0.354034  0.128803  0.324972
    gdT         0.015701  0.044586  0.017606  0.031974
    NKT         0.207992  0.356555  0.173388  0.291621
    NK          0.073829  0.156051  0.084659  0.148015

    """
    df = pd.read_csv(filein)
    df.index = df["Name"]
    samples = [str(i.split("_")[2]) + "_" + str(i.split("_")[3].split("00")[-1]) for i in df[df.index.str.contains(".fcs")].index.tolist()] # Change if necessary
    df = df.loc[targets,["#Cells"]]
    df = pd.DataFrame(np.array([i[0] for i in df.values]).reshape(-1, len(samples)), columns=samples, index=targets)
    return df

def lym_mye_processing(file_lymp, file_mye, lymph_targets, mye_targets):
    # lymphocyte
    #lymph_targets = ["NK", "CD4T", "CD8T", "B","MainPopulation"]
    df_lymp = sampling(file_lymp, lymph_targets).T
    df_lymp = (df_lymp.T / df_lymp["main_population"]).T
    
    # myeloid
    #mye_targets = ["CD43+", "CD43-","CD43intSSChigh","MainPopulation"]
    df_mye = sampling(file_mye, mye_targets).T
    df_mye = (df_mye.T / df_mye["mainpopulation"]).T
    
    # concat
    del df_mye["mainpopulation"], df_lymp["main_population"]
    df_all = pd.concat([df_lymp, df_mye], axis=1).T
    return df_all

def processing(file_mye, file_lymp, samples):
    # myeloid
    targets = ["CD43+", "CD43-","CD43intSSChigh","MainPopulation"]
    df_mye = sampling(file_mye, targets, samples).T
    df_mye["Mon"] = df_mye["CD43+"]+df_mye["CD43-"]
    df_mye["Neu"] = df_mye["CD43intSSChigh"]
    df_mye = (df_mye.T / df_mye["MainPopulation"]).T
    # lymphocyte
    targets = ["NK", "CD4T", "CD8T", "B","MainPopulation"]
    df_lymp = sampling(file_lymp, targets, samples).T
    df_lymp = (df_lymp.T / df_lymp["MainPopulation"]).T
    # concat
    del df_mye["MainPopulation"], df_lymp["MainPopulation"]
    df_all = pd.concat([df_mye, df_lymp], axis=1).T
    return df_all

def barplot(df, ax='', name='ALT', plottype='', marker=''):
    plt.style.use('default')
    sns.set()
    sns.set_style('whitegrid')
    sns.set_palette('gist_yarg')

    if name == 'ALT' or name == 'AST' or name == 'BW' or name == 'total RNA concentration (ng/ul)':
       plottype = "bar"

    if plottype == 'violin':
        sns.violinplot(data=df, x='day', y=name, inner=None, color='lightcyan')
    else:
        x_position = list(range(len(set(df.loc[:, "day"]))))
        value_mean = [df[df.loc[:, "day"] == i].loc[:, name].mean() for i in set(df.loc[:, "day"])]
        value_std = [df[df.loc[:, "day"] == i].loc[:, name].std() for i in set(df.loc[:, "day"])]
        x_label = [str(i) + " day" for i in set(df.loc[:, "day"])]
        error_bar_set = dict(lw=1, capthick=1, capsize=6)
        ax.bar(x_position, value_mean, yerr=value_std, tick_label=x_label, error_kw=error_bar_set)

    for i in range(len(df)):
        if np.isnan(df.loc[:, name].tolist()[i]):
            pass
        else:
            if df.loc[:, name].tolist()[i] == max(df[df.loc[:, "day"] == df.loc[:, "day"].tolist()[i]].loc[:, name].tolist()):
                color="red"
            elif df.loc[:, name].tolist()[i] == min(df[df.loc[:, "day"] == df.loc[:, "day"].tolist()[i]].loc[:, name].tolist()):
                color="blue"
            else:
                color="black"

            if plottype == 'violin':
                ax.plot(list(set(df.loc[:, "day"])).index(df.loc[:, "day"].tolist()[i])+random.uniform(-0.2, 0.2), df.loc[:, name].tolist()[i], "o", color="teal")
            elif marker == 'text':
                ax.text(list(set(df.loc[:, "day"])).index(df.loc[:, "day"].tolist()[i]) + random.uniform(-0.3, 0.3), df.loc[:, name].tolist()[i], str(df.index.tolist()[i]), color=color, fontsize=11, fontweight=700)
            else:
                ax.plot(list(set(df.loc[:, "day"])).index(df.loc[:, "day"].tolist()[i])+random.uniform(-0.2, 0.2), df.loc[:, name].tolist()[i], "o", color="black")

    if plottype == 'violin':
        x_position = list(range(len(set(df.loc[:, "day"]))))
        value_mean = [df[df.loc[:, "day"] == i].loc[:, name].mean() for i in set(df.loc[:, "day"])]
        ax.plot(x_position, value_mean, color='darkcyan', linestyle="dashed")

    if name == 'ALT' or name == 'AST':
        ax.set_ylabel(name + " (U/L)")
    elif name == 'BW':
        ax.set_ylabel(name + " (g)")
    elif name == 'total RNA concentration (ng/ul)':
        ax.set_ylabel(name)
    else:
        ax.set_ylabel("population")
        
    ax.set_xticklabels([str(i) + " day" for i in set(df.loc[:, "day"])], rotation=45, fontsize=12)
    ax.set_title(name, fontsize=16)
    ax.grid(axis="x")

    if plottype == 'violin':
        plt.ylim(0-0.2*max(df.loc[:, name].tolist()), 1.2*max(df.loc[:, name].tolist()))
        plt.grid(True)
    else:
        plt.ylim(0, 1.1*max(df.loc[:, name].tolist()))

def plot(df, target, title="",  plottype='', marker=''):
    if len(target) < 4:
        fig = plt.figure(figsize=(5*len(target), 5*(len(target)//len(target)+1))) #230610 変更 len(target)+1 ← 4+1
        for i, name in enumerate(target):
            ax = fig.add_subplot(len(target)//len(target)+1, len(target), i+1) #230610 変更 len(target)+1 ← 4+1
            barplot(df, ax=ax, name=name, plottype=plottype, marker=marker)
        fig.suptitle(title+"\n", fontsize=20)
        plt.tight_layout()
        plt.show()
    else:
        fig = plt.figure(figsize=(20, 5*(len(target)//4+1)))
        for i, name in enumerate(target):
            ax = fig.add_subplot(len(target)//4+1, 4, i+1)
            barplot(df, ax=ax, name=name, plottype=plottype, marker=marker)
        fig.suptitle(title+"\n", fontsize=24)
        plt.tight_layout()
        plt.show()

"""
file_mye = "first/20220308_myeloid.csv"
file_lymp = "first/20220308_lymphocyte.csv"
fileout = "first/population.csv"
samples = [
    "Colchicine_1",
    "Colchicine_2",
    "Colchicine_3",
    "Colchicine_4",
    "Ctrl_1",
    "Ctrl_2",
    "Ctrl_3",
    "Ctrl_4",
]
df = processing(file_mye, file_lymp, samples)
"""