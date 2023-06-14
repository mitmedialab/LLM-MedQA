
# install "pacman" package (only need to do this once)
install.packages("pacman")

# load external packages into R session
pacman::p_load(
  lme4,        # mixed effects models
  lmerTest,    # p-values for linear mixed effects models
  emmeans,     # post-estimation comparisons for any model
  performance  # ICC
)

##########################################################################################
# Confidence - High Accuracy AI

# read in data and check
dat_Conf_H <- read.csv("/Users/shruthishekar/Desktop/Survey 2/Survey 2 - Conf - High Accuracy AI.csv")
str(dat_Conf_H)
head(dat_Conf_H)

# estimate models
mod_null <- lmer(Confidence ~ 1 + (1 | Participant.ID) + (1 | Question.ID), data = dat_Conf_H)
mod <- lmer(Confidence ~ 1 + Incorrect.Correct + (1 | Participant.ID) + (1 | Question.ID), data = dat_Conf_H)

# LRT (omnibus test)
anova(mod, mod_null)

# pairwise comparisons among conditions
Means <- emmeans(mod, spec = ~ Incorrect.Correct)
contr <- contrast(Means, method="pairwise", adjust="holm")
summary(contr, infer=TRUE)

# calculate intra-class correlation (ICC)
icc(mod) # the "adjusted ICC" is what you want

