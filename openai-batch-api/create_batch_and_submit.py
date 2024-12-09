import argparse
import json
import math
import os
import sys

import pandas as pd
import yaml
from dotenv import load_dotenv
from openai import OpenAI

from utils import create_task, load_config, load_input_file


def main():
    parser = argparse.ArgumentParser(description="Create and submit batch tasks.")
    parser.add_config("--config", required=True, help="Path to configuration YAML")
    args = parser.parse_args()

    config_file = args.config

    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    config = load_config("config.yaml")

    input_file = config["input_file"]
    id_column = config["id_column"]
    content_column = config["content_column"]
    prompt = config["prompt"]
    data_path = config["data_path"]
    batch_size = config["batch_size"]
    model_params = config["model_params"]
    batch_submit_data = config["batch_submit_data"]

    df = load_input_file(input_file)

    # Check if the column is in the input file
    try:
        assert id_column in list(df.columns)
    except AssertionError as e:
        raise Exception(f"Column {id_column} not in {input_file}: Assertion failed {e}")
        sys.exit(1)

    # If the data_path doesn't exist, create it
    if not os.path.exists(data_path):
        os.mkdir(data_path)

    tasks = []
    for idx, row in df.iterrows():
        _id = row[id_column]
        content = row[content_column]
        task = create_task(_id, prompt, content, model_params)
        tasks.append(task)

    # Compute the number of batches to be created
    num_tasks = len(tasks)
    num_batches = math.ceil(
        num_tasks / batch_size
    )  # Ceiling of num_tasks / batch_size gives the actual number of batches

    print("Creating batches")
    for i in range(0, num_batches):
        batch_file_name = f"{data_path}/batch_task_{i+1}.jsonl"
        batch_tasks = tasks[i * batch_size : (i + 1) * batch_size]

        with open(batch_file_name, "w") as f:
            for obj in batch_tasks:
                f.write(json.dumps(obj) + "\n")

    # Submit jobs
    print("Submitting jobs")
    batch_data = []
    for i in range(1, num_batches + 1):
        batch_file_name = f"{data_path}/batch_task_{i}.jsonl"
        batch_file = client.files.create(
            file=open(batch_file_name, "rb"), purpose="batch"
        )

        batch_job = client.batches.create(
            input_file_id=batch_file.id,
            endpoint="/v1/chat/completions",
            completion_window="24h",
        )
        batch_data.append((i, batch_job.id))

    batch_data_df = pd.DataFrame(batch_data, columns=["batch_index", "batch_id"])
    batch_data_df.to_csv(f"{data_path}/{batch_submit_data}", index=False)
    print("Done creating and submitting jobs")
    print("please run python status_jobs.py to get job status")


if __name__ == "__main__":
    main()
