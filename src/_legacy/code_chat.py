from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import DeepLake
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())
openai_api_key = os.environ["OPENAI_API_KEY"]
activeloop_token = os.environ["ACTIVELOOP_TOKEN"]

root_dir = "../../.."

# docs = []
# for dirpath, dirnames, filenames in os.walk(root_dir):
#     for filename in filenames:
#         if filename.endswith(".py") and "./.venv" not in dirpath:
#             try:
#                 loader = TextLoader(os.path.join(dirpath, filename), encoding="utf-8")
#                 docs.extend(loader.load_and_split())
#             except Exception as e:
#                 print(e)
#                 pass

loader = TextLoader("src/data/odyssey.txt", encoding="utf-8")
docs = loader.load()

print(f"{len(docs)} documents loaded.")

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(docs)
print(f"{len(texts)} texts generated.")

embeddings = OpenAIEmbeddings(
    openai_api_key=openai_api_key, model="text-embedding-ada-002"
)  # it's the default model

dataset_path = "hub://maciejreimann/literate"

# db = DeepLake.from_documents(
#     texts, dataset_path=dataset_path, embedding=embeddings, overwrite=True
# )

# db = DeepLake(dataset_path=dataset_path, embedding_function=embeddings, overwrite=True)
# db.add_documents(texts)


db = DeepLake(
    dataset_path=dataset_path,
    read_only=True,
    embedding_function=embeddings,
)

# qa = RetrievalQA.from_chain_type(
#     llm=OpenAIChat(model="gpt-3.5-turbo"),
#     chain_type="stuff",
#     retriever=db.as_retriever(),
# )


retriever = db.as_retriever()
# retriever.search_kwargs["distance_metric"] = "cos"
# retriever.search_kwargs["k"] = 20
# retriever.search_kwargs["maximal_marginal_relevance"] = True
# retriever.search_kwargs["k"] = 20

model = ChatOpenAI(openai_api_key=openai_api_key, model="gpt-4")  # 'gpt-3.5-turbo',
qa = RetrievalQA.from_chain_type(model, chain_type="stuff", retriever=retriever)

# query = "Who was the only one to welcome the main character when he got back home?"
query = "Who was the main character's wife? Think in steps. First find the name of the main character. Then find the name of his wife."
result = qa.run(query)

print(result)

# questions = [
#     "What is the class hierarchy?",
#     # "What classes are derived from the Chain class?",
#     # "What classes and functions in the ./langchain/utilities/ forlder are not covered by unit tests?",
#     # "What one improvement do you propose in code in relation to the class herarchy for the Chain class?",
# ]
# chat_history = []

# for question in questions:
#     result = qa({"question": question, "chat_history": chat_history})
#     chat_history.append((question, result["answer"]))
#     print(f"-> **Question**: {question} \n")
#     print(f"**Answer**: {result['answer']} \n")
