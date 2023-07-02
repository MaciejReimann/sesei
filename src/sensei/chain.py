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

# The plan should be ended with the definitions of each entity used in the plan (Block, Example, Exercise, Session, Goal)


# This is an LLMChain to plan the course of a training.
template_1 = """You are an expert in Computer Science, and your role is to train programmers in new technologies.
They have prior programming experience, so there is no need in explain the basics. They do, however need to master syntax, most popular libraries
and gotchas in a given area. Now, you'll need to plan training for {text}. 
First, you need to plan the training. The plan will be based on the following assumptions: 
1. The basic training unit is a Block;
2. Each Block will be trained during 3 Sessions, each of which should take no longer than 45 minutes;
3. After the third Session, a student will be an expert in the Block's material and will be able to proceed to the next Block;

The requirements for each Block are as follows:
1. Each Block is supposed to include a complete, practical sub-skill that can be mastered in its entirety;
2. Each Block should be composed of high quality Examples 
3. Each Example is paired with an Exercise that give instant feedback to the student;
4. Each Example - Exercise pair approach the Block's material from a different angle;
5. Students will have 200 to 300 exposures to each Example - Exercise pair;

Plan should be presented as a bullet-point list of Blocks, each Block should have a name, and the Goal of the training,
expressed in such a way that it is clear what the assumptions are. 

This is the training plan: """

prompt_template_1 = PromptTemplate(input_variables=["text"], template=template_1)
translation_chain = LLMChain(
    llm=chat, prompt=prompt_template_1, output_key="project_info"
)

# This is an LLMChain to write a list of Examples with Exercises
template_2 = """You are an expert in Computer Science and a master in teaching. 
You created a plan for the training: {project_info}. Execute the first step of the plan.

When creating examples - you should follow this structure:

1.Short description what the example is about;
2.Example
3.Exercise

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

# project_info = open("data/project_info.txt", "r").read()
result = overall_chain.run("Python: control flow")
print(result)
