import os
from dotenv import load_dotenv
load_dotenv()
MONGO_URL = os.getenv("MONGO_URL")
GLOBO_URL_INICIO = os.getenv("GLOBO_URL_INICIO")
GLOBO_URL_FIM = os.getenv("GLOBO_URL_FIM")
GLOBO_ID = os.getenv("GLOBO_ID")
NUM_PAG = os.getenv("NUM_PAG")
SGBD = os.getenv("SGBD")
if len(MONGO_URL) == 0 or MONGO_URL == None:
    raise TypeError("Verifique seu arquivo .env, MONGO_URL ausente")
if len(GLOBO_ID) == 0 or GLOBO_ID == None:
    raise TypeError("Verifique seu arquivo .env, GLOBO_ID ausente")
if len(GLOBO_URL_INICIO) == 0 or GLOBO_URL_INICIO == None:
    raise TypeError("Verifique seu arquivo .env, GLOBO_URL_INICIO ausente")
if len(GLOBO_URL_FIM) == 0 or GLOBO_URL_FIM == None:
    raise TypeError("Verifique seu arquivo .env, GLOBO_URL_FIM ausente")
if len(NUM_PAG) == 0 or NUM_PAG == None:
    raise TypeError("Verifique seu arquivo .env, NUM_PAG ausente")
if len(SGBD) == 0 or SGBD == None:
    raise TypeError("Verifique seu arquivo .env, SGBD ausente")
