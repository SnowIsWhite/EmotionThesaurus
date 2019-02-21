setwd('./Documents/projects/EmotionThesaurus/verb_list/results/gutenberg/csv/')
#hand
data_hand <- read.csv('hand_verb_freq.csv', header = TRUE)
y_hand <- data_hand[,c(2)]
rank_hand <- array(1:length(y_hand))
plot(rank_hand, y_hand, ann = FALSE, type="o", col="blue")

#arm
data_arm <- read.csv('arm_verb_freq.csv', header = TRUE)
y_arm <- data_arm[,c(2)]
rank_arm <- array(1:length(y_arm))
lines(rank_arm, y_arm, type="o", pch=20, lty=2, 
      col="green")

#eye
data_eye <- read.csv('eye_verb_freq.csv', header = TRUE)
y_eye <- data_eye[,c(2)]
rank_eye <- array(1:length(y_eye))
lines(rank_eye, y_eye, type="o", pch=20, lty=2, 
      col="red")

#face
data_face <- read.csv('face_verb_freq.csv', header = TRUE)
y_face <- data_face[,c(2)]
rank_face <- array(1:length(y_face))
lines(rank_face, y_face, type="o", pch=20, lty=2, 
      col="purple")

#foot
data_foot <- read.csv('foot_verb_freq.csv', header = TRUE)
y_foot <- data_foot[,c(2)]
rank_foot <- array(1:length(y_foot))
lines(rank_foot, y_foot, type="o", pch=20, lty=2, 
      col="yellow")

#head
data_head <- read.csv('head_verb_freq.csv', header = TRUE)
y_head <- data_head[,c(2)]
rank_head <- array(1:length(y_head))
lines(rank_head, y_head, type="o", pch=20, lty=2, 
      col="pink")

#lip
data_lip <- read.csv('lip_verb_freq.csv', header = TRUE)
y_lip <- data_lip[,c(2)]
rank_lip <- array(1:length(y_lip))
lines(rank_lip, y_lip, type="o", pch=20, lty=2, 
      col="orange")


title(xlab = 'rank', ylab = 'frequency')
legend(130, 35, c("hand", 'arm', 'eye', 'face', 'foot', 'head', 'lip'), cex=0.8,
       col = c('blue', 'green', 'red', 'purple', 'yellow','pink','orange'),
       pch=21:23, lty=1:3);
