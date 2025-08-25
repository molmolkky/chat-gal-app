import os
from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI
from dotenv import load_dotenv
load_dotenv()

# 修正：環境変数から値を取得するか、直接APIキーを指定
embedding = AzureOpenAIEmbeddings(
    azure_endpoint=os.environ["AZURE_OPENAI_CHAT_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_EMBEDDING_API_KEY"],  # 修正：実際のAPIキーを使用
    api_version=os.environ["AZURE_OPENAI_EMBEDDING_API_VERSION"],
    azure_deployment="text-embedding-3-large",  # デプロイメント名を確認
    model="text-embedding-3-large"
)

llm = AzureChatOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_CHAT_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_CHAT_API_KEY"],
    api_version=os.environ["AZURE_OPENAI_CHAT_API_VERSION"],
    azure_deployment="gpt-4.1",  # デプロイメント名を確認
    model="gpt-4.1",
    temperature=0
)