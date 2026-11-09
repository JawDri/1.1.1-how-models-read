# Lesson 1.1.1 — How Models Actually Read

Demo code for **Lesson 1.1.1** of *AI Automation: From Scratch* (Module 1).

<!-- links:start -->
<!-- links:end -->

<!-- files:start -->
| File | What it shows | Needs |
|---|---|---|
| [`tokenizer_demo.py`](code/tokenizer_demo.py) | Text as tokens and token IDs (GPT-4o tokenizer, like tiktokenizer.vercel.app). `--text "..."` or `--file x.txt` for your own text. | nothing (free, offline after the first run) |
| [`cost_calculator.py`](code/cost_calculator.py) | The support-ticket cost math: $90 → $49.41/month with caching. `--help` for every option. | nothing (free, offline) |
| [`count_tokens_claude.py`](code/count_tokens_claude.py) | The same examples counted with Claude's own tokenizer, next to tiktoken. `--dry-run` sends nothing. | API key (the count_tokens endpoint is free) |
<!-- files:end -->

## Get the code
- **Download:** the green **Code** button → **Download ZIP**, then unzip it.
- **Or clone:** `git clone https://github.com/JawDri/1.1.1-how-models-read.git`

Keep the folder's name as it is: `setup.ps1` and `run.ps1` read the lesson number (1.1.1) from it.

## Run it
Everything is in [`code/README.md`](code/README.md): set up once (`setup.ps1` on Windows, a virtual environment on
Mac / Linux), then run the demos from the `code` folder.

## Your API key stays on your computer
The scripts that call the API read your key from your own key file, outside this folder:
`%USERPROFILE%\.ai-automation-from-scratch\.env` on Windows, `~/.ai-automation-from-scratch/.env` on Mac / Linux.
`code/.env.example` is only the template: never put a real key in it. `.gitignore` keeps `.env` files out of git,
so a fork or a pull request can't carry a key by mistake.
