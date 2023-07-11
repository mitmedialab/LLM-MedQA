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
# Prompt: "Would you follow the advice given in this response?
# Medical Response Source: Doctors' Responses

dat_follow_3_D <- read.csv("/Users/shruthishekar/Documents/GitHub/LLM-MedQA/3) Organized Experiment Data/Experiment 3.csv")
dat_follow_3_D = dat_follow_3_D[dat_follow_3_D$Response.Source == "Follow - D", ] #Limit dataset to responses for this evaluation question type

str(dat_follow_3_D)
head(dat_follow_3_D)

# estimate models
mod_null <- lmer(Response.Scores ~ 1 + (1 | Participant.ID) + (1 | Question.ID), data = dat_follow_3_D)
mod <- lmer(Response.Scores ~ 1 + Random.Header + (1 | Participant.ID) + (1 | Question.ID), data = dat_follow_3_D)

# LRT (omnibus test)
anova(mod, mod_null)

# pairwise comparisons among conditions
Means <- emmeans(mod, spec = ~ Random.Header)
contr <- contrast(Means, method="pairwise", adjust="holm")
summary(contr, infer=TRUE)

# calculate intra-class correlation (ICC)
icc(mod)


