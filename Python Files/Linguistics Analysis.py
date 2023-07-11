#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
import random
import os
import json
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import readability


Health_Q_A = pd.read_csv("/work/Question-Response Pairs/Health Q+R.csv")

Responses = list(Health_Q_A.loc[:, "Response"])
Med_Domains = list(Health_Q_A.loc[:, "Medical Domain"]) 
Resp_Types = list(Health_Q_A.loc[:, "Response Type"]) 


palette = ["lightgrey", "darkseagreen", "lightcoral"]


# Stat function / libraries
# ============================================================================

from IPython.display import clear_output 
clear_output()

import itertools
import scikit_posthocs as sp
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def prerun_stats (sample_keys, group_label, data, y, stats_viz=False):

  ## Stats
  import scipy.stats as stats
  from pingouin import welch_anova, pairwise_gameshowell, pairwise_tukey
  from statistics import stdev
  import numpy as np
  
  MIN_SAMPLE_SIZE = 25
  TOLERANCE = 0.15

  sample_data = [data.copy().apply(lambda z: z[y] if z[group_label] == key else None, axis=1).dropna() for key in sample_keys]
  #sample_data = [data[data[group_label]==key][y] for key in sample_keys]


  sample_data_w_keys = pd.concat([pd.DataFrame({y:data.values, group_label:sample_keys[i]}) for i, data in enumerate(sample_data.copy())], axis=0, ignore_index=True)
  
  if stats_viz is True:
    print(f"Running stats between the samples: {sample_keys}")

  # Means for each sample group
  means_table = data[group_label].value_counts()

  # Check if *all* data points for each sample group are over 25
  sample_sizes_sufficient = all([sample > MIN_SAMPLE_SIZE for sample in means_table])

  # Check if means are equal within the TOLERANCE for each sample group
  sample_sizes_equal = all([abs(sample1 - sample2) < np.mean(means_table) * TOLERANCE for sample1, sample2 in itertools.combinations(means_table, 2)])

  # Dunn Test
  dunn = sp.posthoc_dunn(sample_data, p_adjust='bonferroni')
  replacer = {i+1:key for i, key in enumerate(sample_keys)}
  dunn.rename(columns = replacer, index=replacer, inplace=True)

  # Compile all stats into list
  statz = {'sample_sizes_sufficient': sample_sizes_sufficient,
          'sample_sizes_equal':      sample_sizes_equal,
          'shapiro':                 stats.shapiro(data[y]),
          'levene':                  stats.levene(*sample_data),
          'f_oneway':                stats.f_oneway(*sample_data),
          'kruskal':                 stats.kruskal(*sample_data),
          'welch_anova':             welch_anova(dv=y, between=group_label, data=sample_data_w_keys),
          'gameshowell':             pairwise_gameshowell(dv=y, between=group_label, data=sample_data_w_keys).round(3),
          'tukey':                   pairwise_tukey(dv=y, between=group_label, data=sample_data_w_keys).round(3),
          'dunn':                    dunn,
          'mean_std':                {key:{'mean' : np.mean(population), \
                                           'std' : stats.tstd(population)} for key, population in zip(sample_keys, sample_data)},
  }

  return statz



