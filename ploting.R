#R

library(ggplot2)
library(dplyr)

likes=read.csv("likes.csv")
duplicates=read.csv("duplicates.csv")

likes_summarise=likes %>% group_by(domain) %>% summarise(sum_likes=sum(Likes),sum_shares=sum(Shares))

likes_summarise=likes_summarise[-1,]

likes_summarise=as.data.frame(likes_summarise)
duplicates=as.data.frame(duplicates)

likes_summarise$average=(likes_summarise$sum_likes+likes_summarise$sum_shares)/2

duplicates_summarise=duplicates %>% group_by(domain_duplicates) %>% summarise(counts=n())