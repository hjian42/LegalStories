# LegalStories
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![arXiv](https://img.shields.io/badge/arXiv-2201.07281-b31b1b.svg)](https://arxiv.org/abs/2402.17019)

Official Code for our ACL 2024 Paper "Leveraging Large Language Models for Learning Complex Legal Concepts through Storytelling"

## Crawl Definitions from Wikipedia

1. Copy-paste the doctrine list from the [wikipedia page](https://en.wikipedia.org/wiki/Category:Legal_doctrines_and_principles). Saved as `cralwer/complex-law-doctrine-list.csv`.
2. Crawl and preprocess these doctrines with their definitions from Wikipedia.
    - Downloaded 294 valid doctrine pages from wikipedia, saved as `data/294-doctrines/legal_doctrines_294.csv`.
    - Sampled 101 doctrines out of 294 whose definition length is between 100 and 200 words, saved as `data/101-doctrines/legal_doctrines_101.csv`.
    - Sampled 20 doctrines out of 101 for detailed evaluation, saved as `data/20-doctrines/legal_doctrines_20.csv`.

## Generate Stories

1. Fill your OpenAI key into the `generate_story.py` and run the following commands to generate stories for GPT-4, GPT-3.5, and LLaMA-2:

```
python generate_story.py --model llama2
python generate_story.py --model gpt-3.5-turbo-0613
python generate_story.py --model gpt-4-0613
```
2. run `organize_data.ipynb` to organize the concepts, definitions, and generated stories altogether in tsv files.

## Generate Questions

Fill your OpenAI key into the `generate_question.py` and run the following commands to generate questions for GPT-4, GPT-3.5, and LLaMA-2:
- check out `organize_data.ipynb` to see how we prepare the datasets under the `data` folder

```
python generate_question.py --input_file ./outputs/294-doctrines-llama2/294_doctrine_stories.tsv --output_folder ./outputs/294-doctrines-llama2 --question_type concept_question --model llama2
python generate_question.py --input_file ./outputs/294-doctrines-llama2/294_doctrine_stories.tsv --output_folder ./outputs/294-doctrines-llama2 --question_type ending_question --model llama2
python generate_question.py --input_file ./outputs/294-doctrines-llama2/294_doctrine_stories.tsv --output_folder ./outputs/294-doctrines-llama2 --question_type limitation_question --model llama2

python generate_question.py --input_file ./outputs/294-doctrines-gpt3.5/294_doctrine_stories.tsv --output_folder ./outputs/294-doctrines-gpt3.5 --question_type concept_question --model gpt-3.5-turbo-0613
python generate_question.py --input_file ./outputs/294-doctrines-gpt3.5/294_doctrine_stories.tsv --output_folder ./outputs/294-doctrines-gpt3.5 --question_type ending_question --model gpt-3.5-turbo-0613
python generate_question.py --input_file ./outputs/294-doctrines-gpt3.5/294_doctrine_stories.tsv --output_folder ./outputs/294-doctrines-gpt3.5 --question_type limitation_question --model gpt-3.5-turbo-0613

python generate_question.py --input_file ./outputs/294-doctrines-gpt4/294_doctrine_stories.tsv --output_folder ./outputs/294-doctrines-gpt4 --question_type concept_question --model gpt-4-0613
python generate_question.py --input_file ./outputs/294-doctrines-gpt4/294_doctrine_stories.tsv --output_folder ./outputs/294-doctrines-gpt4 --question_type ending_question --model gpt-4-0613
python generate_question.py --input_file ./outputs/294-doctrines-gpt4/294_doctrine_stories.tsv --output_folder ./outputs/294-doctrines-gpt4 --question_type limitation_question --model gpt-4-0613
```

## Evaluation & Analysis

1. Automatic evaluation with complexity metrics: `analysis/1_complexity_measure.ipynb`
2. Human evaluation: `analysis/2_analyze_human_ratings_and_errors.ipynb`
3. Expert annotations on 20 legal doctrines: `analysis/3_expert_annotation.ipynb`
- the final stories and their corresponding questions: `analysis/expert_annotations/Final_regenerated_questions_20.tsv`
- the final expert-annotated answers for the questions: `analysis/expert_annotations/Final_answer_annotations.tsv`
4. Immediate and follow-up RCT result analyses: `analysis/4_analyze_rct_results.ipynb`
5. Statistical analysis on the RCT results: `analysis/5_statistical_analysis.ipynb`

## References

If you use this repository in your research, please kindly cite [our paper](https://aclanthology.org/2024.acl-long.388/): 

```bibtex
@inproceedings{jiang-etal-2024-leveraging,
    title = "Leveraging Large Language Models for Learning Complex Legal Concepts through Storytelling",
    author = "Jiang, Hang  and
      Zhang, Xiajie  and
      Mahari, Robert  and
      Kessler, Daniel  and
      Ma, Eric  and
      August, Tal  and
      Li, Irene  and
      Pentland, Alex  and
      Kim, Yoon  and
      Roy, Deb  and
      Kabbara, Jad",
    editor = "Ku, Lun-Wei  and
      Martins, Andre  and
      Srikumar, Vivek",
    booktitle = "Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)",
    month = aug,
    year = "2024",
    address = "Bangkok, Thailand",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2024.acl-long.388",
    pages = "7194--7219",
    abstract = "Making legal knowledge accessible to non-experts is crucial for enhancing general legal literacy and encouraging civic participation in democracy. However, legal documents are often challenging to understand for people without legal backgrounds. In this paper, we present a novel application of large language models (LLMs) in legal education to help non-experts learn intricate legal concepts through storytelling, an effective pedagogical tool in conveying complex and abstract concepts. We also introduce a new dataset LegalStories, which consists of 294 complex legal doctrines, each accompanied by a story and a set of multiple-choice questions generated by LLMs. To construct the dataset, we experiment with various LLMs to generate legal stories explaining these concepts. Furthermore, we use an expert-in-the-loop approach to iteratively design multiple-choice questions. Then, we evaluate the effectiveness of storytelling with LLMs through randomized controlled trials (RCTs) with legal novices on 10 samples from the dataset. We find that LLM-generated stories enhance comprehension of legal concepts and interest in law among non-native speakers compared to only definitions. Moreover, stories consistently help participants relate legal concepts to their lives. Finally, we find that learning with stories shows a higher retention rate for non-native speakers in the follow-up assessment. Our work has strong implications for using LLMs in promoting teaching and learning in the legal field and beyond.",
}
```

## Acknowledgement
This work is done in collaboration with researchers from MIT, Harvard Law School, University of Virginia School of Law, Allen Institute for AI (AI2), and University of Tokyo. We want to thank [MIT Center for Constructive Communication](https://www.ccc.mit.edu/) for funding the project. 
