


from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_community.llms import Ollama
llm = Ollama(model="sqlcoder", temperature=0)
#llm = Ollama(model="llama3", temperature=0)

conn_str = "mssql+pyodbc://gg:ostia@lenovo12/iatest?driver=ODBC+Driver+17+for+SQL+Server"
db = SQLDatabase.from_uri(conn_str )#,custom_table_info=table_info2)



system = """You are a {dialect} expert. Given an input question, creat a syntactically correct {dialect} query to run.

Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in double quotes (") to denote them as delimited identifiers.
Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
Pay attention to use date('now') function to get the current date, if the question involves "today".

Only use the following tables:
{table_info}

Write an initial draft of the query. Then double check the {dialect} query for common mistakes, including:
- Using NOT IN with NULL values
- Using UNION when UNION ALL should have been used
- Using BETWEEN for exclusive ranges
- Data type mismatch in predicates
- Properly quoting identifiers
- Using the correct number of arguments for functions
- Casting to the correct data type
- Using the proper columns for joins
- Using the proper columns names
- Using the proper table names
- check the tables names exists 


Use format:

First draft: <<FIRST_DRAFT_QUERY>>
Final answer: <<FINAL_ANSWER_QUERY>>

Output the final SQL query only.
"""
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
##table_names = "\n".join(db.get_usable_table_names())
#table_info=db.get_table_info()
#prompt = ChatPromptTemplate.from_messages(
#    [("system", system), ("human", "{query}")]
#).partial(dialect=db.dialect,table_info=table_info)##

#prompt = ChatPromptTemplate.from_messages(
#    [("system", system), ("human", "{query}")]
#).partial(dialect=db.dialect)
prompt = ChatPromptTemplate.from_messages(
    [("system", system), ("human", "{question}")]
).partial(dialect=db.dialect,table_info=db.get_table_info())
chain = create_sql_query_chain(llm, db)
validation_chain = prompt | llm | StrOutputParser()
full_chain = {"question": chain} | validation_chain
query = full_chain.invoke(
    {
        #"question": "how many invoices are?"
        "question": "Lista de Facturas para el cliente con denomi 'GRUPO MZ'"
        #"question": "List of invoices for customer  'GRUPO MZ'"
         #"question": "total de facturacion del cliente con nombre 'GRUPO MZ'"
    }
)
print(query)
query=(query.split("```")[1]).replace('sql','')
print(db.run(query))




system = """You are a {dialect} expert. Given an input question, creat a syntactically correct {dialect} query to run.
Unless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the LIMIT clause as per {dialect}. You can order the results to return the most informative data in the database.
Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in double quotes (") to denote them as delimited identifiers.
Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
Pay attention to use date('now') function to get the current date, if the question involves "today".

Only use the following tables:
{table_info}

Write an initial draft of the query. Then double check the {dialect} query for common mistakes, including:
- Using NOT IN with NULL values
- Using UNION when UNION ALL should have been used
- Using BETWEEN for exclusive ranges
- Data type mismatch in predicates
- Properly quoting identifiers
- Using the correct number of arguments for functions
- Casting to the correct data type
- Using the proper columns for joins
- Using the proper columns names
- Using the proper table names
- check the tables names exists 


Use format:

First draft: <<FIRST_DRAFT_QUERY>>
Final answer: <<FINAL_ANSWER_QUERY>>


"""
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
##table_names = "\n".join(db.get_usable_table_names())
#table_info=db.get_table_info()
#prompt = ChatPromptTemplate.from_messages(
#    [("system", system), ("human", "{query}")]
#).partial(dialect=db.dialect,table_info=table_info)##

#prompt = ChatPromptTemplate.from_messages(
#    [("system", system), ("human", "{query}")]
#).partial(dialect=db.dialect)
prompt = ChatPromptTemplate.from_messages(
    [("system", system), ("human", "{input}")]
).partial(dialect=db.dialect)

chain = create_sql_query_chain(llm, db,prompt=prompt)
query = chain.invoke(
    {
        #"question": "how many invoices are?"
        #"question": "Lista de Facturas para el cliente con denomi 'GRUPO MZ'"
        "question": "List of invoices for customer  'GRUPO MZ'"
         #"question": "total de facturacion del cliente con nombre 'GRUPO MZ'"
    }
)
print(query)
query=(query.split("```")[1]).replace('sql','')
print(db.run(query))




