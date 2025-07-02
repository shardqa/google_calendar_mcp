.PHONY: check-file-sizes check-file-sizes-summary

check-file-sizes:
	@echo "Analyzing files with more than 100 lines..."
	@echo "================================================"
	@find . -type f \( -name "*.py" -o -name "*.sh" -o -name "*.md" -o -name "*.txt" -o -name "*.yml" -o -name "*.yaml" -o -name "*.toml" -o -name "*.json" \) \
		-not -path "./.venv/*" \
		-not -path "./.git/*" \
		-not -path "./google_calendar_mcp.egg-info/*" \
		-not -path "./__pycache__/*" \
		-not -path "./.coverage/*" \
		-exec sh -c 'lines=$$(wc -l < "$$1"); [ $$lines -gt 100 ] && printf "%4d lines: %s\n" $$lines "$$1"' _ {} \; \
		| sort -nr
	@echo "================================================"
	@echo "Analysis complete. Files shown above exceed 100 lines."

check-file-sizes-summary:
	@echo "Quick File Size Analysis Summary"
	@echo "================================"
	@total=$$(find . -type f \( -name "*.py" -o -name "*.sh" -o -name "*.md" -o -name "*.txt" -o -name "*.yml" -o -name "*.yaml" -o -name "*.toml" -o -name "*.json" \) \
		-not -path "./.venv/*" \
		-not -path "./.git/*" \
		-not -path "./google_calendar_mcp.egg-info/*" \
		-not -path "./__pycache__/*" \
		-not -path "./.coverage/*" \
		-exec sh -c 'lines=$$(wc -l < "$$1"); [ $$lines -gt 100 ] && echo "$$1"' _ {} \; \
		| wc -l); \
	py_count=$$(find . -name "*.py" \
		-not -path "./.venv/*" \
		-not -path "./.git/*" \
		-not -path "./google_calendar_mcp.egg-info/*" \
		-not -path "./__pycache__/*" \
		-exec sh -c 'lines=$$(wc -l < "$$1"); [ $$lines -gt 100 ] && echo "$$1"' _ {} \; \
		| wc -l); \
	md_count=$$(find . -name "*.md" \
		-not -path "./.venv/*" \
		-not -path "./.git/*" \
		-exec sh -c 'lines=$$(wc -l < "$$1"); [ $$lines -gt 100 ] && echo "$$1"' _ {} \; \
		| wc -l); \
	echo "📊 Files over 100 lines: $$total total"; \
	echo "🐍 Python files (*.py): $$py_count"; \
	echo "📝 Markdown files (*.md): $$md_count"; \
	echo "🔧 Other files: $$((total - py_count - md_count))"; \
	echo ""; \
	echo "Run 'make check-file-sizes' for detailed list" 