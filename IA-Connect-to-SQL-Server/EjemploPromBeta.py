#https://python.langchain.com/v0.1/docs/use_cases/sql/prompting/
#https://python.langchain.com/v0.1/docs/use_cases/sql/query_checking/
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_community.llms import Ollama
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
#&&

conn_str = "mssql+pyodbc://gg:ostia@lenovo12/iatest?driver=ODBC+Driver+17+for+SQL+Server"
#db = SQLDatabase.from_uri(conn_str,sample_rows_in_table_info=2)

#https://github.com/langchain-ai/langchain/issues/14440
#db=SQLDatabase(engine=dbengine,include_tables=["invoice","customer"],custom_table_info=table_info2)
#table_info2={'invoice':" the customer_id in invoice table is referenced to customers table's company_id",}
table_info2={'Facturas':" es T_FACTURA",}
#T_FACTURA
db = SQLDatabase.from_uri(conn_str)#,custom_table_info=table_info2)

output_parser=StrOutputParser()
 
 

# Obtener información de las tablas
table_info = db.get_table_info()

# Extraer los nombres de las tablas
table_names =db.get_table_names() #[info['name'] for info in table_info]

# Ahora table_names contiene los nombres de todas las tablas de la base de datos

#llm = Ollama(model="codegemma", temperature=0)
llm = Ollama(model="llama3", temperature=0)
#=========================================================================================================================================================

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

Output the final SQL query only.
"""
prompt = ChatPromptTemplate.from_messages(
    [("system", system), ("human", "{input}")]
).partial(dialect=db.dialect)


def parse_final_answer(output: str) -> str:
    pp=(output.split("Final answer:")[1]).replace('```','')
    return (pp)

#def parse_final_answer(output: str) -> str:
#    pp=output.split("Final answer: ")[0]
#    return (pp)


#chainmapeo = create_sql_query_chain.bind(table_name="Facturas=T_Factura") #| some_other_operation | ...)
#chain = create_sql_query_chain(llm, db, prompt=prompt) | parse_final_answer
#prompt.pretty_print()
#chain =chainmapeo|(create_sql_query_chain(llm, db)) #| parse_final_answer
#chain =create_sql_query_chain(llm, db)
#chaint=prompt | llm| output_parser
#chaint=chain | prompt| output_parser
chain = create_sql_query_chain(llm, db, prompt=prompt)# | parse_final_answer
query = chain.invoke(
    {
       #"input": "listame las facturas del cliente con denomi='GRUPO MZ'"
       # "question": "listame las  articu"

       "question": "listame las facturas del cliente con denomi='GRUPO MZ'"
       # "question": "listame las facturas del cliente con DENOMI 'GRUPO MZ' donde la tabla de facturas se llama T_FACTURA"
       # , "table_info":table_names
       
    }
)
query
query=(query.split("Final answer:")[1]).replace('```','')

#query=(query.split("```")[1]).replace('sql','')
print(query)
print("========================================================================================")

print(db.run(query))

#write_query = create_sql_query_chain(llm, db)
#print(write_query)
#execute_query = QuerySQLDataBaseTool(db=db)
#chain = write_query | execute_query
#response3=chain.invoke({"question": "How many employees are there"})
#print(response3)
#db.run("SELECT * FROM Artist LIMIT 10;")


#db = SQLDatabase.from_uri("sqlite:///Chinook.db", sample_rows_in_table_info=3)
#print(db.dialect)
#print(db.get_usable_table_names())
#Los Posibles pront

#PRUEBA QUE FUNCIONA
#chain = create_sql_query_chain(llm, db)
#print("PRIMERA SALIDA")
#print("================================")
#chain.get_prompts()[0].pretty_print()
#print("SEGUNDA")
#print("===============================")

#print( chain.get_prompts()[0])
#response3=chain.invoke({"question": "How many employees are there"})
#print(response3)
#responce=chain.invoke({"question": "How many employees are there"})
#print(responce)
# EN ESTE ULTIMO DA EL RESULTADO!!

#ESTO NO EJECTO responce2=db.run(responce)
#ESTO NO EJECTO print(responce2)
#FIN




#====================
#===============================
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
chain = create_sql_query_chain(llm, db)

system = """Double check the user's {dialect} query for common mistakes, including:
- Using NOT IN with NULL values
- Using UNION when UNION ALL should have been used
- Using BETWEEN for exclusive ranges
- Data type mismatch in predicates
- Properly quoting identifiers
- Using the correct number of arguments for functions
- Casting to the correct data type
- Using the proper columns for joins

If there are any of the above mistakes, rewrite the query. If there are no mistakes, just reproduce the original query.

Output the final SQL query only."""
prompt = ChatPromptTemplate.from_messages(
    [("system", system), ("human", "{query}")]
).partial(dialect=db.dialect)
validation_chain = prompt | llm | StrOutputParser()

full_chain = {"query": chain} | validation_chain
query = full_chain.invoke(
    {
        "question": "listame las facturas del cliente 'GRUPO MZ'"
    }
)
query
query=(query.split("```")[1]).replace('sql','')
print(db.run(query))

