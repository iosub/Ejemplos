from langchain_community.agent_toolkits import create_sql_agent
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

prompt=PromptTemplate(input_variables=['user_question', 'create_table_statements','instructions'], template=template, validate_template=False )


agent = create_sql_agent(
     llm=llm,
     db=db,
     prompt=prompt,
     verbose=True,
     agent_type="openai-tools",
)