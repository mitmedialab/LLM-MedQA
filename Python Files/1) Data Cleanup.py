#!/usr/bin/env python3
# -*- coding: utf-8 -*-



import pandas as pd
import matplotlib.pyplot as plt


### Function - Cleanup Datasets ####

def clean_up(experiment, dest_directory):
    
    Anonymous = experiment.loc[:, "DistributionChannel"]
    Consent = experiment.loc[:,"Consent"]
    Attention_1 = experiment.loc[:, "ps_0"]
    Attention_2 = experiment.loc[:, "ps_1"]
    Final_screen = experiment.loc[:, "screener_2"]
    Finished = experiment.loc[:, "Finished"]
    Prolific_ID = experiment.loc[:, "prolific_id"]
    
    rows_to_remove = []

    # ANONYMOUS - responses that are not anonymous
    for anon in range(len(Anonymous)):
        if Anonymous[anon] != "anonymous":
            rows_to_remove.append(anon)
             
    # CONSENT - responses of participants that did not provide consent
    for cons in range(len(Consent)):
        if Consent[cons] == "I do not consent":
            if cons not in rows_to_remove:
                rows_to_remove.append(cons)
  
    # ATTENTION 1 - responses of participants that did not pass attention test 1
    for att1 in range(len(Attention_1)):
        if Attention_1[att1] != "15":
            if att1 not in rows_to_remove:
                rows_to_remove.append(att1)
                              
    # ATTENTION 2 - responses of participants that did not pass attention test 2
    for att2 in range(len(Attention_2)):
        if Attention_2[att2] != "Somewhat disagree":
            if att2 not in rows_to_remove:
                rows_to_remove.append(att2)
     
    # FINAL SCREEN - responses of participants that did not pass final screen
    for finsc in range(len(Final_screen)):
        if Final_screen[finsc] != "Red,Green":
            if finsc not in rows_to_remove:
                rows_to_remove.append(finsc) 
   
    # FINISHED - responses of participants that did not pass attention test 1
    for fin in range(len(Finished)):
        if Finished[fin] == "FALSE":
            if fin not in rows_to_remove:
                rows_to_remove.append(fin) 
    
    experiment_copy = experiment.copy()

    # REMOVED ROWS - remove the responses as identified above
    for row in rows_to_remove:
        experiment_copy = experiment_copy.drop(row)

    # PROLIFIC ID
    experiment_copy.drop_duplicates(subset=['prolific_id'])

    new_index_numbers = []
    for i in range(len(experiment_copy)):
        new_index_numbers.append(i)
    
    experiment_copy.insert(0, "index", new_index_numbers)
    experiment_copy.set_index('index', inplace = True)
    experiment_copy.to_csv(dest_directory) 
    

    return("Data all cleaned")



### Datasets from Experiments Conducted ####

# Load Dataset - Experiment 1
Experiment_1_DS = pd.read_csv("/Users/shruthishekar/Documents/GitHub/LLM-MedQA/1) Raw Experiment Data/Experiment 1 - Raw Data.csv")
Experiment_1_directory = "/Users/shruthishekar/Documents/GitHub/LLM-MedQA/2) Cleaned Experiment Data/Cleaned - Experiment 1.csv"
clean_up(Experiment_1_DS, Experiment_1_directory)


# Load Dataset - Experiment 2
Experiment_2_DS = pd.read_csv("/Users/shruthishekar/Documents/GitHub/LLM-MedQA/1) Raw Experiment Data/Experiment 2 - Raw Data.csv")
Experiment_2_directory = "/Users/shruthishekar/Documents/GitHub/LLM-MedQA/2) Cleaned Experiment Data/Cleaned - Experiment 2.csv"
clean_up(Experiment_2_DS, Experiment_2_directory)


# Load Dataset - Experiment 2
Experiment_3_DS = pd.read_csv("/Users/shruthishekar/Documents/GitHub/LLM-MedQA/1) Raw Experiment Data/Experiment 3 - Raw Data.csv")
Experiment_3_directory = "/Users/shruthishekar/Documents/GitHub/LLM-MedQA/2) Cleaned Experiment Data/Cleaned - Experiment 3.csv"
clean_up(Experiment_3_DS, Experiment_3_directory)



Experiment_1_cleaned = pd.read_csv("/Users/shruthishekar/Documents/GitHub/LLM-MedQA/2) Cleaned Experiment Data/Cleaned - Experiment 1.csv")
Experiment_2_cleaned = pd.read_csv("/Users/shruthishekar/Documents/GitHub/LLM-MedQA/2) Cleaned Experiment Data/Cleaned - Experiment 2.csv")
Experiment_3_cleaned = pd.read_csv("/Users/shruthishekar/Documents/GitHub/LLM-MedQA/2) Cleaned Experiment Data/Cleaned - Experiment 3.csv")

print("Experiment 1 sample size = ", len(Experiment_1_cleaned)) 
print("Experiment 2 sample size = ", len(Experiment_2_cleaned))
print("Experiment 3 sample size = ", len(Experiment_3_cleaned))
