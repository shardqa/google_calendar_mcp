.PHONY: check-directory-sizes count-items count-items-quick

EXCLUDE_PATHS := -not -path "./.venv/*" -not -path "./.git/*" -not -path "./google_calendar_mcp.egg-info/*" -not -path "./__pycache__/*" -not -path "./.coverage/*" -not -name ".git"
ROOT_EXCLUDE := __pycache__|\.claude|\.github|\.opencode|\.venv|\.warp|\.coverage|\.coveragerc|\.cursorrules|\.env\.mcp|\.gitignore|claude\.md|gemini\.md|[Mm]akefile|[Oo]pencode\.md|pyproject\.toml|pytest\.ini|[Rr]eadme\.md|requirements\.txt|run_mcp\.py|TODO\.md

define count_items
	@dir="$$1"; \
	if [ "$$dir" = "." ]; then \
		count=$$(ls -1a "$$dir" 2>/dev/null | grep -v -E "^($(ROOT_EXCLUDE))$$" | wc -l); \
	else \
		count=$$(ls -1a "$$dir" 2>/dev/null | grep -v -E "^\.?$$" | wc -l); \
	fi; \
	[ $$count -gt 10 ] && printf "%3d items: %s\n" $$count "$$dir"
endef

check-directory-sizes:
	@echo "Analyzing directories with more than 10 items..."
	@echo "================================================"
	@find . -type d $(EXCLUDE_PATHS) -exec sh -c '$(call count_items,{})' _ {} \; | sort -nr
	@echo "================================================"

count-items:
	@echo "=== Complete item count by directory ==="
	@find . -type d $(EXCLUDE_PATHS) -not -name "__pycache__" | while read dir; do \
		if [ "$$dir" != "." ]; then \
			count=$$(find "$$dir" -maxdepth 1 -not -name "__pycache__" | wc -l); \
			echo "$$count items in $$dir"; \
		fi; \
	done | sort -k1 -n
	@echo
	@echo "=== Directories with more than 10 items ==="
	@find . -type d $(EXCLUDE_PATHS) -not -name "__pycache__" | while read dir; do \
		if [ "$$dir" != "." ]; then \
			count=$$(find "$$dir" -maxdepth 1 -not -name "__pycache__" | wc -l); \
			[ "$$count" -gt 10 ] && echo "⚠️  $$count items in $$dir"; \
		fi; \
	done | sort -k2 -n

count-items-quick:
	@echo "📊 Quick item count by directory:"
	@find . -type d $(EXCLUDE_PATHS) -not -name "__pycache__" | while read dir; do \
		if [ "$$dir" != "." ]; then \
			count=$$(find "$$dir" -maxdepth 1 -not -name "__pycache__" | wc -l); \
			if [ "$$count" -gt 10 ]; then \
				echo "⚠️  $$count items in $$dir"; \
			else \
				echo "✅ $$count items in $$dir"; \
			fi; \
		fi; \
	done | sort -k2 -n 