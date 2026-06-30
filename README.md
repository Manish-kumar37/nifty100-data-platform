# Sprint 1 - Day 1
## Environment Setup

### Objective
Set up the development environment and project structure for the NIFTY 100 Data Platform.

---

## Tasks Completed

### Project Structure

Created the initial project directories:

```text
nifty100-project/
│
├── data/
│   └── raw/
│
├── src/
│   └── etl/
│
├── db/
│
├── tests/
│   └── etl/
│
├── output/
│
├── notebooks/
│
└── docs/
```

---

### Virtual Environment

Created and activated a Python virtual environment.

```bash
python -m venv venv
```

Activation:

```bash
venv\Scripts\activate
```

---

### Dependencies Installed

Core libraries installed:

```bash
pip install pandas
pip install openpyxl
pip install numpy
pip install pytest
pip install sqlalchemy
```

Additional utilities:

- pathlib
- sqlite3
- os
- logging

---

### Configuration

Created:

```text
.env
.gitignore
requirements.txt
```

---

### Git Setup

Initialized local Git repository.

```bash
git init
```

Configured:

```bash
git config --global user.name "<your-name>"
git config --global user.email "<your-email>"
```

---

### Database Planning

Defined initial database architecture:

- Companies
- Profit & Loss
- Balance Sheet
- Cash Flow
- Analysis
- Documents
- Pros & Cons
- Sectors
- Peer Groups
- Financial Ratios
- Stock Prices

---

## Deliverables

- Project structure created
- Virtual environment configured
- Required libraries installed
- Git initialized
- Configuration files created
- Database design finalized

---

## Outcome

Environment successfully prepared for ETL development and database implementation.

Sprint Status:

✅ Day 1 Completed