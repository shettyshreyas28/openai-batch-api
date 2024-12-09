# openai-batch-api

The **openai-batch-api** python package enables batch processing with OpenAI Batch API. It includes functionalities for:
- Creating and submitting batches
- Monitoring batch statuses
- Collating outputs

---

## Features

1. **Batch Creation and Submission**  
   Automatically create batches from input data and submit them to OpenAI's API.
   
2. **Batch Status Monitoring**  
   Monitor the status of submitted batches and retrieve their details.

3. **Result Collation**  
   Collate and process results from completed batches, saving them in a user-defined format.

---

## Installation

To install the module, clone this repository and install it using pip:

```bash
git clone https://github.com/shettyshreyas28/openai-batch-api
cd openai-batch-api
pip install .
```

# Prerequisites
**Python dependencies**
Ensure that you have python 3.10 or later installted. All required dependencies will be installed automatically during the module installation.

**Environment Variables**
The module requires the following environment variable to be set:
* ```OPENAI_API_KEY```: Your OpenAI API Key
You can set this variable in a ```.env``` file
```python
OPENAI_API_KEY=<your_openai_api_key
```

**config.yaml**
The ```config.yaml`` file is not included in the repository. You must create this file and provide its path when running the scripts. Below is 
an example of the ```config.yaml``` structure:
```yaml
input_file: "path/to/input.csv"
id_column: "id"
content_column: "content"
prompt: "Your prompt here"
data_path: "path/to/data"
batch_size: 50
model_params:
  model: gpt-4o-min
  temperature: 0
  response_format:
    type: json_object
batch_submit_data: "batch_submissions.csv"
output_file: "path/to/output.pkl"
```
* input_file: Path to the input file (CSV or PKL).
* id_column: Column name for unique identifiers in the input file.
* content_column: Column name for task content.
* prompt: Prompt to be used for task generation.
* data_path: Path to save batch files and intermediate data.
* batch_size: Number of tasks per batch.
* model_params: Parameters for the OpenAI model (e.g., temperature, max_tokens).
* batch_submit_data: CSV file name for storing batch submission data.
* output_file: Path for the final output file.

# Usage

**Create and submit batches**
```python
create-batch --config path/to/config.yaml
```

**Check Batch Status**
```python
check-status --config path/to/config.yaml
```

**Collate Results**
```python
collate-output --config path/to/config.yaml
```

# Directory Structure

### Explanation of Key Files:
- `openai-batch-api`: The main package directory containing the core functionalities.
  - `create_batch_and_submit.py`: Script to create and submit tasks in batches.
  - `status_jobs.py`: Script to check the status of submitted jobs.
  - `collate_output.py`: Script to collate the outputs of completed jobs.
  - `utils.py`: Utility functions for common operations like loading configurations and creating tasks.
- `setup.py`: Contains the configuration for packaging and distribution.
- `README.md`: Documentation for the repository.
- `requirements.txt`: List of dependencies required to run the module.

