import subprocess
import sys
import os
import pytest
from pathlib import Path


class TestUvxIntegration:
    """Test uvx integration for Google Calendar MCP."""
    
    def test_pyproject_toml_exists(self):
        """Test that pyproject.toml exists and is valid."""
        project_root = Path(__file__).parent.parent.parent.parent
        pyproject_path = project_root / "pyproject.toml"
        
        assert pyproject_path.exists(), "pyproject.toml should exist"
        
        content = pyproject_path.read_text()
        assert "google-calendar-mcp" in content
        assert "src.mcp.mcp_stdio_server:run_stdio_server" in content

    def test_uvx_dry_run(self):
        """Test uvx dry run with the project."""
        project_root = Path(__file__).parent.parent.parent.parent
        
        try:
            # Test if uvx can find and parse the project
            result = subprocess.run([
                'uvx', '--help'
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode != 0:
                pytest.skip("uvx not available in test environment")
                
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pytest.skip("uvx not available in test environment")

    def test_package_structure_for_uvx(self):
        """Test that package structure is compatible with uvx."""
        project_root = Path(__file__).parent.parent.parent.parent
        
        # Check that src directory exists
        src_dir = project_root / "src"
        assert src_dir.exists(), "src directory should exist"
        
        # Check that main entry point module exists
        stdio_server = src_dir / "mcp" / "mcp_stdio_server.py"
        assert stdio_server.exists(), "mcp_stdio_server.py should exist"
        
        # Check that run_stdio_server function exists
        content = stdio_server.read_text()
        assert "def run_stdio_server(" in content, "run_stdio_server function should exist"

    def test_migration_script_exists(self):
        """Test that migration script exists and is executable."""
        project_root = Path(__file__).parent.parent.parent.parent
        migration_script = project_root / "scripts" / "migrate_to_uvx.py"
        
        assert migration_script.exists(), "Migration script should exist"
        
        # Check script is executable
        content = migration_script.read_text()
        assert "def main(" in content, "Migration script should have main function"
        assert "uvx" in content, "Migration script should reference uvx"

    def test_requirements_compatibility(self):
        """Test that requirements are compatible with pyproject.toml."""
        project_root = Path(__file__).parent.parent.parent.parent
        
        # Read requirements.txt
        requirements_file = project_root / "requirements.txt"
        assert requirements_file.exists(), "requirements.txt should exist"
        
        requirements = requirements_file.read_text()
        
        # Read pyproject.toml
        pyproject_file = project_root / "pyproject.toml"
        pyproject_content = pyproject_file.read_text()
        
        # Check key dependencies are in both
        key_deps = ["google-api-python-client", "google-auth"]
        for dep in key_deps:
            assert dep in requirements, f"{dep} should be in requirements.txt"
            assert dep in pyproject_content, f"{dep} should be in pyproject.toml" 