from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()
llm=ChatGroq(groq_api_key=os.getenv("Gorq_api_key"),temperature=1, model_name="llama-3.2-90b-vision-preview")



if __name__=="__main__":
    print(os.getenv("Gorq_api_key"))  
    response=llm.invoke("Write a paragraph about book.")
    print(response.content)

