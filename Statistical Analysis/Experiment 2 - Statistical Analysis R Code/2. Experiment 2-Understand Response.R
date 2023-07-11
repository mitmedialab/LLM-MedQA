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
# Prompt: "I understand the response to this health question."

# read in data and check
dat_und_r <- read.csv("/Users/shruthishekar/Documents/GitHub/LLM-MedQA/3) Organized Experiment Data/Experiment 2.csv")
dat_und_r = dat_und_r[dat_und_r$Question.Type == "Und_R", ] #Limit dataset to responses for this evaluation question type

str(dat_und_r)
head(dat_und_r)

# estimate models
mod_null <- lmer(Response.Scores ~ 1 + (1 | Participant.ID) + (1 | Question.ID), data = dat_und_r)
mod <- lmer(Response.Scores ~ 1 + Response.Source + (1 | Participant.ID) + (1 | Question.ID), data = dat_und_r)

# LRT (omnibus test)
anova(mod, mod_null)

# pairwise comparisons among conditions
Means <- emmeans(mod, spec = ~ Response.Source)
contr <- contrast(Means, method="pairwise", adjust="holm")
summary(contr, infer=TRUE)

# calculate intra-class correlation (ICC)
icc(mod)

