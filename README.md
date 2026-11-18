# The Day in World News, 18 November 2026

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/langsa5kilo-alt/news-image-18nov/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/langsa5kilo-alt/news-image-18nov/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

A 1024 × 1024 illustrated newspaper front page summarizing 28 world-news
stories from Wednesday 18 November 2026. It combines three lead scenes, eight
brief cards, a two-column news index, and a numbered world map.

Regenerate it from the repository root with:

```sh
python3 gen.py entry.png
```

The generator is deterministic and offline. It uses Python's standard library,
the checked-in `mask.txt` land mask, and the installed `rsvg-convert` command;
no Python packages or network access are needed.

To copy the generated image into a make.fun output directory with Node 22:

```sh
MAKEFUN_OUTPUT_DIR=/tmp/news-output node main.ts
```
