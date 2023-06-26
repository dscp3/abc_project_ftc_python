## Business Problem
    
Company ABC is a marketplace of restaurants. That is, its core business is to facilitate contact and negotiations between customers and restaurants. Restaurants sign up on the ABC app, that provides general info to the customers, such as address, type of food served, ratings and more. A new CEO has just arrived and, to better understand the business of ABC, he needs detailed information about the restaurants presented in the database, alongside some metrics regarding the company, ideally presented in a dashboard so he can access at any time.
    
## What were the premises?
    
Data used for this project was provided on Kaggle. It is ficticious and used exclusively for learning purposes. It is also open and available for download in the following link: https://www.kaggle.com/datasets/akashram/zomato-restaurants-autoupdated-dataset?resource=download&select=zomato.csv
    
## Strategy to solve the problem
    
To give an accurate view of ABC to the CEO, I decided to build a dashboard on Streamlit Cloud so it could be easily accessed. 
    
Regarding the main views of the dash, we have: 

  **1. Main Page:** Basically a ‘landing page’ so users can better understand what metrics there are on the dashboard, alongside some general company information. In the side bar, they can navigate through the other pages
    
  **2. Geography:** This page is related to the geographic distribution and detailed information about the restaurants in the database (including a interactive map so the user can select country and city at will). Among the information in this page, we have:
  1. How many countries and cities are presented in the database?
  2. What is the average rating across countries?
  3. How many types of restaurants (’cuisines’) do we have per country?
  4. Countries with lower (or higher) rating score than the average
  5. Countries with less (or more) votes per restaurant than the average (measuring engagement)
  6. Best (and worst) cities by restaurant ratings
    
  **3. Cuisines:** The last page is focused on the type of restaurants and some associated metrics:
  1. How many types of restaurants? Which ones are the relevant?
  2. Which cuisines types have the best (and worst) ratings?
  3. What is the top 10 restaurants by votes and rating? And the bottom 10?
    
## A few insights
    
  **1. India is the most relevant country:**
  In terms of revenue impact to ABC, India is the most important country. We have +3,000 restaurants signed up, in 49 different cities. Besides, indian customers are highly engaged, giving 900 votes per restaurant on average. We also have a relevant number of North Indian type of restaurants (+800)
    
  **2. Indian restaurants have the higher ratings:**
  By ratings and number of votes, 9 out of the 10 best restaurants are indian. This also shows that the main market for ABC is the asian country. For the bottom 10, we have 3 indian ones, but it was not possible to see a clear pattern for this cluster. 
    
  **3. Brazil has the lowest engagement rate and low ratings:**
  Brazil has 200+ restaurants in the database. Despite that, there are only 3 cities and all of them are at the bottom 10 in terms of ratings (Brasília (2.88 - 4th), São Paulo (3.33 - 6th) and Rio de Janeiro (3.76 - 9th). We also could see the worst engagement rate, with only 12 votes per restaurant on average (in terms of comparison, Indonesia has the highest rate, with over 1,100 votes per restaurant).

  **4. North Indian, American and Cafe are the most relevant types of cuisines:**
  More than 1,800 restaurants are in one of those 3 categories. By comparison, more traditional cuisines, such as Pizza, Burguers and Fast Food, have only 743 restaurants.  
    
## Final product
    
The final product is the dashboard built with Streamlit Cloud. It can be accessed through the following link: https://abc-project-ftc-dscp3.streamlit.app/
    
## Conclusion
    
With this project, I could learn numerous features and libraries in Python, such as: folium, streamlit, plotly, ydata-profiling, pandas and inflection, despite learning how to develop a structured project with ETL concepts and hosting it on Cloud with Streamlit

About the business problem, it can be seen that relevant insights were provided regarding both geographic distribution and types of restaurants presented in the database, helping the CEO of ABC Company to better understand the business.
    
## Next steps
    
As next steps to improve that could improve the project:
  
  1. Providing more filter options so users can interact even more with data provided
  2. Bringing specific metrics about the ‘India cluster’, since it is the most relevant country for the company
