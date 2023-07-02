from dotenv import load_dotenv

load_dotenv()

import os
from supabase import create_client, Client

# TODO: move to supabase edge functions

supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
)
from langchain.vectorstores import SupabaseVectorStore
from langchain.document_loaders import TextLoader

# TODO: make use of the metadata & filtering
loader = TextLoader("data/state_of_the_union.txt")
documents = loader.load()
print(documents)


# text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
# docs = text_splitter.split_documents(documents)

# embeddings = OpenAIEmbeddings()
# vector_store = SupabaseVectorStore.from_documents(
#     docs,
#     embeddings,
#     client=supabase,
#     table_name="documents",  # the default
#     query_name="match_documents",  # the default
# )

# print(vector_store)

# query = "How many people need insulin?"
# # matched_docs = vector_store.similarity_search(query)
# # max_marginal_relevance_search_by_vector
# matched_docs = vector_store.similarity_search_with_relevance_scores(query)

# print(matched_docs[0])
