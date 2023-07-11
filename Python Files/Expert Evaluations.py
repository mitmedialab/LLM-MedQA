#!/usr/bin/env python3
# -*- coding: utf-8 -*-



import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
from statsmodels.formula.api import ols
from scipy.stats import ttest_ind


# Finding compiled scores of experts
# =============================================================================
Expert_Eval_Data = pd.read_csv("/Users/shruthishekar/Documents/GitHub/LLM-MedQA/Expert Evals Dataset.csv")

Expert_Eval_Scores = pd.DataFrame()
Expert_Eval_Scores.insert(0, 'Medical Domain', 0)
Expert_Eval_Scores.insert(1, 'Test', 0)
Expert_Eval_Scores.insert(2, 'Score', 0)
Expert_Eval_Scores.insert(3, 'Type', 0)
Expert_Eval_Scores.insert(4, 'Source', 0)

for row_number in range(len(Expert_Eval_Data.index)):
    temp_row_list = Expert_Eval_Data.loc[row_number, :].values.flatten().tolist()
    scores = [temp_row_list[2], temp_row_list[3], temp_row_list[4]]
    final_score = 0

    for score in scores:
        if score == "No":
            final_score = final_score + 1
        if score == "Maybe":
            final_score = final_score + 2
        if score == "Yes":
            final_score = final_score + 3
    
    Expert_Eval_Scores.loc[len(Expert_Eval_Scores)] = [temp_row_list[0], temp_row_list[1], final_score, temp_row_list[5], temp_row_list[6]]

Expert_Eval_Scores.to_csv("/work/4) Expert Evaluations/Expert Eval Scores.csv")


Expert_Eval_Accuracy = Expert_Eval_Scores[Expert_Eval_Scores['Test'] == "Accuracy"]
Expert_Eval_Strength = Expert_Eval_Scores[Expert_Eval_Scores['Test'] == "Strength"]
Expert_Eval_Completeness = Expert_Eval_Scores[Expert_Eval_Scores['Test'] == "Completeness"]
# =============================================================================




# Performing Two-way ANOVA 
# =============================================================================
# Accuracy
model = ols('Score ~ C(Type) + C(Source) +\
C(Type):C(Source)',
            data=Expert_Eval_Accuracy).fit()
result = sm.stats.anova_lm(model, type=2)
print(result)



# Strength
model = ols('Score ~ C(Type) + C(Source) +\
C(Type):C(Source)',
            data=Expert_Eval_Strength).fit()
result = sm.stats.anova_lm(model, type=2)
print(result)



# Completeness
model = ols('Score ~ C(Type) + C(Source) +\
C(Type):C(Source)',
            data=Expert_Eval_Completeness).fit()
result = sm.stats.anova_lm(model, type=2)
print(result)
# =============================================================================




# T - Test
# =============================================================================
Tests = ["Accuracy", "Strength", "Completeness"]

df = pd.DataFrame()
df.insert(0, "Test", 0) 
df.insert(1, "Type", 0) 
df.insert(2, "AI: Mean", 0) 
df.insert(3, "AI: Std. Dev", 0)
df.insert(4, "Doc: Mean", 0) 
df.insert(5, "Doc: Std. Dev", 0)
df.insert(6, "AI - Doc: P-value", 0)

for test in Tests:
    Expert_Eval_test = Expert_Eval_Scores[Expert_Eval_Scores['Test'] == test]

    blind_dataset = Expert_Eval_test[Expert_Eval_test["Type"] == "Blind"]
    blind_AI_dataset = blind_dataset[blind_dataset["Source"] == "AI"]
    blind_Doc_dataset = blind_dataset[blind_dataset["Source"] == "Doc"]
    blind_AI_array = np.array(blind_AI_dataset["Score"])
    blind_Doc_array = np.array(blind_Doc_dataset["Score"])

    blind_AI_mean = np.mean(blind_AI_array)
    blind_AI_stddev = np.std(blind_AI_array)
    blind_Doc_mean = np.mean(blind_Doc_array)
    blind_Doc_stddev = np.std(blind_Doc_array)

    blind_Ttest = ttest_ind(a = blind_AI_array, b = blind_Doc_array)
    df.loc[len(df.index)] = [test, "Blind", blind_AI_mean, blind_AI_stddev, blind_Doc_mean, blind_Doc_stddev, blind_Ttest[1]]

    non_blind_dataset = Expert_Eval_test[Expert_Eval_test["Type"] == "Non-Blind"]
    non_blind_AI_dataset = non_blind_dataset[non_blind_dataset["Source"] == "AI"]
    non_blind_Doc_dataset = non_blind_dataset[non_blind_dataset["Source"] == "Doc"]
    non_blind_AI_array = np.array(non_blind_AI_dataset["Score"])
    non_blind_Doc_array = np.array(non_blind_Doc_dataset["Score"])

    non_blind_AI_mean = np.mean(non_blind_AI_array)
    non_blind_AI_stddev = np.std(non_blind_AI_array)
    non_blind_Doc_mean = np.mean(non_blind_Doc_array)
    non_blind_Doc_stddev = np.std(non_blind_Doc_array)

    non_blind_Ttest = ttest_ind(a = non_blind_AI_array, b = non_blind_Doc_array)
    df.loc[len(df.index)] = [test, "Non-Blind", non_blind_AI_mean, non_blind_AI_stddev, non_blind_Doc_mean, non_blind_Doc_stddev, non_blind_Ttest[1]]
# =============================================================================


display(df)