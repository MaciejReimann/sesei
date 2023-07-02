import os
from dotenv import load_dotenv, find_dotenv
import openai
import json
import time

_ = load_dotenv(find_dotenv())  # read local .env file
openai_api_key = os.environ["OPENAI_API_KEY"]
openai.api_key = openai_api_key

# 1. Format the references
# This is an system message content to format one reference.
system_message = """You are an author of an academic article. Change the reference into Harvard Referencing System:

1.Author(s) first listed author's name inverted in the bibliography entry;
2.Order within the reference: [Year, Article title, Journal title in italic type, Volume, Issue, Page numbers <specific page number in a note; page range in a bibliography entry>, City];
3.In giving the city of publication, an internationally well-known city (such as London, The Hague, or New York) is given as the city alone.
If the city is not internationally well known, the country (or state and country if in the U.S.) is given;

Wrapped in ### is an example of a well-formatted reference:
###
Heilman, J. M. and West, A. G. 2015. "Wikipedia and Medicine: Quantifying Readership, Editors, and the Significance of Natural Language." Journal of Medical Internet Research, 17 (3), p.e62. doi:10.2196/jmir.4069.
###

Don't try to make up things, if they're missing, leave them as is, but alert about it. Respond with JSON format:
{
    "formatted_reference": #formatted reference#,
    "issues": #array of issues with the reference, if no issues, leave empty array#
}

If you can't format the reference, respond with JSON format:

{
    "formatted_reference": ERROR,
    "issues": ERROR
}
"""

references = open("src/data/references-long-4.txt", "r").readlines()


def format_references(references):
    formatted_with_issues = []
    for reference in references:
        max_retries = 5
        for i in range(max_retries):
            try:
                chat_completion = openai.ChatCompletion.create(
                    model="gpt-4",
                    temperature=0.0,
                    messages=[
                        {"role": "system", "content": system_message},
                        {
                            "role": "user",
                            "content": "The reference to format:" + reference,
                        },
                    ],
                )
                response = chat_completion.choices[0].message.content
                print(response)

                formatted_with_issues.append(response)
                break
            except openai.error.APIConnectionError:
                if i < max_retries - 1:  # i is zero indexed
                    time.sleep(1)  # wait for 1 second before trying again
                    print("retrying connecting to OpenAI...")
                    continue
                else:
                    raise
    return formatted_with_issues


formatted_with_issues = format_references(references)

file_name = "formatted_issues_long_4.json"
with open(file_name, "w") as file:
    json.dump(formatted_with_issues, file, ensure_ascii=False)


clean_data = [
    json.dumps(json.loads(item), indent=4, ensure_ascii=False)
    for item in formatted_with_issues
]
# Write the cleaned data to a file
with open("formatted_issues_long_4.txt", "w") as text_file:
    for item in clean_data:
        text_file.write(item + "\n\n")


# 2. Evaluate the responses
# This is an system message content to evaluate the whole list.
evaluation_system_message = """You are a proofreader of an academic article, your job is to evaluate a bibliography references list.
In particular, check if:
- all references are formatted according to one standard
- Author(s) first listed author's name inverted in the bibliography entry
- this order is kept: [Year, Article title, Journal title in italic type, Volume, Issue, Page numbers <specific page number in a note; page range in a bibliography entry>, City]
- In giving the city of publication, an internationally well-known city (such as London, The Hague, or New York) is given as the city alone. If the city is not internationally well known, the country (or state and country if in the U.S.) is given.

Wrapped in ### is an example of well-formatted reference:
###
Heilman, J. M. and West, A. G. 2015. "Wikipedia and Medicine: Quantifying Readership, Editors, and the Significance of Natural Language." Journal of Medical Internet Research, 17 (3), p.e62. doi:10.2196/jmir.4069.
###

Responsd with JSON format:
{
    issues_after_evaluation: #array of issues with the reference, if no issues, leave empty array#
}

"""

with open(file_name, "r") as json_file:
    data = json.load(json_file)


def evaluate(responses):
    evaluations = []

    for response in responses:
        res = json.loads(response)
        content = res.get("formatted_reference")
        print("evaluating: ", content)

        max_retries = 5
        for i in range(max_retries):
            try:
                chat_completion = openai.ChatCompletion.create(
                    model="gpt-4",
                    temperature=0.0,
                    messages=[
                        {"role": "system", "content": evaluation_system_message},
                        {
                            "role": "user",
                            "content": "The reference to evaluate is:" + content,
                        },
                    ],
                )

                evaluation = chat_completion.choices[0].message.content
                print(evaluation)

                evaluations.append(evaluation)
                break
            except openai.error.APIConnectionError:
                if i < max_retries - 1:  # i is zero indexed
                    time.sleep(1)  # wait for 1 second before trying again
                    print("retrying connecting to OpenAI...")
                    continue
                else:
                    raise

    return evaluations


evaluated = evaluate(data)

print(evaluated)


with open("evaluated_formatted_long_4.json", "w") as file_with_evaluations:
    json.dump(evaluated, file_with_evaluations, ensure_ascii=False)

###
###

with open("formatted_issues_long_4.json", "r") as json_file:
    formatted_data = json.load(json_file)

with open("evaluated_formatted_long_4.json", "r") as json_file:
    evaluated_data = json.load(json_file)

combined = [
    {**json.loads(a), **json.loads(b)} for a, b in zip(formatted_data, evaluated_data)
]

clean_data = [json.dumps(item, indent=4, ensure_ascii=False) for item in combined]

# Write the cleaned data to a file
with open("evaluated_formatted_long_4.txt", "w") as text_file:
    for item in clean_data:
        text_file.write(item + "\n\n")


print("FINISHED")
