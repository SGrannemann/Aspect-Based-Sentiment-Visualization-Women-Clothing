import pandas as pd
import sqlite3







def setup_db_with_key(cursor):
    
    cursor.execute("""CREATE TABLE reviews ("index" INTEGER PRIMARY KEY NOT NULL,
                "Clothing_ID" INTEGER,
                "Age" INTEGER,
                "Title" TEXT,
                "Review_Text" TEXT,
                "Rating" INTEGER,
                "Recommended_IND" INTEGER ,
                "Positive_Feedback_Count" INTEGER,
                "Division_Name" TEXT,
                "Department_Name" TEXT,
                "Class_Name" TEXT
                );
                """)
    cursor.execute("""CREATE TABLE user_query ("index" INTEGER PRIMARY KEY NOT NULL, "user_query" TEXT) """)

if __name__ == '__main__':
    data = pd.read_csv('Womens Clothing E-Commerce Reviews.csv')
    # replace spaces in columns names because that can mess with SQL
    data.columns = data.columns.str.replace(' ', '_')
    data.drop('Unnamed:_0', axis=1, inplace=True)

    con = sqlite3.connect('reviews.sqlite')
    #with con.cursor() as cursor:
    #    setup_db_with_key(cursor)

    data.to_sql("reviews", con, if_exists='append', index=False)

    con.close()