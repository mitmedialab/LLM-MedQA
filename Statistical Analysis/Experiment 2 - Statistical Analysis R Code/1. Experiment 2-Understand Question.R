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
# Prompt: "I understand this health question."

# read in data and check
dat_und_q <- read.csv("/Users/shruthishekar/Documents/GitHub/LLM-MedQA/3) Organized Experiment Data/Experiment 2.csv")
dat_und_q = dat_und_q[dat_und_q$Question.Type == "Und_Q", ] #Limit dataset to responses for this evaluation question type

str(dat_und_q)
head(dat_und_q)

# estimate models
mod_null <- lmer(Response.Scores ~ 1 + (1 | Participant.ID) + (1 | Question.ID), data = dat_und_q)
mod <- lmer(Response.Scores ~ 1 + Response.Source + (1 | Participant.ID) + (1 | Question.ID), data = dat_und_q)

# LRT (omnibus test)
anova(mod, mod_null)

# pairwise comparisons among conditions
Means <- emmeans(mod, spec = ~ Response.Source)
contr <- contrast(Means, method="pairwise", adjust="holm")
summary(contr, infer=TRUE)

# calculate intra-class correlation (ICC)
icc(mod)

