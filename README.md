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
- 
- Calculated some more KPI's like top 10 customers, regular customers, revenue of each order, monthly sales with 3 and 6 month moving average, YOY Growth, and seasonality
- And plot some graphs Profit vs Discount, Profit vs Weighted Discount and Profit vs Sales

## To Do
- Can find Just to confirm
  - Correlation by product category
  - Correlation by region
  - Correlation by customer segment
- Find the top loss making products year wise
- Start visualizing the insights I found.
 
## Revision things
- df.resample()
  - `mont_sales = df.resample('ME', on='Order Date')[['Sales','Profit','Discount']].sum()`
  -  It works similarly to a groupby operation but is specialized for datetime-like indices. 
  -  This method is a powerful tool used for frequency conversion and resampling of time-series data.
  -  Resampling generally falls into two categories:
    1. **Downsampling:** Reducing the data frequency (e.g., converting daily data into weekly totals). This requires an aggregation function like .sum() or .mean().
    2. **Upsampling:** Increasing the data frequency (e.g., converting monthly data into daily data). This often creates missing values, requiring imputation methods like .ffill() (forward fill) or .interpolate().
  - Parameter:
    1. rule: A frequency string that defines the target interval (e.g., 'D' for Day, 'ME' for Month End, 'W' for Week).
    2. on: Optional column name to use for resampling if the datetime is not in the index.
    3. label:  Defines which side of the interval is "closed" and which label to use for the resulting bins.

- I use a **Weighted average discount** instead of an average discount because
    - Average discount treats all orders equal, irrespective of sales
    - But weighted average discount calculates the average, depending on the order sales, i.e. gives more value to larger sales value.
    </br>Formula: ` weighted_discount = sum(discount * sales) / sum(sales) `

- df.rolling()
  - The rolling() method in pandas is used to perform rolling window calculations.
  - It creates a window of a specified size that slides over your data, allowing you to apply **statistical functions** (like mean, sum, standard deviation or even custom function through apply()) to that subset of data at each step.
  - ` monthly_sales['Sales_MA_6'] = monthly_sales['Sales'].rolling(window=6).mean() `
  - It left NaN for starting ending windows where window size is less than the required window.
  - To avoid NaN I use `.fillna(0)`
