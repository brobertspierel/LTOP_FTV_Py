# LTOP Overview

version: 0.0.3

## These docs and the associated python scripts are currently (10/18/2022) in testing and subject 
to change. 

LandTrendr (LT) is a set of spectral-temporal segmentation algorithms that focuses on removing the 
natural spectral variations in a time series of Landsat Images. Stabilizing the natural variation 
in a time series emphasizes how a landscape evolves with time. This is useful in many areas as it 
gives information on the state of a landscape. This includes many different natural and 
anthropogenic processes including: growing seasons, phenology, stable landscapes, senesence, 
clearcut etc. LandTrendr is mostly used in Google Earth Engine (GEE), an online image processing 
console, where it is readily available for use.  

One impediment to running LT over large geographic domains is selecting the best paramater set for
a given landscape. The LandTrendr GEE function uses 9 arguments: 8 parameters that control how 
spectral-temporal segmentation is executed, and an annual image collection on which to assess and 
remove the natural variations. The original LandTrendr article (Kennedy et al., 2010) illustrates 
some of the effects and sensitivity of changing some of these values. The default parameters for 
the LandTrendr GEE algorithm do a satisfactory job in many circumstances, but extensive testing 
and time is needed to hone the parameter selection to get the best segmentation out of the 
LandTrendr algorithm for a given region. Thus, augmenting the LandTrendr parameter selection 
process would save time and standardize a method to choose parameters, but we also aim to take 
this augmentation a step further. 

Traditionally, LT has been run over an image collection with a single LT parameter configuration 
and is able to remove natural variation for every pixel time series in an image. But no individual 
LandTrendr parameter configuration is best for all surface conditions. For example, one paramater 
set might be best for forest cover change while another might be preferred for agricultural 
phenology or reservoir flooding. To address this shortcoming, we developed a method that 
delineates patches of spectrally similar pixels from input imagery and then finds the best 
LandTrendr parameters group. We then run LandTrendr on each patch group location with a number of 
different paramater sets and assign scores to decide on the best parameter configuration. 
This process is referred to as LandTrendr Optimization (LTOP). 