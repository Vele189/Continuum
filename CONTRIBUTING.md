# Contributing to Continuum Frontend

## Pre-Commit Hooks

This project uses **Husky** and **lint-staged** to automatically run code quality checks before each commit. This ensures consistent code quality across the team.

### Setup

After cloning the repository, run the following from the **project root** (not the frontend folder):

```bash
cd Continuum
npm install
```

This installs Husky and configures the Git hooks automatically.

> **Note:** You also need to install frontend dependencies:
> ```bash
> cd continuum-frontend
> npm install
> ```

### What Happens on Commit

When you run `git commit`, the pre-commit hook automatically:

1. **Runs ESLint** on all staged `.ts` and `.tsx` files in `continuum-frontend/src/`
2. **Auto-fixes** any fixable issues (formatting, simple lint errors)
3. **Blocks the commit** if there are unfixable errors

Example output when commit is blocked:

```
✖ eslint --fix:
  /src/components/Button.tsx
    5:10  error  'unused' is defined but never used  @typescript-eslint/no-unused-vars
```

### Fixing Lint Errors

If your commit is blocked, fix the reported errors and try again:

```bash
# See all lint errors in the frontend
cd continuum-frontend
npm run lint

# Auto-fix what can be fixed
npm run lint:fix

# Check TypeScript errors
npm run typecheck
```

### Common ESLint Errors

| Error | Solution |
|-------|----------|
| `no-unused-vars` | Remove or use the variable |
| `no-explicit-any` | Replace `any` with a proper type |
| `react-hooks/exhaustive-deps` | Add missing dependencies to the array |

### Bypassing Hooks (Emergency Only)

In rare cases where you need to commit without running hooks:

```bash
git commit --no-verify -m "your message"
```

⚠️ **Use sparingly** — this defeats the purpose of code quality checks.

### Troubleshooting

#### "lint-staged not found" or npm errors

Re-run installation from the project root:

```bash
cd Continuum
rm -rf node_modules
npm install
```

#### Hooks not running at all

Ensure Husky is installed:

```bash
cd Continuum
npx husky install
```

#### WSL/Windows path issues

The hooks are configured to work with both Windows and WSL. If you encounter issues, try committing from PowerShell or Git Bash instead of WSL.

---

## Available Scripts

From `continuum-frontend/`:

| Script | Description |
|--------|-------------|
| `npm run dev` | Start development server |
| `npm run build` | Build for production |
| `npm run lint` | Run ESLint |
| `npm run lint:fix` | Run ESLint with auto-fix |
| `npm run typecheck` | Run TypeScript type checking |
| `npm run preview` | Preview production build |

