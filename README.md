# Sales-Dashboard
A sales dashboard created on Super Store dataset available on kaggle.
- In this project, the dataset I used named Superstore Dataset is record of 4 year sale of a Store, has almost 10,000 rows and 21 Columns. Dataset link: https://www.kaggle.com/datasets/vivek468/superstore-dataset-final
- My plan to make a sales dashboard using this dataset, and also train a model which predicts the sales and profit, based on given details like product, price, region etc.

## Progress
- I checked the dataset is clean or not
- Calculated some KPIs (Key Performance Indicator)
  - Total Sales, Total Profit, Total Orders (unique Order ID), Average Order Value, Profit Margin(%)
  - KPIs are the outcomes that we need to measure that have the most impact moving an organisation towards it's vision or sucess.
- I expnad my aggregation by:
  - Created "month_sales", stores mnth wise sale, total sales, and profit.
  - And created "cat_sales", "sub_cat_sales", "region_sales and "seg_sales"
  - By creating these I can answer to questions like
    - Which category is most profit?
    - Which region has highest revenue?
    - Which segment gives maximum profit?
- Calculated the correlation between sales, profit, and discount
> Below Correlation matrix value is rounded to 3 decimal places 

  |  | Sales | Profit | Discount |
  | --- | --- | --- | --- |
  | Sales | 1.000 | 0.479 | -0.028 |
  | Profit | 0.479 | 1.000 | -0.219 |
  | Discount | -0.028 | -0.219 | 1.000 |

  - As we observe:
    - Sales and Discount:
      - The value is very close to 0 (means no relation), which can be interpreted as discount is not increasing sales
    - Sales and profit has positive correlation
      - Sales helps growth profit
    - Profit and Discount has negative correlation: which resonable as discount eats the profit margin
      - It has weak negative correlation, discounts slightly reduces the profit, but it is not only factor affecting it.
    - Insights:
      -  Discounts not increasing the sales
      -  And discount slightly reuces the profit
    -  That suggest discount strategy is ineffective
    - Might be
      - Dicounting too randomly
      - Discounting on products that already sell well
      - Discounting on low demanded products without impact

## To Do
- Can find Just to confirm
  - Correlation by product category
  - Correlation by region
  - Correlation by customer segment
- can plot scatter plot for ( sale vs profit, or discount vs profit )
- Because overall correlation can hide patterns.
- Find the loss making products (can be done year wise)
- Find Year-Over-Year growth
- Find Time Series
  - A time series is data collected and recorded over time in sequence.
  - means data points are arranged by date, month, quarter, or year. How things change over time.
  - ex: sales over months
