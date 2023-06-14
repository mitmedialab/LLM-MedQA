
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
# Understanding Response

# read in data and check
dat_und_r <- read.csv("/Users/shruthishekar/Desktop/Survey 1 - Und R.csv")
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
icc(mod) # the "adjusted ICC" is what you want

