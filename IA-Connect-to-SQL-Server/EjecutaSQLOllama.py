


from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_community.llms import Ollama
llm = Ollama(model="llama3", temperature=0)

conn_str = "mssql+pyodbc://gg:ostia@lenovo12/iatest?driver=ODBC+Driver+17+for+SQL+Server"
db = SQLDatabase.from_uri(conn_str )#,custom_table_info=table_info2)

system = """Double check the user's {dialect} query for common mistakes, including:
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
    [("system", system), ("human", "{query}")]
).partial(dialect=db.dialect)
chain = create_sql_query_chain(llm, db)
validation_chain = prompt | llm | StrOutputParser()
full_chain = {"query": chain} | validation_chain
query = full_chain.invoke(
    {
        "question": "listame las facturas del cliente 'GRUPO MZ'"
          #"question": "total de facturacion del cliente 'GRUPO MZ'"
    }
)
print(query)
query=(query.split("```")[1]).replace('sql','')
print(db.run(query))
