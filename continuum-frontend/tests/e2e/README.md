# E2E Testing with Playwright

End-to-end tests for the authentication flow using **Playwright**.
All tests use **mocked API responses** for frontend-only testing.

---

## Prerequisites

* Node.js **18+**
* npm or yarn
* Dev server running on **[http://localhost:5173](http://localhost:5173)**

---

## Setup

> **Important:** All commands below must be run from the following directory:
>
> `Continuum\continuum-frontend>`

### 1. Install Dependencies

```bash
npm install
```

### 2. Install Playwright Browsers

```bash
npx playwright install
```

---

## Running Tests

### Start Frontend Server (Required)

**Terminal 1:**

```bash
npm run dev
```

Wait for the server to start before running tests.

---

### Run Tests(Different ways to run tests)

**Terminal 2:**

#### Run all auth tests

```bash
npx playwright test
```

#### Run specific test file

```bash
npx playwright test auth-login
npx playwright test auth-register
npx playwright test auth-forgot-password
npx playwright test auth-reset-password
```

#### Run with UI mode (recommended for development)

```bash
npx playwright test --ui
```

#### Run in headed mode (see browser)

```bash
npx playwright test --headed
```

#### Run specific test by name

```bash
npx playwright test -g "should validate empty email"
```

---

## Debug mode

```bash
npx playwright test --debug
```

---

## If you encounter issues:

* Check `test-results/` for screenshots
* Run the Playwright report:

```bash
npx playwright show-report
```

* Use the `--debug` flag to step through tests
* Review test logs in the console output
