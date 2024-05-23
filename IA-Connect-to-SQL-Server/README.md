Mi Primer Ejemplo de IA
Para Instalar en windows los Requerimintos y el Enviroment Virtual
 python -m venv C:\IA\Iosu\Ejemplos\IA-Connect-to-SQL-Server 
 .\Scripts\Activate.ps1
pip install -r .\requirements.txt  
git repo clone iosub/IA-InvoiceEntityExtractor
 python -m venv C:\IA\Ios 
https://huggingface.co/blog/Andyrasika/agent-helper-langchain-hf
https://python.langchain.com/v0.1/docs/integrations/chat/huggingface/

pip install python-dotenv

import os
from dotenv import load_dotenv

load_dotenv()

GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")
STORAGE_BUCKET_NAME = os.getenv("STORAGE_BUCKET_NAME")
