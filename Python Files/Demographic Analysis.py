#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pandas as pd
import matplotlib.pyplot as plt
import math
import re
import numpy as np


#Load Dataset - SURVEYS
Experiment_1 = pd.read_csv("/Users/shruthishekar/Documents/GitHub/LLM-MedQA/2) Cleaned Experiment Data/Cleaned - Experiment 1.csv")
Experiment_2 = pd.read_csv("/Users/shruthishekar/Documents/GitHub/LLM-MedQA/2) Cleaned Experiment Data/Cleaned - Experiment 2.csv")
Experiment_3 = pd.read_csv("/Users/shruthishekar/Documents/GitHub/LLM-MedQA/2) Cleaned Experiment Data/Cleaned - Experiment 3.csv")


Experiments = [Experiment_1, Experiment_2, Experiment_3]
Exp_names = ["Experiment 1", "Experiment 2", "Experiment 3"]

# Function to complete a demographic analysis
def Demo_analysis(demo, demo_categories):
    df_perc = pd.DataFrame()
    df_perc.insert(0, "Experiment", 0)

    for c in range(len(demo_categories)):
        category = demo_categories[c]
        df_perc.insert(c+1, str(category), 0)

    Survey_demographics = {}

    for k in range(len(Experiments)):
        survey_list = Experiments[k].loc[:, demo]
        demo_list = list(np.zeros(len(demo_categories)))

        for sample in survey_list:
            for i in range(len(demo_categories)):
                if sample == demo_categories[i]:
                    demo_list[i] = demo_list[i] + 1
        
        Survey_demographics[Exp_names[k]] = (demo_list, sum(demo_list), len(survey_list))
    

    return(print(demo, Survey_demographics))



# Age
Age_categories = ['18-24', '25-34', '35-49', '50-64', '65+']
Demo_analysis('age', Age_categories)


# Ethnicity
Ethn_categories = ['White / Caucasian', 'Hispanic / Latino', 'Black / African American', 'Native American / American Indian', 'Asian / Pacific Islander', 'Other']
Demo_analysis('ethnicity', Ethn_categories)


# Education
Edu_categories = ['Less than high school degree', 'High school degree or equivalent (e.g. GED)', 'Some college but not degree', 'Associate degree', 'Bachelor degree', 'Ph.D. or higher','Trade school', 'Prefer not to say', 'Other']
Demo_analysis('education', Edu_categories)


# Gender
Gender_categories = ['Male', 'Female', 'Non-binary', 'Other', 'Prefer not to response']
Demo_analysis('gender', Gender_categories)


# Health Literacy
Health_Answers = ['Urine', 'Work', 'Treatment', 'Healthy', 'Loss', 'Virus', 'Addiction', 'Birth', 'Dizzy', 'Amount', 'Growth', 'Different', 'Instruction', 'Anxiety', 'Blocked', 'Evaluation', 'Veins', 'Condom']

for j in range(len(Experiments)):
    experiment = Experiments[j]
    pie_chart_labels = ["High Literacy", "Low Literacy"]
    pie_chart_scores = [0,0]

    for row in range(len(experiment)):
        individ_score = 0
        for i in range(18):
            health_ques = "Health_lit_" + str(i+1)
            health_answer = experiment.loc[row, health_ques]
            if health_answer == Health_Answers[i]:
                individ_score = individ_score + 1
        if individ_score > 14:
            pie_chart_scores[0] = pie_chart_scores[0] + 1
        else:
            pie_chart_scores[1] = pie_chart_scores[1] + 1

    fig = plt.figure(figsize =(10, 7))
    plt.pie(pie_chart_scores, labels = pie_chart_labels)
    plt.pie(pie_chart_scores, labels = pie_chart_labels)
    plt.title(Exp_names[j])
    # show plot
    plt.show()




