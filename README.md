# webapp-st-boilerplate

A template for building web applications with Streamlit, designed to provide a solid and secure foundation for rapid development with user management, authentication, login, and authorization features.

## Main Features
- **User management**: Registration, authentication, and permission management.
- **Secure login**: Implementation of best practices for access security.
- **Authorization**: User role and permission control.
- **Modular structure**: Code organized for easy extension and maintenance.
- **Database integration**: Support for SQLAlchemy and Alembic for data management and migrations.
- **Ready to use**: Includes tools for testing, coverage, and linting.

## Project Structure
- `src/webapp_st_boilerplate/` — Main application code
- `tests/` — Automated tests
- `alembic/` — Database migration management

## Getting Started
To start the application, follow these steps:

1. **Install the virtual environment** (the repository uses [uv](https://github.com/astral-sh/uv)):
   ```bash
   uv sync
   ```
2. **Create the secrets file**:
   - Copy the structure from `secrets_template.toml` and create a new file named `secrets.toml` inside the `.streamlit` directory.
   - Populate the environment variables as needed for your setup.
3. **Activate the virtual environment** (if running on WSL):
   ```bash
   source .venv/bin/activate
   ```
4. **Start the web application**:
   ```bash
   make webapp
   ```

## Code Coverage
<!-- coverage:start -->
## 📊 Code Coverage
██████████████████████████░░░░  88.4%<br>
Updated at: 2025-07-01 23:20:18
<!-- coverage:end -->

## Author
Salvatore Albore — [salvatore.albore@gmail.com](mailto:salvatore.albore@gmail.com)
