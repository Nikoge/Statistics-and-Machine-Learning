name<-"Andreas Stasinakis"
liuid<-"andst745"

sheldon_game<-function(player1,player2){
  choices<-c("scissors"=0,"paper"=1,"rock"=2,"lizard"=3,"spock"=4)
  if ((player1%in%names(choices)) && (player2%in%names(choices)))
{  
  if(choices[player1]==choices[player2]){
    return("Draw!")
  }else if(((choices[player1]-choices[player2])%%5)%in%c(2,4)){
    return("Player 1 wins!")
  }else{
    return("Player 2 wins!")
  } 
}else{
  stop("not correct input")
}
}
#1.2.1
my_moving_median<-function(x,n, ...){
  if(is.numeric(x)==FALSE | is.numeric(n)==FALSE){
    stop("No numeric vector and scalar")
    }else{
      vect<-c()
      for (i in 1:length(x)) {
        if(i+n<length(x)+1){
        
        vect<-c(vect,median(c(x[i:(i+n)]), ...))
        
        }
        
      }
      return(vect)
  
}}
#1.2.2
for_mult_table<-function(from,to){
  if( is.numeric(from)==TRUE & is.numeric(to)==TRUE){
    v<-c()
    for (i in from:to) {
      a<-c(i*(from:to))
      v<-c(v,a)
      }
    name<-c(from:to)
    mat<-matrix(v,nrow = (to-from)+1)
    colnames(mat)<-name
    rownames(mat)<-name
    return(mat)
    
  }else{ 
    
    stop("The arquments are not numeric scalars")}
} 

#1.3
#1.3.1
find_cumsum<-function(x,find_sum){
  if( is.numeric(x)==TRUE & is.numeric(find_sum)==TRUE)
    { 
    i<-1
    cum.s<-cumsum(x)
    while(head(cum.s,1)<find_sum & i<length(x)){
      cum.s<-cum.s[-1]
      i<- i+1
      
  }
    return((head(cum.s,1)))
     }else {
    stop("no numerical vector or scalar")}
  }

#1.3.2
while_mult_table<-function(from,to){
  if( is.numeric(from)==TRUE & is.numeric(to)==TRUE){
    v<-c()
    i<-from
    while (i>= from & i<=to) {
      a<-c(i*(from:to))
      v<-c(v,a)
      i<-i+1
    }
    name<-c(from:to)
    mat<-matrix(v,nrow = (to-from)+1)
    colnames(mat)<-name
    rownames(mat)<-name
    return(mat)
    
  }else{ 
    
    stop("The arquments are not numeric scalars")}
} 

#1.4.1
repeat_find_cumsum<-function(x,find_sum){
  if( is.numeric(x)==TRUE & is.numeric(find_sum)==TRUE)
  { 
    i<-1
    cum.s<-cumsum(x)
    repeat{
      cum.s<-cum.s[-1]
      i<-i+1
    if(head(cum.s,1)>find_sum | i>=length(x)){
      break
    }}
      return(as.numeric(head(cum.s,1)))
  }else {
    stop("no numerical vector or scalar")}
}

#1.4.2
repeat_my_moving_median<-function(x,n, ...){
  if(is.numeric(x)==FALSE | is.numeric(n)==FALSE){
    stop("No numeric vector and scalar")
  }else{
    vect<-c()
    i<-1
    while (i<=length(x)) {
      if(i+n<length(x)+1){
        
        vect<-c(vect,median(c(x[i:(i+n)]), ...))
        
      } 
      i<-i+1
      
    }
    return(vect)
    
  }}

#1.5.1

in_environment<-function(env){
return(ls(env))
}

#1.6.1
cov<-function(X){
  if(is.data.frame(X)==TRUE){
  c<-lapply(X,function(y){
    a<-((sd(y))/(mean(y)))
    return(a)}
  )
  return(unlist(c))}
else  stop("no data frame")
}

  #1.7.1
moment<-function(i){
  if (is.numeric(i)==TRUE){
var<-function(X){
  mi<-mean((X-mean(X))^i)
  return(mi)}
  }
  else stop("No numeric scalars")
}

