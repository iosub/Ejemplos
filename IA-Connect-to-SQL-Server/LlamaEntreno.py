from langchain_core.prompts import PromptTemplate
from langchain_community.llms import LlamaCpp


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

llm = LlamaCpp(
    model_path="model.gguf",
    temperature=0,
    n_ctx=2048,
    top_p=1,
    verbose=True,  
)


user_question= """
Question: 
"""

instructions=""

create_table_statements=""

print(llm.invoke({"user_question":user_question,"create_table_statements":create_table_statements,"instructions":instructions}))
