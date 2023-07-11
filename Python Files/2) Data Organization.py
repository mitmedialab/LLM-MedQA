#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pandas as pd
import random
import os
import json
import re
import matplotlib.pyplot as plt


#Load Dataset
Experiment_1 = pd.read_csv("/Users/shruthishekar/Documents/GitHub/LLM-MedQA/2) Cleaned Experiment Data/Cleaned - Experiment 1.csv")
Experiment_2 = pd.read_csv("/Users/shruthishekar/Documents/GitHub/LLM-MedQA/2) Cleaned Experiment Data/Cleaned - Experiment 2.csv")
Experiment_3 = pd.read_csv("/Users/shruthishekar/Documents/GitHub/LLM-MedQA/2) Cleaned Experiment Data/Cleaned - Experiment 3.csv")


Response_Source = ["_D_", "_H_", "_L_"] # _D_ = Doctor, _H_ = High Accuracy AI-Generated, _L_ = Low Accuracy AI-Generated
Medical_Domain = ["_Preventative_", "_Conditions_", "_Diagnostic", "_Procedures_", "_Medications_", "_Recovery_"] # 6 Different medical domains

Question_Names_Exp_1 = ["Und_Q", "Und_R", "AI_or_Human", "Confidence"] # Question Names in Experiment 1
Question_Type_Exp_1 = ["_2_1", "_4_1", "_6", "_7_1"] # Number labels for each question in the raw dataset

Question_Names_Exp_2_3 = ["Und_Q", "Und_R", "Valid", "Trust", "Satis", "Follow", "Action", "Info"]# Question Names in Experiment 2
Question_Type_Exp_2_3 = ["_2_1", "_4_1", "_6", "_7_1", "_8_1", "_10_1", "_11_1", "_12_1"] # Number labels for each question in the raw dataset





###### EXPERIMENT 1 - Data Analysis ######


# DATA EXTRACTION - Experiment 1
# =============================================================================
Exp1_Lists = {"Und_Q": [], "Und_R": [], "AI_or_Human": [], "Confidence": [], "_D_": [], "_H_": [], "_L_": [], "_Preventative_": [], "_Conditions_": [], "_Diagnostic": [], "_Procedures_": [], "_Medications_": [], "_Recovery_":[]} 
# Experiment 1 - Dictionary of empty lists for each question type to organize the different columns from the raw dataset into their respective question type

Experiment_1_df = pd.DataFrame(Experiment_1)
column_headers = list(Experiment_1_df)

for column in column_headers:
    for i in range(len(Question_Type_Exp_1)): # Organizing raw dataset columns into participant evaluation question type
        question = Question_Type_Exp_1[i]
        ques_title = Question_Names_Exp_1[i]
        if question in column:
            Exp1_Lists[ques_title].append(column)       
        
    for source in Response_Source: # Organizing raw dataset columns into medical response source
        if source in column:
            Exp1_Lists[source].append(column)
    
    for domain in Medical_Domain: # Organizing raw dataset columns into medical response domain
        if domain in column:
            Exp1_Lists[domain].append(column)



# Creating empty dataset for Experiment 1 to fill and organize data from raw dataset

# (Understanding Question & Response results)
dataset_exp_1 = pd.DataFrame()
dataset_exp_1.insert(0, "Question Type", 0)
dataset_exp_1.insert(1, "Response Scores", 0)
dataset_exp_1.insert(2, "Response Source", 0)
dataset_exp_1.insert(3, "Participant ID", 0)
dataset_exp_1.insert(4, "Question ID", 0)

# (Determining response source - AI or Human - and Confidence  results)
dataset_exp_1_2 = pd.DataFrame()
dataset_exp_1_2.insert(0, "Question Type", 0)
dataset_exp_1_2.insert(1, "Incorrect/Correct", 0)
dataset_exp_1_2.insert(2, "Response Scores", 0)
dataset_exp_1_2.insert(3, "Confidence", 0)
dataset_exp_1_2.insert(4, "Response Source", 0)
dataset_exp_1_2.insert(5, "Participant ID", 0)
dataset_exp_1_2.insert(6, "Question ID", 0)
# =============================================================================




