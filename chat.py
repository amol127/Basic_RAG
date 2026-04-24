from dotenv import load_dotenv
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from  langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI
import os
load_dotenv()
api = os.getenv("OPENAI_API_KEY")


# With OpenAI 
# openai_client = OpenAI()

# with other AI Model 
openai_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api,
    default_headers={
        "HTTP-Referer": "http://localhost",
        "X-Title": "Basic RAG"
    }

)

# Vector Ebedding  
embedding_model =  OpenAIEmbeddings(
    model="text-embedding-3-large",
    base_url="https://openrouter.ai/api/v1",
    api_key=api
)

vector_db = QdrantVectorStore.from_existing_collection(
    embedding=embedding_model,
    url = "http://localhost:6333",
    collection_name = "learning_rag"
)



# take user input 

user_query = input("Ask something:")

search_results = vector_db.similarity_search(query = user_query)

context = "\n\n\n".join([f"Page Content : {result.page_content}\nPage Number : {result.metadata['page_label']}\nFile Location: {result.metadata['source']}" for result in search_results])
SYSTEM_PROMPT = f"""
you are a helpfull AI Assistance who answer user query based on the available context retrieved from a PDF file along with page_contents and page number.

you should only ans the user based on the following context and navigation the user to open the right page number to know more.

Context:{context}
"""

response = openai_client.chat.completions.create(
 model="openai/gpt-4o-mini",
messages=[
    {"role":"system", "content":SYSTEM_PROMPT},
    {"role":"user", "content":user_query},
]
)


print(f"AI > ",{response.choices[0].message.content})



