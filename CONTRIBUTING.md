# Contributing to Continuum

## Pre-Commit Hooks (Local CI Runners)

This project uses **pre-commit** to automatically run code quality checks before each commit. This ensures that all code meets quality standards before it reaches the repository, catching issues locally before they hit GitHub Actions.

### Quick Setup

Run the setup script from the project root:

```bash
./setup-hooks.sh
```

This will:
- Install backend Python dependencies (including pylint, mypy, black, isort)
- Install frontend npm dependencies
- Configure Git pre-commit and pre-push hooks

### Manual Setup

If you prefer to set things up manually:

```bash
# 1. Set up backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Set up frontend
cd ../continuum-frontend
npm install

# 3. Install pre-commit hooks
cd ..
source backend/venv/bin/activate
pre-commit install
pre-commit install --hook-type pre-push
```

---

## What Happens on Commit

When you run `git commit`, the following checks run automatically:

### General Checks
| Check | Description |
|-------|-------------|
| Trailing whitespace | Removes trailing whitespace |
| End of file fixer | Ensures files end with a newline |
| YAML/JSON validation | Validates YAML and JSON syntax |
| Large file check | Blocks files > 1MB |
| Merge conflict check | Detects merge conflict markers |
| Private key detection | Prevents committing secrets |

### Backend Checks (Python)
| Check | Description |
|-------|-------------|
| **Black** | Auto-formats Python code |
| **isort** | Sorts and organizes imports |
| **Pylint** | Static code analysis for bugs and style issues |
| **Mypy** | Static type checking |
| **pytest** | Runs the test suite |

### Frontend Checks (TypeScript/React)
| Check | Description |
|-------|-------------|
| **TypeScript** | Type checking via `tsc --noEmit` |
| **ESLint** | Linting for TypeScript/React |

### On Push Only
| Check | Description |
|-------|-------------|
| **Frontend Build** | Verifies the frontend builds successfully |

---

## Running Hooks Manually

```bash
# Run all hooks on all files
pre-commit run --all-files

# Run a specific hook
pre-commit run backend-pylint --all-files
pre-commit run frontend-typecheck --all-files

# Run hooks on staged files only
pre-commit run
```

### Available Hook IDs

| Hook ID | Description |
|---------|-------------|
| `backend-pylint` | Python linting |
| `backend-mypy` | Python type checking |
| `backend-tests` | Python tests (pytest) |
| `frontend-typecheck` | TypeScript type checking |
| `frontend-lint` | ESLint |
| `frontend-build` | Build verification |
| `black` | Python formatting |
| `isort` | Python import sorting |

---

## Fixing Common Issues

### Backend (Python)

```bash
cd backend
source venv/bin/activate

# See all pylint issues
pylint app --rcfile=.pylintrc

# Auto-format code with Black
black app --line-length=100

# Sort imports
isort app --profile=black --line-length=100

# Run type checker
mypy app --ignore-missing-imports

# Run tests
pytest tests -v
```

### Frontend (TypeScript/React)

```bash
cd continuum-frontend

# See all lint errors
npm run lint

# Auto-fix what can be fixed
npm run lint:fix

# Check TypeScript errors
npm run typecheck

# Test build
npm run build
```

---

## Common Errors and Solutions

### Python

| Error | Solution |
|-------|----------|
| Pylint: `line-too-long` | Break line or use Black to format |
| Mypy: `Missing type hints` | Add type annotations |
| Import error | Check virtual environment is activated |

### TypeScript/React

| Error | Solution |
|-------|----------|
| `no-unused-vars` | Remove or use the variable |
| `no-explicit-any` | Replace `any` with a proper type |
| `react-hooks/exhaustive-deps` | Add missing dependencies to the array |

---

## Bypassing Hooks (Emergency Only)

In rare cases where you need to commit without running hooks:

```bash
git commit --no-verify -m "your message"
```

⚠️ **Use sparingly** — this defeats the purpose of code quality checks. CI will still run on GitHub and block merging if checks fail.

---

## Troubleshooting

### "pre-commit: command not found"

Ensure you've activated the backend virtual environment:

```bash
source backend/venv/bin/activate
```

### Hooks not running

Re-install the hooks:

```bash
source backend/venv/bin/activate
pre-commit install
pre-commit install --hook-type pre-push
```

### Backend tests failing

Make sure you have the test database set up:

```bash
cd backend
source venv/bin/activate
pytest tests -v --tb=long
```

### Frontend npm errors

Re-install dependencies:

```bash
cd continuum-frontend
rm -rf node_modules
npm install
```

---

## Available Scripts

### Backend (`backend/`)

| Script | Description |
|--------|-------------|
| `pytest tests` | Run test suite |
| `pylint app` | Run linter |
| `mypy app` | Run type checker |
| `black app` | Format code |
| `alembic upgrade head` | Run database migrations |

### Frontend (`continuum-frontend/`)

| Script | Description |
|--------|-------------|
| `npm run dev` | Start development server |
| `npm run build` | Build for production |
| `npm run lint` | Run ESLint |
| `npm run lint:fix` | Run ESLint with auto-fix |
| `npm run typecheck` | Run TypeScript type checking |
| `npm run preview` | Preview production build |
