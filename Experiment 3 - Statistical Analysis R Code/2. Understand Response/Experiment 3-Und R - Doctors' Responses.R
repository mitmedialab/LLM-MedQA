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
# Prompt: "I understand the response to this health question."
# Medical Response Source: Doctors' Responses

dat_und_r_3_D <- read.csv("/Users/shruthishekar/Desktop/Organized Experiment Data/Experiment 3.csv")
dat_und_r_3_D = dat_und_r_3_D[dat_und_r_3_D$Response.Source == "Und_R - D", ] #Limit dataset to responses for this evaluation question type

str(dat_und_r_3_D)
head(dat_und_r_3_D)

# estimate models
mod_null <- lmer(Response.Scores ~ 1 + (1 | Participant.ID) + (1 | Question.ID), data = dat_und_r_3_D)
mod <- lmer(Response.Scores ~ 1 + Random.Header + (1 | Participant.ID) + (1 | Question.ID), data = dat_und_r_3_D)

# LRT (omnibus test)
anova(mod, mod_null)

# pairwise comparisons among conditions
Means <- emmeans(mod, spec = ~ Random.Header)
contr <- contrast(Means, method="pairwise", adjust="holm")
summary(contr, infer=TRUE)

# calculate intra-class correlation (ICC)
icc(mod)