def stats_tree(sample_keys, sample_sizes_sufficient, sample_sizes_equal, shapiro, levene, f_oneway, kruskal, welch_anova, gameshowell, tukey, dunn, mean_std=None, stats_viz=False):

  import itertools

  ALPHA = 0.05
  indent = '   '


  if sample_sizes_sufficient or shapiro.pvalue > ALPHA:
    if stats_viz is True:
      print("> Sample size sufficient" if sample_sizes_sufficient else f">Sample size insufficient but *normality is met*: w_shapiro={shapiro.statistic}, p_shapiro={shapiro.pvalue}")

    if sample_sizes_equal or levene.pvalue > ALPHA:
      if stats_viz is True:
        print(f"{indent*1}> Sample sizes equal" if sample_sizes_equal else f"{indent*1}>Sample sizes not equal but *homogeneity is met*: s_levene={levene.statistic}, p_levene={levene.pvalue}")

      if f_oneway.pvalue < ALPHA:
        if stats_viz is True:
          print(f"{indent*2}> Thus running BASIC ANOVA:\n{indent*3}> Basic ANOVA (f_oneway) *significant*: s_bANOVA={f_oneway.statistic}, p_bANOVA={f_oneway.pvalue}")
          print(f"\n> Thus running Tukey Test:")
          print(tukey)
          print(f"mean_std: {mean_std}")

        pairs = (zip(tukey["A"].tolist(), tukey["B"].tolist()))
        p_values = tukey["p-tukey"].tolist()
        
        return pairs, p_values

      elif f_oneway.pvalue > ALPHA:
        if stats_viz is True:
          print(f"{indent*2}> Thus running BASIC ANOVA:\n{indent*3}> Basic ANOVA *NOT SIGNIFICANT*: s_bANOVA={f_oneway.statistic}, p_bANOVA={f_oneway.pvalue}" if stats_viz is True else "")
          print(f"mean_std: {mean_std}" )

        pairs = (zip(tukey["A"].tolist(), tukey["B"].tolist()))
        p_values = tukey["p-tukey"].tolist()

        return pairs, p_values

    elif not sample_sizes_equal or levene.pvalue < ALPHA:
      if stats_viz is True:
        print(f"{indent*1}> Sample sizes are unequal and homogeneity *NOT MET*: w_levene={levene.statistic}, p_levene={levene.pvalue}")

      if welch_anova['p-unc'][0] < ALPHA:
        if stats_viz is True:
          print(f"{indent*3}> Thus running ANOVA Welch:\n{indent*4}> ANOVA Welch *SIGNIFICANT*: welch=\n{welch_anova}")#{welch_anova['F']}, p_welch={welch_anova['p-unc'][0]}")
          print(f"\n>Thus running Games-Howell test:")
          print(gameshowell)
          print(f"mean_std: {mean_std}")
        
        pairs = (zip(gameshowell["A"].tolist(), gameshowell["B"].tolist()))
        p_values = gameshowell["pval"].tolist()

        return pairs, p_values

      elif welch_anova['p-unc'][0] > ALPHA:
        if stats_viz is True:
          print(f"{indent*3}> Thus running ANOVA Welch:\n{indent*4}> ANOVA Welch *NOT SIGNIFICANT*: welch=\n{welch_anova}")#F_welch={welch_anova['F']}, p_welch={welch_anova['p-unc'][0]}")
          print(f"mean_std: {mean_std}")

        pairs = (zip(gameshowell["A"].tolist(), gameshowell["B"].tolist()))
        p_values = gameshowell["pval"].tolist()

        return pairs, p_values

  elif not sample_sizes_sufficient or shapiro.pvalue < ALPHA:
    if stats_viz is True:
      print(f"{indent*1}> Both minimum sample size and normality were *NOT MET*: w_shapiro={shapiro.statistic}, p_shapiro={shapiro.pvalue}")

    if kruskal.pvalue < ALPHA:
      if stats_viz is True:
        print(f"{indent*2}> Thus running Kruskal Wallis:\n Kruskal Wallis *SIGNIFICANT*: s_kruskal={kruskal.statistic}, p_kruskal={kruskal.pvalue}")
        print(f"{indent*2}> Running DUNN test:")
        print(dunn)
        print(f"mean_std: {mean_std}")
      
      pairs = [p for p in itertools.combinations(sample_keys, 2)]
      p_values = [dunn.at[x[0],x[1]] for x in pairs]

      return pairs, p_values

    elif kruskal.pvalue > ALPHA:
      if stats_viz is True:
        print(f"{indent*2}> Thus running Kruskal Wallis:\n{indent*3}>Kruskal Wallis *NOT SIGNIFICANT*: s_kruskal={kruskal.statistic}, p_kruskal={kruskal.pvalue}")
        print(f"mean_std: {mean_std}")
      
      pairs = [p for p in itertools.combinations(sample_keys, 2)]
      p_values = [dunn.at[x[0],x[1]] for x in pairs]

      return pairs, p_values



def plot_stats(pairs, p_values, y, x, hue=None, figsize=[4,8], ylim=None, **kwgs):

  from statannotations.Annotator import Annotator

  if figsize is None and hue is not None:
    figsize = [data[x].nunique()*data[hue].nunique()*1.2, 8]
  elif figsize is None and hue is None:
    figsize = [data[x].nunique()*1.2, 8]

  # plot 
  fig, ax = plt.subplots(figsize=figsize)
  plt.tight_layout()
  sns.barplot(ax=ax, **plot_params)
  #annot = Annotator(ax, pairs, **plot_params)
  #annot.configure(text_format="star", loc='outside', line_offset=True, line_offset_to_group=True, line_height=.01)
  #annot.set_pvalues_and_annotate(p_values)

  # styling
  #ax.text(x=0.5, y=-0.3, s=lbl, fontsize=10, ha='center', va='bottom', transform=ax.transAxes)

  #ax.set_title(f"{y} for {x}")
  #if hue is not None:
    #ax.set_title(f"{y} for {x} by {hue.lower()}")


  if ylim is not None:
    ax.set_ylim(ylim)

  ax.get_legend().remove()
  ax.set_xlabel('')
  ax.set_ylabel('')

  plt.show()


