# Recipe: a money engine (bank statements)

Give this file to the agent: "Build the money engine from prompts/recipes/money.md." It builds the engine
in this folder, for your accounts.

## What you get

"What did I spend on food this month?" "Can I afford the trip?" answered from your real transactions,
reconciled to the cent against your bank's own statements, with a receipt saying which statement the
numbers run through.

## What you need

Statements from each account you want tracked: CSV exports where the bank offers them, PDFs where it
doesn't. A couple of months each to start.

## The rules (why it works)

1. **Reconcile to the cent.** For each statement, the parsed transactions must add up to the statement's
   own opening and closing balance. If they don't, the import stops and says so. A ledger that is off by
   $3 cannot be trusted for anything, because you can't tell where else it is wrong.
2. **No AI in the math.** Parsing, totals, and categories are deterministic code. The agent proposes a
   category for a new merchant; you confirm it once; it becomes a rule in `config/finance/rules.yaml`
   (merchant pattern → category) and the code applies it from then on.
3. **Facts vs advice.** Spending by category, month over month, is a fact. "Cut back on takeout" is
   advice, written separately and labelled.
4. **Raw statements never reach git.** They go in `private/imports/`. Never put a full account number in
   any tracked file; use the last four digits at most.
5. **Visible staleness.** The summary says how old the newest transaction is, so a month-old ledger never
   reads as current.
6. **Casual mentions stay in `daily/`.** "Bought shoes for 120" in chat goes to the daily note, not the
   ledger. The ledger is fed by statements only.

## Build steps (for the agent)

1. Ask which accounts, and have the user drop one statement per account into `private/imports/`.
2. Write one parser per bank, each recognizing its file by content, not filename. Each transaction:
   date, account, amount, description, merchant, category, and an id that survives re-imports.
3. Write `scripts/reconcile.py`: parse everything in `private/imports/`, check each statement ties to the
   cent, apply the category rules, and write the ledger to `private/ledger/` (or to `data/finance/` if you
   decide to commit it to a private repo). Unknown merchants go to an "Uncategorized" queue it prints.
4. Write `scripts/spending.py`: spend by category for a month, change from last month, top merchants, and
   the date of the newest transaction.
5. Create `wiki/domains/money.md` (accounts by nickname, rules, gotchas) and link it from
   `wiki/domains/index.md`.

## Check before trusting it

Every statement ties to the cent. Then pick five transactions at random and find each one on the bank's
website.
