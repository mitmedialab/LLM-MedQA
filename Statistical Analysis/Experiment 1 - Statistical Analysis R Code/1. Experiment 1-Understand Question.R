# install "pacman" package
install.packages("pacman")

# load external packages into R session
pacman::p_load(
  lme4,              # mixed effects models
  lmerTest,        # p-values for linear mixed effects models
  emmeans,       # post-estimation comparisons for any model
  performance,  # ICC
  glmmTMB,    # beta mixed effects models
  car                  # logit function
)
set.seed(42)
library(dplyr)


##########################################################################################
# STATISTICAL ANALYSES - Linear Mixed Effects Model
# Experiment 1
# Prompt: "I understand this health question."

# read in data and check
dat_und_q_1 <- read.csv("/Users/shruthishekar/Documents/GitHub/LLM-MedQA/3) Organized Experiment Data/Experiment 1.csv")
dat_und_q_1 = dat_und_q_1[dat_und_q_1$Question.Type == "Und_Q", ] #Limit dataset to responses for this evaluation question type
dat_und_q_1 <- dat_und_q_1%>%mutate_at(vars(Response.Scores),list(Response_Scores_5=~./5))

str(dat_und_q_1)
head(dat_und_q_1)

# estimate models
mod_null <- lmer(Response.Scores ~ 1 + (1 | Participant.ID) + (1 | Question.ID), data = dat_und_q_1)
mod <- lmer(Response.Scores ~ 1 + Response.Source + (1 | Participant.ID) + (1 | Question.ID), data = dat_und_q_1)

# LRT (omnibus test)
anova(mod, mod_null)

# pairwise comparisons among conditions
Means <- emmeans(mod, spec = ~ Response.Source)
contr <- contrast(Means, method="pairwise", adjust="holm")
summary(contr, infer=TRUE)

# calculate intra-class correlation (ICC)
icc(mod)


# logit transform the response (make sure the rating is on the interval [0, 1])
dat_und_q_1$rating_logit <- car::logit(dat_und_q_1$Response.Scores)

# fit linear model to logit transformed response
mod <- lmer(rating_logit ~ 1 + Response.Source + (1 | Participant.ID) + (1 | Question.ID), data = dat_und_q_1)



