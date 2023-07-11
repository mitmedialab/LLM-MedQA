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
# Experiment 1
# Prompt: "I am confident in the answer I selected for the previous question? (Doctor vs. AI)"
# Medical Response Source: Doctors' Responses

# read in data and check
dat_Conf_D <- read.csv("/Users/shruthishekar/Desktop/Organized Experiment Data/Experiment 1 - 2.csv")
dat_Conf_D = dat_Conf_D[dat_Conf_D$Response.Source == "Doctor", ] #Limit dataset to responses for this evaluation question type

str(dat_Conf_D)
head(dat_Conf_D)

# estimate models
mod_null <- lmer(Confidence ~ 1 + (1 | Participant.ID) + (1 | Question.ID), data = dat_Conf_D)
mod <- lmer(Confidence ~ 1 + Incorrect.Correct + (1 | Participant.ID) + (1 | Question.ID), data = dat_Conf_D)

# LRT (omnibus test)
anova(mod, mod_null)

# pairwise comparisons among conditions
Means <- emmeans(mod, spec = ~ Incorrect.Correct)
contr <- contrast(Means, method="pairwise", adjust="holm")
summary(contr, infer=TRUE)

# calculate intra-class correlation (ICC)
icc(mod)
