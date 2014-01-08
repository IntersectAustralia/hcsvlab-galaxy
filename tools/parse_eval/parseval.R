parseval <- function (words_per_word_type, word_types,...) {
  #parseval <- function (parse=c("simplex", "complex"), ...) {
  
  # extract phonetic parameters into more transparently labeled variables
  C1p<-42 # plateau duration of the first consonant in triconsonantal clusters
  C1stdv<-20 # standard deviation of the first consonant in triconsonantal clusters
  C2p<-42 # plateau duration of the second consonant in triconsonantal clusters and the first consonant in bi-consonantal clusters
  C2stdv<-20 # standard deviation of the second consonant in triconsonantal clusters and the first consonant in bi-consonantal clusters 
  C3p<-42 # plateau duration of the immediately prevocalic consonant
  C3stdv<-20 # standard deviation of the immediately prevocalic consonant
  C12ipi<-66  # the duration of the interval between the plateaus of the first two consonants in triconsonantal clusters
  C12stdv<-20 # the standard deviation of the interval between the plateaus of the first two consonants in triconsonantal clusters
  C23ipi<-66# the duration of the interval between the plateaus of the first two consonants in biconsonantal clusters and between the second two consonants in triconsonantal clusters
  C23stdv<-20 # the standard deviation of the interval between the plateaus of the first two consonants in biconsonantal clusters and between the second two consonants in triconsonantal clusters
  vowel_duration<-196 # the duration of the vowel
  
  # extract variability parameters into more transparently labeled variables
  variability_range<-15 # number of stepwise increases in variability simulated by the model
  variability_resolution<-5 # size of each stepwise increase in variability
  # words_per_word_type<-30 # the number of words (stimuli) per word type, aka "little n"
  # word_types<-3 # number of different word types, e.g. #CV-, #CCV-, #CCCV-
  simN<-1000 # the number of simulation runs over which hit rate is calculated, aka "big N"
  
  # input experimental data
  # data_RE_RSD = input('Enter the RSD of the right edge to anchor interval > ');
  data_RE_RSD<-0.112
  # data_CC_RSD = input('Enter the RSD of the center to anchor interval > ');
  data_CC_RSD<-0.159
  # data_LE_RSD = input('Enter the RSD of the left edge to anchor interval > ');
  data_LE_RSD<-0.246
  data_RSD<-c(data_RE_RSD, data_LE_RSD, data_CC_RSD) # lumps RSD measures into single array
  
  A_simp <- matrix(nrow=variability_range, ncol=words_per_word_type)
  A_comp <- matrix(nrow=variability_range, ncol=words_per_word_type)
  
  # creating matrices to hold the SD values
  LE_SD_simp<-matrix(nrow=simN, ncol=variability_range, byrow=TRUE)
  LE_SD_comp<-matrix(nrow=simN, ncol=variability_range, byrow=TRUE)
  RE_SD_simp<-matrix(nrow=simN, ncol=variability_range, byrow=TRUE)
  RE_SD_comp<-matrix(nrow=simN, ncol=variability_range, byrow=TRUE)
  CC_SD_simp<-matrix(nrow=simN, ncol=variability_range, byrow=TRUE)
  CC_SD_comp<-matrix(nrow=simN, ncol=variability_range, byrow=TRUE)
  
  # creating matrices to hold the RSD values
  LE_RSD_simp<-matrix(nrow=simN, ncol=variability_range, byrow=TRUE)
  LE_RSD_comp<-matrix(nrow=simN, ncol=variability_range, byrow=TRUE)
  RE_RSD_simp<-matrix(nrow=simN, ncol=variability_range, byrow=TRUE)
  RE_RSD_comp<-matrix(nrow=simN, ncol=variability_range, byrow=TRUE)
  CC_RSD_simp<-matrix(nrow=simN, ncol=variability_range, byrow=TRUE)
  CC_RSD_comp<-matrix(nrow=simN, ncol=variability_range, byrow=TRUE)
  
  if (word_types=="3") {
    tepa<-c("Testing Triads")
    for (count in 1:simN) {
      # generate CCC tokens
      # generate timestamps for C3 (the prevocalic consonant)
      # generate general error-term for use later on
      e <- C3stdv*(rnorm(1))
      # generate R(ight plateau edge = Release) of prevocalic consonant
      # generate words_per_word_type/word_types Gaussian distributed numbers (for CCC tokens only)
      # with mean 500, variance 10
      CCCR3 <- rnorm(words_per_word_type/word_types, mean=500, sd=sqrt(20))
      # generate L(eft plateau edge = Target) of prevocalic consonant  
      CCCL3 <- CCCR3-C3p+e #generate L3 corresponding to R3 by assuming a plateau duration of C3p
      # calculate midpoint of prevocalic consonant plateau
      CCCM3 <- ((CCCR3+CCCL3)/2)
      
      # generate timestamps for C2
      # generate general error-term for use later on
      e1<-C23stdv*(rnorm(1)) #normally distributed random error
      e2<-C2stdv*(rnorm(1)) #normally distributed random error
      # Generate right edge of C2
      CCCR2 <- CCCL3 - C23ipi + e1 # generate right edge of C2 from left edge of C3 assuming an ipi of C23ipi
      # Generate left edge of C2
      CCCL2 <- CCCR2 - C2p + e2 # generate left edge from right edge by assuming a plateau duration
      # Calculate midpoint of C2
      CCCM2 <- ((CCCR2+CCCL2)/2)
      
      # generate timestamps for C1
      # generate general error-term for use later on
      e1<-C12stdv*(rnorm(1)) # normally distributed random error
      e2<-C3stdv*(rnorm(1))
      # Generate right edge 
      CCCR1 <- CCCL2 - C12ipi + e1 # generate right edge of C1 from left edge of C2 assuming ipi of 40ms
      # generate L(eft plateau edge = Target) of C1
      CCCL1 <- CCCR1 - C3p + e2 # generate L2 corresponding to CR1 by assuming a plateau of 10ms
      # calculate midpoint of prevocalic consonant
      CCCM1 <-  ((CCCR1 + CCCL1)/2) # right edge of C1
      
      #generate CC tokens
      #generate timestamps for C3 (prevocalic consonant)
      # generate general error-term for use later on      
      e<-C3stdv*(rnorm(1)) # normally distributed random error, 0 mean
      # generate R(ight plateau edge = Release) of prevocalic consonant
      CCR3 <- rnorm(words_per_word_type/word_types, mean=500, sd=sqrt(20)) # generate N Gaussian distributed numbers with mean 500, variance 10
      # generate L(eft plateau edge = Target) of prevocalic consonant
      CCL3 <- CCR3-C3p+e # generate L3 corresponding to R3 by assuming a plateau duration of C3p
      # calculate midpoint of prevocalic consonant plateau
      CCM3 <- ((CCR3+CCL3)/2)
      
      #generate timestamps for C2
      # generate general error-term for use later on
      e1<-C23stdv*(rnorm(1))
      e2<-C2stdv*(rnorm(1))
      # Generate right edge of C2
      CCR2 <- CCL3-C23ipi+e1 # generate right edge of C2 from left edge of C3 assuming an ipi of C23ipi
      # Generate left edge of C2
      CCL2 <- CCR2-C2p+e2 # generate left edge from right edge by assuming a plateau duration
      # Calculate midpoint of C2
      CCM2 <- ((CCR2+CCL2)/2)
      
      # generate C tokens
      # generate timestamps for C3 (the prevocalic consonant)
      # generate general error-term for use later on
      e <- C3stdv * (rnorm(1))
      # Generate R(ight plateau edge = Release) of prevocalic consonant
      CR3 <- rnorm(words_per_word_type/word_types, mean=500, sd=sqrt(20)) # generate N Gaussian distributed numbers with mean 500, variance 10
      # generate L(eft plateau edge = Target) of prevocalic consonant 
      CL3 <- CR3 - C3p + e # generate L3 corresponding to R3 by assuming a plateau duration of C3p
      # calculate midpoint of prevocalic consonant plateau
      CM3 <- ((CR3 + CL3)/2)
      
      # generate timestamps for CCglobal
      # for CCC clusters
      CCglobal <- apply(cbind(CCCM1, CCCM2, CCCM3), 1, mean) #mean of consonant plateaux midpoints        
      # for CC clusters
      CCglobal <- append(CCglobal, apply(cbind(CCM2, CCM3), 1, mean)) # mean of consonant plateaux midpoints
      # for C clusters
      CCglobal <- append(CCglobal, CM3)
      
      # populate a single array with the midpoint of the pre-vocalic
      # consonant of every word type; this array will be used to generate anchors
      # for CCC clusters
      Global_CM3 <- CCCM3 # mean of consonant plateaux midpoints
      # for CC clusters
      Global_CM3 <- append(Global_CM3, CCM3) # mean of consonant plateaux midpoints
      # for C clusters
      Global_CM3 <- append(Global_CM3, CM3)
      
      # populate a single array with the Left_edge of the consonant cluster for every token
      # this array will be used to calculate SD and RSD for EDGE to Anchor intervals
      # for CCC clusters
      Global_CL1 <- CCCL1 # Assigns the left edge of tri-consonantal tokens to the first third of Global_Cl1
      # for CC clusters
      Global_CL1 <- append(Global_CL1, CCL2) # Assigns the left edge of bi-consonantal tokens to the second third of Global_Cl1
      # for C clusters
      Global_CL1 <- append(Global_CL1, CL3) # Assigns the left edge of mono-consonantal tokens to the last third of Global_Cl1
      
      # populate a single array with the Right_edge of the consonant cluster for every token
      # this array is used to calculate SD and RSD for EDGE to Anchor intervals
      # for CCC clusters
      Global_CR3 <- CCCR3 # mean of consonant plateaux midpoints
      # for CC clusters
      Global_CR3 <- append(Global_CR3, CCR3) # mean of consonant plateaux midpoints
      # for C clusters
      Global_CR3 <- append(Global_CR3, CR3) # CCglobal synchronous with prevocalic consonant's plateau midpoint
      
      # generate series of anchor points increasing
      # in variability and/or distance from the prevocalic consonant
      # reset the anchor array to zero; one row for each anchor and one column for each token
      
      # loop produces anchor for each token based on Simplex Hypothesis
      stdv <- 0 # reset the value of the anchor stdev to zero
      Ae <- NULL # reset error term
      for (cycle in 1:variability_range){ #creates multiple anchor points for each token
        for (m in 1:words_per_word_type){ #creates anchor point for each token from the right edge of the token
          Ae<-stdv*(rnorm(n=1)) #normally distributed random error, assuming mean of 0
          #print(c(cycle, m, Ae, stdv))
          A_simp[cycle, m]<-Global_CM3[m] + vowel_duration + Ae #generate anchor A according to the simplex onset hypothesis
          #A(cycle, m) = CCglobal(m) + vowel_duration + Ae #generate anchor A according to the complex onset hypothesis
        }
        stdv<-stdv+variability_resolution #creates new anchor point
      }
      # loop produces anchor for each token based on Complex Hypothesis
      stdv <- 0 # reset the value of the anchor stdev to zero
      Ae <- NULL # reset error term
      for (cycle in 1:variability_range){ #creates multiple anchor points for each token
        for (m in 1:words_per_word_type){ #creates anchor point for each token from the right edge of the token
          Ae<-stdv*(rnorm(1)) #normally distributed random error, assuming mean of 0
          #print(c(cycle, m, Ae, stdv))
          A_comp[cycle, m]<-CCglobal[m]+vowel_duration+Ae #generate anchor A according to the complex onset hypothesis
        }
        stdv<-stdv+variability_resolution #creates new anchor point
      }
      # Note about consonantal landmarks: they are replaced with each cycle of the simulation
      # in constrast, RSD values for each landmark are stored across simulations.
      #creating matrices to hold the SD values
      x <- function(x){sd(x-Global_CL1)}
      y <- function(y){sd(y-Global_CR3)}
      z <- function(z){sd(z-CCglobal)}
      # computing the SD values
      LE_SD_simp[count,] <- apply(A_simp, 1, x)
      LE_SD_comp[count,] <- apply(A_comp, 1, x)
      RE_SD_simp[count,] <- apply(A_simp, 1, y)
      RE_SD_comp[count,] <- apply(A_comp, 1, y)
      CC_SD_simp[count,] <- apply(A_simp, 1, z)
      CC_SD_comp[count,] <- apply(A_comp, 1, z)
      # computing the RSD values
      LE_RSD_simp[count,] <- (apply(A_simp, 1, x))/((apply(A_simp, 1, mean))-mean(Global_CL1))
      LE_RSD_comp[count,] <- (apply(A_comp, 1, x))/((apply(A_comp, 1, mean))-mean(Global_CL1))
      RE_RSD_simp[count,] <- (apply(A_simp, 1, y))/((apply(A_simp, 1, mean))-mean(Global_CR3))
      RE_RSD_comp[count,] <- (apply(A_comp, 1, y))/((apply(A_comp, 1, mean))-mean(Global_CR3))
      CC_RSD_simp[count,] <- (apply(A_simp, 1, z))/(apply(A_simp, 1, mean)-mean(CCglobal))
      CC_RSD_comp[count,] <- (apply(A_comp, 1, z))/(apply(A_comp, 1, mean)-mean(CCglobal))
    } #simulating data ends here
  } # end of word_types==3
  if (word_types=="2") {
    tepa<-c("Testing Dyads")
    for (count in 1:simN) {
      # generate CCC tokens
      # generate timestamps for C3 (the prevocalic consonant)
      # generate general error-term for use later on
      e <- C3stdv*(rnorm(1))
      # generate R(ight plateau edge = Release) of prevocalic consonant
      # generate words_per_word_type/word_types Gaussian distributed numbers (for CCC tokens only)
      # with mean 500, variance 10
      CCCR3 <- rnorm(words_per_word_type/word_types, mean=500, sd=sqrt(20))
      # generate L(eft plateau edge = Target) of prevocalic consonant  
      CCCL3 <- CCCR3-C3p+e #generate L3 corresponding to R3 by assuming a plateau duration of C3p
      # calculate midpoint of prevocalic consonant plateau
      CCCM3 <- ((CCCR3+CCCL3)/2)
      
      # generate timestamps for C2
      # generate general error-term for use later on
      e1<-C23stdv*(rnorm(1)) #normally distributed random error
      e2<-C2stdv*(rnorm(1)) #normally distributed random error
      # Generate right edge of C2
      CCCR2 <- CCCL3 - C23ipi + e1 # generate right edge of C2 from left edge of C3 assuming an ipi of C23ipi
      # Generate left edge of C2
      CCCL2 <- CCCR2 - C2p + e2 # generate left edge from right edge by assuming a plateau duration
      # Calculate midpoint of C2
      CCCM2 <- ((CCCR2+CCCL2)/2)
      
      # generate timestamps for C1
      # generate general error-term for use later on
      e1<-C12stdv*(rnorm(1)) # normally distributed random error
      e2<-C3stdv*(rnorm(1))
      # Generate right edge 
      CCCR1 <- CCCL2 - C12ipi + e1 # generate right edge of C1 from left edge of C2 assuming ipi of 40ms
      # generate L(eft plateau edge = Target) of C1
      CCCL1 <- CCCR1 - C3p + e2 # generate L2 corresponding to CR1 by assuming a plateau of 10ms
      # calculate midpoint of prevocalic consonant
      CCCM1 <-  ((CCCR1 + CCCL1)/2) # right edge of C1
      
      #generate CC tokens
      #generate timestamps for C3 (prevocalic consonant)
      # generate general error-term for use later on      
      e<-C3stdv*(rnorm(1)) # normally distributed random error, 0 mean
      # generate R(ight plateau edge = Release) of prevocalic consonant
      CCR3 <- rnorm(words_per_word_type/word_types, mean=500, sd=sqrt(20)) # generate N Gaussian distributed numbers with mean 500, variance 10
      # generate L(eft plateau edge = Target) of prevocalic consonant
      CCL3 <- CCR3-C3p+e # generate L3 corresponding to R3 by assuming a plateau duration of C3p
      # calculate midpoint of prevocalic consonant plateau
      CCM3 <- ((CCR3+CCL3)/2)
      
      #generate timestamps for C2
      # generate general error-term for use later on
      e1<-C23stdv*(rnorm(1))
      e2<-C2stdv*(rnorm(1))
      # Generate right edge of C2
      CCR2 <- CCL3-C23ipi+e # generate right edge of C2 from left edge of C3 assuming an ipi of C23ipi
      # Generate left edge of C2
      CCL2 <- CCR2-C2p+e # generate left edge from right edge by assuming a plateau duration
      # Calculate midpoint of C2
      CCM2 <- ((CCR2+CCL2)/2)
      
      # generate timestamps for CCglobal
      # for CCC clusters
      CCglobal <- apply(cbind(CCCM1, CCCM2, CCCM3), 1, mean) #mean of consonant plateaux midpoints        
      # for CC clusters
      CCglobal <- append(CCglobal, apply(cbind(CCM2, CCM3), 1, mean)) # mean of consonant plateaux midpoints
      
      # populate a single array with the midpoint of the pre-vocalic
      # consonant of every word type; this array will be used to generate anchors
      # for CCC clusters
      Global_CM3 <- CCCM3 # mean of consonant plateaux midpoints
      # for CC clusters
      Global_CM3 <- append(Global_CM3, CCM3, after=length(CCCM3)) # mean of consonant plateaux midpoints
      
      # populate a single array with the Left_edge of the consonant cluster for every token
      # this array will be used to calculate SD and RSD for EDGE to Anchor intervals
      # for CCC clusters
      Global_CL1 <- CCCL1 # Assigns the left edge of tri-consonantal tokens to the first third of Global_Cl1
      # for CC clusters
      Global_CL1 <- append(Global_CL1, CCL2, after=length(CCCL1)) # Assigns the left edge of bi-consonantal tokens to the second third of Global_Cl1
      
      # populate a single array with the Right_edge of the consonant cluster for every token
      # this array is used to calculate SD and RSD for EDGE to Anchor intervals
      # for CCC clusters
      Global_CR3 <- CCCR3 # mean of consonant plateaux midpoints
      # for CC clusters
      Global_CR3 <- append(Global_CR3, CCR3, after=length(CCCR3)) # mean of consonant plateaux midpoints
      
      # generate series of anchor points increasing
      # in variability and/or distance from the prevocalic consonant
      # reset the anchor array to zero; one row for each anchor and one column for each token
      
      # loop produces anchor for each token based on Simplex Hypothesis
      stdv <- 0 # reset the value of the anchor stdev to zero
      Ae <- NULL # reset error term
      for (cycle in 1:variability_range){ #creates multiple anchor points for each token
        for (m in 1:words_per_word_type){ #creates anchor point for each token from the right edge of the token
          Ae<-stdv*(rnorm(n=1)) #normally distributed random error, assuming mean of 0
          #print(c(cycle, m, Ae, stdv))
          A_simp[cycle, m]<-Global_CM3[m] + vowel_duration + Ae #generate anchor A according to the simplex onset hypothesis
          #A(cycle, m) = CCglobal(m) + vowel_duration + Ae #generate anchor A according to the complex onset hypothesis
        }
        stdv<-stdv+variability_resolution #creates new anchor point
      }
      # loop produces anchor for each token based on Complex Hypothesis
      stdv <- 0 # reset the value of the anchor stdev to zero
      Ae <- NULL # reset error term
      for (cycle in 1:variability_range){ #creates multiple anchor points for each token
        for (m in 1:words_per_word_type){ #creates anchor point for each token from the right edge of the token
          Ae<-stdv*(rnorm(1)) #normally distributed random error, assuming mean of 0
          #print(c(cycle, m, Ae, stdv))
          A_comp[cycle, m]<-CCglobal[m]+vowel_duration+Ae #generate anchor A according to the complex onset hypothesis
        }
        stdv<-stdv+variability_resolution #creates new anchor point
      }
      # Note about consonantal landmarks: they are replaced with each cycle of the simulation
      # in constrast, RSD values for each landmark are stored across simulations.
      #creating matrices to hold the SD values
      x <- function(x){sd(x-Global_CL1)}
      y <- function(y){sd(y-Global_CR3)}
      z <- function(z){sd(z-CCglobal)}
      # computing the SD values
      LE_SD_simp[count,] <- apply(A_simp, 1, x)
      LE_SD_comp[count,] <- apply(A_comp, 1, x)
      RE_SD_simp[count,] <- apply(A_simp, 1, y)
      RE_SD_comp[count,] <- apply(A_comp, 1, y)
      CC_SD_simp[count,] <- apply(A_simp, 1, z)
      CC_SD_comp[count,] <- apply(A_comp, 1, z)
      # computing the RSD values
      LE_RSD_simp[count,] <- (apply(A_simp, 1, x))/((apply(A_simp, 1, mean))-mean(Global_CL1))
      LE_RSD_comp[count,] <- (apply(A_comp, 1, x))/((apply(A_comp, 1, mean))-mean(Global_CL1))
      RE_RSD_simp[count,] <- (apply(A_simp, 1, y))/((apply(A_simp, 1, mean))-mean(Global_CR3))
      RE_RSD_comp[count,] <- (apply(A_comp, 1, y))/((apply(A_comp, 1, mean))-mean(Global_CR3))
      CC_RSD_simp[count,] <- (apply(A_simp, 1, z))/(apply(A_simp, 1, mean)-mean(CCglobal))
      CC_RSD_comp[count,] <- (apply(A_comp, 1, z))/(apply(A_comp, 1, mean)-mean(CCglobal))
    } #simulating data ends here
    
  }
  # assorted variables for diagnostics / plotting
  aip_1<-rep(c(1:variability_range), 3)
  edgep_1<-rep(c("LE_RSD", "RE_RSD", "CC_RSD"), each=variability_range)
  LE_RSD_simp_median<-apply(apply(LE_RSD_simp, 2, sort), 2, median)
  RE_RSD_simp_median<-apply(apply(RE_RSD_simp, 2, sort), 2, median)
  CC_RSD_simp_median<-apply(apply(CC_RSD_simp, 2, sort), 2, median)
  LE_RSD_comp_median<-apply(apply(LE_RSD_comp, 2, sort), 2, median)
  RE_RSD_comp_median<-apply(apply(RE_RSD_comp, 2, sort), 2, median)
  CC_RSD_comp_median<-apply(apply(CC_RSD_comp, 2, sort), 2, median)
  simp<-c(LE_RSD_simp_median, RE_RSD_simp_median, CC_RSD_simp_median)
  comp<-c(LE_RSD_comp_median, RE_RSD_comp_median, CC_RSD_comp_median)
  RE_RSD_median<-c(RE_RSD_simp_median, RE_RSD_comp_median)
  CC_RSD_median<-c(CC_RSD_simp_median, CC_RSD_comp_median)
  # median RDSs across simulations as a function of anchorindex
  plot.1<-data.frame(anchorindex=aip_1, edge=edgep_1, parse_s=simp, parse_c=comp)
  # aggregating data for goodness of fit evaluation
  RE_RSD_simp<-t(RE_RSD_simp)
  LE_RSD_simp<-t(LE_RSD_simp)
  CC_RSD_simp<-t(CC_RSD_simp)
  RE_RSD_comp<-t(RE_RSD_comp)
  LE_RSD_comp<-t(LE_RSD_comp)
  CC_RSD_comp<-t(CC_RSD_comp)
  # looping through the data to get the gof results
  tata_simp<-matrix(ncol=4)
  tata_comp<-matrix(ncol=4)
  sigfit<-function(x) {
    if(x > 98.503) {
      SigFit<-1
    } else {
      SigFit<-0
    }
  }
  # analyzing data simplex
  for (i in 1 : variability_range) {
    sim_RSD<-cbind(RE_RSD_simp[i,], LE_RSD_simp[i,],CC_RSD_simp[i,])
    temp<-apply(sim_RSD, 1, function(x) (lm(x ~ data_RSD)))
    # organizing data for final analyses
    # creating anchor-index
    anchor_idx<-rep(i, times=simN)
    # extracting F-Statistics
    fstat<-unlist(lapply(temp, function(x) summary(x)$fstatistic[1]))
    # extracting R-Squared values
    rsquared<-unlist(lapply(temp, function(x) summary(x)$r.squared))
    # check for SigFit
    # applying criterion based on one model parameter (df=1) and three data points (df=2), actually 98.503
    sgf<-sapply(fstat, sigfit)
    # aggregating data
    test<-matrix(data=c(anchor_idx, fstat, rsquared, sgf), nrow=length(anchor_idx), ncol=4, dimnames=list(c(NULL), c("Anchorindex", "Fratio", "Rsquared", "SigFit")))
    # adding sgf to existing data
    tata_simp<-rbind(tata_simp, test)
  }
  #outp_sp<-temp
  tata_simp<-tata_simp[complete.cases(tata_simp),]
  tata_simp<-as.data.frame(tata_simp)
  tata_simp$Anchorindex<-as.factor(tata_simp$Anchorindex)
  output_simp<-tapply(tata_simp$SigFit, tata_simp$Anchorindex, sum)
  # analyzing data complex
  for (i in 1 : variability_range) {
    sim_RSD<-cbind(RE_RSD_comp[i,], LE_RSD_comp[i,],CC_RSD_comp[i,])
    temp<-apply(sim_RSD, 1, function(x) (lm(x ~ data_RSD)))
    # organizing data for final analyses
    anchor_idx<-rep(i, times=simN)
    # extracting F-Statistics
    fstat<-unlist(lapply(temp, function(x) summary(x)$fstatistic[1]))
    # extracting R-Squared values
    rsquared<-unlist(lapply(temp, function(x) summary(x)$r.squared))
    # check for SigFit
    # applying criterion based on one model parameter (df=1) and three data points (df=2), actually 98.503
    sgf<-sapply(fstat, sigfit)
    # aggregating data
    test<-matrix(data=c(anchor_idx, fstat, rsquared, sgf), nrow=length(anchor_idx), ncol=4, dimnames=list(c(NULL), c("Anchorindex", "Fratio", "Rsquared", "SigFit")))
    # adding sgf to existing data
    tata_comp<-rbind(tata_comp, test)
  }
  #outp_cp<-temp
  tata_comp<-tata_comp[complete.cases(tata_comp),]
  tata_comp<-as.data.frame(tata_comp)
  tata_comp$Anchorindex<-as.factor(tata_comp$Anchorindex)
  output_comp<-tapply(tata_comp$SigFit, tata_comp$Anchorindex, sum)
  # diagnostic plot 2
  output_plot.2<-cbind(output_simp, output_comp)
  names(output_plot.2)<-NULL
  colnames(output_plot.2)<-c("parse_s", "parse_c")
  aip_2<-(1:variability_range)
  plot.2<-data.frame(anchorindex=aip_2, output_plot.2, hitr_s=(output_simp/simN), hitr_c=(output_comp/simN))
  # assessing overall model quality
  # sum of hits per number of simulations
  modq_s<-(sum(plot.2[,2]))/simN
  modq_c<-(sum(plot.2[,3]))/simN
  # assorted data for third diagnostic plot
  # sorting by Rsquared (asc), tie-breaker by Fratio (asc)
  tata_simp<-tata_simp[order(tata_simp[,3], tata_simp[,2]),]
  tata_comp<-tata_comp[order(tata_comp[,3], tata_comp[,2]),]
  aip_3<-rep(c(1:variability_range), 2)
  parse.f<-rep(c("simp","comp"), each=variability_range)
  # median
  simp_rs_median<-tapply(tata_simp$Rsquared, tata_simp$Anchorindex, median)
  comp_rs_median<-tapply(tata_comp$Rsquared, tata_comp$Anchorindex, median)
  simp_fr_median<-tapply(tata_simp$Fratio, tata_simp$Anchorindex, median)
  comp_fr_median<-tapply(tata_comp$Fratio, tata_comp$Anchorindex, median)
  rs_median<-c(simp_rs_median, comp_rs_median)
  fr_median<-c(simp_fr_median, comp_fr_median)
  plot.3_median<-data.frame(anchorindex=aip_3, parse=parse.f, rs_median=rs_median, fr_median=fr_median)
  # mean
  simp_rs_mean<-tapply(tata_simp$Rsquared, tata_simp$Anchorindex, mean)
  comp_rs_mean<-tapply(tata_comp$Rsquared, tata_comp$Anchorindex, mean)
  simp_fr_mean<-tapply(tata_simp$Fratio, tata_simp$Anchorindex, mean)
  comp_fr_mean<-tapply(tata_comp$Fratio, tata_comp$Anchorindex, mean)
  rs_mean<-c(simp_rs_mean, comp_rs_mean)
  fr_mean<-c(simp_fr_mean, comp_fr_mean)
  plot.3_mean<-data.frame(anchorindex=aip_3, parse=parse.f, rs_mean=rs_mean, fr_mean=fr_mean)
  # combine analyses for output
  output<-list("perf"=list("Performance Simplex"=modq_s, "Performance Complex"=modq_c), "mode"=tepa, "Plot_1"=plot.1, "Plot_2"=plot.2, "Plot_3"=list("mean"=plot.3_mean, "median"=plot.3_median))
  cat("\n","Overall Quality of Modell-Performance", "\t", "(", tepa, ")", "\n",
      "(Ratio of:","\t", "Total Number of (any Anchor-)Hits / Number of Simulations)","\n",
      "------------------------","\n",
      "Simplex Modelling:", "\t", modq_s, "\t","\t","\t","\t", sum(plot.2[,2])," / ", simN, "\n",
      "Complex Modelling:", "\t", modq_c, "\t","\t","\t","\t", sum(plot.2[,3])," / ", simN, "\n", sep="")
  return(invisible(output))
}