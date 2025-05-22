# Are LLMs Ready to Help Non-Expert Users Make Charts of Official Statistics Data?

This repository contains the complete experimental data and results supporting our research on LLM-based automated chart generation from official statistics data.

## Research Overview

This study evaluates the capability of Large Language Models (LLMs) to democratize access to official statistics by automatically generating visualizations from complex tabular data in response to natural language queries. Working with diverse datasets from Statistics Netherlands, we conducted a comprehensive comparison across **10 different LLM approaches** to assess whether current generative AI models can bridge the gap between expert data analysis and non-expert user needs.

## Repository Contents

### Model Comparison Results

We evaluated **10 different LLM approaches** across the same Statistics Netherlands datasets:

#### Single-Shot Generation Models
- **CLAUDE 3.5** (`claude-3-5-sonnet-20241022`) - Anthropic's Claude 3.5 Sonnet
- **DEEPSEEK-CHAT** - DeepSeek's conversational model
- **GEMINI 2.0 FLASH THINKING** (`gemini-2.0-flash-thinking-exp-01-21`) - Google's Gemini with reasoning
- **GEMMA 2** - Google's open-source Gemma model
- **GPT-4o** (`gpt-4o-2024-11-20`) - OpenAI's GPT-4o
- **LLAMA3.1** - Meta's Llama 3.1 model
- **O1-HIGH** (`o1-2024-12-17-high`) - OpenAI's O1 model with high reasoning
- **O1-HIGH + ADDITIONAL CONTEXT** - O1 with enhanced prompting context
- **QWEN 2.5** - Alibaba's Qwen model

#### Iterative Agentic Approach
- **CLAUDE 3.7** (`CLAUDE 3.7_25_iterations_more_context_data_visualization`) - Our iterative self-evaluation system with up to 25 refinement iterations

### Datasets from Statistics Netherlands

All models were tested on 7 official Statistics Netherlands datasets:

- **Industry Production** - Industrial output and manufacturing statistics
- **Milk Supply** - Agricultural supply chain data
- **Caribbean Netherlands** - Demographic birth statistics for Caribbean Netherlands
- **Consumer Prices** - Consumer price index and inflation data
- **Producer Price Index (PPI)** - Manufacturing and wholesale price indices
- **Municipal Accounts** - Local government financial statistics
- **Population** - Demographic and population census data

### Task Complexity Levels
- **Easy** - Direct visualization of single data series
- **Medium** - Multi-step data processing with moderate complexity
- **Hard** - Complex analytical tasks requiring sophisticated data manipulation

## Understanding the Results Structure

### Single-Shot Model Results
Each single-shot model directory contains:
- **Dataset subdirectories** organized by topic (e.g., `CARIBBEAN NETHERLANDS/`, `CONSUMER PRICES/`)
- **Visualization outputs** (`.png` files) named with model identifier and task difficulty
- **Multiple attempts** for some tasks (indicated by `_2.py.png` suffixes)

### Iterative Agentic Results (Claude 3.7)
The `CLAUDE 3.7_25_iterations_more_context_data_visualization/` directory contains detailed traces of the iterative process:

**Directory naming:** `YYYYMMDD_HHMMSS_[dataset]_[difficulty]`

**Contents per experiment:**
- **`.log`** - Complete reasoning process and decision-making trace
- **`code_iteration_X.py`** - Evolution of generated Python code across iterations
- **`visualization.png`** - Final chart output
- **Auxiliary files** - Dataset-specific helper files when needed

This approach demonstrates our iterative self-evaluation system:
1. **Initial Attempt** - LLM generates first solution
2. **Self-Assessment** - Model evaluates its own output
3. **Iterative Refinement** - Up to 25 iterations of improvement
4. **Convergence** - Process stops when satisfactory or maximum iterations reached

## Core Evaluation Documents

- **`final_evaluation_results.pdf`** - Complete quantitative and qualitative analysis across all models
- **`summary_results_by_difficulty.pdf`** - Performance trends across complexity levels for all approaches
- **`dataset_retrieval_results.pdf`** - Analysis of data retrieval capabilities across models
- **`full_evaluation_questions.pdf`** - All evaluation prompts and assessment criteria
- **`full_list_of_prompts.pdf`** - Complete prompt engineering details
