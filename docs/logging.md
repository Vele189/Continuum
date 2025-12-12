# Logging Guide

This document describes the project's logging setup and how to use the helper logger in `backend/utils`.

## Files
- `backend/utils/logger.py` — central logging configuration and `get_logger(name: str)` helper.
- `backend/utils/test_logger.py` — small FastAPI demo and a test/demo function that shows usage.

## Importing the Logger
Use the helper function provided by the project to obtain a consistent, named logger:

```python
from backend.utils.logger import get_logger
logger = get_logger(__name__)
```

(If you are running a script from inside `backend/utils` directly, `import logger` will also work as in the demo; however the explicit import above is preferred for clarity.)

## Overview
- Purpose: `logger.py` calls `logging.basicConfig(...)` once to set a consistent format and level across the backend and exposes `get_logger(name)` so modules can obtain a named logger.
- Benefit: consistent timestamps, message format, and easy per-module filtering.

## API
- `get_logger(name: str)` — returns a `logging.Logger` instance configured with the project's global settings.
- Use the returned logger exactly like a standard Python logger:
  - `logger.debug(...)`, `logger.info(...)`, `logger.warning(...)`, `logger.error(...)`, `logger.exception(...)`, `logger.critical(...)`.

## Quick Usage
- Typical import pattern (recommended):

```python
from backend.utils.logger import get_logger
logger = get_logger(__name__)

logger.info("Starting up")
```

## Example (module)
```python
from backend.utils.logger import get_logger

logger = get_logger(__name__)

def do_work():
    logger.info("Starting work")
    try:
        # do something
        pass
    except Exception:
        logger.exception("Work failed")
```

## FastAPI integration / demo
`backend/utils/test_logger.py` demonstrates using the logger in a FastAPI app:
- It creates a logger, logs environment and port info, logs requests to the root endpoint, and provides a `test_logging()` demo call.

To run the demo with Uvicorn:

```bash
python3 backend/utils/test_logger.py
# or
uvicorn backend.utils.test_logger:app --reload --host 0.0.0.0 --port 8000
```

You can set environment variables when running the demo:

```bash
ENV=production PORT=8080 python3 backend/utils/test_logger.py
```

## Default Configuration
The default settings configured in `backend/utils/logger.py` are:
- Level: `INFO`
- Format: `%(levelname)s | %(asctime)s | [%(name)s] %(message)s`
- Date format: `%Y-%m-%d %H:%M:%S`

Notes:
- `logging.basicConfig(...)` configures the root logger only once; subsequent calls usually have no effect if handlers are already set.

## Changing behaviour (handlers / level / files)
- Change root level at runtime:

```python
import logging
logging.getLogger().setLevel(logging.DEBUG)
```

- Add a file handler (example):

```python
import logging
from backend.utils.logger import get_logger

root = logging.getLogger()
fh = logging.FileHandler("app.log")
fh.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)s | %(asctime)s | [%(name)s] %(message)s")
fh.setFormatter(formatter)
root.addHandler(fh)

logger = get_logger(__name__)
logger.info("Now logging to console and app.log")
```

## Testing and demo
- `test_logging()` in `backend/utils/test_logger.py` is a simple demonstration helper — running the file directly will call it and then start Uvicorn when executed as `__main__`.

```bash
python3 backend/utils/test_logger.py
```

- For pytest you can capture logs with `caplog` fixture, or set levels inside tests to assert log output.

## Best practices
- Use `get_logger(__name__)` in each module to get per-module names in logs.
- Configure handlers and levels at application startup, not inside library modules.
- Prefer adding handlers (file, rotating file, or structured/JSON) rather than re-calling `basicConfig` throughout the code.
- For structured logs, add a handler with a JSON formatter instead of changing the basic format string.

## Where to change settings
- For global changes, update `backend/utils/logger.py` or add additional handlers at the main application startup (e.g., in `backend/app/main.py`).

---

*This section documents the project's `utils` logger helper and shows examples for daily use and integration.*
