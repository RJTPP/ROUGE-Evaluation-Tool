import os
from typing import List

from json_helper import *
from rouge_score import *

def create_data_directory():
    if not os.path.exists("data"):
        os.makedirs("data")


def check_dataset_file():
    if not os.path.exists(os.path.join("data", "dataset.json")):
        raise Exception("Dataset file (data/dataset.json) not found")

def main():
    # Read dataset
    print("Reading dataset...")
    datasets = read_json(os.path.join("data", "dataset.json"))

    scores = []

    print("Calculating ROUGE scores...")
    for dataset in datasets:
        reference = dataset["reference"]
        candidates_list = dataset["candidate"]
        try:

            for candidate in candidates_list:
                rouge1_score = rouge1(candidate, reference)
                rouge2_score = rouge2(candidate, reference)
                rouge_l_score = rouge_l(candidate, reference)

                scores.append({
                    "candidate": candidate,
                    "reference": reference,
                    "ROUGE-1": {
                        "precision": rouge1_score[0],
                        "recall": rouge1_score[1],
                        "f-measure": rouge1_score[2]
                    },
                    "ROUGE-2": {
                        "precision": rouge2_score[0],
                        "recall": rouge2_score[1],
                        "f-measure": rouge2_score[2]
                    },
                    "ROUGE-L": {
                        "precision": rouge_l_score[0],
                        "recall": rouge_l_score[1],
                        "f-measure": rouge_l_score[2]
                    }
                })
        except Exception as e:
            print(f"Error processing candidate: {candidate}")
            print(f"Error processing dataset: {e}")
    
    print("Saving ROUGE scores...")
    write_json(os.path.join("data", "scores.json"), scores, indent=True)
    print("ROUGE scores saved to data/scores.json")


if __name__ == "__main__":
    create_data_directory()
    check_dataset_file()
    main()
