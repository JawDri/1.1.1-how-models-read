"""Lesson 1.1.1 - See text the way a model sees it: tokens and token IDs.

Free, offline after the first run (no API key). Uses tiktoken, OpenAI's open-source tokenizer -
the same one tiktokenizer.vercel.app shows. Claude uses its own tokenizer, so Claude's counts are
different (usually a bit higher): run count_tokens_claude.py to compare.

  .\\run.ps1 tokenizer_demo.py                      the lesson's examples
  .\\run.ps1 tokenizer_demo.py --text "your text"   any text
  .\\run.ps1 tokenizer_demo.py --file prompt.txt    a whole file (for example a system prompt)
"""
import argparse
import os
import sys

sys.dont_write_bytecode = True
from course_env import cache_path  # noqa: E402

# tiktoken downloads its vocabulary file once; keep it outside the lesson folder.
os.environ.setdefault("TIKTOKEN_CACHE_DIR", str(cache_path("tiktoken")))
import tiktoken  # noqa: E402

EXAMPLES = [
    "AI Automation from scratch is a superpower.",
    "Strawberry",
    "948,271.55",
    '{"customer_id": 84920, "status": "approved"}',
    "L'automatisation par l'IA est un super-pouvoir.",
]


def show(enc, text, ids_too=True):
    ids = enc.encode(text)
    pieces = [enc.decode([i]) for i in ids]
    words = len(text.split())
    print(f"\nTEXT   {text}")
    print(f"       {len(text)} characters | {words} word{'s' * (words != 1)} | {len(ids)} tokens")
    # A dot marks a space, so you can see that the space is part of the next token.
    print("PIECES " + " ".join(f"[{p.replace(' ', '·')}]" for p in pieces))
    if ids_too:
        print("IDS    " + " ".join(str(i) for i in ids))
    return len(text), words, len(ids)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--text", help="tokenize this text instead of the examples")
    p.add_argument("--file", help="tokenize a text file")
    p.add_argument("--encoding", default="o200k_base",
                   help="tiktoken encoding (o200k_base = GPT-4o and newer, cl100k_base = GPT-4)")
    args = p.parse_args()
    enc = tiktoken.get_encoding(args.encoding)
    print(f"Tokenizer: {args.encoding} (OpenAI). Claude's tokenizer splits text differently.")

    if args.file:
        with open(args.file, encoding="utf-8") as f:
            text = f.read()
        ids = enc.encode(text)
        print(f"\n{args.file}: {len(text):,} characters | {len(text.split()):,} words | {len(ids):,} tokens")
        print(f"= {len(text) / max(len(ids), 1):.1f} characters per token, "
              f"{len(text.split()) / max(len(ids), 1):.2f} words per token")
        return

    texts = [args.text] if args.text else EXAMPLES
    totals = [show(enc, t, ids_too=len(t) < 80) for t in texts]
    if len(totals) > 1:
        chars, words, toks = (sum(x) for x in zip(*totals[:1]))
        print(f"\nRule of thumb (plain English): 1 token ~ 4 characters ~ 3/4 of a word."
              f"\nFirst sentence: {chars / toks:.1f} characters per token, {words / toks:.2f} words per token."
              "\nNumbers, JSON, code and other languages use MORE tokens: always tokenize a real sample.")


if __name__ == "__main__":
    main()
