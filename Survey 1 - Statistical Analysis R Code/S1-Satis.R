
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
# Satis

# read in data and check
dat_satis <- read.csv("/Users/shruthishekar/Desktop/Survey 1 - Satis.csv")
str(dat_satis)
head(dat_satis)

# estimate models
mod_null <- lmer(Response.Scores ~ 1 + (1 | Participant.ID) + (1 | Question.ID), data = dat_satis)
mod <- lmer(Response.Scores ~ 1 + Response.Source + (1 | Participant.ID) + (1 | Question.ID), data = dat_satis)

# LRT (omnibus test)
anova(mod, mod_null)

# pairwise comparisons among conditions
Means <- emmeans(mod, spec = ~ Response.Source)
contr <- contrast(Means, method="pairwise", adjust="holm")
summary(contr, infer=TRUE)

# calculate intra-class correlation (ICC)
icc(mod) # the "adjusted ICC" is what you want

