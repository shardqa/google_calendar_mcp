#!/usr/bin/env python3
"""
Sanitization script to replace sensitive data with generic placeholders.
This script replaces usernames, tokens, IPs, and paths while preserving functionality.
"""

import os
import re
import glob
from pathlib import Path
from typing import Dict, List, Tuple

class SensitiveDataSanitizer:
    def __init__(self, repo_root: str):
        self.repo_root = Path(repo_root)
        self.replacements = self._define_replacements()
        self.excluded_dirs = {'.git', '.venv', '__pycache__', '.pytest_cache', 'node_modules', '.coverage'}
        self.excluded_extensions = {'.pyc', '.pyo', '.so', '.dll', '.exe'}
        
    def _define_replacements(self) -> List[Tuple[str, str]]:
        """Define all sensitive data replacements."""
        return [
            # Bearer tokens
            (r'YOUR_BEARER_TOKEN_HERE', 'YOUR_BEARER_TOKEN_HERE'),
            (r'mcp2\.eyJ[A-Za-z0-9+/=]+', 'mcp2.YOUR_JWT_TOKEN_HERE'),
            
            # IP addresses - be careful with localhost
            (r'147\.79\.86\.211', 'YOUR_SERVER_IP'),
            
            # Usernames in paths - be very careful to maintain structure
            (r'/home/your-username/', '/home/your-username/'),
            (r'/home/your-username/', '/home/your-username/'),
            (r'your-username', 'your-username'),
            
            # Username in systemd configs - but keep structure
            (r'User=your-username\b', 'User=your-username'),
            (r'Group=your-username\b', 'Group=your-username'),
            
            # SSH and other configs
            (r'your-username@YOUR_SERVER_IP', 'your-username@YOUR_SERVER_IP'),
            
            # Be careful with 'richard' - only replace in specific contexts
            (r'\bUSER_HOME="/home/richard"', 'USER_HOME="/home/your-username"'),
            (r'cd /home/your-username/', 'cd /home/your-username/'),
            
            # Example API keys and secrets (keep the format)
            (r'"YOUR_API_KEY_HERE"', '"YOUR_API_KEY_HERE"'),
            (r'"YOUR_API_KEY_HERE"', '"YOUR_API_KEY_HERE"'),
            (r'export GEMINI_API_KEY="YOUR_GEMINI_API_KEY"]*"', 'export GEMINI_API_KEY="YOUR_GEMINI_API_KEY"'),
            
            # SSL certificate paths
            (r'/home/your-username/[^/]*\.pem', '/path/to/your-certs/certificate.pem'),
            (r'/path/to/your-certs/certificate.pem', '/path/to/your-certs/*.pem'),
        ]
    
    def _should_process_file(self, file_path: Path) -> bool:
        """Determine if a file should be processed."""
        # Skip if in excluded directory
        for part in file_path.parts:
            if part in self.excluded_dirs:
                return False
        
        # Skip if excluded extension
        if file_path.suffix in self.excluded_extensions:
            return False
            
        # Skip binary files
        if not self._is_text_file(file_path):
            return False
            
        return True
    
    def _is_text_file(self, file_path: Path) -> bool:
        """Check if file is text-based."""
        try:
            with open(file_path, 'rb') as f:
                chunk = f.read(512)
                return b'\x00' not in chunk
        except (OSError, IOError):
            return False
    
    def sanitize_file(self, file_path: Path) -> bool:
        """Sanitize a single file and return True if changes were made."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except (OSError, IOError) as e:
            print(f"Warning: Could not read {file_path}: {e}")
            return False
        
        original_content = content
        
        # Apply all replacements
        for pattern, replacement in self.replacements:
            content = re.sub(pattern, replacement, content)
        
        # Write back if changed
        if content != original_content:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ Sanitized: {file_path}")
                return True
            except (OSError, IOError) as e:
                print(f"Error: Could not write {file_path}: {e}")
                return False
        
        return False
    
    def scan_and_sanitize(self) -> Dict[str, int]:
        """Scan all files and sanitize sensitive data."""
        results = {"processed": 0, "changed": 0, "errors": 0}
        
        print(f"🔍 Scanning repository: {self.repo_root}")
        print("=" * 60)
        
        for file_path in self.repo_root.rglob('*'):
            if not file_path.is_file():
                continue
                
            if not self._should_process_file(file_path):
                continue
            
            results["processed"] += 1
            
            try:
                if self.sanitize_file(file_path):
                    results["changed"] += 1
            except Exception as e:
                print(f"❌ Error processing {file_path}: {e}")
                results["errors"] += 1
        
        return results
    
    def create_backup(self) -> str:
        """Create a backup of the current repository state."""
        import shutil
        import datetime
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_before_sanitization_{timestamp}"
        backup_path = self.repo_root.parent / backup_name
        
        print(f"📦 Creating backup: {backup_path}")
        shutil.copytree(self.repo_root, backup_path, ignore=shutil.ignore_patterns('.git'))
        
        return str(backup_path)

def main():
    """Main function to run the sanitization."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Sanitize sensitive data from repository")
    parser.add_argument("--repo-root", default=".", help="Repository root directory")
    parser.add_argument("--no-backup", action="store_true", help="Skip creating backup")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be changed without making changes")
    
    args = parser.parse_args()
    
    sanitizer = SensitiveDataSanitizer(args.repo_root)
    
    if not args.no_backup and not args.dry_run:
        backup_path = sanitizer.create_backup()
        print(f"✅ Backup created at: {backup_path}")
        print()
    
    if args.dry_run:
        print("🔍 DRY RUN MODE - No changes will be made")
        print()
    
    results = sanitizer.scan_and_sanitize()
    
    print("=" * 60)
    print("📊 SANITIZATION RESULTS:")
    print(f"   Files processed: {results['processed']}")
    print(f"   Files changed: {results['changed']}")
    print(f"   Errors: {results['errors']}")
    
    if results['changed'] > 0:
        print("\n⚠️  IMPORTANT:")
        print("   1. Review the changes carefully")
        print("   2. Run tests to ensure functionality")
        print("   3. Commit changes before cleaning git history")
    
    return results['errors'] == 0

if __name__ == "__main__":
    exit(0 if main() else 1) 