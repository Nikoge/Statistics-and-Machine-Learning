name<-"Andreas Stasinakis"
liuid<-"andst745"
# 1.1 Vector

#1.1.1 My_num_vector()
my_num_vector<-function(){
  num.vector<-c(log10(11),cos(pi/5),exp(pi/3),(1173%%7)/19)
  return(num.vector)
}
#1.1.2 filter_my_vector(x,leq)
filter_my_vector<-function(x,leq){
   filter<-replace(x,x>=leq,NA)
   return(filter)
}
#1.1.3 dot_prod(a,b)
dot_prod<-function(a,b){
  c<-as.matrix(b)
  prod<-sum(a*c)
  return(prod)
}
#1.1.4 approx_e(N)
 approx_e<-function(N){
   result<-0
    for (n in 0:N) {
     result<-result+sum(1/factorial(n))}
   return(result)
   #The N in order to approximate e to the fifth dimical place is N=8
   
}
# 1.2 Matrices
# 1.2.1 my_magic_matrix()
 my_magic_matrix<-function(){
   a<-c(4,3,8)
   b<-c(9,5,1)
   c<-c(2,7,6)
   mat<-matrix(c(a,b,c),nrow=3)
   return(mat)
 }
 my_magic_matrix() #the sum of any element in a row or colum is always 15
   
 #1.2.2 Calculate_elements(A)
 calculate_elements<-function(A){
   return(length(A))}
 
 #1.2.3 row_to_zero (A,i)
 row_to_zero<-function(A,i){
   A[i,]<-0
   return(A)
 }

 #1.2.4 add_elements_to_matrix(A,x,i,j)
   add_elements_to_matrix<-function(A,x,i,j){
   A[i,j]<-A[i,j]+x
   return(A)
 }

#1.3 Lists
 #1.3.1 my_magic_list()
 
 my_magic_list<-function(){
   magiclist<-list(info="my own list",my_num_vector(),my_magic_matrix())
   return(magiclist)
 }
   
  #1.3.2 change_info(x,text)
   change_info<-function(x,text){
     x$info<-text
     return(x)}
   
   #1.3.3 add_note(x,note)
   add_note<-function(x,note){
     x$note<-note
     return(x)
   }
   
    #1.3.4 sum_numeric_parts (x)  
   sum_numeric_parts<-function(x){
       x<-unlist(x)
       num.list<-as.numeric(x)
       num.list[is.na(num.list)==TRUE]<-0
       sum.list<-sum(num.list)
       return(sum.list)
     }
    
     #1.4 data.frames
   #1.4.1 my.data.frame()
   my_data.frame<-function(){
     id<-c(1:3)
     name<-c("John","Lisa","Azra")
     income<-c(7.3,0.00,15.21)
     rich<-c(FALSE,FALSE,TRUE)
     data<-data.frame(id,name,income,rich)
     return(data)
   }
   
   #1.4.2 sort_head(df,var.name,n)
   sort_head<-function(df,var.name,n){
     sort<-head(df[order(-df[var.name]),],n)
     return(sort)
    }
   
   #1.4.3 add_median_variable
   add_median_variable<-function(df,j){
     median<-median(df[[j]])
     name<-c("Greater","Smaller","Median")
     compared_to_median <- c()
     for (i in 1:length(df[[j]])) {
       if(df[[j]][i]>median){
     compared_to_median<-c(compared_to_median,name[1])
   }else if(df[[j]][i]<median){
     compared_to_median<-c(compared_to_median,name[2])
     
   }else
     compared_to_median<-c(compared_to_median,name[3])
   }  

      df$compared_to_median<-compared_to_median
      return(df)
}
  
#1.4.4 analyse_columns(df,j)
  analyze_columns<-function(df,j){
   a <-c(mean=mean(df[,j[1]]),median=median(df[,j[1]]),sd=sd(df[,j[1]]))
    b<-c(mean=mean(df[,j[2]]),median=median(df[,j[2]]),sd=sd(df[,j[2]]))
    correlation_matrix<-cor(df[,j],df[,j])
    list.abc<-list(a,b,correlation_matrix)
    names(list.abc)<-c(names(df)[j[1]],names(df)[j[2]],"correlation_matrix")
    return(list.abc)
  }
  