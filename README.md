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

## To Do
- Now I have to calculate the corelation between sales, profit, and discount.
- Find the loss making products
- Find Year-Over-Year growth
