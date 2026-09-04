# BrandFlow AI

A small Python portfolio project built around one product idea: **brand context should be reusable instead of re-entered for every content request**.

BrandFlow AI separates persistent brand context from the authoring task, then uses both to produce content for emails, landing pages and forms.



\## Demo



\### Brand-aware authoring workflow



!\[BrandFlow AI main interface](docs/brandflow-main.png)



\### Generated content and consistency checks



!\[BrandFlow AI generated result](docs/brandflow-result.png)





## What changed in v2

* cleaner Streamlit UI
* reusable local brand profiles
* quick content presets
* structured brand/task brief
* editable generated result
* deterministic consistency checks
* JSON export
* optional OpenAI-compatible HTTP provider
* automated tests

## Why this project

Most text-generation demos are basically a single prompt box. I wanted to explore a slightly more product-oriented workflow:

1. save brand context once,
2. keep the content task separate,
3. generate from both,
4. make the brief inspectable,
5. run a few deterministic checks on the result.

The default provider is deterministic, so the project runs without API keys.

## Run locally

```bash
python -m venv .venv
```

Windows:

```bash
.venv\\Scripts\\activate
```

Install:

```bash
pip install -r requirements.txt
```

Test:

```bash
pytest -q
```

Run:

```bash
streamlit run app.py
```

## Optional AI provider

Set:

```text
BRANDFLOW\_PROVIDER=http
LLM\_API\_URL=https://your-provider.example/v1/chat/completions
LLM\_API\_KEY=your\_key
LLM\_MODEL=your\_model
```

Never commit a real `.env` file or API key.

## Project structure

```text
brandflow-ai/
├── .streamlit/
│   └── config.toml
├── brandflow/
│   ├── evaluator.py
│   ├── models.py
│   ├── profiles.py
│   ├── prompting.py
│   └── providers.py
├── tests/
│   ├── test\_evaluator.py
│   ├── test\_profiles.py
│   └── test\_prompting.py
├── app.py
├── requirements.txt
└── README.md
```

## Author

**Kamil Jozef Ginter**  
Trieste, Italy

