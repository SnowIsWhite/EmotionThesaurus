setwd('/Users/jaeickbae/Documents/projects/EmotionThesaurus/data/idioms')
data_fam <- read.csv('FAMILIARITY-Table 1.csv', header = TRUE)
data_decomp <- read.csv('GLOBAL DECOMPOSABILITY-Table 1.csv', header = TRUE)
data_plaus <- read.csv('LITERAL PLAUSIBILITY-Table 1.csv', header = TRUE)
data_meaning <- read.csv('MEANINGFULNESS-Table 1.csv', header = TRUE)
data_pred <- read.csv('PREDICTABILITY-Table 1.csv', header = TRUE)

idioms <- data_fam[,c(1)]
decomp <- data_decomp[1:870,c(3)]
fam <- data_fam[,c(3)]
meaning <- data_meaning[,c(3)]
plaus <- data_plaus[,c(3)]
pred <- data_pred[,c(3)]

df <- data.frame(decomp, fam, meaning, plaus, pred)
cols <- character(nrow(df))
cols[] <- 'white'
cols[df$decomp<0.2] <- 'red'
cols[df$decomp >= 0.2 & df$decomp <0.4] <- 'blue'
cols[df$decomp >= 0.4 & df$decomp < 0.6] <- 'green'
cols[df$decomp >= 0.6 & df$decomp < 0.8] <- 'yellow'
cols[df$decomp >= 0.8 & df$decomp < 1.0] <- 'black'

pairs(df, col = cols)