# FUNCTIONS - Experiment 1
# =============================================================================
# Function to identify if participant answer of AI or Human matches the true source of the response shown to them
def AI_or_Human(Question, Dataset, Stat_dataset, Survey_Dict) :

    Source_Str = ["Doctor", "High Accuracy AI", "Low Accuracy AI"]

    for i in range(len(Response_Source)):
        Source = Response_Source[i]
        Source_list = Survey_Dict[Source]
        Ques_list = Survey_Dict[Question]

        Sample = sorted(list(set(Ques_list) & set(Source_list)))

        for col in Sample:
            Question_ID = col
            Temp_column = Dataset.loc[:, col]
            conf_str = str(col)
            conf = conf_str[0:-1] + '7_1'
            Conf_column = Dataset.loc[:, conf]
            Participants = Dataset.loc[:, "prolific_id"]

            for j in range(len(Temp_column)):
                resp = Temp_column[j]
                confidence = Conf_column[j]
                Participant_ID = Participants[j]

                try: 
                    if str(resp) == "Doctor":
                        if Source_Str[i] == "Doctor":
                            Stat_dataset.loc[len(Stat_dataset)] = [Question, "Correct", 1, confidence, Source_Str[i], Participant_ID, Question_ID]
                        if Source_Str[i] == "High Accuracy AI":
                            Stat_dataset.loc[len(Stat_dataset)] = [Question, "Incorrect", 0, confidence, Source_Str[i], Participant_ID, Question_ID]
                        if Source_Str[i] == "Low Accuracy AI":
                            Stat_dataset.loc[len(Stat_dataset)] = [Question, "Incorrect", 0, confidence, Source_Str[i], Participant_ID, Question_ID]

                    if str(resp) == "AI Text Generator":
                        if Source_Str[i] == "Doctor":
                            Stat_dataset.loc[len(Stat_dataset)] = [Question, "Incorrect", 0, confidence, Source_Str[i], Participant_ID, Question_ID]
                        if Source_Str[i] == "High Accuracy AI":
                            Stat_dataset.loc[len(Stat_dataset)] = [Question, "Correct", 1, confidence, Source_Str[i], Participant_ID, Question_ID]
                        if Source_Str[i] == "Low Accuracy AI":
                            Stat_dataset.loc[len(Stat_dataset)] = [Question, "Correct", 1, confidence, Source_Str[i], Participant_ID, Question_ID]

                except:
                    pass

    return('Done')


# Function for analyzing likert scale participant responses
def Likert(Question, Dataset, Stat_dataset, Survey_Str, Survey_Dict) :

    Source_Str = ["Doctor", "High Accuracy AI", "Low Accuracy AI"]

    for i in range(len(Response_Source)):
        Source = Response_Source[i]
        Source_list = Survey_Dict[Source]
        Ques_list = Survey_Dict[Question]

        Sample = sorted(list(set(Ques_list) & set(Source_list)))
     
        for col in Sample:
            Question_ID = col
            Temp_column = Dataset.loc[:, col]
            Participants = Dataset.loc[:, "prolific_id"]
        
            for j in range(len(Temp_column)):
                resp = Temp_column[j]
                Participant_ID = Participants[j]
                try:                
                    if 0 <= float(resp) <= 5:
                        Stat_dataset.loc[len(Stat_dataset)] = [Question, float(resp), Source_Str[i], Participant_ID, Question_ID]
                except:
                    pass

    return('Done')
# =============================================================================




# EXECTION - Experiment 1
# =============================================================================
Likert("Und_Q", Experiment_1, dataset_exp_1, "Experiment 1", Exp1_Lists)
Likert("Und_R", Experiment_1, dataset_exp_1, "Experiment 1", Exp1_Lists)
AI_or_Human("AI_or_Human", Experiment_1, dataset_exp_1_2, Exp1_Lists)
# =============================================================================





###### EXPERIMENT 2 - Data Analysis ######


# DATA EXTRACTION - Experiment 2
# =============================================================================
Exp2_Lists = {"Und_Q": [], "Und_R": [], "Valid": [], "Trust": [], "Satis": [], "Follow": [], "Action": [], "Info": [], "_D_": [], "_H_": [], "_L_": [], "_Preventative_": [], "_Conditions_": [], "_Diagnostic": [], "_Procedures_": [], "_Medications_": [], "_Recovery_":[]}

# Experiment 2 - Dictionary of empty lists for each question type to organize the different columns from the raw dataset into their respective question type

Experiment_2_df = pd.DataFrame(Experiment_2)
column_headers = list(Experiment_2_df)

for column in column_headers:
    for i in range(len(Question_Type_Exp_2_3)): # Organizing raw dataset columns into participant evaluation question type
        question = Question_Type_Exp_2_3[i]
        ques_title = Question_Names_Exp_2_3[i]
        if question in column:
            Exp2_Lists[ques_title].append(column)       
        
    for source in Response_Source: # Organizing raw dataset columns into medical response source
        if source in column:
            Exp2_Lists[source].append(column)
    
    for domain in Medical_Domain: # Organizing raw dataset columns into medical response domain
        if domain in column:
            Exp2_Lists[domain].append(column)


