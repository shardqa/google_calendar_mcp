# Gemini Development Rules

- Follow Test-Driven Development: write a failing test, implement functionality,
  then refactor while keeping tests green
- Keep a maximum of ten items per folder; when exceeded, create sub-folders
  and adjust imports accordingly
- After creating any markdown file, run `markdownlint --fix` and include at
  least two links to relevant markdown documents
- Ensure that no file exceeds one hundred lines; if it does, split it into
  smaller, logically-named files and update imports or links. For code files,
  always run tests after refactoring to ensure functionality remains intact
- Excluded from auto-refactor/move checks (never move these): .cursor, .github,
  .venv, .coverage, .coveragerc, .cursorrules, .gitignore, Makefile, README.md, Gemini.md,
  requirements.txt, TODO.md from the root folder.
- When completing a task 100%, move it from TODO.md to COMPLETED.md and keep
  only active tasks that require action in TODO.md
- After any code change, run the full test suite and restore global coverage
  to 100% before committing

---

- See also: [TODO.md](TODO.md) and [COMPLETED.md](COMPLETED.md)
