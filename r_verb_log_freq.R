setwd('/Users/jaeickbae/Documents/projects/EmotionThesaurus/verb_list/results/gutenberg/csv/')
#hand
data_hand <- read.csv('hand_verb_freq.csv', header = TRUE)
y_hand <- log(data_hand[,c(2)])
rank_hand <- log(array(1:length(y_hand)))
plot(rank_hand, y_hand, ann = FALSE, col="blue")
title(xlab = 'log of rank', ylab = 'log of appearence')
#linear regression 
res <-lm(rank_hand ~ y_hand)
abline(res$coefficients, col = "blue")

#arm
data_arm <- read.csv('arm_verb_freq.csv', header = TRUE)
y_arm <- log(data_arm[,c(2)])
rank_arm <- log(array(1:length(y_arm)))
points(rank_arm, y_arm, pch=20, lty=2, 
      col="green")
#linear regression 
res <-lm(rank_arm ~ y_arm)
abline(res$coefficients, col = "green")

#eye
data_eye <- read.csv('eye_verb_freq.csv', header = TRUE)
y_eye <- log(data_eye[,c(2)])
rank_eye <- log(array(1:length(y_eye)))
points(rank_eye, y_eye, pch=20, lty=2, 
      col="red")
#linear regression 
res <-lm(rank_eye ~ y_eye)
abline(res$coefficients, col = "red")

#face
data_face <- read.csv('face_verb_freq.csv', header = TRUE)
y_face <- log(data_face[,c(2)])
rank_face <- log(array(1:length(y_face)))
points(rank_face, y_face, pch=20, lty=2, 
      col="purple")
#linear regression 
res <-lm(rank_face ~ y_face)
abline(res$coefficients, col = "purple")

#foot
data_foot <- read.csv('foot_verb_freq.csv', header = TRUE)
y_foot <- log(data_foot[,c(2)])
rank_foot <- log(array(1:length(y_foot)))
points(rank_foot, y_foot, pch=20, lty=2, 
      col="yellow")
#linear regression 
res <-lm(rank_foot ~ y_foot)
abline(res$coefficients, col = "yellow")

#head
data_head <- read.csv('head_verb_freq.csv', header = TRUE)
y_head <- log(data_head[,c(2)])
rank_head <- log(array(1:length(y_head)))
points(rank_head, y_head, pch=20, lty=2, 
      col="pink")
#linear regression 
res <-lm(rank_head ~ y_head)
abline(res$coefficients, col = "pink")

#lip
data_lip <- read.csv('lip_verb_freq.csv', header = TRUE)
y_lip <- log(data_lip[,c(2)])
rank_lip <- log(array(1:length(y_lip)))
points(rank_lip, y_lip, pch=20, lty=2, 
      col="orange")
#linear regression 
res <-lm(rank_lip ~ y_lip)
abline(res$coefficients, col = "orange")


legend(4, 3, c("hand", 'arm', 'eye', 'face', 'foot', 'head', 'lip'), cex=0.8,
       col = c('blue', 'green', 'red', 'purple', 'yellow','pink','orange'),
       pch=21:23, lty=1:3);
