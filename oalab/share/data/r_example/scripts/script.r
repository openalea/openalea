#!/usr/var/env Rscript

library(deSolve)

parameters = c(h = 10, h2=1,lambda = 1, lambda2=1)

state = c(LFY=0,CAL=0,AGL=0,AP1=0,TFL1=1,AUX=0,AUX2=1,AUX3=0,FT=0)

network=function(t, state, parameters) {
	with(as.list(c(state, parameters)),{
	     #node inputs
		 w_LFY = max(min(AGL,AUX),min(FT,AUX,1-TFL1),min(AP1,AUX),CAL)
		 w_CAL = LFY
		 w_AGL = min(1-LFY,1-AP1,FT)  
		 w_AP1 = max(LFY,max(FT,1-TFL1),CAL)
	     w_TFL1 = min(1-AP1,1-LFY)
		 w_AUX = 1-AUX2
		 w_AUX2 = 1-AUX3
		 w_AUX3 = 1-AUX
		 w_FT = 1
						
	     #rates of change
		 dLFY = ((-exp(0.5*h)+exp(-h*(w_LFY)))/((1-exp(0.5*h))*(1+exp(-h*(w_LFY-0.5)))))-(lambda*LFY)
	     dCAL = 0
	     dAGL = ((-exp(0.5*h)+exp(-h*(w_AGL)))/((1-exp(0.5*h))*(1+exp(-h*(w_AGL-0.5)))))-(lambda*AGL)
		 dAP1 = 0
		 dTFL1 = ((-exp(0.5*h)+exp(-h*(w_TFL1)))/((1-exp(0.5*h))*(1+exp(-h*(w_TFL1-0.5)))))-(lambda*TFL1)
		 dAUX = ((-exp(0.5*h)+exp(-h*(w_AUX)))/((1-exp(0.5*h))*(1+exp(-h*(w_AUX-0.5)))))-(lambda*AUX)
		 dAUX2 = ((-exp(0.5*h)+exp(-h*(w_AUX2)))/((1-exp(0.5*h))*(1+exp(-h*(w_AUX2-0.5)))))-(lambda*AUX2)
		 dAUX3 = ((-exp(0.5*h)+exp(-h*(w_AUX3)))/((1-exp(0.5*h))*(1+exp(-h*(w_AUX3-0.5)))))-(lambda*AUX3)
		 dFT = ((-exp(0.5*h2)+exp(-h2*(w_FT)))/((1-exp(0.5*h2))*(1+exp(-h2*(w_FT-0.5)))))-(lambda*FT)
		 
		 # return the rate of change
		 list(c(dLFY, dCAL, dAGL, dAP1, dTFL1, dAUX, dAUX2, dAUX3, dFT))
	})
}

times =seq(0,20,by=0.01)

out = ode(y=state,times=times,func=network,parms=parameters)

out

plot(out)