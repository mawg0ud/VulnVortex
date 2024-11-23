# Developer Guide for VulnVortex

This document serves as a comprehensive guide for developers contributing to or extending VulnVortex.

## **Table of Contents**
1. [Project Structure](#project-structure)
2. [Setting Up the Development Environment](#setting-up-the-development-environment)
3. [Coding Standards](#coding-standards)
4. [Adding Features](#adding-features)
5. [Testing](#testing)
6. [API Architecture](#api-architecture)
7. [CI/CD Integration](#ci-cd-integration)

---

## **Project Structure**

```plaintext
VulnVortex/
├── src/
│   ├── core/               # Core logic
│   ├── scanners/           # Scanning modules
│   ├── utils/              # Helper utilities
│   ├── cli.py              # Command-line interface
├── tests/                  # Unit and integration tests
├── docs/                   # Documentation
├── requirements.txt        # Python dependencies
├── setup.py                # Installation script
└── README.md               # Project overview
```

---

## **Setting Up the Development Environment**

1. Fork and clone the repository:
   ```bash
   git clone https://github.com/mawg0ud/VulnVortex.git
   cd VulnVortex
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## **Coding Standards**

- Follow [PEP 8](https://peps.python.org/pep-0008/) for Python code.
- Use descriptive commit messages (e.g., `feat: add SQL injection scanner`).
- Ensure functions have docstrings using the Google style guide.

---

## **Adding Features**

### Steps to Add a Feature:
1. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Add or modify modules in `src/`.
3. Write unit tests in the `tests/` directory.
4. Run the tests:
   ```bash
   pytest
   ```
5. Submit a pull request.

---

## **Testing**

VulnVortex uses `pytest` for testing. Ensure tests cover:
- Core functionality
- Edge cases
- Error handling

Run tests locally:
```bash
pytest --cov=src
```

---

## **API Architecture**

VulnVortex’s API is modular and consists of:
1. **Core modules:** Handle scanning logic and integrations.
2. **Plugins:** Extend functionality with additional scanners.
3. **CLI:** Interfaces with the core modules.

---

## **CI/CD Integration**

- **GitHub Actions**: The repository includes workflows for:
  - Running tests
  - Code quality checks
- Customize workflows in `.github/workflows/`.
