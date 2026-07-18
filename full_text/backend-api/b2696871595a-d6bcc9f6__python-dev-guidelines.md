---
name: python-dev-guidelines
description: Python and Flask development standards — PEP 8, route conventions, imports, error handling, and dependency management.
---

# Python Development Guidelines

## Standards

### Code Style
- Follow PEP 8 strictly — use 4-space indentation, snake_case for functions/variables, PascalCase for classes
- Maximum line length: 120 characters (not 79 — we use modern editors)
- Use type hints for function signatures: `def get_product(product_id: int) -> dict:`
- Prefer f-strings over `.format()` or `%` formatting

### Flask Conventions
- All routes MUST include `.html` extension for Flask-Frozen static generation compatibility
- Use `url_for()` for all internal links — never hardcode paths
- Session-based state is acceptable for demo/prototype purposes
- POST routes will fail during static generation — this is expected behavior, not a bug

### Imports
- Group imports: stdlib → third-party → local, separated by blank lines
- Use absolute imports over relative imports
- Never use wildcard imports (`from module import *`)

### Error Handling
- Use specific exception types, not bare `except:`
- Log errors with context: `logger.error(f"Failed to load product {product_id}: {e}")`
- Return appropriate HTTP status codes from Flask routes (404 for not found, 400 for bad input)

### Dependencies
- Pin versions in `requirements.txt` (e.g., `Flask==3.0.3`, not `Flask>=3.0`)
- Separate dev/test dependencies into `requirements-dev.txt` or `requirements-e2e.txt`
- Minimize dependencies — prefer stdlib solutions when reasonable

### Virtual Environment
- Use `.venv/` directory (not `venv/`)
- Always activate before running: `source .venv/bin/activate`
- Run `pip install -r requirements.txt` after pulling changes
