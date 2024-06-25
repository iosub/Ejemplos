from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.llms import Ollama
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI

from langchain_core.prompts import PromptTemplate

template= """
<|begin_of_text|><|start_header_id|>user<|end_header_id|>

Generate a SQL query to answer this question: `{user_question}`
{instructions}

DDL statements:
{create_table_statements}<|eot_id|><|start_header_id|>assistant<|end_header_id|>

The following SQL query best answers the question `{user_question}`:
```sql
"""

conn_str = "mssql+pyodbc://gg:ostia@minipc/iatest?driver=ODBC+Driver+17+for+SQL+Server"

tables=["T_FACTURA","CLIENTE"]#,"DIVISA"]


prompt=PromptTemplate(input_variables=['user_question', 'create_table_statements','instructions'], template=template, validate_template=False )
llm = ChatOpenAI(model="gpt-4o", temperature=0)

llmhh= 5#Ollama(model="mannix/defog-llama3-sqlcoder-8b:q8_0", temperature=0)
print(prompt)
db = SQLDatabase.from_uri(conn_str,include_tables=tables,lazy_table_reflection=True  )#,custom_table_info=table_info2)


agent = create_sql_agent(
     llm=llm,
     db=db,
     prompt=prompt,
     verbose=True,
     agent_type="openai-tools",
)
agent.invoke("total de facturacion del cliente 'GRUPO MZ' agrupado por años")
#print(quee)
