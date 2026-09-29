# Hindsight: A Crypto Strategy Backtester

**Two-week mentored project plan** · Mentor = you · Mentee = your friend

*"Hindsight" is a working title, so rename it freely. It fits because a backtest is literally a hindsight simulation, and the project's biggest lesson is how easily hindsight fools traders.*

---

## 1. At a glance

**The product.** A web app where you pick a coin, a trading strategy and its settings, and instantly see how that strategy would have performed historically versus simply buying and holding, after fees and with honest risk metrics. It lives at a public URL from Day 1 onward.

**What he'll learn.** Python fundamentals, APIs and JSON, data analysis with pandas, basic SQL, unit testing, the Git/GitHub team workflow (branches, pull requests, code review), CI, and deploying a web app. On the trading side: returns, volatility, the Sharpe ratio and drawdowns, plus the three traps that sink most amateur strategies: lookahead bias, fees, and overfitting.

**What goes on his resume.** A live demo link, a clean public repo with tests and a green CI badge, a README containing a genuine research finding, and a pull-request history that shows real collaborative development.

**Time assumptions.** Mentee: about 3 focused hours per weekday (roughly 30–35 hours over 10 working days), with weekends as buffer. Mentor: 4–5 hours of setup before Day 1, then about an hour a day (check-in, concept lesson, PR review) plus two longer sessions, for roughly 15–20 hours total. If his time is tighter, use the scope-cut order in Section 10.

**Owner tags used throughout:**

| Tag | Meaning |
|---|---|
| 🟦 **Mentee** | He writes the code; you review the PR. |
| 🟩 **Mentor** | You write it; he reviews your PR and explains it back to you. |
| 🟨 **Pair** | One screen, *him typing*, you navigating. |
| 💡 **Concept checkpoint** | A short lesson from you *before* he starts the task (teaching notes in Section 8). |

---

## 2. Why this project

It rides on an interest he already has. He knows what candles, moving averages and RSI are, so every day he's translating intuition he already owns into code and numbers. Motivation stays high, and he gets to be the domain expert in the room. Every component maps onto a transferable engineering skill (APIs, data wrangling, modular functions, testing, version control, deployment), and the math never goes beyond averages, percentages and standard deviation, each introduced exactly when it's needed. The finished result is also easy for a recruiter to evaluate in a minute: click the live link, skim the README.

Two tempting alternatives are deliberately out of scope. A **live trading bot** adds real money, API-key security and order-execution complexity, and there a bug costs money; the backtester teaches the same decision logic safely (signal alerts are a stretch goal). An **ML price predictor** needs statistics he doesn't have yet and makes it very easy to produce impressive-looking but meaningless results through data leakage, which experienced interviewers spot instantly. A backtester that honestly reports "my optimized strategy lost to buy-and-hold on unseen data" is a far stronger signal than a model claiming 90% accuracy.

### MVP: must ship by Day 10

1. Fetch and locally cache daily candles (OHLCV) for BTC/USD and ETH/USD.
2. Three hand-written, unit-tested indicators: SMA, EMA, RSI.
3. Two strategies (SMA crossover, RSI mean-reversion) plus a buy-and-hold benchmark.
4. A backtest engine that charges fees and cannot peek into the future.
5. Metrics: total return, CAGR, annualized volatility, Sharpe ratio, max drawdown, number of trades, time in market.
6. An interactive Streamlit dashboard, deployed publicly.
7. An in-sample vs. out-of-sample experiment written up in the README, with all tests running in CI.

### Stretch goals: only after the MVP is merged

A third strategy designed and built solo (for example a breakout or Bollinger Band strategy); a trade list with win rate and average win/loss; deeper price history via API pagination; the parameter heatmap as a tab in the app; a scheduled GitHub Action that posts the day's signal to a Discord channel via webhook (alerts only, never orders); 4-hour candles; a Dockerfile (mentor-owned).

---

## 3. Tech stack

| Layer | Choice | Why it fits this project and this learner | Considered instead |
|---|---|---|---|
| Language | **Python 3.12+** | Reads almost like pseudocode, so he fights concepts rather than syntax. It's the default language of data analysis, quant research and fintech prototyping, and every tool below is Python-native. | JavaScript: essential for web front-ends, but weaker data tooling, and it would split his focus. |
| Environment & packages | **uv** | One fast tool installs Python itself, creates the virtual environment, manages dependencies and writes a lockfile. `uv run …` spares a beginner the "did I activate the venv?" trap, and the lockfile makes his laptop, yours, CI and the server identical. | pip + venv: perfectly fine, but more steps and more ways to break on Day 1. (Still teach *what* a virtual environment is.) |
| Editor & scratchpad | **VS Code** with the Python, Jupyter and Ruff extensions | Free and industry-standard, with a debugger and Git UI built in. Notebooks run inside the editor for exploration, while real code lives in `.py` files, a habit worth forming early. | PyCharm (heavier); standalone JupyterLab (one more tool). |
| Market data | **CCXT**, public endpoints only | One unified call (`fetch_ohlcv`) across 100+ exchanges. Public market data needs no API key, so there are no secrets to leak and no exchange account is required. Widely used in real crypto tooling. | Raw `requests` calls (every exchange has different quirks); yfinance (unofficial, prone to breaking or rate limits); keyed data APIs (sign-ups, tighter free tiers). |
| Data analysis | **pandas** (+ NumPy) | The standard for tabular and time-series data, and its core operations map one-to-one onto trading ideas: `rolling()` is a moving average, `pct_change()` is returns, `shift()` is "yesterday", `cummax()` is the running peak. Endless beginner tutorials and Q&A. | Polars: faster and elegant, but fewer beginner resources, and speed is irrelevant at a few thousand rows. |
| Storage / cache | **SQLite** (built into Python) | A zero-install, single-file database. Caching candles avoids re-downloading and rate limits, speeds up the app, and gives him genuine SQL practice, a skill in almost every data and developer job description. | CSV/Parquet files (simpler, and the fallback if time runs short); PostgreSQL (needs a server, overkill here). |
| Charts | **Plotly** | Interactive candlestick charts with zoom and hover in a few lines; renders identically in notebooks and in Streamlit. | Matplotlib: static, and much more code for candlesticks. |
| Web app | **Streamlit** | A real web app in pure Python, with no HTML, CSS or JavaScript. Sliders and dropdowns map directly onto strategy parameters. He ships a product without learning a second language. | Dash (more boilerplate); FastAPI + React (weeks of extra learning). |
| Testing | **pytest** | Tests are plain functions with `assert`. They're what catch the subtle math bugs in indicators and backtests, and a tested project immediately stands out among junior portfolios. | unittest (more ceremony). |
| Lint & format | **Ruff** | One fast tool replaces flake8, black and isort. Auto-formatting ends style debates in review, so reviews focus on logic. | black + flake8 (two tools, same outcome). |
| Collaboration | **Git + GitHub**: branches, pull requests, reviews, Issues and a Projects board | This *is* how software teams work, and his PR history becomes public, verifiable proof of work. | — |
| CI | **GitHub Actions** | Runs lint and tests on every pull request automatically, is free for public repos, and puts a green "passing" badge on the README. | — |
| Hosting | **Streamlit Community Cloud** | Free, deploys straight from the GitHub repo, redeploys on every push to `main`, and reads `uv.lock` directly, so no extra dependency file is needed. The live link is the centerpiece of the resume entry. | Render, Fly.io or Docker on a VPS: more ops work than learning value at this stage. |

**Pick a US-accessible exchange for data.** Many CCXT tutorials default to Binance, but Binance's main API rejects requests from US IP addresses with HTTP 451, and Streamlit Community Cloud and GitHub Actions both run on US-based servers. A Binance-based app can therefore work on a laptop and then fail after deployment. Default to **Kraken** and keep the exchange a single configurable setting. One limit to know: Kraken's public candle endpoint returns only the most recent 720 candles per timeframe (about two years of daily data), which is enough for the MVP. For deeper history, Coinbase Exchange's candle endpoint (CCXT id `coinbaseexchange`) can be paged backwards 300 candles at a time, which makes a good stretch task for writing a pagination loop.

