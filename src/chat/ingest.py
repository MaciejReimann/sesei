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


text_splitter = text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    separators=["\n\n", "\n", ".", "?", "!", ", "],
    chunk_overlap=100,
)
docs = text_splitter.split_documents(documents)
print(f"    Text splitter created {len(docs)} documents")


# embeddings = OpenAIEmbeddings()
from langchain.embeddings import HuggingFaceEmbeddings, SentenceTransformerEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

from numpy import dot


# doc_result_1 = embeddings.embed_query(text_1)
# doc_result_2 = embeddings.embed_query(text_2)

# prod = dot(doc_result_1, doc_result_2)

# print(prod)


vector_store = SupabaseVectorStore.from_documents(
    docs,
    embeddings,
    client=supabase,
    table_name="documents",  # the default
    query_name="match_documents",  # the default
)

# print(vector_store)

query = "What is Inflation Reduction Act?"
# matched_docs = vector_store.similarity_search(query)
# max_marginal_relevance_search_by_vector
matched_docs = vector_store.similarity_search_with_relevance_scores(query)

print(f"    Found {len(matched_docs)} matching documents")

for i, doc in enumerate(matched_docs):
    print(i)
    print(doc[0].page_content)
    print(doc[1])

from langchain.chains import RetrievalQA
from langchain.llms import OpenAI


retriever = vector_store.as_retriever(
    search_type="similarity_score_threshold", search_kwargs={"score_threshold": 0.5}
)
retrieved_docs = retriever.get_relevant_documents(query)
print(f"    Found {len(retrieved_docs)} relevant documents above specified threshold")

qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=retriever)
response = qa.run(query)

print(f"    Answer: {response}")
