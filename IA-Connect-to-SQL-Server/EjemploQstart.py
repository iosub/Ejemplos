from langchain.chains.openai_tools import create_extraction_chain_pydantic
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
llm = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0)


class Table(BaseModel):
    """Table in SQL database."""

    name: str = Field(description="Name of table in SQL database.")

conn_str = "mssql+pyodbc://gg:ostia@lenovo12/iatest?driver=ODBC+Driver+17+for+SQL+Server"
db = SQLDatabase.from_uri(conn_str )#,custom_table_info=table_info2)
table_names = "\n".join(db.get_usable_table_names())


system = f"""Return the names of ALL the SQL tables that MIGHT be relevant to the user question. \
The tables are:

{table_names}

Remember to include ALL POTENTIALLY RELEVANT tables, even if you're not sure that they're needed."""
table_chain = create_extraction_chain_pydantic(Table, llm, system_message=system)
#t=table_chain.invoke({"input": "listame las facturas del cliente con DENOMI 'GRUPO MZ' donde la tabla de facturas se llama T_FACTURA"})
table_chain.invoke({"input": "listame las facturas "})
#print (t)
#print (t2)
system = """Return the names of the SQL tables that are relevant to the user question. \
The tables are:

CLIENTE
T_FACTURA
"""
category_chain = create_extraction_chain_pydantic(Table, llm, system_message=system)
a1=category_chain.invoke({"input": "listame las facturas"})
print(a1)

from typing import List


def get_tables(categories: List[Table]) -> List[str]:
    tables = []
    for category in categories:
        if category.name == "FACTURAHH":
            tables.extend(
                [
                    "Album",
                    "Artist",
                    "Genre",
                    "MediaType",
                    "Playlist",
                    "PlaylistTrack",
                    "Track",
                ]
            )
        elif category.name == "Businessjjj":
            tables.extend(["Customer", "Employee", "Invoice", "InvoiceLine"])
    return tables


table_chain = category_chain | get_tables  # noqa
table_chain.invoke({"input": "listame las facturas"})
from operator import itemgetter

from langchain.chains import create_sql_query_chain
from langchain_core.runnables import RunnablePassthrough

query_chain = create_sql_query_chain(llm, db)
# Convert "question" key to the "input" key expected by current table_chain.
table_chain = {"input": itemgetter("question")} | table_chain
# Set table_names_to_use using table_chain.
full_chain = RunnablePassthrough.assign(table_names_to_use=table_chain) | query_chain

query = full_chain.invoke(
    {"question": "listame las facturas "}
)
print(query)


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
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
prompt = ChatPromptTemplate.from_messages(
    [("system", system), ("human", "{query}")]
).partial(dialect=db.dialect)
chain = create_sql_query_chain(llm, db)
validation_chain = prompt | llm | StrOutputParser()
full_chain = {"query": chain} | validation_chain
query = full_chain.invoke(
    {
        "question": "total de facturacion del cliente 'GRUPO MZ'"
        #"question": "listame las facturas del cliente 'GRUPO MZ'"
    }
)
query
query=(query.split("```")[1]).replace('sql','')
print(db.run(query))

#system = f"""Return the names of ALL the SQL tables that MIGHT be relevant to the user question. \
#The tables are:

#{table_names}

#Remember to include ALL POTENTIALLY RELEVANT tables, even if you're not sure that they're needed."""
#table_chain = create_extraction_chain_pydantic(Table, llm, system_message=system)
#t=table_chain.invoke({"input": "listame las facturas del cliente con DENOMI 'GRUPO MZ' donde la tabla de facturas se llama T_FACTURA"})
#table_chain.invoke({"input": "listame las facturas del cliente con DENOMI 'GRUPO MZ'"})
#print (t)
#print (t2)
#system = """Return the names of the SQL tables that are relevant to the user question. \
#The tables are:

#CLIENTE
#T_EQUIPO
#T_FACTURA
#"""
#category_chain = create_extraction_chain_pydantic(Table, llm, system_message=system)
#a1=category_chain.invoke({"input": "listame las facturas"})
#print(a1)
