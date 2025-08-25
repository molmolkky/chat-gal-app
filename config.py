import os
from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI
from dotenv import load_dotenv
load_dotenv()

embedding = AzureOpenAIEmbeddings(
    azure_endpoint=os.environ["AZURE_OPENAI_EMBEDDING_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_EMBEDDING_API_KEY"],
    api_version=os.environ["AZURE_OPENAI_EMBEDDING_API_VERSION"],
    azure_deployment=os.environ["AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME"],
    model=os.environ["AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME"]
)

llm = AzureChatOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_CHAT_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_CHAT_API_KEY"],
    api_version=os.environ["AZURE_OPENAI_CHAT_API_VERSION"],
    azure_deployment=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
    model=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
    temperature=0
)