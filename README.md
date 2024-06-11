# LegalStories
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![arXiv](https://img.shields.io/badge/arXiv-2201.07281-b31b1b.svg)](https://arxiv.org/abs/2402.17019)

Official Code for "Leveraging Large Language Models for Learning Complex Legal Concepts through Storytelling"

## Crawl definitions from Wikipedia

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

## References

If you use this repository in your research, please kindly cite [our paper](https://arxiv.org/abs/2402.17019): 

```bibtex
@article{jiang2024leveraging,
  title={Leveraging Large Language Models for Learning Complex Legal Concepts through Storytelling},
  author={Jiang, Hang and Zhang, Xiajie and Mahari, Robert and Kessler, Daniel and Ma, Eric and August, Tal and Li, Irene and Pentland, Alex'Sandy' and Kim, Yoon and Kabbara, Jad and others},
  journal={arXiv preprint arXiv:2402.17019},
  year={2024}
}
```

## Acknowledgement
This work is done in collaboration with researchers from MIT, Harvard Law School, University of Virginia School of Law, Allen Institute for AI (AI2), and University of Tokyo. We want to thank [MIT Center for Constructive Communication](https://www.ccc.mit.edu/) for funding the project. 
