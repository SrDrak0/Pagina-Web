import os
import google.generativeai as genai
from dotenv import load_dotenv

# Carga la clave de API desde tu archivo .env
load_dotenv()

try:
    # Configura la API key
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    
    print("✅ Clave de API encontrada. Buscando modelos disponibles...\n")
    
    # Busca y lista los modelos
    print("--- Modelos que puedes usar ---")
    for model in genai.list_models():
        # Verificamos que el modelo soporte la función de generar contenido (chatear)
        if 'generateContent' in model.supported_generation_methods:
            print(model.name)
    print("---------------------------------")
    print("\nCopia uno de estos nombres de modelo y pégalo en tu archivo main.py.")

except Exception as e:
    print(f"❌ Ocurrió un error: {e}")