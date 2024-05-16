#https://python.langchain.com/v0.1/docs/use_cases/sql/prompting/
#https://python.langchain.com/v0.1/docs/use_cases/sql/query_checking/
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_community.llms import Ollama
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


conn_str = "mssql+pyodbc://gg:ostia@lenovo12/MspLitePro_V3GG?driver=ODBC+Driver+17+for+SQL+Server" #Korta_Anterior
db = SQLDatabase.from_uri(conn_str)
llm = Ollama(model="llama3", temperature=0)

chain = create_sql_query_chain(llm, db)
chain.get_prompts()[0].pretty_print()
query = chain.invoke(
    {
        #"question": "cuantos cliente hay"
        #"question": "cual es la fecha de mi ultima factura?"
        "question": "listame las facturas del cliente con denomi=GRUPO MZ"
    }
)
print(query)
query=(query.split("```")[1]).replace('sql','')
print(db.run(query))
