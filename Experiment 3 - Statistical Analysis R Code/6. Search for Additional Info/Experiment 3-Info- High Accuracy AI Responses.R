# install "pacman" package
install.packages("pacman")

# load external packages into R session
pacman::p_load(
  lme4,        # mixed effects models
  lmerTest,    # p-values for linear mixed effects models
  emmeans,     # post-estimation comparisons for any model
  performance  # ICC
)

##########################################################################################
# STATISTICAL ANALYSES - Linear Mixed Effects Model
# Experiment 3
# Prompt: "Would you need to search for additional info?"
# Medical Response Source: High Accuracy AI-Generated Responses

dat_info_3_H <- read.csv("/Users/shruthishekar/Desktop/Organized Experiment Data/Experiment 3.csv")
dat_info_3_H = dat_info_3_H[dat_info_3_H$Response.Source == "Satis - H", ] #Limit dataset to responses for this evaluation question type

str(dat_info_3_H)
head(dat_info_3_H)

# estimate models
mod_null <- lmer(Response.Scores ~ 1 + (1 | Participant.ID) + (1 | Question.ID), data = dat_info_3_H)
mod <- lmer(Response.Scores ~ 1 + Random.Header + (1 | Participant.ID) + (1 | Question.ID), data = dat_info_3_H)

# LRT (omnibus test)
anova(mod, mod_null)

# pairwise comparisons among conditions
Means <- emmeans(mod, spec = ~ Random.Header)
contr <- contrast(Means, method="pairwise", adjust="holm")
summary(contr, infer=TRUE)

# calculate intra-class correlation (ICC)
icc(mod)


