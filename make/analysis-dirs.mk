.PHONY: check-directory-sizes check-directory-sizes-clean check-directory-sizes-summary

check-directory-sizes:
	@echo "Analyzing directories with more than 10 items..."
	@echo "================================================"
	@find . -type d \
		-not -path "./.venv/*" \
		-not -path "./.git/*" \
		-not -path "./google_calendar_mcp.egg-info/*" \
		-not -path "./__pycache__/*" \
		-not -path "./.coverage/*" \
		-exec sh -c ' \
			dir="$$1"; \
			if [ "$$dir" = "." ]; then \
				count=$$(ls -1a "$$dir" 2>/dev/null | grep -v -E "^(__pycache__|\.claude|\.github|\.opencode|\.venv|\.warp|\.coverage|\.coveragerc|\.cursorrules|\.env\.mcp|\.gitignore|claude\.md|gemini\.md|[Mm]akefile|[Oo]pencode\.md|pyproject\.toml|pytest\.ini|[Rr]eadme\.md|requirements\.txt|run_mcp\.py|TODO\.md)$$" | wc -l); \
			else \
				count=$$(ls -1a "$$dir" 2>/dev/null | grep -v -E "^\\.?$$" | wc -l); \
			fi; \
			[ $$count -gt 10 ] && printf "%3d items: %s\n" $$count "$$dir"' _ {} \; \
		| sort -nr
	@echo "================================================"
	@echo "Analysis complete. Directories shown above exceed 10 items."

check-directory-sizes-clean:
	@echo "Analyzing directories with more than 10 items (excluding __pycache__)..."
	@echo "======================================================================"
	@find . -type d \
		-not -path "./.venv/*" \
		-not -path "./.git/*" \
		-not -path "./google_calendar_mcp.egg-info/*" \
		-not -path "./__pycache__/*" \
		-not -path "./.coverage/*" \
		-not -path "*/__pycache__" \
		-exec sh -c ' \
			dir="$$1"; \
			if [ "$$dir" = "." ]; then \
				count=$$(ls -1a "$$dir" 2>/dev/null | grep -v -E "^(__pycache__|\.claude|\.github|\.opencode|\.venv|\.warp|\.coverage|\.coveragerc|\.cursorrules|\.env\.mcp|\.gitignore|claude\.md|gemini\.md|[Mm]akefile|[Oo]pencode\.md|pyproject\.toml|pytest\.ini|[Rr]eadme\.md|requirements\.txt|run_mcp\.py|TODO\.md)$$" | wc -l); \
			else \
				count=$$(ls -1a "$$dir" 2>/dev/null | grep -v -E "^\\.?$$" | wc -l); \
			fi; \
			[ $$count -gt 10 ] && printf "%3d items: %s\n" $$count "$$dir"' _ {} \; \
		| sort -nr
	@echo "======================================================================"
	@echo "Analysis complete. Directories shown above exceed 10 items (no __pycache__)."

check-directory-sizes-summary:
	@echo "Quick Directory Analysis Summary"
	@echo "================================"
	@total=$$(find . -type d \
		-not -path "./.venv/*" \
		-not -path "./.git/*" \
		-not -path "./google_calendar_mcp.egg-info/*" \
		-not -path "./__pycache__/*" \
		-not -path "./.coverage/*" \
		-exec sh -c ' \
			dir="$$1"; \
			if [ "$$dir" = "." ]; then \
				count=$$(ls -1a "$$dir" 2>/dev/null | grep -v -E "^(__pycache__|\.claude|\.github|\.opencode|\.venv|\.warp|\.coverage|\.coveragerc|\.cursorrules|\.env\.mcp|\.gitignore|claude\.md|gemini\.md|[Mm]akefile|[Oo]pencode\.md|pyproject\.toml|pytest\.ini|[Rr]eadme\.md|requirements\.txt|run_mcp\.py|TODO\.md)$$" | wc -l); \
			else \
				count=$$(ls -1a "$$dir" 2>/dev/null | grep -v -E "^\\.?$$" | wc -l); \
			fi; \
			[ $$count -gt 10 ] && echo "$$dir"' _ {} \; \
		| wc -l); \
	clean_total=$$(find . -type d \
		-not -path "./.venv/*" \
		-not -path "./.git/*" \
		-not -path "./google_calendar_mcp.egg-info/*" \
		-not -path "./__pycache__/*" \
		-not -path "./.coverage/*" \
		-not -path "*/__pycache__" \
		-exec sh -c ' \
			dir="$$1"; \
			if [ "$$dir" = "." ]; then \
				count=$$(ls -1a "$$dir" 2>/dev/null | grep -v -E "^(__pycache__|\.claude|\.github|\.opencode|\.venv|\.warp|\.coverage|\.coveragerc|\.cursorrules|\.env\.mcp|\.gitignore|claude\.md|gemini\.md|[Mm]akefile|[Oo]pencode\.md|pyproject\.toml|pytest\.ini|[Rr]eadme\.md|requirements\.txt|run_mcp\.py|TODO\.md)$$" | wc -l); \
			else \
				count=$$(ls -1a "$$dir" 2>/dev/null | grep -v -E "^\\.?$$" | wc -l); \
			fi; \
			[ $$count -gt 10 ] && echo "$$dir"' _ {} \; \
		| wc -l); \
	echo "📁 Directories over 10 items: $$total total"; \
	echo "📁 Excluding __pycache__: $$clean_total directories"; \
	echo "🗂️  __pycache__ directories: $$((total - clean_total))"; \
	echo ""; \
	echo "Run 'make check-directory-sizes' for detailed list"; \
	echo "Run 'make check-directory-sizes-clean' to exclude __pycache__" 