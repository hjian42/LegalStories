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

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def generate_story(text, concept, prompt_file, model):
    """
    Generate a story based on the given text, concept, and prompt file using the specified model.

    Parameters:
    text (str): The doctrine wikipedia definition
    concept (str): The doctrine name around which the story should be developed.
    prompt_file (str): The file path to the prompt file containing additional instructions or templates.
    model (str): The specific LLM model to use for generating the story

    Returns:
    response (str): The generated story as a string.
    """
    # Read prompt template
    prompt_template = open(prompt_file).read()

    prompt = prompt_template.replace("{TEXT}", text)
    prompt = prompt.replace("{CONCEPT}", concept)
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
    parser.add_argument("--input_file", type=str, default="./data/294-doctrines/legal_doctrines_294.tsv")
    parser.add_argument("--prompt_file_path", default="./prompts/story.txt", type=str)
    parser.add_argument("--output_folder", type=str, default="./outputs/295-doctrines/")
    parser.add_argument("--model", default="gpt-3.5-turbo-0613", type=str)
    args = parser.parse_args()

    df_text = pd.read_csv(args.input_file, encoding="utf-8", delimiter="\t")
    df_text = df_text.iloc[:]
    print(df_text.shape)
    print(df_text)
    output_folder = args.output_folder

    Path(output_folder).mkdir(parents=True, exist_ok=True)
    Path(os.path.join(output_folder, args.model)).mkdir(parents=True, exist_ok=True)
    Path(os.path.join(output_folder, args.model, "story")).mkdir(parents=True, exist_ok=True)

    # normal call to debug
    # for concept_name, text in tqdm(zip(df_text.concept.to_list(), df_text.intro_text.to_list())):
    #     concept_name = " ".join(concept_name.split("_"))
    #     response = generate_story(text, concept_name, args.prompt_file_path, args.model)
    #     full_text = "".join([each for each in response])
    #     print(full_text)
    #     break

    pool = multiprocessing.Pool()

    responses = []

    for concept_name, text in tqdm(zip(df_text.concept.to_list(), df_text.intro_text.to_list())):
        concept_name_string = " ".join(concept_name.split("_"))
        response = pool.apply_async(generate_story, args=(text, concept_name, args.prompt_file_path, args.model))
        responses.append([concept_name, text, concept_name_string, response])

    for concept_name, text, concept_name_string, response in tqdm(responses):
        json_obj = {"id": concept_name, "text": text}
        json_obj["annotation"] = response.get()
        json_obj = json.dumps(json_obj, indent=4)
        with open(os.path.join(output_folder, args.model, "story", "{}.json".format(concept_name)), "w", encoding='UTF-8') as out:
            out.write(json_obj)

    pool.close()
    pool.join()

if __name__ == "__main__":
    main()
