#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 16:30:30 2023

@author: shruthishekar
"""

import pandas as pd
from scipy.stats import ttest_ind
import matplotlib.pyplot as plt
import math
import re
import numpy as np
from itertools import combinations
import seaborn as snsar


Experiment_1_data = pd.read_csv("/Users/shruthishekar/Documents/GitHub/LLM-MedQA/3) Organized Experiment Data/Experiment 1.csv")
Experiment_1_2_data = pd.read_csv("/Users/shruthishekar/Documents/GitHub/LLM-MedQA/3) Organized Experiment Data/Experiment 1 - 2.csv")
Experiment_2_data = pd.read_csv("/Users/shruthishekar/Documents/GitHub/LLM-MedQA/3) Organized Experiment Data/Experiment 2.csv")
Experiment_3_data = pd.read_csv("/Users/shruthishekar/Documents/GitHub/LLM-MedQA/3) Organized Experiment Data/Experiment 3.csv")

Question_Names_Exp_1 = ["Und_Q", "Und_R", "AI_or_Human", "Confidence"]
Question_Names_Exp_2_3 = ["Und_Q", "Und_R", "Valid", "Trust", "Satis", "Follow", "Action", "Info"]
Response_Source = ["Doctor", "High Accuracy AI", "Low Accuracy AI"]
Random_Labels = ['Doctor', 'AI', 'Doctor + AI']




# EXPERIMENT 1-
# =============================================================================
palette = ["lightgrey", "darkseagreen", "lightcoral"]


# Understanding Question / Response Graphs

for ques in Question_Names_Exp_1[0:-2]:
    temp_ds = Experiment_1_data[Experiment_1_data["Question Type"] == ques]

    temp_ds_D_array = np.array(temp_ds[temp_ds["Response Source"] == "Doctor"]["Response Scores"])
    temp_ds_H_array = np.array(temp_ds[temp_ds["Response Source"] == "High Accuracy AI"]["Response Scores"])
    temp_ds_L_array = np.array(temp_ds[temp_ds["Response Source"] == "Low Accuracy AI"]["Response Scores"])

    print(ques)
    print("Doctor - ", "Mean: ", np.mean(temp_ds_D_array), "SD :", np.std(temp_ds_D_array))
    print("High Accuracy AI - ", "Mean: ", np.mean(temp_ds_H_array), "SD :", np.std(temp_ds_H_array))
    print("Low Accuracy AI - ", "Mean: ", np.mean(temp_ds_L_array), "SD :", np.std(temp_ds_L_array))

    plot_params = {
        'x': "Question Type",
        'y' : "Response Scores",
        'hue' : 'Response Source',
        'data' : temp_ds,
        'palette': palette,
        'order' : [ques],
        'hue_order' : ['Doctor', 'High Accuracy AI', 'Low Accuracy AI'],
    }
    fig, ax = plt.subplots(figsize=[5,5])
    plt.tight_layout()
    snsar.barplot(ax=ax, **plot_params)
    ax.set_ylim([1,5])
    ax.legend(bbox_to_anchor=(1.05, 1.0),loc='upper left')
    
    
    
# AI or Human Graphs (Source Determination)

temp_ds_D_array = np.array(Experiment_1_2_data[Experiment_1_2_data["Response Source"] == "Doctor"]["Response Scores"])
temp_ds_H_array = np.array(Experiment_1_2_data[Experiment_1_2_data["Response Source"] == "High Accuracy AI"]["Response Scores"])
temp_ds_L_array = np.array(Experiment_1_2_data[Experiment_1_2_data["Response Source"] == "Low Accuracy AI"]["Response Scores"])

print("AI or Human")
print("Doctor - ", "Mean: ", np.mean(temp_ds_D_array), "SD :", np.std(temp_ds_D_array))
print("High Accuracy AI - ", "Mean: ", np.mean(temp_ds_H_array), "SD :", np.std(temp_ds_H_array))
print("Low Accuracy AI - ", "Mean: ", np.mean(temp_ds_L_array), "SD :", np.std(temp_ds_L_array))

plot_params = {
    'x': "Question Type",
    'y' : "Response Scores",
    'hue' : 'Response Source',
    'data' : Experiment_1_2_data,
    'palette': palette,
    'order' : ["AI_or_Human"],
    'hue_order' : ['Doctor', 'High Accuracy AI', 'Low Accuracy AI'],
}

fig, ax = plt.subplots(figsize=[5,5])
plt.tight_layout()
snsar.barplot(ax=ax, **plot_params)
ax.set_ylim([0,1])
ax.legend(bbox_to_anchor=(1.05, 1.0),loc='upper left')



# AI or Human Confidence Graphs

palette_2 = ['#acc8d7', '#779eb2']

for j in range(len(Response_Source)):
    source = Response_Source[j]
    temp_ds = Experiment_1_2_data[Experiment_1_2_data["Response Source"] == source]

    temp_ds_correct_array = np.array(temp_ds[temp_ds["Incorrect/Correct"] == "Correct"]["Confidence"])
    temp_ds_incorrect_array = np.array(temp_ds[temp_ds["Incorrect/Correct"] == "Incorrect"]["Confidence"])

    print(source)
    print("Correct - ", "Mean: ", np.mean(temp_ds_correct_array), "SD :", np.std(temp_ds_correct_array))
    print("Incorrect - ", "Mean: ", np.mean(temp_ds_incorrect_array), "SD :", np.std(temp_ds_incorrect_array))

    plot_params = {
        'x': "Response Source",
        'y' : "Confidence",
        'hue' : 'Incorrect/Correct',
        'data' : temp_ds,
        'palette': palette_2,
        'order' : [source],
        'hue_order' : ['Correct', 'Incorrect'],

    }
    fig, ax = plt.subplots(figsize=[2,5])
    plt.tight_layout()
    snsar.barplot(ax=ax, **plot_params)
    ax.set_ylim([1,5])
    ax.legend(bbox_to_anchor=(1.05, 1.0),loc='upper left')
# =============================================================================





# EXPERIMENT 2
# =============================================================================
for ques in Question_Names_Exp_2_3:

    temp_ds = Experiment_2_data[Experiment_2_data["Question Type"] == ques]

    temp_ds_D_array = np.array(temp_ds[temp_ds["Response Source"] == "Doctor"]["Response Scores"])
    temp_ds_H_array = np.array(temp_ds[temp_ds["Response Source"] == "High Accuracy AI"]["Response Scores"])
    temp_ds_L_array = np.array(temp_ds[temp_ds["Response Source"] == "Low Accuracy AI"]["Response Scores"])

    print(ques)
    print("Doctor - ", "Mean: ", np.mean(temp_ds_D_array), "SD :", np.std(temp_ds_D_array))
    print("High Accuracy AI - ", "Mean: ", np.mean(temp_ds_H_array), "SD :", np.std(temp_ds_H_array))
    print("Low Accuracy AI - ", "Mean: ", np.mean(temp_ds_L_array), "SD :", np.std(temp_ds_L_array))

    if ques != "Valid":
        plot_params = {
            'x': "Question Type",
            'y' : "Response Scores",
            'hue' : 'Response Source',
            'data' : temp_ds,
            'palette': palette,
            'order' : [ques],
            'hue_order' : ['Doctor', 'High Accuracy AI', 'Low Accuracy AI'],
        }
        fig, ax = plt.subplots(figsize=[5,5])
        plt.tight_layout()
        snsar.barplot(ax=ax, **plot_params)
        ax.set_ylim([1,5])
        ax.legend(bbox_to_anchor=(1.05, 1.0),loc='upper left')

    else:
        plot_params = {
            'x': "Question Type",
            'y' : "Response Scores",
            'hue' : 'Response Source',
            'data' : temp_ds,
            'palette': palette,
            'order' : [ques],
            'hue_order' : ['Doctor', 'High Accuracy AI', 'Low Accuracy AI'],
        }
        fig, ax = plt.subplots(figsize=[5,5])
        plt.tight_layout()
        snsar.barplot(ax=ax, **plot_params)
        ax.set_ylim([0,1])
        ax.legend(bbox_to_anchor=(1.05, 1.0),loc='upper left')
# =============================================================================





# EXPERIMENT 3
# =============================================================================
palette_3_H = ['#dbe8d7', '#b8d1ae', 'darkseagreen']
palette_3_L = ['#ffd6d6', '#ffb3b3', 'lightcoral']
palette_3_D = ['lightgray', 'darkgray', 'dimgray']

palettes_3 = [palette_3_D, palette_3_H, palette_3_L]

for ques in Question_Names_Exp_2_3:
    temp_ds = Experiment_3_data[Experiment_3_data["Question Type"] == ques]

    Doctor = ques + " - D"
    High_Accuracy_AI = ques + " - H"
    Low_Accuracy_AI = ques + " - L"

    Sources = [Doctor, High_Accuracy_AI, Low_Accuracy_AI]

    temp_ds_D = temp_ds[temp_ds["Response Source"] == Sources[0]]
    temp_ds_H = temp_ds[temp_ds["Response Source"] == Sources[1]]
    temp_ds_L = temp_ds[temp_ds["Response Source"] == Sources[2]]

    temp_ds_list = [temp_ds_D, temp_ds_H, temp_ds_L]

    print(ques)
    print("Doctor - ", "Mean: ", np.mean(np.array(temp_ds_D["Response Scores"])), "SD :", np.std((np.array(temp_ds_D["Response Scores"]))))
    print("High Accuracy AI - ", "Mean: ", np.mean(np.array(temp_ds_H["Response Scores"])), "SD :", np.std((np.array(temp_ds_H["Response Scores"]))))
    print("Low Accuracy AI - ", "Mean: ", np.mean(np.array(temp_ds_L["Response Scores"])), "SD :", np.std((np.array(temp_ds_L["Response Scores"]))))


    for i in range(len(temp_ds_list)):
        current_ds = temp_ds_list[i]
        source = Sources[i]
        palette = palettes_3[i]

        if ques != "Valid":
            y_lim = [1,5]
        else:
            y_lim = [0,1]

        plot_params = {
            'x': 'Response Source',
            'y' : "Response Scores",
            'hue' : "Random Header",
            'data' : current_ds,
            'palette': palette,
            'order' : [Sources[i]],
            'hue_order' : Random_Labels,
        }
        fig, ax = plt.subplots(figsize=[5,5])
        plt.tight_layout()
        snsar.barplot(ax=ax, **plot_params)
        ax.set_ylim(y_lim)
        ax.legend(bbox_to_anchor=(1.05, 1.0),loc='upper left')
# =============================================================================
