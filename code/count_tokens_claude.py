"""Lesson 1.1.1 (optional) - Count tokens with Claude's own tokenizer.

Needs an Anthropic API key (see README.md). Counting tokens is free: it uses the
count_tokens endpoint, which bills nothing and generates nothing.

  .\\run.ps1 count_tokens_claude.py                    the lesson's examples, Claude vs tiktoken
  .\\run.ps1 count_tokens_claude.py --file prompt.txt  count a whole prompt file
  .\\run.ps1 count_tokens_claude.py --dry-run          show the request without sending it
"""
import argparse
import json
import os
import sys

sys.dont_write_bytecode = True
from course_env import cache_path, require_anthropic_key  # noqa: E402
from tokenizer_demo import EXAMPLES  # noqa: E402

MODEL = "claude-sonnet-5-5"  # token counts depend on the model: use the one you will run


def tiktoken_count(text):
    os.environ.setdefault("TIKTOKEN_CACHE_DIR", str(cache_path("tiktoken")))
    import tiktoken
    return len(tiktoken.get_encoding("o200k_base").encode(text))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--file", help="count the tokens of a text file")
    p.add_argument("--model", default=MODEL)
    p.add_argument("--dry-run", action="store_true", help="print the request, send nothing")
    args = p.parse_args()

    texts = [open(args.file, encoding="utf-8").read()] if args.file else EXAMPLES
    if args.dry_run:
        print("POST /v1/messages/count_tokens")
        print(json.dumps({"model": args.model, "messages": [{"role": "user", "content": texts[0]}]}, indent=2))
        return

    require_anthropic_key()
    import anthropic
    client = anthropic.Anthropic()

    def count(text):
        return client.messages.count_tokens(
            model=args.model, messages=[{"role": "user", "content": text}]).input_tokens

    # The count includes a few tokens that wrap every message. Measure them once and remove them,
    # so the numbers below are for your text only ("a" is a single token).
    wrapper = count("a") - 1
    print(f"Model: {args.model}  (message wrapper = {wrapper} tokens, removed below)\n")
    print(f"{'Claude':>7} {'tiktoken':>9}  text")
    for text in texts:
        claude = count(text) - wrapper
        label = text if len(text) < 60 else f"{args.file} ({len(text):,} characters)"
        print(f"{claude:>7,} {tiktoken_count(text):>9,}  {label}")
    print("\nSame text, different tokenizers, different counts. Price a client job with the"
          "\ntokenizer of the model you will actually run.")


if __name__ == "__main__":
    main()
