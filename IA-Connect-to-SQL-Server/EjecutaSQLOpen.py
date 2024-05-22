#from langchain.chains.openai_tools import create_extraction_chain_pydantic
#from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain

from langchain_community.llms import Ollama

llm = ChatOpenAI(model="gpt-4o", temperature=0)
#llm = Ollama(model="llama3:8b-instruct-q8_0", temperature=0)
tables=["T_FACTURA","CLIENTE","DIVISA"]


conn_strBueno = 44#"mssql+pyodbc://gg:ostia@lenovo12/iatest?driver=ODBC+Driver+17+for+SQL+Server"

conn_str ="mssql+pyodbc://gg:ostia@lenovo12/MspLitePro_V3GG?driver=ODBC+Driver+17+for+SQL+Server"

dbold = 5#SQLDatabase.from_uri(conn_str )#,custom_table_info=table_info2)
db = SQLDatabase.from_uri(conn_str,include_tables=tables,lazy_table_reflection=True  )#,custom_table_info=table_info2)


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

Output the final SQL query only"""
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers import MarkdownListOutputParser


prompt = ChatPromptTemplate.from_messages(
    [("system", system), ("human", "{query}")]
).partial(dialect=db.dialect)
chain = create_sql_query_chain(llm, db)
validation_chain = prompt | llm | StrOutputParser()
full_chain = {"query": chain} | validation_chain

query = full_chain.invoke(
    {
      "question": "a que cliente le he facturado mas?"

      #"question": "total de facturacion en Euros por clientes agrupado por años y muestrame el nombre del cliente en la respuesta"

        #"question": "listame las facturas del cliente 'GRUPO MZ'"
        #  "question": "total de facturacion del cliente 'GRUPO MZ' agrupado por años"
    }
)
print(query)
query=(query.split("```")[1]).replace('sql','')
resultado=db.run(query) 
print(query)
print(resultado)

for item in resultado:
    print(f"Item: {item}, Length: {len(item)}")



resultado=(resultado.replace("[","")).replace("]","")

for item in resultado:
    print(f"Item: {item}, Length: {len(item)}")



import json
from decimal import Decimal
columnas = ["year", "company_name", "revenue"]

def convertir_a_json(resultado, columnas):
    # Manejar el caso de una sola fila
    if isinstance(resultado, tuple):
        resultado = [resultado]

    # Transformar a una lista de diccionarios
    resultado_diccionarios = [
        {columnas[0]: row[0], columnas[1]: row[1], columnas[2]: row[2]}
        for row in resultado
    ]

    # Convertir a JSON
    return json.dumps(resultado_diccionarios, indent=4)


# Nombres de las columnas (suponiendo que los conoces)
resultado_json = convertir_a_json(resultado, columnas)
print(resultado_json)

#def convertir_a_json(resultado, columnas):
    # Transformar a una lista de diccionarios
  #  resultado_diccionarios = [
  #      {columnas[0]: row[0], columnas[1]: row[1], columnas[2]: float(row[2])}
   #     for row in resultado
  #  ]

    # Convertir a JSON
  #  return json.dumps(resultado_diccionarios, indent=4)

# Uso de la función
#resultado_json = convertir_a_json(resultado, columnas)

#print(resultado_json)



#import json

# Convertir el resultado a JSON
#resultado_json = json.dumps(resultado)

# Imprimir o devolver el resultado JSON
#print(resultado_json)

#print(resultado)

#print(db.get_table_info())
import json
from decimal import Decimal

# Resultado de SQLDatabase.run

# Verificar la estructura del resultado


# Resultado de SQLDatabase.run
#resultado = [
#    (2004, 'COMERCIAL ASKAR, S.A.', Decimal('6587700.0000')),
#    (2004, 'GALARRETA, S.A.', Decimal('6240800.0000')),
#    (2004, 'PMG POLMETASA,S.A.U.', Decimal('5150200.0000')),
##    (2004, 'AGEN TRANSF DESAR EUROCIUDAD VASCA BAYONA SS', Decimal('4292000.0000'))
#]

# Transformar a una lista de di




