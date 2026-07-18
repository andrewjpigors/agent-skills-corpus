---
name: development
description: Full development lifecycle skill — project architecture, implementation workflow, Flask patterns, and pre-commit checklist.
---

# Development Agent Skill

## Project Context

### Architecture
- **Backend**: Flask 3.0.3 web application with Jinja2 templating
- **Data layer**: Hardcoded product catalog in `db.py` (no external database)
- **Frontend**: Server-rendered HTML with CSS custom properties for theming
- **Deployment**: Dual mode — dynamic Flask server + static site via Flask-Frozen
- **Container**: Docker image with port 8000 exposed

### Key Files
| File | Purpose |
|------|---------|
| `app.py` | All Flask routes and business logic |
| `db.py` | Product catalog and data models |
| `templates/base.html` | Base template — all pages extend this |
| `static/css/style.css` | Global styles with CSS custom properties |
| `Makefile` | Development commands (`make develop`, `make test`, `make static`) |
| `.gitlab-ci.yml` | CI/CD pipeline — validate with `glab ci lint` before committing |

## Development Workflow

### Before writing code
1. Read the issue or task description completely
2. Read existing code in the files you'll modify — understand the patterns
3. Check `.agents-context/` for prior decisions and feature context
4. Identify which tests will be affected

### While writing code
1. Follow existing patterns in the codebase — don't introduce new conventions
2. Keep changes minimal and focused — one feature per branch
3. Routes MUST end in `.html` for Flask-Frozen compatibility
4. Test both dynamic (`make develop`) and static (`make static`) modes
5. Run `pytest tests/` after every meaningful change

### Before committing
1. Lint: `ruff check --fix .` — auto-fix import order, unused imports, style issues
2. Format: `ruff format .` — consistent code style
3. Test: `pytest tests/` — full test suite must pass
4. If CI config changed: `glab ci lint`
5. Review your own diff: `git diff --staged`
6. Use conventional commit format: `feat: add product filtering`

## Implementation Patterns

### Adding a new route
```python
@app.route("/feature.html")
def feature():
    # Note: .html extension required for static generation
    return render_template("feature.html", products=get_products())
```

### Adding a new template
- Always extend `base.html`
- Use `url_for('static', filename='...')` for assets
- Use `url_for('route_function')` for links

### Modifying the product catalog
- Edit `db.py` directly — products are hardcoded dicts
- Each product needs: `id`, `name`, `description`, `price`, `image_url`, `category`
- Run `pytest tests/test_products.py` after changes

## Constraints
- **Static generation**: POST routes fail during `make static` — this is expected
- **No real payments**: Checkout is demo-only, no payment processing
- **Demo vulnerabilities**: Routes under `/demo/` contain intentional vulns for security scanning demos — DO NOT fix these
- **Port 8000**: Always use port 8000 for development and Docker