**Deliberately left out.** No order placement or private API keys (safety and scope). No machine learning (see Section 2). No ready-made indicator or backtesting libraries such as TA-Lib, Backtrader or vectorbt: they would do precisely the thinking he's supposed to learn. A good *post*-project exercise is re-running one strategy in an established library to cross-check his engine. No JavaScript front-end, and no Docker or cloud infrastructure in the MVP.

---

## 4. Roles and ownership

### Guiding principles

1. **He owns the brain; you own the plumbing.** Indicators, strategies, backtest math, metrics, charts and the written findings are what interviewers will ask about and where the learning is, so they're his. Repo setup, tooling config, CI, caching and deployment wiring are high-friction and low-learning for a first-week beginner, so you absorb them, but you walk him through each one so nothing stays magic.
2. **I do → We do → You do.** For every repeated pattern (indicators, strategies, tests) you build the first one while thinking aloud, you pair on the second, and he builds the third alone.
3. **Contract-first scaffolding.** In Week 1 you write function stubs (name, inputs, outputs, docstring) plus tests, and his job is to make them pass. From Day 7 he writes his own tests. Clear targets remove the blank-page paralysis beginners feel.
4. **Explain-back rule.** Nothing merges into `main` that he can't explain line by line, including your code. He reviews your PRs and leaves at least one question on each; reading other people's code is a day-one job skill.
5. **The keyboard stays with him.** When pairing, he types. If you catch yourself reaching for the keyboard, ask a question instead.
6. **AI assistants are a tutor, not a ghostwriter.** On 🟦 tasks he can use AI to explain concepts and error messages, but not to generate the solution. If AI-written code does land in a PR, he says so in the description, and the explain-back rule still applies. His resume claims and interview answers depend on him genuinely knowing this code.

**When he's stuck, climb the hint ladder one rung at a time:** (1) ask a question that points at the problem ("what's the value of `window` on that line?"); (2) name the concept or doc page ("look at what `shift` does"); (3) show a similar, not identical, example; (4) pair on it, with him typing. Agree on a **30-minute rule**: after 30 minutes stuck, he messages you with what he tried, the full error, and what he expected. Asking a good technical question is itself a skill he's practicing.

### Ownership matrix

| Component | Owner | Your role | His role |
|---|---|---|---|
| Repo scaffold, `pyproject.toml`, Ruff/pytest config | 🟩 | Build on Day 0 | Read it; ask three questions on Day 1 |
| CI workflow | 🟩 | Build on Day 0 | Explain what each step does |
| Function stubs + tests for Days 2–6 | 🟩 | Write the "contracts" | Make them pass |
| Data fetching (`candles_to_dataframe`, `fetch_ohlcv`) | 🟦 | 💡 APIs, JSON, timestamps | Implement and explore the data |
| SQLite cache | 🟩 + 🟦 | Schema, save and refresh logic | One SQL query function |
| Returns and buy-and-hold | 🟦 | 💡 compounding | Implement and test |
| Indicators | 🟩 SMA → 🟨 EMA → 🟦 RSI | Demo, then pair | RSI solo, validated against his charting platform |
| Strategies | 🟩 SMA crossover → 🟦 RSI reversion | Reference implementation | Stateful strategy + tests |
| Backtest engine | 🟨 (he types) | 💡 lookahead bias and fees; write the trap tests | Implement until the tests pass |
| Metrics | 🟦 | 💡 volatility, Sharpe, drawdown; two test cases | All functions, plus his own tests |
| Streamlit app | 🟩 skeleton → 🟦 charts and metrics | Layout, widgets, caching, error handling | Charts and metric cards |
| Experiments and findings | 🟦 | 💡 overfitting; check the methodology | Sweep, out-of-sample test, write-up |
| Deployment | 🟨 | Guide the first deploy | Owns the repo and the app; verifies each release |
| README, resume bullets, pitch | 🟦 | Edit; run the mock interview | Write and present |

By the end he should have written roughly 70% of the application code and reviewed 100% of yours.

---

## 5. Architecture and repo layout

Every stage is a plain function: DataFrame or Series in, DataFrame or Series out. That's the single most useful software idea in the project. Each piece can be tested on a five-row example with no internet, and pieces can be swapped (new coin, new strategy) without touching the others.

```
 Exchange (Kraken) ──CCXT──► data.py ◄──► SQLite cache (data/market.db)
                               │  DataFrame: open, high, low, close, volume (UTC daily index)
                               ▼
                        indicators.py    sma(), ema(), rsi()
                               ▼
                        strategies.py    buy_and_hold(), sma_crossover(), rsi_reversion()
                               │  position Series: 1 = holding the coin, 0 = in cash
                               ▼
                         backtest.py     run_backtest(df, position, fee) → equity curve
                               ▼
                          metrics.py     total_return, cagr, sharpe_ratio, max_drawdown, …
                               ▼
                            app.py       Streamlit + Plotly dashboard (deployed)
```

**The key contract.** A strategy answers exactly one question per day, "should I be holding the coin (1) or cash (0)?", and returns the answers as a *position series*. The backtester never needs to know how a decision was made, which is why adding a new strategy later is a 20-line job. Long-only, with no leverage and no shorting, keeps the math simple.

```
hindsight/
├── app.py                        # Streamlit entry point: UI wiring only, no strategy math
├── hindsight/                    # the core package: all logic lives here
│   ├── __init__.py
│   ├── data.py
│   ├── indicators.py
│   ├── strategies.py
│   ├── backtest.py
│   └── metrics.py
├── tests/
│   ├── fixtures/btc_sample.csv   # ~60 real daily candles for offline tests and demos
│   ├── test_data.py
│   ├── test_indicators.py
│   ├── test_strategies.py
│   ├── test_backtest.py
│   └── test_metrics.py
├── notebooks/exploration.ipynb   # scratchpad; never imported by the app
├── data/                         # SQLite cache (git-ignored)
├── .github/
│   ├── workflows/ci.yml
│   └── pull_request_template.md
├── .vscode/settings.json         # lets notebooks import from the repo root
├── pyproject.toml
├── uv.lock
└── README.md
```

### The contracts (you write these stubs on Day 0)

```python
# Sketch of the stubs. Each real stub gets a full docstring and a body of:
#     raise NotImplementedError
# The trailing comment shows who implements it, and when.

# hindsight/data.py
def candles_to_dataframe(raw: list[list[float]]) -> pd.DataFrame:        # 🟦 Day 2
    """[[timestamp_ms, open, high, low, close, volume], ...] -> DataFrame indexed by
    UTC datetime, columns open/high/low/close/volume as floats."""
def fetch_ohlcv(symbol="BTC/USD", timeframe="1d", exchange_id="kraken"):  # 🟦 Day 2
    """Network call via CCXT, then candles_to_dataframe(). Drops the still-forming candle."""
def save_candles(df, symbol, timeframe) -> None:                          # 🟩 Day 3
def load_candles(symbol, timeframe, start=None, end=None) -> pd.DataFrame:  # 🟦 Day 3 (SQL)
def get_candles(symbol, timeframe="1d", refresh=False) -> pd.DataFrame:     # 🟩 Day 3
    """Serve from the cache; download only when missing, stale, or refresh=True."""

# hindsight/indicators.py
def sma(close: pd.Series, window: int) -> pd.Series:                      # 🟩 Day 4 (I do)
def ema(close: pd.Series, span: int) -> pd.Series:                        # 🟨 Day 4 (we do)
def rsi(close: pd.Series, window: int = 14) -> pd.Series:                 # 🟦 Day 4 (you do)

# hindsight/strategies.py (every strategy returns a 0/1 position Series)
def buy_and_hold(df: pd.DataFrame) -> pd.Series:                          # 🟦 Day 5
def sma_crossover(df, fast: int = 20, slow: int = 50) -> pd.Series:       # 🟩 Day 5
def positions_from_thresholds(indicator, lower, upper) -> pd.Series:      # 🟦 Day 5
def rsi_reversion(df, window=14, lower=30.0, upper=70.0) -> pd.Series:    # 🟦 Day 5

# hindsight/backtest.py
def daily_returns(close: pd.Series) -> pd.Series:                         # 🟦 Day 3
def equity_curve(returns: pd.Series) -> pd.Series:                        # 🟦 Day 3
def run_backtest(df, position: pd.Series, fee: float = 0.001) -> pd.DataFrame:  # 🟨 Day 6
    """Columns: position_held, asset_return, trade, strategy_return, equity."""

# hindsight/metrics.py
def total_return(equity: pd.Series) -> float:                             # 🟦 Day 7
def cagr(equity: pd.Series, periods_per_year: int = 365) -> float:        # 🟦 Day 7
def annual_volatility(returns, periods_per_year: int = 365) -> float:     # 🟦 Day 7
def sharpe_ratio(returns, periods_per_year: int = 365) -> float:          # 🟦 Day 7
def max_drawdown(equity: pd.Series) -> float:                             # 🟦 Day 7
def count_trades(position: pd.Series) -> int:                             # 🟦 Day 7
def summarize(result: pd.DataFrame) -> dict[str, float]:                  # 🟦 Day 7
```

