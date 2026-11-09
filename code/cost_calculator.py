"""Lesson 1.1.1 - The client cost math from the video, step by step.

Free, offline, no API key. Prices come from prices.json (check the pricing page and update it).

  .\\run.ps1 cost_calculator.py                          the lesson's support-ticket example
  .\\run.ps1 cost_calculator.py --runs-per-day 2000 --model haiku
  .\\run.ps1 cost_calculator.py --help                   every option
"""
import argparse
import sys

sys.dont_write_bytecode = True
from course_env import load_prices  # noqa: E402


def money(x):
    return f"${x:,.2f}"


def millions(tokens):
    return f"{tokens / 1e6:,.1f}M"


def main():
    prices = load_prices()
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--runs-per-day", type=int, default=500, help="tickets, emails, leads... per day")
    p.add_argument("--days", type=int, default=30)
    p.add_argument("--input-tokens", type=int, default=2000, help="input tokens per run (all of it)")
    p.add_argument("--output-tokens", type=int, default=200, help="output tokens per run")
    p.add_argument("--cached-tokens", type=int, default=1500,
                   help="part of the input that is identical on every run (0 = no caching)")
    p.add_argument("--refills-per-day", type=int, default=20,
                   help="runs per day that rewrite the cache (the first run after a 5-minute quiet gap)")
    p.add_argument("--model", choices=sorted(prices["models"]), default="sonnet")
    a = p.parse_args()

    m = prices["models"][a.model]
    runs = a.runs_per_day * a.days
    tin, tout = runs * a.input_tokens, runs * a.output_tokens

    print(f"CLIENT COST MATH  -  {m['name']}  (${m['input']:.2f} in / ${m['output']:.2f} out per 1M tokens,"
          f" prices checked {prices['checked_on']})\n")
    print(f"Step 1  Input per run     {a.input_tokens:>12,} tokens")
    print(f"Step 2  Output per run    {a.output_tokens:>12,} tokens")
    print(f"Step 3  Runs per month    {runs:>12,}         ({a.runs_per_day:,} a day x {a.days} days)")
    print(f"Step 4  Tokens per month  {tin:>12,} in  |  {tout:,} out")

    cost_in, cost_out = tin / 1e6 * m["input"], tout / 1e6 * m["output"]
    total = cost_in + cost_out
    print("\nWITHOUT CACHING")
    print(f"  Input   {millions(tin):>7} x {money(m['input']):>6}  = {money(cost_in):>10}")
    print(f"  Output  {millions(tout):>7} x {money(m['output']):>6}  = {money(cost_out):>10}")
    print(f"  TOTAL                      {money(total):>10} / month")

    if a.cached_tokens:
        refills = min(a.refills_per_day, a.runs_per_day) * a.days
        reads = (runs - refills) * a.cached_tokens
        writes = refills * a.cached_tokens
        fresh = runs * (a.input_tokens - a.cached_tokens)
        lines = [
            ("Cached input (read)", reads, m["cache_read"]),
            ("Cache refills (write)", writes, m["cache_write_5m"]),
            ("Fresh input", fresh, m["input"]),
            ("Output", tout, m["output"]),
        ]
        print(f"\nWITH PROMPT CACHING  (the first {a.cached_tokens:,} input tokens are identical on every run)")
        cached_total = 0.0
        for label, tokens, price in lines:
            cost = tokens / 1e6 * price
            cached_total += cost
            print(f"  {label:<22} {millions(tokens):>7} x {money(price):>6}  = {money(cost):>10}")
        print(f"  TOTAL                                  {money(cached_total):>10} / month"
              f"   ({1 - cached_total / total:.0%} less)")
        print(f"\n  Output is now {cost_out / cached_total:.0%} of the bill: keep outputs short and structured.")
        print(f"  Cache refills assume {a.refills_per_day} a day: the cache expires after 5 quiet minutes.")


if __name__ == "__main__":
    main()
