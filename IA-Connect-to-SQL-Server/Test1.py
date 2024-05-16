from langchain_community.llms import Ollama
from langchain.chains import  create_sql_query_chain
from langchain_community.utilities import SQLDatabase

# Conectar a SQL Server
conn_str = "mssql+pyodbc://gg:ostia@lenovo12/MspLitePro_V3GG?driver=ODBC+Driver+17+for+SQL+Server"
db = SQLDatabase.from_uri(conn_str)

# Inicializar Ollama con un modelo específico y una temperatura baja
ollama = Ollama(model="llama3", temperature=0.2)

# Crear una cadena que genera consultas SQL
sql_query_chain = create_sql_query_chain(llm=ollama, db=db)

# Función para generar y ejecutar consultas SQL basadas en preguntas en lenguaje natural
def generate_and_execute_sql(question):
    # Generar la consulta SQL

    sql_query = sql_query_chain.invoke({"question": "How many employees are there"})
    
    #sql_query = sql_query_chain.invoke({question:question})
    
    # Ejecutar la consulta SQL
    result = db.run(sql_query)
    
    return result

# Ejemplo de uso
question = "¿Cuántos productos hay en stock?"
result = generate_and_execute_sql(question)
print(result)
