import os
from dotenv import load_dotenv

load_dotenv()
openkey=os.getenv("OPENKEY")
print(openkey)