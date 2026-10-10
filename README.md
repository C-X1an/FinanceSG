# FinanceSG

A legacy Flask learning prototype for Singapore budgeting and cost-estimation forms.

**Current status:** local registration/login and the budget percentage demonstration work. Salary/CPF, vehicle, property and university POST calculations return HTTP 501 with an explanation: their original formulas contain runtime errors or outdated assumptions and need independent validation before use. The forms remain available to inspect the original interface. No financial estimate is produced or stored by the paused endpoints.

## Run locally

Use Python 3.12 and fictional input only:

```sh
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python init_db.py
python -m flask --app app run
```

The initializer creates an empty `users` table and refuses to overwrite existing files. Register a fictional local account through the app. Set `FINANCESG_DATABASE` to use a different database path, `FINANCESG_SESSION_DIR` to choose session storage, and `FINANCESG_SECRET_KEY` for a stable local secret. The default generated secret changes on restart. Database and session files are ignored by Git.

## Correctness boundaries

- The legacy CPF code used a $6,800 Ordinary Wage ceiling; the [official 2026 CPF rates](https://www.cpf.gov.sg/content/dam/web/employer/employer-obligations/documents/CPFcontributionratesfrom1Jan2026.pdf) specify $8,000. Use the [current CPF calculator](https://www.cpf.gov.sg/member/tools-and-services/calculators/cpf-contribution-calculator).
- Vehicle code contained fixed COE amounts and incorrect arithmetic. Consult [LTA's current tax structure](https://onemotoring.lta.gov.sg/content/onemotoring/home/buying/upfront-vehicle-costs/tax-structure.html); this prototype has not implemented it.
- Property and university calculations have unresolved formula and input-conversion errors. Their old implementations remain in source for review, guarded from execution.
- Budget percentages are arithmetic on user input. The original comparison thresholds are legacy heuristics with no validated advisory basis; they are not recommendations.

This app needs CSRF protection, rate limits, comprehensive validation and secure deployment work before any public service. Do not enter real financial or account data. No license has been declared; public visibility alone is not a reuse license.

## Verify

```sh
python -m pip install -r requirements-dev.txt
python -m pytest -q
python -m pip_audit -r requirements.txt
```

Tests initialize temporary databases, exercise registration/login and budget input validation, and verify that legacy financial endpoints cannot emit misleading results. No external financial services are called.