---

## 6. Day 0: your setup (before he starts, about 4–5 hours)

Everything here is 🟩 unless marked otherwise.

1. **Repo on his account (10-minute call).** He creates an empty *public* repo on his own GitHub account, so it appears on his profile, and invites you as a collaborator. Add an MIT license and a Python `.gitignore` extended with `data/*.db` and `.env`.
2. **Diagnose before you plan.** On the same call, give him three tiny tasks (print the larger of two numbers; loop over a list of prices; write a function that returns a percent change). Ten minutes of watching him tells you whether Day 1's Python block needs one hour or three.
3. **Scaffold with uv:** `uv init --python 3.12`, then `uv add ccxt pandas plotly streamlit` and `uv add --dev pytest ruff ipykernel`. Create the layout from Section 5, and add a `.vscode/settings.json` containing `{"jupyter.notebookFileRoot": "${workspaceFolder}"}` so notebooks can `import hindsight`.
4. **Stubs and tests** for Days 2–6: each stub has its docstring and `raise NotImplementedError`. Mark each day's tests with `@pytest.mark.skip(reason="unlock on Day N")` so CI stays green. Deleting that line is the first thing he does when starting a task, which makes progress visible.
5. **Tooling config** (Appendix A): Ruff rules, and pytest's `pythonpath = ["."]` so tests can import the package.
6. **CI** (Appendix A): Ruff and pytest on every PR. No test may touch the network, because exchanges rate-limit and geo-block CI runners.
7. **Offline fixture:** commit about 60 real BTC daily candles as `tests/fixtures/btc_sample.csv`, for integration tests and as a demo fallback when the API is down.
8. **Hello app:** an `app.py` with a title and one hard-coded chart, ready for him to deploy on Day 1.
9. **The plan as Issues:** one Issue per task in Section 7, labeled `mentee`, `mentor`, `pair` or `concept`, on a GitHub Projects board. Dragging cards to Done is surprisingly motivating, and the board is visible evidence of real process.
10. **Templates:** the PR template (Appendix B) and a short `CONTRIBUTING.md` with the setup commands.
11. **Dry-run the setup** on a clean machine or a fresh GitHub Codespace matching his OS. Environment setup is the number-one risk to Day 1.

---

## 7. Day-by-day plan

**Daily rhythm.** A 10-minute check-in (what I did · what I'll do · what's blocking me) → the 💡 concept checkpoint → his focused work block → he opens a PR and writes three lines in a learning log (what I learned · what confused me · a bug I fixed) → you review it the same evening. Fast feedback beats thorough feedback. The learning log doubles as his source material for interview stories.

### Week 1 — Foundations: from raw data to trading signals

#### Day 1: Setup, Python essentials, first PR, live URL

**Goal:** a working environment, a mental map of the project, his first merged PR, and a live (if nearly empty) app.

💡 **Concept checkpoint (~45 min).** Walk the architecture diagram: each box is a file, each arrow is a function call. Terminal basics: moving between folders and running commands. The Git mental model: a commit is a save point, a branch is a parallel draft, and a pull request is "please review my draft before it goes into the real version." Then flip roles: have *him* explain candles, OHLCV, moving averages and RSI to *you* the way he'd explain them to a fellow trader, while you sketch how each will look as a table of numbers. He starts the project as the domain expert, which does wonders for confidence.

| Owner | Task | Time |
|---|---|---|
| 🟦 (you on call) | Install VS Code, Git and uv; clone; `uv sync`; `uv run pytest` (everything shows as *skipped*, which is expected); `uv run streamlit run app.py`. | 45 min |
| 🟨 | As repo owner, he protects `main` (require a PR, one approval and passing CI) and deploys the hello app on Streamlit Community Cloud, choosing Python 3.12 under Advanced settings. Deploying requires admin rights on the repo, which is why he does it. From now on every merge updates the live site. | 20 min |
| 🟦 | Python essentials in a scratch notebook, trading-flavored: variables, lists, dicts, `if`, `for`, functions, `return` vs. `print`. Exercises: compute each day's % change from a hard-coded list of ten BTC closes with a loop; find the biggest up-day; write `pct_change(old, new)`. | 60–90 min |
| 🟦 | First PR: on a branch, add himself to the README's Authors section plus one line on what he wants to learn. You leave one comment, he addresses it, and it merges. | 20 min |
| 🟦 | Read `pyproject.toml` and `ci.yml`, then post three questions about them. | 15 min |

