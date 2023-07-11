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
# Experiment 2
# Prompt: "Would you seek medical attention?"

# read in data and check
dat_action <- read.csv("/Users/shruthishekar/Documents/GitHub/LLM-MedQA/3) Organized Experiment Data/Experiment 2.csv")
dat_action = dat_action[dat_action$Question.Type == "Action", ] #Limit dataset to responses for this evaluation question type

str(dat_action)
head(dat_action)

# estimate models
mod_null <- lmer(Response.Scores ~ 1 + (1 | Participant.ID) + (1 | Question.ID), data = dat_action)
mod <- lmer(Response.Scores ~ 1 + Response.Source + (1 | Participant.ID) + (1 | Question.ID), data = dat_action)

# LRT (omnibus test)
anova(mod, mod_null)

# pairwise comparisons among conditions
Means <- emmeans(mod, spec = ~ Response.Source)
contr <- contrast(Means, method="pairwise", adjust="holm")
summary(contr, infer=TRUE)

# calculate intra-class correlation (ICC)
icc(mod) 

