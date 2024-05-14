from langchain_community.llms import Ollama
from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_core.prompts import PromptTemplate
#https://python.langchain.com/v0.1/docs/use_cases/sql/quickstart/ !!!!!!!!!!!!!!!

template = '''Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
Use the following format:

Question: "Question here"
SQLQuery: "SQL Query to run"
SQLResult: "Result of the SQLQuery"
Answer: "Final answer here"

Only use the following tables:

{table_info}.

Question: {input}'''
prompt = PromptTemplate.from_template(template)



# Conectar a SQL Server
conn_str = "mssql+pyodbc://gg:ostia@lenovo12/MspLitePro_V3GG?driver=ODBC+Driver+17+for+SQL+Server"
db = SQLDatabase.from_uri(conn_str)

#conn_str = "mssql+pyodbc:///?odbc_connect=DRIVER={SQL Server};SERVER=(local);DATABASE=MspLitePro_V3GG;Trusted_Connection=yes;"
#db = SQLDatabase.from_uri(conn_str)
#db=SQLDatabase.from_uri()
#https://github.com/langchain-ai/langchain/discussions/17852
#conn_str = 'mssql+pyodbc://@SSC10205F/SkillDB?trusted_connection=yes&driver=SQL+Server'
#db =  SQLDatabase.from_uri(conn_str)

#https://github.com/langchain-ai/langchain/issues/9848
#db = SQLDatabase.from_uri(
#"mssql+pyodbc://gg:ostia@lenovo12\MSSQLSERVER/MspLitePro_V3GG?driver=SQL+Server",)

# Inicializar Ollama con un modelo específico
#ollama = Ollama(model="llama3")
ollama = Ollama(model="llama3", temperature=0)

# Crear una cadena que genera consultas SQL
#sql_query_chain = create_sql_query_chain(llm=ollama, db=db)


execute_query = QuerySQLDataBaseTool(db=db)
write_query = create_sql_query_chain(ollama, db)
chain = write_query | execute_query
response3=chain.invoke({"question": "How many employees are there"})
print(response3)



sql_query_chain = create_sql_query_chain(ollama, db)

response2 = sql_query_chain.invoke({"question": "How many employees are there"})
print(response2)

print(response2['output'])

# Función para generar y ejecutar consultas SQL basadas en preguntas en lenguaje natural
def generate_and_execute_sql(question, offset=0, batch_size=100):
    # Generar la consulta SQL con paginación
    #sql_query = sql_query_chain.invoke({question:question}) + f" OFFSET {offset} ROWS FETCH NEXT {batch_size} ROWS ONLY"
    
    sql_query = sql_query_chain.invoke({"question": "How many employees are there"}) + f" OFFSET {offset} ROWS FETCH NEXT {batch_size} ROWS ONLY"

    
   #https://api.python.langchain.com/en/latest/utilities/langchain_community.utilities.sql_database.SQLDatabase.html#langchain_community.utilities.sql_database.SQLDatabase.from_uri    # Ejecutar la consulta SQL
    result = db.run(sql_query)
    
    return result

# Ejemplo de uso con paginación
total_rows = 1000  # Suponiendo que sabemos el total de filas
batch_size = 100
results = []

for offset in range(0, total_rows, batch_size):
    question = "¿Cuántos productos hay en stock?"
    batch_result = generate_and_execute_sql(question, offset, batch_size)
    results.extend(batch_result)

# Procesar los resultados combinados
print(results)
