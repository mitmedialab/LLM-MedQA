# install "pacman" package
install.packages("pacman")

# load external packages into R session
pacman::p_load(
  lme4,        # mixed effects models
  lmerTest,    # p-values for linear mixed effects models
  emmeans,     # post-estimation comparisons for any model
  performance  # ICC
)

set.seed(42)

##########################################################################################
# STATISTICAL ANALYSES - Linear Mixed Effects Model
# Experiment 3
# Prompt: "The given response is trustworthy."
# Medical Response Source: High Accuracy AI-Generated Responses

dat_trust_3_H <- read.csv("/Users/shruthishekar/Documents/GitHub/LLM-MedQA/3) Organized Experiment Data/Experiment 3.csv")
dat_trust_3_H = dat_trust_3_H[dat_trust_3_H$Response.Source == "Trust - H", ] #Limit dataset to responses for this evaluation question type

str(dat_trust_3_H)
head(dat_trust_3_H)

# estimate models
mod_null <- lmer(Response.Scores ~ 1 + (1 | Participant.ID) + (1 | Question.ID), data = dat_trust_3_H)
mod <- lmer(Response.Scores ~ 1 + Random.Header + (1 | Participant.ID) + (1 | Question.ID), data = dat_trust_3_H)

# LRT (omnibus test)
anova(mod, mod_null)

# pairwise comparisons among conditions
Means <- emmeans(mod, spec = ~ Random.Header)
contr <- contrast(Means, method="pairwise", adjust="holm")
summary(contr, infer=TRUE)

# calculate intra-class correlation (ICC)
icc(mod) 


