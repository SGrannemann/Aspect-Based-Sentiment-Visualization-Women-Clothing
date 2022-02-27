
"""
Script used to setup the initial database from the CSV files. This is necessary because pandas itself does not provide a means to set a primary key.
So we set up the database "manually" and then append the data with pandas.
"""
import pandas as pd
import sqlite3




def setup_db_with_key(cursor):
    """Method that creates the tables using the sqlite3 cursor.
    """
    cursor.execute("""CREATE TABLE reviews ("index" INTEGER PRIMARY KEY NOT NULL,
                "Review_Text" TEXT
                );
                """)
    cursor.execute("""CREATE TABLE user_query ("index" INTEGER PRIMARY KEY NOT NULL, "user_query" TEXT) """)

if __name__ == '__main__':
    data = pd.read_csv('Womens Clothing E-Commerce Reviews.csv')
    # replace spaces in columns names because that can mess with SQL
    data.columns = data.columns.str.replace(' ', '_')
    #data.drop('Unnamed:_0', axis=1, inplace=True)
    data = data['Review_Text']
    con = sqlite3.connect('reviews.sqlite')
    cursor = con.cursor()
    setup_db_with_key(cursor)
    cursor.close()
    data.to_sql("reviews", con, if_exists='append', index=False)

    con.close()