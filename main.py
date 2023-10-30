import warnings
import os
import openai
import evadb
import subprocess


# Suppress warnings
warnings.filterwarnings("ignore")

# Set OpenAI API key
os.environ['OPENAI_KEY'] = 'sk-.....'
open_ai_key = os.environ.get('OPENAI_KEY')
openai.api_key = open_ai_key

cursor = evadb.connect().cursor()

#Using the SQLLite engine
params = {
    "database": "evadb.db"
}
query = f"""CREATE DATABASE sqlite_data WITH ENGINE = 'sqlite', PARAMETERS = {params};"""

# Drop the PLAYERDATA table if it exists
dropTableIfExists = "DROP TABLE IF EXISTS PLAYERDATA;"
cursor.query(dropTableIfExists).execute()

# Create PLAYERDATA table
createTable = """
CREATE TABLE IF NOT EXISTS PLAYERDATA(
    sofifa_id INTEGER PRIMARY KEY,
    short_name TEXT,
    long_name TEXT,
    player_positions TEXT,
    overall INTEGER,
    potential INTEGER,
    wage_eur FLOAT(64,64),
    value_eur FLOAT(64,64),
    age INTEGER
);
"""
cursor.query(createTable).df()

# Load data into PLAYERDATA table
loadData = """LOAD CSV 'out.csv' INTO PLAYERDATA;"""
cursor.query(loadData).execute()

# Query PLAYERDATA table
cursor.query("""SELECT * FROM PLAYERDATA""").df()

# Function to chat with OpenAI and convert English to SQL
def ChatWithPandas(message, tableName):
    try:
        # Interact with the chat model
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"""You are a helpful assistant that converts English sentence to SQL in postgresql.
                First we need to know the schema of {tableName} and then run the
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = '{tableName}';"""},
                {"role": "user", "content": message},
            ],
        )
        sql_query = response.choices[0].message['content']
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None
    return sql_query

# Execute SQL queries
result_df = ChatWithPandas('output the sum of the age in the dataset', 'PLAYERDATA')
chat_query1 = f"""{result_df}"""
cursor.query(chat_query1).df()
print(result_df)
print(cursor.query(chat_query1).df())

result_df2 = ChatWithPandas('output the sum wage_eur in the dataset', 'PLAYERDATA')
chat_query2 = f"""{result_df2}"""
cursor.query(chat_query2).df()
print(result_df2)
print(cursor.query(chat_query2).df())
