![Alt text](logos/logo_v1.jpg?raw=true "Title")
## First Stop for First-time home buyers
Team:Sha Li, Mobing Zhuang, Gary Gregg, Deepa Agrawal | Course project for Data 515A
### Background: 
First time new buyers in this generation have some of the questions same as previous generations that what budget they should have to get their dream home, These buyers also have some very unique problems like what bidding price will help them get the first home they make an offer on or what will be the all-in monthly cost they would incur after buying home of their dreams.Our project aims at solving all of these problems. We would achieve this by first building a regression model to predict house prices. We are using King County housing dataset for the year 2014-2015 with prices for about 21k houses. As a part of the regression model, we would first try to find all the features which are strongly correlated with the house prices. Once we have identified the most relevant features, we would give the user the capability to enter values for those features and get the prediction they are looking for. For this purpose, we aim to build a web UI tool. This tool would be most helpful to first-time home buyers to set up expectations, plan budgets and make an informed decision on expenses before they even go through the exhaustive house-hunting process given current real-estate market status. 

### Organization of the project

The project has the following structure:

```
UWHousingTeam/
  |- README.md
  |- UWHousingTeam/
     |- data/
        |-Merged_Data.csv
        |-Database_HousePrice.py
     |- html_landing_page/ 
        |- ...
     |- Scripts/
        |-part1_predict_price.py
        |-part2_bid_price.py
        |-part3_monthly_cost.py
        |-house_price_model_2
     |- tests/
        |- ...
  |- examples
     |- User_Guide
  |- logos
     |- logo_v1  
  |- doc/
     |- FunctionalSpec
     |- Designspec
     |- Projectplan
     |- TechnologyReview
     |-Final presentation
  |- setup.py
  |- LICENSE
  |- requirements.txt
```
### Installation

To install FirstStop perform following steps:

* clone the repo: git clone https://github.com/sliwhu/UWHousingTeam
* run the setup.py file: python setup.py install
* run requirements.txt to ensure all dependencies exist : pip install -r requirements.txt
* go to Scripts folder: cd UWHousing/Scripts
* run bokeh server: bokeh serve --port 5001 part1_predict_price.py
* Open another terminal and go to Scripts folder: cd UWHousing/Scripts
* run bokeh server: bokeh serve --port 5002 part2_bid_price.py
* Open another terminal and go to Scripts folder: cd UWHousing/Scripts
* run bokeh server: bokeh serve --port 5003 part3_monthly_cost.py
* go to landing page http://housing-prediction.azurewebsites.net/UWHousingTeam/html_landing_page/
* follow the User_Guide in examples folder 
