Mi Primer Ejemplo de IA
Para Instalar en windows los Requerimintos y el Enviroment Virtual
 python -m venv C:\IA\Iosu\Ejemplos\IA-Connect-to-SQL-Server 
 .\Scripts\Activate.ps1
pip install -r .\requirements.txt  
git repo clone iosub/IA-InvoiceEntityExtractor
 python -m venv C:\IA\Ios 
https://huggingface.co/blog/Andyrasika/agent-helper-langchain-hf
https://python.langchain.com/v0.1/docs/integrations/chat/huggingface/

https://huggingface.co/docs/huggingface_hub/package_reference/hf_api

https://huggingface.co/docs/huggingface_hub/quick-start#authentication
pip install python-dotenv
https://klu.ai/blog/open-source-llm-models
https://numbersstation.ai/introducing-nsql-open-source-sql-copilot-foundation-models/

https://pub.towardsai.net/nsql-first-ever-fully-opensource-sql-foundation-model-f7b501d91ca4

https://pub.towardsai.net/nsql-first-ever-fully-opensource-sql-foundation-model-f7b501d91ca4

import os
from dotenv import load_dotenv

load_dotenv()

GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")
STORAGE_BUCKET_NAME = os.getenv("STORAGE_BUCKET_NAME")
