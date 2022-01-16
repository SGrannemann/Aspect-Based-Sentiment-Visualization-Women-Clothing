import pandas as pd
import sqlite3

data = pd.read_csv('Womens Clothing E-Commerce Reviews.csv')
# replace spaces in columns names because that can mess with SQL
data.columns = data.columns.str.replace(' ', '_')

con = sqlite3.connect('reviews.sqlite')

data.to_sql("Reviews", con)

con.close()