# Creating empty dataset for Experiment 2 to fill and organize data from raw dataset
dataset_exp_2 = pd.DataFrame()
dataset_exp_2.insert(0, "Question Type", 0)
dataset_exp_2.insert(1, "Response Scores", 0)
dataset_exp_2.insert(2, "Response Source", 0)
dataset_exp_2.insert(3, "Participant ID", 0)
dataset_exp_2.insert(4, "Question ID", 0)
# =============================================================================




# FUNCTION - Experiment 2
# =============================================================================
# Function for analyzing yes / no participant responses (i.e. Validity Responses)

def yes_or_no(Question, Dataset, Stat_dataset, Survey_Dict) :

    Source_Str = ["Doctor", "High Accuracy AI", "Low Accuracy AI"]

    for i in range(len(Response_Source)):
        Source = Response_Source[i]
        Source_list = Survey_Dict[Source]
        Ques_list = Survey_Dict[Question]

        Sample = sorted(list(set(Ques_list) & set(Source_list)))

        for col in Sample:
            Question_ID = col
            Temp_column = Dataset.loc[:, col]
            Participants = Dataset.loc[:, "prolific_id"]
        
            for j in range(len(Temp_column)):
                Participant_ID = Participants[j]
                resp = Temp_column[j]
                try:                
                    if str(resp) == "Yes":
                        Stat_dataset.loc[len(Stat_dataset)] = [Question, 1, Source_Str[i], Participant_ID, Question_ID]
                    if str(resp) == "No":
                        Stat_dataset.loc[len(Stat_dataset)] = [Question, 0, Source_Str[i], Participant_ID, Question_ID]

                except:
                    pass

    return('Done')

# Use likert function from earlier to analyze likert scale participant responses
# =============================================================================



# EXECUTION - Experiment 2
# =============================================================================
for ques in Question_Names_Exp_2_3:
    if ques != "Valid":
        Likert(ques, Experiment_2, dataset_exp_2, "Experiment 2", Exp2_Lists)
    else:
        yes_or_no(ques, Experiment_2, dataset_exp_2, Exp2_Lists)
# =============================================================================




###### EXPERIMENT 3 - Data Analysis ######


# DATASET EXTRACTION - Experiment 3
# =============================================================================
Random_Source = Experiment_3.loc[:, "Assigned_Conditions"]

# Experiment 3 - Dictionary of empty lists for each question type to organize the different columns from the raw dataset into their respective question type

Exp3_Lists = {"Und_Q": [], "Und_R": [], "Valid": [], "Trust": [], "Satis": [], "Follow": [], "Action": [], "Info": [], "_D_": [], "_H_": [], "_L_": [], "_Preventative_": [], "_Conditions_": [], "_Diagnostic": [], "_Procedures_": [], "_Medications_": [], "_Recovery_":[]}

Experiment_3_df = pd.DataFrame(Experiment_3)
column_headers = list(Experiment_3_df)

for column in column_headers: # Organizing raw dataset columns into participant evaluation question type
    for i in range(len(Question_Type_Exp_2_3)):
        question = Question_Type_Exp_2_3[i]
        ques_title = Question_Names_Exp_2_3[i]
        if question in column:
            Exp3_Lists[ques_title].append(column)       
        
    for source in Response_Source: # Organizing raw dataset columns into medical response source
        if source in column:
            Exp3_Lists[source].append(column)
    
    for domain in Medical_Domain: # Organizing raw dataset columns into medical response domain
        if domain in column:
            Exp3_Lists[domain].append(column)


# Creating empty dataset for Experiment 1 to fill and organize data from raw dataset
dataset_exp_3 = pd.DataFrame()
dataset_exp_3.insert(0, "Question Type", 0)
dataset_exp_3.insert(1, "Response Scores", 0)
dataset_exp_3.insert(2, "Response Source", 0)
dataset_exp_3.insert(3, "Random Header", 0)
dataset_exp_3.insert(4, "Participant ID", 0)
dataset_exp_3.insert(5, "Question ID", 0)
# =============================================================================



# FUNCTIONS - Experiment 3
# =============================================================================
# Function for analyzing likert scale participant responses in Experiment 3 --> made specific to take into account the three different random lables presented ("Doctor", "AI", "Doctor-assisted by AI")