#========================== BUENO
system=""" 
### Instructions:
Your task is to convert a question into a SQL query, given a {dialect} database schema.
Adhere to these rules:
- **Deliberately go through the question and database schema word by word** to appropriately answer the question
- **Use Table Aliases** to prevent ambiguity. For example, `SELECT table1.col1, table2.col1 FROM table1 JOIN table2 ON table1.id = table2.id`.
- When creating a ratio, always cast the numerator as float

### Input:
Generate a SQL query that answers the question `{question}`.
This query will run on a database whose schema is represented in this string:
CREATE TABLE [CLIENTE] (
    [Id_CLIENTE] INTEGER , 
    [Id_EMPRESA] INTEGER , 
    [CODCLI] NVARCHAR(10) , 
    [DENOMI] NVARCHAR(100)
    );
CREATE TABLE [T_FACTURA] (
    [Id_FACTURA] INTEGER, 
    [Id_EMPRESA] INTEGER, 
    [TIPOREG] VARCHAR(2) , 
    [FACTURA] INTEGER NOT NULL, 
    [FECHAF] DATE NOT NULL, 
    [Id_CLIENTE] INTEGER NULL
    );

-- T_FACTURA.Id_CLIENTE can be joined with Cliente.Id_CLIENTE
Output the final SQL query only.

### Response:
Based on your instructions, here is the SQL query I have generated to answer the question `{question}`:

```sql
"""



system = """Double check the user's {dialect} query for common mistakes, including:
  Only use the following table information:
  CREATE TABLE [CLIENTE] (
            [Id_CLIENTE] INTEGER NOT NULL IDENTITY(1,1), 
            [Id_EMPRESA] INTEGER NOT NULL, 
            [CODCLI] NVARCHAR(10) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
            [DENOMI] NVARCHAR(100) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL);
   CREATE TABLE [T_FACTURA] 
            ([Id_FACTURA] INTEGER NOT NULL IDENTITY(1,1), 
            [Id_EMPRESA] INTEGER NOT NULL, 
            [TIPOREG] VARCHAR(2) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
            [FACTURA] INTEGER NOT NULL, 
            [FECHAF] DATE NOT NULL, 
            [Id_CLIENTE] INTEGER NULL);

- Using NOT IN with NULL values
- Using UNION when UNION ALL should have been used
- Using BETWEEN for exclusive ranges
- Data type mismatch in predicates
- Properly quoting identifiers
- Using the correct number of arguments for functions
- Casting to the correct data type
- Using the proper columns for joins
- Using the proper table names
- check the tables names exists 
If there are any of the above mistakes, rewrite the query. If there are no mistakes, just reproduce the original query.

Output the final SQL query only."""



system=""" 
### Instructions:
Your task is to convert a question into a SQL query, given a Postgres  database schema.
Adhere to these rules:
- **Deliberately go through the question and database schema word by word** to appropriately answer the question
- **Use Table Aliases** to prevent ambiguity. For example, `SELECT table1.col1, table2.col1 FROM table1 JOIN table2 ON table1.id = table2.id`.
- When creating a ratio, always cast the numerator as float

### Input:
Generate a SQL query that answers the question `{question}`.
This query will run on a database whose schema is represented in this string:
 CREATE TABLE [CLIENTE] (
[Id_CLIENTE] INTEGER NOT NULL IDENTITY(1,1), 
[Id_EMPRESA] INTEGER NOT NULL, 
[CODCLI] NVARCHAR(10) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
[DENOMI] NVARCHAR(100) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL);
CREATE TABLE [T_FACTURA] 
([Id_FACTURA] INTEGER NOT NULL IDENTITY(1,1), 
[Id_EMPRESA] INTEGER NOT NULL, 
[TIPOREG] VARCHAR(2) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
[FACTURA] INTEGER NOT NULL, 
[FECHAF] DATE NOT NULL, 
[Id_CLIENTE] INTEGER NULL);

### Response:
Based on your instructions, here is the SQL query I have generated to answer the question `{question}`:
```sql
"""
