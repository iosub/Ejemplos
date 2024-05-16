from operator import itemgetter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.llms import Ollama
from langchain_community.utilities import SQLDatabase
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain.chains import create_sql_query_chain


# Conectar a SQL Server
conn_str = "mssql+pyodbc://gg:ostia@lenovo12/MspLitePro_V3GG?driver=ODBC+Driver+17+for+SQL+Server"
db = SQLDatabase.from_uri(conn_str)
llm = Ollama(model="llama3", temperature=0)
chain = create_sql_query_chain(llm, db)
response = chain.invoke({"question": "How many employees are there"})
print(response)
db.run(response)

#https://python.langchain.com/v0.1/docs/use_cases/sql/
#NOOOOOOOOOOOOOOOO https://github.com/langchain-ai/langchain/blob/master/cookbook/sql_db_qa.mdx
#https://python.langchain.com/v0.1/docs/use_cases/sql/quickstart/
#https://github.com/langchain-ai/langchain/issues/10325
#https://python.langchain.com/v0.1/docs/use_cases/sql/query_checking/

answer_prompt = PromptTemplate.from_template(
    """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

Question: {question}
SQL Query: {query}
SQL Result: {result}
Answer: """
)
# Conectar a SQL Server
conn_str = "mssql+pyodbc://gg:ostia@lenovo12/MspLitePro_V3GG?driver=ODBC+Driver+17+for+SQL+Server"
db = SQLDatabase.from_uri(conn_str)
llm = Ollama(model="llama3", temperature=0)
sql_query_chain = create_sql_query_chain(llm, db)

sql_query_chain.run("How many employees are there?")