def stats(data, y, x, hue=None, graph_viz=True, stats_viz=False, ylim=None, figsize=None, **kwgs):

  target_data = [data] # The data to be used for statistical analysis
  target_label = x # The column name with the groups to be compared between
  within_sample = [None] # The value of a column for hue groups to be compared within 

  if hue is not None:

    within_sample = data[x].unique()
    target_data = [data[data[x]==group] for group in within_sample]
    target_label = hue

  pairs = []
  p_values = []

  for i, data in enumerate(target_data):
    
    if stats_viz is True:
      print(f"----\nWithin the '{within_sample[i]}' group of '{x}':\n----" if len(within_sample) > 1 else "----")

    sample_keys = [key for key in data[target_label].unique()]
    stat_results = prerun_stats (sample_keys, target_label, data, y, stats_viz=stats_viz)
    pair, p_value = stats_tree(sample_keys, **stat_results, stats_viz=stats_viz)

    for pair_item, p_value_item in zip(pair, p_value):
      if hue is not None:
        pair_item = [pair_w_sample_label for pair_w_sample_label in itertools.product([within_sample[i]],pair_item)]
      pairs.append(pair_item)
      p_values.append(p_value_item)
    print("----" if stats_viz is True else "")

  if graph_viz:
    plot_stats(pairs, p_values, ylim=ylim, figsize=figsize, **plot_params)

print("Installation Complete")
# =============================================================================


# WORD COUNT
# =============================================================================
df_wc = pd.DataFrame()
df_wc.insert(0, "Medical Domain", 0)
df_wc.insert(1, "Response Type", 0)
df_wc.insert(2, "Number", 0)
df_wc.insert(3, "Test", 0)

def word_count(string):
    return(len(string.strip().split(" ")))


for i in range(len(Responses)):
    resp = Responses[i]
    word_c = word_count(resp)
    df_wc.loc[len(df_wc)] = [Med_Domains[i], Resp_Types[i], word_c, "Word Count"]
    

plot_params = {
    'x': "Test",
    'y' : "Number",
    'hue' : 'Response Type',
    'data' : df_wc,
    'palette': palette,
    'order' : ['Word Count'],
    'hue_order' : ['Doctor', 'High', 'Low '],
}
stats(**plot_params, graph_viz=True, ylim=[0,60], figsize=[5,5], stats_viz=True)
# =============================================================================



# READABILITY
# =============================================================================
df_read = pd.DataFrame()
df_read.insert(0, "Medical Domain", 0)
df_read.insert(1, "Response Type", 0)
df_read.insert(2, "Response", 0)
df_read.insert(3, "Number", 0)
df_read.insert(4, "Test", 0)


for i in range(len(Responses)):
    resp = Responses[i]
    result = readability.getmeasures(resp, lang='en')
    #print(result)
    Read_GunningFogIndex = result['readability grades']['FleschReadingEase']
    df_read.loc[len(df_read)] = [Med_Domains[i], Resp_Types[i], resp, Read_GunningFogIndex, "Readability"]
    

plot_params = {
    'x': "Test",
    'y' : "Number",
    'hue' : 'Response Type',
    'data' : df_read,
    'palette': palette,
    'order' : ['Readability'],
    'hue_order' : ['Doctor', 'High', 'Low '],
}
stats(**plot_params, graph_viz=True, ylim=[0,40], figsize=[5,5], stats_viz=True)
# =============================================================================



# SENTIMENT
# =============================================================================
df_sen = pd.DataFrame()
df_sen.insert(0, "Medical Domain", 0)
df_sen.insert(1, "Response Type", 0)
df_sen.insert(2, "Number", 0)
df_sen.insert(3, "Test", 0)

analyzer = SentimentIntensityAnalyzer()

for i in range(len(Responses)):
    resp = Responses[i]
    vader_sen = analyzer.polarity_scores(resp)
    vader_sen_ = vader_sen.get("compound")
    df_sen.loc[len(df_sen)] = [Med_Domains[i], Resp_Types[i], vader_sen_, "Sentiment"]
    

plot_params = {
    'x': "Test",
    'y' : "Number",
    'hue' : 'Response Type',
    'data' : df_sen,
    'palette': palette,
    'order' : ['Sentiment'],
    'hue_order' : ['Doctor', 'High', 'Low '],
}
stats(**plot_params, graph_viz=True, ylim=[-1,1], figsize=[5,5], stats_viz=True)
# =============================================================================
