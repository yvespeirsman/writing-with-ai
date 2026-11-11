# Experiment 1: Character Name Variation

Generate stories via OpenRouter, extract character names with an LLM, and visualize the results.

## Requirements

- Python 3
- `OPENROUTER_API_KEY` environment variable set
- Optional: create and activate a virtual environment in the project root:
  ```bash
  cd ..
  python3 -m venv venv
  source venv/bin/activate
  pip install matplotlib
  ```

## Scripts

### 1. Generate stories

```bash
python3 generate_stories.py [language] [model]
```

- **language**: `en` (default) or `nl`
- **model**: any OpenRouter model slug (default: `openai/gpt-6-luna`)

Stories are saved to `stories/<language>/<model_slug>/story_001.txt` … `story_100.txt`.

Examples:
```bash
python3 generate_stories.py
python3 generate_stories.py nl
python3 generate_stories.py en openai/gpt-4o-mini
```

### 2. Extract characters

```bash
python3 extract_characters.py <stories_folder>
```

Sends each story to the LLM and asks for comma-separated character names. Results are written to `<stories_folder>/characters.csv`.

Example:
```bash
python3 extract_characters.py stories/en/openai_gpt-6-luna
```

### 3. Visualize

Requires matplotlib in the root-level venv.

```bash
source ../venv/bin/activate
python3 visualize_characters.py <base_directory> [top_n]
```

Reads all `characters.csv` files under the given directory, counts names per model, and outputs a horizontal bar chart PNG for each model.

Example:
```bash
source ../venv/bin/activate
python3 visualize_characters.py stories 10
```

Output: `stories/characters_<model_slug>.png`
