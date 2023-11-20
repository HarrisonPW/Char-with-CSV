import warnings
import os
import openai
import evadb
import time
import matplotlib.pyplot as plt
import seaborn as sns

# Suppress warnings
warnings.filterwarnings("ignore")

# Set OpenAI API key
os.environ['OPENAI_KEY'] = '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'
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
dropTableIfExistsForCustomer = "DROP TABLE IF EXISTS customer;"
cursor.query(dropTableIfExistsForCustomer).execute()
dropTableIfExistsForOrder = "DROP TABLE IF EXISTS order;"
cursor.query(dropTableIfExistsForOrder).execute()

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

createTableForCustomer = """
CREATE TABLE IF NOT EXISTS customer (
    customer_id INTEGER PRIMARY KEY,
    customer_name TEXT,
    contact_name TEXT,
    address TEXT,
    city TEXT,
    postal_code INTEGER,
    country TEXT
);
"""
cursor.query(createTableForCustomer).df()
createTableForOrder = """
CREATE TABLE IF NOT EXISTS order (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    employee_id INTEGER,
    order_date TEXT,
    shipper_id INTEGER
);
"""
cursor.query(createTableForOrder).df()

# Load data into PLAYERDATA table
loadData = """LOAD CSV 'out.csv' INTO PLAYERDATA;"""
cursor.query(loadData).execute()
loadDataForCustomer = """LOAD CSV 'Customers.csv' INTO customer;"""
cursor.query(loadDataForCustomer).execute()
loadDataForOrder = """LOAD CSV 'Orders.csv' INTO order;"""
cursor.query(loadDataForOrder).execute()

# Query PLAYERDATA table
cursor.query("""SELECT * FROM PLAYERDATA""").df()


# Function to chat with OpenAI and convert English to SQL
def ChatWithPandas(message, tableName, tableInfo):
    try:
        # Interact with the chat model
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"""You are a helpful assistant that converts English sentence to SQL in sqlite.
                First we give you the name of the table as a list, which is {tableName}
                Second the schema of {tableName} is {tableInfo}
                Last you need to convert the English sentence to SQL in sqlite.""" },
                {"role": "user", "content": message},
            ],
        )
        sql_query = response.choices[0].message['content']
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None
    return sql_query

tableInfo = dict()
#add the customer and the related information to the dictionary
tableInfo['customer'] = cursor.query(f"""SELECT * FROM customer;""").df().columns
#add the order and the related information to the dictionary
tableInfo['order'] = cursor.query(f"""SELECT * FROM order;""").df().columns
#add the playerdata and the related information to the dictionary
tableInfo['PLAYERDATA'] = cursor.query(f"""SELECT * FROM PLAYERDATA;""").df().columns



def plot_data_distribution(column_name, table_name):
    query = f"""SELECT {column_name} FROM {table_name}"""
    data = cursor.query(query).df()
    plt.figure(figsize=(10, 6))
    sns.histplot(data[column_name], kde=True)
    plt.title(f'{column_name} Distribution in {table_name}')
    plt.xlabel(column_name)
    plt.ylabel('Frequency')
    plt.show()


if __name__ == "__main__":
    memoryDict = dict()
    while True:
        print("\nMenu:")
        print("1. Run a SQL query")
        print("2. Show a data distribution plot")
        print("3. Use ChatWithPandas to convert English to SQL")
        print("4. Run a SQL query using caching")
        print("5. Exit")

        choice = input("Enter your choice (1/2/3/4/5): ")

        if choice == '1':
            # Direct SQL query execution
            sql_query = input("Enter a SQL query: ")
            try:
                result = cursor.query(sql_query).df()
                print("--------------------------------------------------")
                print("Result: ")
                print(result)
                print("--------------------------------------------------")
            except Exception as e:
                print(f"Error executing query: {e}")

        elif choice == '2':
            # Data visualization
            column_name = input("Enter the column name for visualization: ")
            table_name = input("Enter the table name: ")
            plot_data_distribution(column_name, table_name)

        elif choice == '3':
            # Using ChatWithPandas for query generation
            english_sentence = input("Enter your English sentence for SQL conversion: ")
            table_name = input("Enter the table name: ")
            #if table_name contains multiple tables we need to pass correct table name to the function
            tableName = list()
            finalTableInfo = list()
            for table in table_name.split():
                tableName.append(table)
                finalTableInfo.append(tableInfo[table])
            sql_query = ChatWithPandas(english_sentence, tableName, finalTableInfo)
            print("--------------------------------------------------")
            print("SQL query generated: ")
            print(sql_query)
            print("--------------------------------------------------")
            try:
                result = cursor.query(sql_query).df()
                print("--------------------------------------------------")
                print("Result: ")
                print(result)
                print("--------------------------------------------------")
            except Exception as e:
                print(f"Error executing query: {e}")
        elif choice == '4':
            print(memoryDict)
            start_time = time.time()
            sql_query = input("Enter a SQL query: ")
            try:
                print(sql_query in memoryDict)
                if sql_query in memoryDict:
                    print(memoryDict[sql_query])
                    print("--------------------------------------------------")
                else:
                    result = cursor.query(sql_query).df()
                    memoryDict[sql_query] = result
                    print("--------------------------------------------------")
                    print("Result: ")
                    print(result)
                    print("--------------------------------------------------")
                end_time = time.time()
                execution_time = end_time - start_time
                print(f"Execution time: {execution_time} seconds")
            except Exception as e:
                print(f"Error executing query: {e}")
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")