Optional resources: lectures 0–2 of CS50P (Harvard's free *Introduction to Programming with Python*), Kaggle Learn's short Python course, and GitHub Skills' "Introduction to GitHub."

✅ **Done when:** the app runs locally and at a public URL, tests run, and his first PR is merged.
❓ **Ask him:** "What's the difference between a commit and a push?" · "Why do we work on a branch instead of `main`?" · "What does `return` do that `print` doesn't?"

#### Day 2: APIs, pulling real market data

**Goal:** `candles_to_dataframe()` and `fetch_ohlcv()` return a clean DataFrame of real BTC/USD daily candles.

💡 **Concept checkpoint (~40 min).** What an API is (a restaurant menu: you can order anything listed, and the kitchen stays hidden); request and response; JSON; public vs. private endpoints (we only ever use public market data, so no keys and no trading); rate limits (be polite and cache results); timestamps as milliseconds since 1 January 1970 UTC, and why crypto data should always stay in UTC. Then pandas basics: DataFrame, columns, index, dtypes, `head()`, `describe()`. Finally, the design idea of the day: keep the network call (`fetch_ohlcv`) separate from the transformation (`candles_to_dataframe`) so the logic can be tested without internet.

| Owner | Task | Time |
|---|---|---|
| 🟩 Demo | In a notebook, run `ccxt.kraken().fetch_ohlcv("BTC/USD", "1d", limit=5)` and inspect the raw list of lists together. | 15 min |
| 🟦 | Unlock and pass the tests for `candles_to_dataframe()`: list → DataFrame, ms → UTC datetime index, correct column names, float dtypes. | 60 min |
| 🟦 | Implement `fetch_ohlcv()` as a thin wrapper and verify it by hand in the notebook (never in tests). Notice that the last candle is today's and is still changing; should a backtest use it? (No, so drop it here.) | 30 min |
| 🟦 | Explore: plot the close price. Ask for data starting in 2018; how far back do you actually get? If it's less, find out why in the exchange's API docs (a real-world lesson in API limits). What was the biggest one-day % move? How many days fell more than 5%? | 60 min |

Optional resource: Kaggle Learn's Pandas course, lessons 1–2.

✅ **Done when:** tests pass in CI and the notebook shows a real BTC chart.
❓ "Why don't our tests call the real API?" · "What's your DataFrame's index, and why does it matter?" · "What would happen if the app called the exchange every time someone moved a slider?"

#### Day 3: Caching and returns

**Goal:** candles load from the local SQLite cache, and he can compute returns and a buy-and-hold equity curve.

💡 **Concept checkpoint (~40 min).** Returns and compounding, the idea everything else builds on: a +50% day followed by a −50% day does not bring you back to even (100 → 150 → 75), so returns are multiplied, not added. An equity curve is simply "what $1 invested at the start is worth each day." Then databases in five minutes: a table, rows and columns, a primary key (why the same candle can't be stored twice), and parameterized queries with `?` placeholders. Never build SQL with f-strings, because of SQL injection.

| Owner | Task | Time |
|---|---|---|
| 🟩 | Build `save_candles()` and `get_candles()` on the schema `candles(symbol, timeframe, ts, open, high, low, close, volume, PRIMARY KEY (symbol, timeframe, ts))`, using an upsert. Walk him through it. | before session + 15 min |
| 🟦 | `load_candles(symbol, timeframe, start, end)`: his first `SELECT … WHERE … ORDER BY`, with parameters. | 45 min |
| 🟦 | `daily_returns()` and `equity_curve()`. The test *is* the concept: prices `[100, 150, 75]` → returns `[0, 0.5, −0.5]` → equity `[1.0, 1.5, 0.75]`. | 45 min |
| 🟦 | Notebook: BTC vs. ETH buy-and-hold equity on one Plotly chart, both starting at $1. | 45 min |

✅ **Done when:** running the notebook twice makes only one network call (he proves it with a log line), and the return tests pass.
❓ "Up 10%, then down 10%: where are you?" (−1%) · "Why multiply returns instead of adding them?" · "What does the primary key prevent?"

#### Day 4: Indicators (I do → We do → You do)

**Goal:** SMA, EMA and RSI, implemented from scratch and tested.

💡 **Concept checkpoint (~40 min).** Rolling windows: draw five closes on paper and slide a three-day window across them before any code exists. The warm-up period: the first N−1 values of an N-day average don't exist and must stay empty (NaN), never zero. EMA as an average with a fading memory. RSI from trader intuition to formula (Section 8.3). How to write a test from a tiny hand-calculated example, and why floats are compared with `pytest.approx` (0.1 + 0.2 isn't exactly 0.3 in almost any programming language).

| Owner | Task | Time |
|---|---|---|
| 🟩 I do | Live-code `sma()` and its test while thinking aloud: read the docstring → hand-compute `[1, 2, 3, 4, 5]` with window 3 → `[NaN, NaN, 2, 3, 4]` → write the test → implement with `rolling().mean()` → green → commit. | 20 min |
| 🟨 We do | `ema()`, with him typing. Find pandas' `adjust` parameter in the docs together and see why the recursive EMA traders use corresponds to `adjust=False`. Test: `[1, 2, 3]` with span 3 → `[1.0, 1.5, 2.25]`. | 40 min |
| 🟦 You do | `rsi()` solo, with property tests: steadily rising prices → 100 after warm-up; steadily falling → 0; every value between 0 and 100. | 75 min |
| 🟦 | Real-world check: compare his BTC/USD daily RSI with the RSI on the charting platform he already uses (same exchange, pair and timeframe). They should agree closely; small gaps come from how much history each side uses to warm up the average. | 20 min |

✅ **Done when:** indicator tests pass in CI, and the notebook shows price with SMA-20/SMA-50 overlays and an RSI panel.
❓ "Why are the first 19 values of SMA-20 empty?" · "What would go wrong if we filled them with zeros?" · "Why can RSI never exceed 100?"

#### Day 5: Strategies as functions + Week-1 demo

**Goal:** each strategy returns a position series (1 = holding the coin, 0 = in cash).

💡 **Concept checkpoint (~30 min).** The contract: every strategy is `f(df, **settings) → Series of 0s and 1s`, and the backtester doesn't care how the decision was made. Signal vs. position: a signal is an event ("buy now"), while a position is a state ("I'm holding"). Some strategies are stateless (SMA crossover just compares two lines each day); others need memory ("stay in until RSI rises above 70" means remembering that you're in).

| Owner | Task | Time |
|---|---|---|
| 🟩 I do | `sma_crossover()` as the reference strategy (a one-line comparison of fast and slow SMA, with warm-up days → 0), plus its test. | 20 min |
| 🟦 | `buy_and_hold()` (all ones): the benchmark every strategy must beat. | 10 min |
| 🟦 You do | `positions_from_thresholds()` with a plain `for` loop and an `in_position` variable: enter below `lower`, exit above `upper`, otherwise keep doing what you were doing. Test with fake indicator values `[50, 25, 40, 75, 60]`, lower 30 and upper 70 → `[0, 1, 1, 0, 0]`, plus a test that NaN warm-up values never trigger a trade. Then `rsi_reversion()` simply combines `rsi()` with this helper. | 75 min |
| 🟩 Refactor lesson | Show a vectorized version (mark entries and exits, then forward-fill). His tests prove both versions agree, which is the moment he sees *why* tests exist: they make changing code safe. | 20 min |
| 🟦 | Week-1 demo: ten minutes presenting the notebook as if to a recruiter, covering what's built, what he learned, and what still confuses him. | 15 min |
| 🟩 | Retro: compare progress with the plan and apply scope cuts (Section 10) *now*, not on Day 9. | 15 min |

✅ **Done when:** strategy tests pass, and the notebook shows buy/sell markers on the BTC chart for both strategies.
❓ "What's the difference between a signal and a position?" · "Why does the RSI strategy need memory when the SMA one doesn't?"

**Weekend 1: buffer.** Catch up first. If he's ahead: finish the Kaggle Pandas course, watch CS50P lecture 5 (unit tests) before Day 7, or take on the pagination stretch task for deeper history before Day 9.

### Week 2 — The engine, the product, and the story

#### Day 6: The backtest engine (pairing day)

**Goal:** `run_backtest()` turns prices and positions into an honest equity curve, with fees and no lookahead bias.

💡 **Concept checkpoint (~45 min): the most important lesson in the project.** Lookahead bias means trading on information you didn't have yet. A decision made from today's close can only earn *tomorrow's* return, which in code is a single `shift(1)`. Walk through the "cheater" example in Section 8.4 on paper: without the shift, a strategy that peeks at each day's own return looks like a money machine. Then fees: every change in position costs a percentage (typically somewhere around 0.1–0.6% per trade depending on exchange and fee tier, which is why it's a parameter), and a strategy that trades often can bleed to death through fees alone. Leave him with a maxim: *if a backtest looks amazing, assume it's a bug until proven otherwise.*

| Owner | Task | Time |
|---|---|---|
| 🟩 | Before the session, write three trap tests (ready-made examples in Section 8.4): a hand-computed five-day example; the cheater test, in which a strategy that peeks at same-day returns must *not* make money; and the fee test, in which one round trip with no price change must end at `(1 − fee)²`. | before session |
| 🟨 | Implement `run_backtest()` together, with him typing, until all three tests pass. Then run it on real BTC data for all three strategies. | 90 min |
| 🟦 | Break it on purpose: delete the `shift(1)`, run the tests, watch the cheater test fail, explain why in his own words, then restore it. | 15 min |
| 🟦 | Notebook: equity curves for all three strategies at fee = 0% vs. 0.25%, plus a three-sentence observation. | 45 min |

✅ **Done when:** all trap tests pass, and he can explain without notes why the `shift(1)` is there.
❓ "Which test failed when you deleted the shift, and why?" · "A strategy makes 100 round trips a year at 0.25% per side. Roughly what do fees cost it?" (About 40% of capital a year, before the strategy earns anything. That's the point.)

#### Day 7: Performance metrics

**Goal:** a `summarize()` scorecard for any backtest.

💡 **Concept checkpoint (~40 min).** Draw two equity curves that end at the same place, one smooth and one wild, and ask which he'd rather have lived through. That's volatility (the standard deviation of daily returns: how bumpy the ride is) and max drawdown (the worst fall from a peak: the pain you'd have had to sit through). The Sharpe ratio is return per unit of bumpiness. Annualizing: crypto trades 365 days a year (stocks about 252), so daily volatility is scaled by √365; accept the square root for now as "risk grows with the square root of time." CAGR is the steady yearly growth rate that would get you from start to finish. Formulas are in Sections 8.6–8.8.

| Owner | Task | Time |
|---|---|---|
| 🟩 | Two test cases with expected values: the max drawdown of equity `[1.0, 1.2, 0.9, 1.1, 0.6, 1.3]` is −50%, and an equity curve that doubles over 730 daily periods has a CAGR of √2 − 1 ≈ 41.42%. | 10 min |
| 🟦 | Implement all the metric functions. | 75 min |
| 🟦 Milestone | His *own* tests, written without a template, for `total_return`, `count_trades` and time in market, including the edge case of a strategy that never trades. | 45 min |
| 🟦 | `summarize()` plus a comparison table (strategies × BTC/ETH) in the notebook. | 30 min |
| 🟦 Stretch | Trade list: turn positions into individual trades (entry, exit, return) → win rate, average win vs. average loss. | — |

✅ **Done when:** the metric tests pass, including the ones he wrote himself, and the comparison table exists.
❓ "Two strategies both returned 80%. One had a −70% drawdown, the other −25%. Which could you actually have stuck with?" · "Why √365 and not √252?"

#### Day 8: The dashboard

**Goal:** the interactive app works locally and at the live URL.

💡 **Concept checkpoint (~30 min).** How Streamlit works: the whole script reruns top to bottom every time a widget changes, which is exactly why data loading must be cached with `@st.cache_data`, a callback to Day 2's "don't hammer the API." Layout: sidebar for inputs, main area for results. Separation of concerns: `app.py` only wires tested functions together, so there is no strategy math in the UI file.

| Owner | Task | Time |
|---|---|---|
| 🟩 | App skeleton, built before the session: page config; a sidebar with coin, date range, a strategy picker that shows the right sliders for the chosen strategy, and a fee input; cached data loading; a friendly error message with a fallback to cached data (or the sample fixture) if the exchange is unreachable; empty placeholders for charts and metrics. | before session + 15 min walkthrough |
| 🟦 | Candlestick chart with indicator overlays and buy/sell markers. | 60 min |
| 🟦 | Equity curve (strategy vs. buy-and-hold) and a drawdown ("underwater") chart. | 45 min |
| 🟦 | Metric cards (`st.metric`) showing each metric and its difference from buy-and-hold. | 30 min |
| 🟨 | Merge via PR and watch the live app redeploy. Open it on a phone. Hand it to someone non-technical with no instructions and note where they get confused. | 30 min |

✅ **Done when:** the live URL works end to end.
❓ "Step by step, what happens when you move a slider?" · "Why is there no strategy math inside `app.py`?"

#### Day 9: Experiments, or can we fool ourselves?

**Goal:** a genuine, honestly reported research finding.

💡 **Concept checkpoint (~40 min).** Overfitting: have 100 people each flip a coin ten times and someone will almost certainly get eight or more heads, but that doesn't make them a skilled flipper. Testing twenty parameter combinations and crowning the best one is the same thing. The defense is out-of-sample testing: tune on the first ~70% of the history, then test *once* on the untouched last ~30%, like practicing on past exams and then sitting a new one. If you peek at the test period and re-tune, it's no longer a test.

| Owner | Task | Time |
|---|---|---|
| 🟦 | Parameter sweep with nested loops (fast ∈ {5, 10, 20, 30, 50}, slow ∈ {50, 100, 150, 200}, skipping fast ≥ slow), computing Sharpe for each and showing the grid as a Plotly heatmap. Great loop practice with a striking visual. | 60 min |
| 🟦 | Out-of-sample test: the best in-sample settings vs. buy-and-hold on the held-out period, with a results table for both periods. | 45 min |
| 🟦 | Write the Findings section of the README: 5–8 sentences with real numbers. Whatever the result, honest reporting is what impresses; "the optimized strategy lost to buy-and-hold out of sample" is a great finding. | 45 min |
| 🟩 | Methodology review: did any test-period data leak into the tuning? Are warm-up days handled consistently in both periods? | 20 min |

✅ **Done when:** the heatmap, the in-sample/out-of-sample table and the written findings all exist.
❓ "Why can't you choose parameters using the test period?" · "If the best settings work on BTC but fail on ETH, what does that suggest?"

#### Day 10: Polish, ship, and tell the story

**Goal:** a portfolio-ready repo and a mentee who can present it with confidence.

| Owner | Task | Time |
|---|---|---|
| 🟦 | README, following the checklist in Section 11.1. | 60 min |
| 🟦 | Cleanup: a docstring on every public function, dead code deleted, Ruff clean, notebook tidied with headings and conclusions. | 30 min |
| 🟩 | Final review pass over the whole codebase. | 30 min |
| 🟦 | Create the `v1.0.0` GitHub release with short release notes. | 10 min |
| 🟨 | Mock interview: the two-minute pitch plus the questions in Section 11.3. | 30 min |
| 🟦 | Resume bullets (Section 11.2) and, optionally, a LinkedIn post with a GIF of the app. | 20 min |
| 🟩 + 🟦 | Retrospective: what went well, what was hard, what v2 looks like. | 15 min |

✅ **Done when:** the README checklist is complete, `v1.0.0` is released, and he has delivered the pitch once without notes.

**Weekend 2: buffer,** then stretch goals once everything above is merged.

---

## 8. Concept guide: your teaching notes

Use these notes for the 💡 checkpoints. Four habits make the concepts stick. Draw it on paper before any code exists. Use tiny examples of about five numbers that can be checked by hand; those same examples then become the unit tests. Ask him to predict the output before running anything, because a wrong prediction is the most teachable moment there is. And ask rather than tell: "what do you think happens to the average on day 3?" beats any explanation. The math never goes beyond school arithmetic. The only genuinely new idea is standard deviation, which you can introduce as "the typical distance from the average" and compute by hand once.

**These notes contain answers.** Reference code sits in collapsed blocks, so the plan can live in the repo without spoiling his tasks. Agree with him that he opens a block only after his own version passes the tests; at that point, comparing the two versions is a lesson in itself.

### 8.1 Returns and compounding (Day 3)

**The idea.** A return is "how much $1 grew today." Returns compound: they multiply rather than add, which is why +50% followed by −50% leaves you at 0.75, not 1.00. An equity curve is the running product, the value of $1 invested at the start.

**Formulas.** `r[t] = P[t] / P[t-1] - 1` and `E[t] = E[t-1] * (1 + r[t])`, starting from `E[0] = 1`.

**Test example.** Prices [100, 150, 75] → returns [0, 0.5, −0.5] → equity [1.0, 1.5, 0.75]. The first return is set to 0 rather than left empty, so the equity curve starts at exactly 1.

**Watch for.** Adding returns: 0.5 + (−0.5) = 0 says "break-even" when he actually lost 25%. Averaging them has the same flaw: +60% then −50% averages +5% a day, yet leaves him down 20%. Mixing percentages and fractions: keep fractions (0.05) everywhere in code and turn them into "5%" only when displaying them.

<details>
<summary>Reference solution (open after his own version passes)</summary>

```python
def daily_returns(close: pd.Series) -> pd.Series:
    return close.pct_change().fillna(0)


def equity_curve(returns: pd.Series) -> pd.Series:
    return (1 + returns).cumprod()
```

</details>

### 8.2 Moving averages: SMA and EMA (Day 4)

**The idea.** A simple moving average (SMA) is the average of the last N closes, recomputed as the window slides forward one day at a time. Every day inside the window counts equally, then drops out abruptly. An exponential moving average (EMA) has a fading memory: each day it moves a fixed fraction α of the way from yesterday's value toward today's price, so recent days count most and old days never quite disappear. That's why it reacts faster.

**Formulas.** SMA: the sum of the last N closes divided by N. EMA: `ema[t] = alpha * p[t] + (1 - alpha) * ema[t-1]`, with `alpha = 2 / (N + 1)`, starting from the first price.

**In pandas.** `close.rolling(window).mean()` and `close.ewm(span=span, adjust=False).mean()`, where `adjust=False` selects exactly the recursive formula above.

**Test examples.** SMA of [1, 2, 3, 4, 5] with window 3 → [NaN, NaN, 2, 3, 4]. EMA of [1, 2, 3] with span 3 (α = 0.5) → [1.0, 1.5, 2.25].

**Watch for.** Filling the warm-up NaNs with zeros: a moving average of 0 looks like a price crash and fires fake signals. `rolling(..., center=True)`, which centers the window on each day and therefore averages in future prices: lookahead bias in disguise. Also note that, unlike the SMA, this EMA has a value from day one because it starts from the first price, so its earliest values are rough. That's fine here, and worth one line in the docstring.

### 8.3 RSI (Day 4)

**The idea, in his language.** Of all the recent price movement, how much was upward? An RSI near 100 means almost all recent movement was up (what traders call overbought), near 0 almost all down, and 50 an even split. Let him explain overbought and oversold first; your only job is to turn his intuition into these steps:

1. Daily change: `delta[t] = P[t] - P[t-1]`.
2. Split it: the gain is the change on up days (otherwise 0), and the loss is the size of the change on down days (otherwise 0), so losses are positive numbers.
3. Smooth both with Wilder's average: an EMA whose α is 1/N rather than 2/(N + 1), with N = 14 by default.
4. `RS = average gain / average loss`.
5. `RSI = 100 - 100 / (1 + RS)`.

**Edge cases, which make the best tests.** Prices that only rise: the average loss is 0, so RS is infinite and RSI = 100. (pandas turns x / 0 into infinity and 100 / (1 + ∞) into 0, so this falls out without any special code.) Prices that only fall: RS = 0, so RSI = 0. Perfectly flat prices: 0 / 0 is NaN, which is genuinely undefined, so decide together whether to leave it NaN or show 50, and document the choice. With N = 14 the first 14 values are NaN, because the first difference uses up one day.

**A hand-checkable example (window 2).** Closes [10, 11, 12, 11, 12] → gains [–, 1, 1, 0, 1] and losses [–, 0, 0, 1, 0] → average gain [–, –, 1, 0.5, 0.75] and average loss [–, –, 0, 0.5, 0.25] → RSI [NaN, NaN, 100, 50, 75]. It's small enough to do on paper, it gives the same answer whether Wilder's average is seeded the pandas way or with a simple average, and it catches the most common RSI bug: smoothing with `span=window` instead of `alpha=1/window`, which produces a jumpier RSI that won't match any charting platform.

**Real-world check.** His values should closely match the RSI on his charting platform for the same exchange, pair and timeframe. Small differences come from how much history each side used to warm up the average, and they shrink as the history gets longer.

**Watch for.** The `span` mix-up above, and keeping losses as negative numbers, which makes RS negative and pushes RSI outside 0–100. The "always between 0 and 100" test catches that one.

<details>
<summary>Reference solution (open after his own version passes)</summary>

```python
def rsi(close: pd.Series, window: int = 14) -> pd.Series:
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)  # losses as positive numbers
    avg_gain = gain.ewm(alpha=1 / window, min_periods=window, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / window, min_periods=window, adjust=False).mean()
    rs = avg_gain / avg_loss  # x / 0 -> inf -> RSI 100;  0 / 0 -> NaN
    return 100 - 100 / (1 + rs)
```

</details>

### 8.4 Lookahead bias and the backtest engine (Day 6)

**The idea.** A backtest is a time machine with one rule: no peeking. A decision made from today's close can only earn *tomorrow's* return, because by the time today's candle has closed, today's move is already over. Trading on it anyway is like betting on a horse race after watching the replay. In code the entire safeguard is one `shift(1)`: the position decided on day t is the position *held* on day t + 1.

**The cheater example (on paper first).** Prices go 100 → 110 → 99 → 108.9 → 98.01, alternating +10% and −10%. A "cheater" strategy holds the coin on exactly the days that go up, which it can only know by looking at that same day's return, so its position is [0, 1, 0, 1, 0]. Without the shift it catches both +10% days and turns $1 into $1.21 (+21%). With the shift it's always one day late, catches both −10% days instead, and ends at $0.81 (−19%). That second number is the honest one.

**The three trap tests you write before the session** (fee = 0 in the first two):

1. **Hand-computed example.** Prices [100, 110, 121, 108.9, 108.9] and position [1, 1, 0, 0, 0] → equity [1.0, 1.1, 1.21, 1.21, 1.21]. Talk it through, counting from day 0: the decision to buy at day 0's close earns days 1 and 2, and the decision at day 2's close to go to cash avoids day 3's −10%.
2. **Cheater test.** The example above, asserting that the final equity is below 1.
3. **Fee test.** Flat prices [100, 100, 100, 100, 100], position [0, 1, 1, 0, 0] and a fee `f`: that's exactly one buy and one sell, so the final equity must equal `(1 - f) ** 2`.

**Watch for lookahead in disguise.** `shift(-1)`, which is tomorrow's value; `rolling(..., center=True)`; back-filling missing values with `bfill()`, which copies future values into the past; scaling or normalizing with statistics of the whole history (for example "RSI above its all-time average" quietly uses the future); using the still-forming last candle, which is why Day 2 drops it; and choosing parameters on the same period you report (Section 8.9).

**The honest limitation.** The engine assumes every trade happens exactly at the signal day's close. In reality he'd get a slightly different price a moment later (slippage). Setting the fee a little higher is a crude allowance for this, and it belongs in the README's limitations.

<details>
<summary>Reference solution (open after the pairing session)</summary>

```python
def run_backtest(df: pd.DataFrame, position: pd.Series, fee: float = 0.001) -> pd.DataFrame:
    asset_return = df["close"].pct_change().fillna(0)  # what holding the coin earned each day
    held = position.shift(1).fillna(0)  # decided at yesterday's close, held today
    trade = held.diff().abs().fillna(0)  # 1 on each day the holding changes
    strategy_return = held * asset_return - trade * fee  # earnings minus fees
    equity = (1 + strategy_return).cumprod()  # value of $1 over time
    return pd.DataFrame(
        {
            "position_held": held,
            "asset_return": asset_return,
            "trade": trade,
            "strategy_return": strategy_return,
            "equity": equity,
        }
    )
```

Subtracting the fee on the first day of each new holding, rather than multiplying by `1 - fee`, ignores a tiny fee × return cross term (a fraction of a basis point per trade) in exchange for test math that stays clean.

</details>

### 8.5 Fees and turnover (Days 6–7)

**The idea.** Every change of position costs a percentage of the capital traded, and a round trip (buy, then sell) pays twice. Fees are charged whether a trade wins or loses, which makes them the one cost a strategy can never avoid.

**Rule of thumb.** Yearly fee drag ≈ round trips per year × 2 × fee, as long as that product is small. For bigger numbers, compound it: the fraction of capital left is `(1 - fee) ** (2 * round_trips)`. Ten round trips a year at 0.25% per side cost about 5%. A hundred round trips mean 200 payments, and 0.9975²⁰⁰ ≈ 0.61, so roughly 40% of the capital is gone before the strategy has earned anything. The lesson: frequent trading needs a big edge.

**Make it real.** Have him look up the fee schedule of the exchange he actually uses and make it the dashboard's default fee. The function default of 0.1% sits at the cheap end of retail fees.

**Counting trades.** Decide with him whether `count_trades` counts every buy and every sell (which matches how fees are charged) or round trips (which is how traders usually talk), and write the answer into the docstring. Either is defensible; being vague isn't. Time in market is simply the average of the `position_held` column: the fraction of days spent holding the coin.

### 8.6 Volatility and the Sharpe ratio (Day 7)

**The idea.** Volatility is how bumpy the ride is: the standard deviation of daily returns, or "the typical distance from the average." Do one by hand: returns of +1%, −1%, +1%, −1% average 0%, and each sits 1% away from that average, so daily volatility is about 1%. The Sharpe ratio is return per unit of bumpiness: of two strategies with the same return, the smoother one scores higher.

**Formulas.** `annual_volatility = daily_std * sqrt(365)` and `sharpe = daily_mean / daily_std * sqrt(365)`, with a risk-free rate of 0 (state that assumption in the README). Why 365? Crypto trades every day of the year. Why a square root at all? Ups and downs partly cancel out over time, so risk grows more slowly than time does, with its square root. For a beginner, "accept it for now" is a perfectly good answer.

**Reading a Sharpe ratio.** Below 0, the strategy lost money. Around 1 is respectable for a real strategy. A simple daily strategy showing 3 or more in a backtest is far more likely to be a bug or overfitting than genius.

**Watch for.** Using √252, which is for stock markets (about 252 trading days a year) and shrinks both numbers for crypto. The pandas/NumPy split: pandas' `Series.std()` divides by n − 1 while NumPy's `np.std()` divides by n, so on the ±1% example NumPy gives exactly 1.00% and pandas about 1.15%. That matters in four-number tests and not at all on 700 days, so use pandas everywhere and compute test expectations the same way. Comparing Sharpe ratios across different periods: market conditions dominate, so only compare strategies over the same dates, which is why the dashboard always shows buy-and-hold alongside. And the never-trades edge case: every return is 0, the standard deviation is 0, and the formula divides by zero. Decide what to return (NaN, displayed as "n/a", is the honest choice) and test it.

### 8.7 Max drawdown (Day 7)

**The idea.** The worst fall from a previous peak: the pain he'd have had to sit through without selling. Traders feel drawdowns far more than they feel volatility. A fact worth sharing: after a −50% drawdown, it takes +100% just to get back to even.

**Formula.** Running peak = the highest equity so far; drawdown = equity / running peak − 1; max drawdown = the most negative drawdown. The dashboard's underwater chart is simply the drawdown plotted over time.

**Test example.** Equity [1.0, 1.2, 0.9, 1.1, 0.6, 1.3] → running peak [1.0, 1.2, 1.2, 1.2, 1.2, 1.3] → drawdowns [0, 0, −25%, −8.3%, −50%, 0] → max drawdown −50%.

**Watch for.** Using the overall minimum and maximum (min / max − 1), which ignores the order of events: on a curve that only rises, such as [1, 2, 3], it reports −67% when the true drawdown is 0. Sign conventions: keep drawdowns negative in code and display them as "−50%".

### 8.8 CAGR (Day 7)

**The idea.** The steady yearly growth rate that would take the starting equity to the ending equity. In other words: what yearly interest rate would a savings account have needed to match this?

**Formula.** `CAGR = (E_end / E_start) ** (365 / n) - 1`, where n is the number of daily returns, which is `len(equity) - 1`.

**Test example.** Doubling over 730 daily periods gives 2^½ − 1 = √2 − 1 ≈ 41.42% a year, not 50%, because 1.4142 × 1.4142 = 2. Ask him to explain why before you reveal it.

**Watch for.** The off-by-one: n counts the steps between days, not the days themselves, and the Day 7 test is precise enough to catch it (dividing by 731 gives 41.35%). Annualizing short periods: a +20% month annualizes to roughly +800%, so have the dashboard show CAGR only when the selected range covers at least a year, and total return otherwise.

<details>
<summary>Reference solutions for 8.6–8.8 (open after his own versions pass)</summary>

```python
import math


def annual_volatility(returns: pd.Series, periods_per_year: int = 365) -> float:
    return returns.std() * math.sqrt(periods_per_year)


def sharpe_ratio(returns: pd.Series, periods_per_year: int = 365) -> float:
    sd = returns.std()
    if pd.isna(sd) or sd == 0:  # never traded, or too little data
        return float("nan")
    return returns.mean() / sd * math.sqrt(periods_per_year)


def max_drawdown(equity: pd.Series) -> float:
    return (equity / equity.cummax() - 1).min()


def cagr(equity: pd.Series, periods_per_year: int = 365) -> float:
    n = len(equity) - 1  # number of daily steps, not days
    return (equity.iloc[-1] / equity.iloc[0]) ** (periods_per_year / n) - 1
```

</details>

### 8.9 Overfitting and out-of-sample testing (Day 9)

**The idea.** If 100 people each flip a coin ten times, someone will almost certainly get eight or more heads (the odds are better than 99%), and it says nothing about their skill. A parameter sweep is the same game: try about twenty settings and the best one will look skilled partly by luck. The only cure is to test the chosen settings on data that played no part in choosing them.

**The procedure.** Split by time, never randomly, because shuffling days would leak the future into the past. Tune on the first ~70% of the history, then run the winner *once* on the last ~30%. Compute indicators and positions on the full history (they only look backward, so this isn't leakage, and it avoids a second warm-up gap at the start of the test period), then score each period separately by re-compounding its daily strategy returns from $1. Score like with like: every cell of the sweep and the buy-and-hold benchmark must be measured over the same dates. Otherwise a 200-day average, which sits in cash while it warms up, is judged on a different stretch of market than a 50-day one. The simplest rule is to start scoring after the longest warm-up in the grid. Report how many combinations he tried alongside the winner, since readers can only judge the role of luck if they know how many draws there were.

**Reading the heatmap.** A broad plateau of similar colors around the best cell is encouraging, because the result doesn't hinge on one exact setting. A lone bright cell among dark neighbors is a lucky spike.

**Watch for.** Re-running the out-of-sample test after tweaking anything: at that point the test period has become training data, and only a new, untouched period can serve as a test again. Picking the split date after seeing the results. And over-claiming: with roughly 720 daily candles, the test period is about seven months of a single market mood, and a 200-day average spends a big share of the training window warming up. The finding is suggestive, not proof, and the README should say exactly that. (It's also the best argument for the deeper-history stretch goal.)

---

## 9. Workflow and code review

**Branches and pull requests.** One branch per task, named by type: `feat/rsi`, `fix/nan-warmup`, `docs/findings`. Keep PRs small, under about 200 changed lines, so they get reviewed the same day; huge PRs get skimmed and rubber-stamped. Write commit messages in the imperative, like an instruction to the codebase: "Add RSI with Wilder smoothing", not "stuff" or "fixed things". Put "Closes #12" in the PR description so that merging closes the Issue and the board moves its card to Done. Use *Squash and merge*, so `main` reads as one clear commit per PR.

**Definition of Done.** A task is done when its code and tests are merged through a reviewed PR, CI is green, public functions have docstrings, and he can explain every line. "It works on my machine" is not done.

**When CI goes red.** Read the log from the bottom up, find the first real error, reproduce it locally with the same `uv run` command, fix it and push again. Treat each red build as a free lesson rather than a failure; this is exactly what the job looks like day to day.

**Reviewing his PRs.** Review the same day, because momentum matters more than thoroughness. Limit yourself to 3–5 comments: twenty comments crush a beginner, so save the rest for the Day 10 final pass. Priorities, in order: correctness, then clarity, then naming. Style belongs to Ruff, so never spend a comment on it. Prefix every comment so he knows what's blocking: `must:` (fix before merging), `q:` (explain this to me, often the most valuable kind) and `nit:` (optional polish). End each review with one specific piece of praise, such as "this test name reads like a sentence." Specific praise teaches; generic praise doesn't.

**His reviews of your PRs.** He checks out your branch, runs the tests, leaves at least one `q:`, and approves only once he can explain the change. Reading code he didn't write, and questioning a more experienced developer's choices, is a skill most juniors have to be pushed into, so push.

---

## 10. Risks and how to handle them

| Risk | Prevention | If it happens anyway |
|---|---|---|
| Setup problems eat Day 1 | Dry-run the setup on Day 0 on his operating system. uv installs Python itself, which sidesteps most PATH trouble. | Move him to a GitHub Codespace (VS Code in the browser, with free monthly hours for personal accounts) and fix the laptop later. The project doesn't wait on it. |
| The exchange API is down, rate-limited or blocked | Everything is cached, tests never touch the network, the exchange is one setting, and the sample fixture is committed. | The app falls back to cached data or the fixture with a visible notice. Switch `exchange_id`, for example to `coinbaseexchange`. |
| He falls behind | The Day 5 retro compares progress with the plan and makes cuts during Week 1, not on Day 9. | Cut in this order: stretch goals → the heatmap (a small table of a few settings is enough) → SQLite (cache to a CSV file instead) → ETH (BTC only) → the drawdown chart. Never cut the tests, the lookahead safeguards, the fees or the honest findings; they are the project's credibility. |
| You over-help | The owner tags, the hint ladder and the keyboard rule. | If you catch yourself having solved a 🟦 task, turn it into an exercise: he re-implements it from the tests without looking at your version. |
| AI-written code he can't explain | "Tutor, not ghostwriter," plus the disclosure line in the PR template. | The explain-back fails, so the PR doesn't merge until he rewrites the part he can't explain. Keep it matter-of-fact rather than a telling-off. |
| Results look too good | The maxim "amazing means bug until proven otherwise," backed by the trap tests. | Check the shift, the fees, the NaN handling and the dates; recompute a few days by hand; confirm the benchmark covers exactly the same dates. |
| Motivation dips on Days 6–7, the densest days | A live URL from Day 1 and a board full of Done cards keep progress visible. | Shrink the day's goal to one small merged PR, and remind him of the finding he's heading toward. |
| Scope creep ("let's add a live bot, ML, more coins") | The MVP list in Section 2 is the contract. | Put the idea into a "v2 ideas" Issue and move on. It becomes his answer to "what would you build next?" |
| The live app is asleep when a recruiter clicks | Free Community Cloud apps go to sleep after a stretch without visitors, so the README's screenshot or GIF has to tell the story on its own. | Open the app shortly before any interview or demo so that it's awake. |

---

## 11. The finish line: README, resume, interview

### 11.1 README checklist

| Section | What it contains |
|---|---|
| Title and one-line pitch | For example: "Backtest crypto trading strategies with realistic fees and no peeking at the future." |
| Live link and badges | The Streamlit URL at the very top, plus the CI status badge. |
| Screenshot or GIF | The dashboard in action. Many visitors look only at this, and it still works when the app is asleep. |
| Features | The MVP list, written for a user rather than a developer. |
| How it works | The architecture diagram from Section 5 and the position-series contract, in three or four sentences. |
| Tech stack | One line per tool with the reason for it (a condensed Section 3). |
| Run it locally | After installing uv: `git clone <repo-url>`, `cd hindsight`, `uv run streamlit run app.py` (uv installs everything on the first run), plus `uv run pytest` for the tests. |
| Findings | The Day 9 write-up with real numbers, and the heatmap image. |
| Limitations | Trades at the signal day's close; no slippage model; long-only; about two years of daily data from one exchange; a risk-free rate of 0; results specific to the period tested. |
| Disclaimer | An educational project, not financial advice. |
| Authors and acknowledgements | Him as the author, and you credited as his mentor. |

### 11.2 Resume bullets

Templates only: replace every placeholder with real numbers from the repo.

> **Hindsight: Crypto Strategy Backtester** · Python, pandas, SQL, Streamlit, pytest, GitHub Actions · [Live demo] · [GitHub]
>
> - Built and deployed an interactive web app that backtests crypto trading strategies on [N] years of daily BTC and ETH data, pulled through the CCXT exchange API and cached in SQLite.
> - Implemented technical indicators (EMA, RSI) and performance metrics (CAGR, volatility, Sharpe ratio, max drawdown) from first principles in pandas, covered by [N] unit tests that run in CI on every pull request.
> - Co-developed a fee-aware backtest engine with regression tests proving that a strategy peeking at same-day prices cannot profit, guarding against lookahead bias.
> - Ran a [N]-combination parameter sweep with out-of-sample validation: the best in-sample strategy returned [X%] vs. [Y%] for buy-and-hold on unseen data, documented with its limitations in the README.

**An honesty note.** Every bullet must survive "tell me more about that." In interviews he should say plainly that the project was mentored and be specific about who built what; the ownership matrix in Section 4 makes that easy. Mentorship is a positive signal, since it shows he seeks feedback and can work inside a real review process. Overclaiming is the one thing that can turn this project from an asset into a liability.

### 11.3 The two-minute pitch and practice questions

**The pitch**, practiced until it fits in two minutes with the live app open: the problem in one sentence (most strategies shared online are tested in ways that quietly cheat); a 30-second demo; one technical decision he's proud of (the one-line shift, and the test that proves it matters); the honest finding; and what he'd build next. Recording it once on his phone and watching it back is uncomfortable and very effective.

| Question | A strong answer covers |
|---|---|
| "Walk me through what happens when I move this slider." | Streamlit reruns the script; the data comes from the cache; the strategy function returns positions; the backtest and metrics run; the charts redraw. No strategy math lives in `app.py`. |
| "What is lookahead bias, and how do you know your backtest doesn't have it?" | A decision at today's close can only earn tomorrow's return; the `shift(1)`; the cheater test, which he watched fail when he deleted the shift on Day 6. |
| "How do you know your RSI is correct?" | The hand-checked example, the property tests (rising → 100, falling → 0, always within bounds), and the comparison with a charting platform, including why small differences remain. |
| "Why Streamlit, pandas and SQLite? What would change with 10,000 users?" | Each is the simplest tool that fits a small Python data app. At scale the bottleneck is the exchange API, so data would be fetched on a schedule into a shared database such as PostgreSQL rather than per visitor, and popular backtests could be cached or precomputed. |
| "What are the limitations of your results?" | The README's list, offered without prompting. He should sound like a skeptic of his own work. |
| "How would you turn this into a paper-trading bot?" | A scheduled job fetches the latest closed candle, calls the same strategy function, compares the new position with the current one, and logs a simulated order and its P&L. The strategy code is reused unchanged, which is the payoff of the position-series contract. Real trading would add API keys, order handling and failure recovery. |
| "What was the hardest bug you fixed?" | A real story from his learning log: the symptom, how he narrowed it down, the fix, and the test he added so it can't come back. |

---

## Appendix A: Config snippets and everyday commands

**`pyproject.toml` additions** (uv writes the `[project]` section itself):

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]             # lets tests import the hindsight package

[tool.ruff]
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "I", "B"]  # pycodestyle errors, Pyflakes, import sorting, bugbear
ignore = ["E501"]              # leave line length to the formatter
```

**`.github/workflows/ci.yml`:**

```yaml
name: CI

on:
  pull_request:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      # From v8 on, setup-uv publishes exact version tags only (there is no @v8)
      - uses: astral-sh/setup-uv@v8.1.0
      - run: uv sync --locked  # fails if uv.lock is out of date with pyproject.toml
      - run: uv run ruff check .
      - run: uv run ruff format --check .
      - run: uv run pytest -q
```

When you set this up on Day 0, check both actions' release pages and use their newest versions.

**Everyday commands:**

```bash
uv sync                        # install exactly what uv.lock specifies
uv add <package>               # add a dependency; commit pyproject.toml and uv.lock together
uv run pytest                  # run the tests
uv run ruff check --fix .      # lint, auto-fixing what it can
uv run ruff format .           # format the code
uv run streamlit run app.py    # start the app locally

git switch main                # start every task from an up-to-date main
git pull
git switch -c feat/rsi         # a new branch for the task
git add -A
git commit -m "Add RSI with Wilder smoothing"
git push -u origin feat/rsi    # then open the pull request on GitHub
```

The commands are one per line on purpose: Windows PowerShell 5.1, still the default shell on many Windows machines, doesn't support chaining commands with `&&`.

---

## Appendix B: Pull request template

Save this as `.github/pull_request_template.md`, and GitHub will pre-fill every new PR with it.

```markdown
## What does this PR do?
<!-- One or two sentences. Link the Issue: "Closes #12" -->

## How did you test it?
<!-- Tests added or unlocked, plus anything you checked by hand -->

## Screenshot
<!-- For anything visible in the app or a chart; delete if not relevant -->

## Checklist
- [ ] I can explain every line in this PR
- [ ] Tests pass locally (`uv run pytest`)
- [ ] Ruff is clean (`uv run ruff check .` and `uv run ruff format --check .`)
- [ ] New public functions have docstrings

## AI help used?
<!-- "None", or what you asked and how you used the answer -->

## Learning log
<!-- What I learned · What confused me · A bug I fixed -->
```

---

*Adapt this plan freely. If the schedule and the learning ever conflict, the learning wins.*
