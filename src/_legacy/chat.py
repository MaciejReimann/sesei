import os
from dotenv import load_dotenv, find_dotenv

from langchain.llms import OpenAI

_ = load_dotenv(find_dotenv())  # read local .env file
openai_api_key = os.environ["OPENAI_API_KEY"]
llm = OpenAI(openai_api_key=openai_api_key)


from langchain.chat_models import ChatOpenAI

chat = ChatOpenAI(openai_api_key=openai_api_key, temperature=0.1)

from langchain import PromptTemplate, LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.chains import SimpleSequentialChain
from langchain.chains import SequentialChain
from langchain.memory import SimpleMemory


# This is an LLMChain to write a synopsis given a title of a play.
template_1 = """You are a technical translator working in the IT industry. Given the text in Polish, it is your job to translate it to English.
Be consistent when translating domain-specific terms.

Wrapped in "###" you will find the copied text from the existing implementation. This should be translated as well - keeping it wrapped in "###".
Wrapped in <TABLE> you will find a copied content of Google Sheets - this should be translated as well - keeping it wrapped in <TABLE>.

When text is in english - don't translate it, only rephrase if necessary - it's not written by a native speaker.

Text: {text}

This is the translation for the above text:"""

prompt_template_1 = PromptTemplate(input_variables=["text"], template=template_1)
translation_chain = LLMChain(
    llm=chat, prompt=prompt_template_1, output_key="project_info"
)

# This is an LLMChain to write a review of a play given a synopsis.
template_2 = """You are an IT analyst hired to work on an initial phase of a project. 
You are an expert in Domain Driven Design. You need to get a deep, but high level understanding of the domain. 
When in doubt - don't  try to imagine the answer, but ask the client for clarification.

Wrapped in "###" you will find the copied text from the existing implementation. You should analyze it carefully. 
Wrapped in <TABLE> you will find a copied content of Google Sheets - this should be parsed and analyzed as well.

Project Info:
{project_info}

Follow up questions to the above process description, that will help to, find blind spots, and clarify doubts.
You can ask as many questions as you need at this stage. The client will answer them one by one.
Do not ask questions that are outside the scope of the task, namely: timeline, budget, team, implementations. 

Questions: <list questions here>
Summary: <provide a high-level summary of the events necessary to complete the business process>
"""
prompt_template_2 = PromptTemplate(
    input_variables=["project_info"], template=template_2
)
analysis_chain = LLMChain(llm=chat, prompt=prompt_template_2)

# This is the overall chain where we run these two chains in sequence.
overall_chain = SimpleSequentialChain(
    chains=[translation_chain, analysis_chain],
    verbose=True,
)

project_info = open("src/data/project_info.txt", "r").read()
result = overall_chain.run(project_info)
print(result)