def Indicated_Source_Likert(Question, Dataset, Stat_dataset, Survey_Str, Survey_Dict) :
    
    Add = [" - D", " - H", " - L"]
    Ques = Survey_Dict[Question]

    for i in range(3):
        name = Question + Add[i]
        curr_set = Survey_Dict[Response_Source[i]]
        Sample = sorted(list(set(Ques) & set(curr_set)))

        for col in Sample:
            Temp_column = Dataset.loc[:, col]
            Question_ID = col
            Participants = Dataset.loc[:, "prolific_id"]

            for ind in Dataset.index:
                resp = Temp_column[ind]
                Participant_ID = Participants[ind]
                if str(Random_Source[ind]) == "DOCTOR":
                    if 0 <= float(resp) <= 5:
                        Stat_dataset.loc[len(Stat_dataset)] = [Question, float(resp), name, "Doctor", Participant_ID, Question_ID]
                    
                if str(Random_Source[ind]) == "ARTIFICIAL INTELLIGENCE (A.I.)":
                    if 0 <= float(resp) <= 5:
                        Stat_dataset.loc[len(Stat_dataset)] = [Question, float(resp), name, "AI", Participant_ID, Question_ID]
                
                if str(Random_Source[ind]) == "DOCTOR ASSISTED BY ARTIFICIAL INTELLIGENCE (A.I.)":
                    if 0 <= float(resp) <= 5:
                        Stat_dataset.loc[len(Stat_dataset)] = [Question, float(resp), name, "Doctor + AI", Participant_ID, Question_ID]

    return("Done")



# Function for analyzing yes / no participant responses (i.e. Validity responses) in Experiment 3 --> made specific to take into account the three different random lables presented ("Doctor", "AI", "Doctor-assisted by AI")

def Yes_or_No_Exp3(Question, Dataset, Stat_dataset, Survey_Dict):
    
    Add = [" - D", " - H", " - L"]
    Ques = Survey_Dict[Question]

    for i in range(3):
        name = Question + Add[i]
        curr_set = Survey_Dict[Response_Source[i]]
        Sample = sorted(list(set(Ques) & set(curr_set)))

        for col in Sample:
            Temp_column = Dataset.loc[:, col]
            Question_ID = col
            Participants = Dataset.loc[:, "prolific_id"]

            for ind in Dataset.index:
                resp = Temp_column[ind]
                Participant_ID = Participants[ind]

                if str(Random_Source[ind]) == "DOCTOR":
                    if resp == "Yes":
                        Stat_dataset.loc[len(Stat_dataset)] = [Question, 1, name, "Doctor", Participant_ID, Question_ID]

                    if resp == "No":
                        Stat_dataset.loc[len(Stat_dataset)] = [Question, 0, name, "Doctor", Participant_ID, Question_ID]
                    

                if str(Random_Source[ind]) == "ARTIFICIAL INTELLIGENCE (A.I.)":
                    if resp == "Yes":
                        Stat_dataset.loc[len(Stat_dataset)] = [Question, 1, name, "AI", Participant_ID, Question_ID]

                    if resp == "No":
                        Stat_dataset.loc[len(Stat_dataset)] = [Question, 0, name, "AI", Participant_ID, Question_ID]
                    

                if str(Random_Source[ind]) == "DOCTOR ASSISTED BY ARTIFICIAL INTELLIGENCE (A.I.)":
                    if resp == "Yes":
                        Stat_dataset.loc[len(Stat_dataset)] = [Question, 1, name, "Doctor + AI", Participant_ID, Question_ID]

                    if resp == "No":
                        Stat_dataset.loc[len(Stat_dataset)] = [Question, 0, name, "Doctor + AI", Participant_ID, Question_ID]

    return("Done")
# =============================================================================



# EXECUTION - Experiment 3
# =============================================================================
for ques in Question_Names_Exp_2_3:
    if ques != "Valid":
        Indicated_Source_Likert(ques, Experiment_3, dataset_exp_3, "Experiment 3", Exp3_Lists)
    else:
        Yes_or_No_Exp3(ques, Experiment_3, dataset_exp_3, Exp3_Lists)
# =============================================================================



# Dataset Conversion to CSV Files
dataset_exp_1.to_csv("/Users/shruthishekar/Documents/GitHub/LLM-MedQA/3) Organized Experiment Data/Experiment 1.csv")
dataset_exp_1_2.to_csv("/Users/shruthishekar/Documents/GitHub/LLM-MedQA/3) Organized Experiment Data/Experiment 1 - 2.csv")
dataset_exp_2.to_csv("/Users/shruthishekar/Documents/GitHub/LLM-MedQA/3) Organized Experiment Data/Experiment 2.csv")
dataset_exp_3.to_csv("/Users/shruthishekar/Documents/GitHub/LLM-MedQA/3) Organized Experiment Data/Experiment 3.csv")