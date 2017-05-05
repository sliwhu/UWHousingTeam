# Technology review
## --Visualization tools evaluation
### Shiny

pros: 

* well developed
* more reference can be found online
* more familiar
* can be hosted on shinyapps.io
* some of us already have certain level of Shiny knowledge
      
cons: 

* possibly less flexibility than Bokeh 
* most of our data will be processed using python and python packages, 
  may have some compatibility problems

### Bokeh

pros: 

* this is a python class, opportunity of practicing a new tool
* powerful computation and interactive visualization
* much easier to combine with our data and prediction output
      
cons: 

* brand new technology to all of our team members, learning curve
* less reference can be found online
* there is not known place to host Bokeh apps, to our knowledge. 

## --Statistical modeling tools evaluation
### Python scikit learn

#### Ordinary linear regression
In linear regression, the relationships are modeled using linear predictor functions whose unknown model parameters are estimated from the data. 

pros: 
* The most important advantage of Ordinary linear regression is its simplicity. 

cons: 
* There is a disadvantage of overfitting the model

#### Ridge regression
Ridge regression solves a regression model where the loss function is the linear least squares function and regularization is given by the l2-norm. 

pros: 
* The ridge regression has two important advantages over the linear regression. 
* The most important one is that it penalizes the estimates. 
* It doesn't penalize all the feature’s estimate arbitrarily. 

cons:
* Ridge regression cant zero out the co-efficients

#### Lasso regression
LASSO is a regression analysis method that performs both variable selection and regularization in order to enhance the prediction accuracy and interpretability of the statistical model it produces. 
pros:
* The biggest advantage of Lasso is that it produces sparse matrix. This implies that lasso can zero out coefficients and we are able to get a better sense of which features are more corelated with response.

cons:
* 

#### Principal Component Analysis


### Self written up algorithms
### ..
