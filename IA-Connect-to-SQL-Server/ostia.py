#https://python.langchain.com/v0.1/docs/use_cases/sql/quickstart/
#https://api.python.langchain.com/en/latest/chains/langchain.chains.sql_database.query.create_sql_query_chain.html
from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.llms import Ollama
from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_core.prompts import PromptTemplate

answer_prompt = PromptTemplate.from_template(
    """Given the following user question, corresponding SQL query, and SQL result, answer the user question. Dont use any literal SQL

Question: {question}
SQL Query: {query}
SQL Result: {result}
Answer: """
)

# Conectar a SQL Server
conn_str = "mssql+pyodbc://gg:ostia@lenovo12/MspLitePro_V3GG?driver=ODBC+Driver+17+for+SQL+Server"
db = SQLDatabase.from_uri(conn_str)
ollama = Ollama(model="llama3", temperature=0)

# Crear una cadena que genera consultas SQL
#sql_query_chain = create_sql_query_chain(llm=ollama, db=db)


execute_query = QuerySQLDataBaseTool(db=db)
write_query = create_sql_query_chain(ollama, db)
#chain = write_query | execute_query

answer = answer_prompt | ollama | StrOutputParser()
print(answer)

chain = (
    RunnablePassthrough.assign(query=write_query).assign(
        result=itemgetter("query") | execute_query
    )
    | answer
)

response3=chain.invoke({"question": "How many employees are there"})
print(response3)
print(answer)