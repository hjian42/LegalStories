import json
import openai
import os
import pandas as pd
import sys
import glob
from tqdm import tqdm
import argparse
from pathlib import Path
from tenacity import retry, stop_after_attempt, wait_random_exponential
import multiprocessing
import replicate

openai.organization = ""
openai.api_key = ""


def run_gpt4_query(filled_prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful legal assistant."},
            {"role": "user", "content": filled_prompt},
        ],
        temperature=0,
    )
    return response

def run_llama2_query(filled_prompt):
    response = replicate.run(
    "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
        input={"prompt": filled_prompt,
               "system_prompt": "You are a helpful legal assistant.",
               "max_new_tokens": 1000,
               "temperature": 0.01,
               "top_p": 1.0,
               }
    )
    return response

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(15))
def generate_question(text, concept, story, prompt_file, model):
    """
    Generate a question based on the given text, concept, story, and prompt file using the specified model.

    Parameters:
    text (str): The doctrine wikipedia definition
    concept (str): The doctrine name around which the story should be developed.
    story (str): The generated story based on the concept and definition from the previous story generation step.
    prompt_file (str): The file path to the prompt file containing additional instructions or templates.
    model (str): The specific LLM model to use for generating the story

    Returns:
    response (str): The generated question as a string.
    """
    # Read prompt template
    prompt_template = open(prompt_file).read()

    prompt = prompt_template.replace("{TEXT}", text)
    prompt = prompt.replace("{CONCEPT}", concept)
    # replace the beginning of the simplification
    # story = story.replace("Concept Simplified:", "").strip("\n")
    prompt = prompt.replace("{STORY}", story)
    prompt = prompt.strip("\n").strip()
    prompt = prompt + "\n"
    # print(prompt)
    if model[:3].lower() == "gpt":
        response = run_gpt4_query(prompt)
        response = response["choices"][0]['message']['content'].strip("\n")
    elif model == "llama2":
        response = run_llama2_query(prompt)
        response = "".join([each for each in response])
    return response

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", type=str, default="./outputs/294-doctrines-gpt4/294_doctrine_stories.tsv")
    parser.add_argument("--output_folder", default="./outputs/294-doctrines-gpt4", type=str)
    parser.add_argument("--question_type", default="concept_question", type=str)
    parser.add_argument("--model", default="gpt-4-0613", type=str)
    args = parser.parse_args()

    df_text = pd.read_csv(args.input_file, encoding="utf-8", delimiter="\t")
    df_text = df_text.iloc[:]
    print(df_text.shape)
    # print(df_text)
    args.prompt_file_path = "./prompts/{}.txt".format(args.question_type)
    args.output_folder = os.path.join(args.output_folder, args.question_type)
    Path(args.output_folder).mkdir(parents=True, exist_ok=True)

    # normal call to debug
    # for concept_name, text, story in tqdm(zip(df_text.concept.to_list(), df_text.intro_text.to_list(), df_text.story.to_list())):
    #     concept_name = " ".join(concept_name.split("_"))
    #     response = generate_question(text, concept_name, story, args.prompt_file_path)
    #     print(response)
    #     break

    pool = multiprocessing.Pool()

    responses = []

    for concept_name, text, story in tqdm(zip(df_text.concept.to_list(), df_text.intro_text.to_list(), df_text.story.to_list())):
        response = pool.apply_async(generate_question, args=(text, concept_name, story, args.prompt_file_path, args.model))
        responses.append([concept_name, text, story, response])

    for concept_name, text, story, response in tqdm(responses):
        json_obj = {"id": concept_name, "text": text, "story": story}
        json_obj["annotation"] = response.get()
        json_obj = json.dumps(json_obj, indent=4)
        with open(os.path.join(args.output_folder, "{}.json".format(concept_name)), "w", encoding='UTF-8') as out:
            out.write(json_obj)

    pool.close()
    pool.join()

if __name__ == "__main__":
    main()
