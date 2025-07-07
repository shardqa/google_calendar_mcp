#!/usr/bin/env python3
"""
Git history cleanup script to remove sensitive data from all commits.
Uses git-filter-repo to rewrite history and remove sensitive patterns.
"""

import os
import sys
import subprocess
import tempfile
from pathlib import Path
from typing import List

class GitHistoryCleaner:
    def __init__(self, repo_root: str):
        self.repo_root = Path(repo_root)
        self.sensitive_patterns = self._get_sensitive_patterns()
        
    def _get_sensitive_patterns(self) -> List[str]:
        """Define patterns of sensitive data to remove from git history."""
        return [
            # Bearer tokens (exact matches)
            'YOUR_BEARER_TOKEN_HERE',
            
            # Server IP
            'YOUR_SERVER_IP',
            
            # Personal paths and usernames
            '/home/your-username/',
            '/home/your-username/',
            'your-username',
            
            # API key examples
            'YOUR_API_KEY_HERE',
            'YOUR_API_KEY_HERE',
            
            # SSH examples  
            'your-username@YOUR_SERVER_IP',
        ]
    
    def check_git_filter_repo(self) -> bool:
        """Check if git-filter-repo is available."""
        try:
            result = subprocess.run(['git', 'filter-repo', '--version'], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def install_git_filter_repo(self) -> bool:
        """Try to install git-filter-repo."""
        print("📦 git-filter-repo not found. Attempting to install...")
        
        try:
            # Try pip install
            result = subprocess.run([sys.executable, '-m', 'pip', 'install', 'git-filter-repo'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ git-filter-repo installed successfully")
                return True
        except Exception as e:
            print(f"❌ Failed to install git-filter-repo via pip: {e}")
        
        print("\n⚠️  Please install git-filter-repo manually:")
        print("   pip install git-filter-repo")
        print("   or")
        print("   https://github.com/newren/git-filter-repo/blob/main/INSTALL.md")
        return False
    
    def create_replacements_file(self) -> str:
        """Create a temporary file with text replacements for git-filter-repo."""
        replacements = []
        
        for pattern in self.sensitive_patterns:
            if pattern.startswith('/home/your-username/'):
                replacement = pattern.replace('/home/your-username/', '/home/your-username/')
            elif pattern.startswith('/home/your-username/'):
                replacement = pattern.replace('/home/your-username/', '/home/your-username/')
            elif pattern == 'your-username':
                replacement = 'your-username'
            elif pattern == 'YOUR_SERVER_IP':
                replacement = 'YOUR_SERVER_IP'
            elif pattern == 'YOUR_BEARER_TOKEN_HERE':
                replacement = 'YOUR_BEARER_TOKEN_HERE'
            elif 'api_key' in pattern or 'chave' in pattern:
                replacement = 'YOUR_API_KEY_HERE'
            elif 'richard@' in pattern:
                replacement = pattern.replace('richard@', 'your-username@').replace('YOUR_SERVER_IP', 'YOUR_SERVER_IP')
            else:
                replacement = f'REDACTED_{pattern[:10]}'
            
            replacements.append(f"{pattern}==>{replacement}")
        
        # Create temporary file
        fd, temp_path = tempfile.mkstemp(suffix='.txt', prefix='git_replacements_')
        try:
            with os.fdopen(fd, 'w') as f:
                f.write('\n'.join(replacements))
            return temp_path
        except:
            os.close(fd)
            raise
    
    def create_git_backup(self) -> str:
        """Create a backup of the git repository."""
        import shutil
        import datetime
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"git_backup_{timestamp}"
        backup_path = self.repo_root.parent / backup_name
        
        print(f"📦 Creating git backup: {backup_path}")
        
        # Clone the repository to backup
        result = subprocess.run([
            'git', 'clone', '--bare', str(self.repo_root), str(backup_path)
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            raise Exception(f"Failed to create git backup: {result.stderr}")
        
        return str(backup_path)
    
    def clean_history(self, create_backup: bool = True) -> bool:
        """Clean sensitive data from git history."""
        if not self.check_git_filter_repo():
            if not self.install_git_filter_repo():
                return False
        
        if create_backup:
            try:
                backup_path = self.create_git_backup()
                print(f"✅ Git backup created at: {backup_path}")
            except Exception as e:
                print(f"❌ Failed to create backup: {e}")
                print("Continuing without backup...")
        
        # Create replacements file
        replacements_file = self.create_replacements_file()
        
        try:
            print("🧹 Cleaning git history...")
            print("⚠️  This will rewrite ALL commits!")
            
            # Run git filter-repo
            cmd = [
                'git', 'filter-repo', 
                '--replace-text', replacements_file,
                '--force'
            ]
            
            print(f"Running: {' '.join(cmd)}")
            result = subprocess.run(cmd, cwd=self.repo_root, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Git history cleaned successfully!")
                print("\n⚠️  IMPORTANT:")
                print("   - All commit hashes have changed")
                print("   - You'll need to force-push to remote: git push --force-with-lease")
                print("   - Collaborators will need to re-clone the repository")
                return True
            else:
                print(f"❌ git-filter-repo failed: {result.stderr}")
                return False
                
        finally:
            # Clean up temporary file
            try:
                os.unlink(replacements_file)
            except:
                pass
        
        return False
    
    def verify_cleanup(self) -> bool:
        """Verify that sensitive data was removed from history."""
        print("🔍 Verifying cleanup...")
        
        failed_patterns = []
        
        for pattern in self.sensitive_patterns:
            # Search git history for the pattern
            result = subprocess.run([
                'git', 'log', '--all', '--grep', pattern, '--oneline'
            ], cwd=self.repo_root, capture_output=True, text=True)
            
            if result.stdout.strip():
                failed_patterns.append(pattern)
                continue
            
            # Search file contents in history
            result = subprocess.run([
                'git', 'log', '--all', '-S', pattern, '--oneline'
            ], cwd=self.repo_root, capture_output=True, text=True)
            
            if result.stdout.strip():
                failed_patterns.append(pattern)
        
        if failed_patterns:
            print("❌ The following patterns are still present in history:")
            for pattern in failed_patterns:
                print(f"   - {pattern}")
            return False
        else:
            print("✅ All sensitive patterns removed from history!")
            return True

def main():
    """Main function to run the git history cleanup."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Clean sensitive data from git history")
    parser.add_argument("--repo-root", default=".", help="Repository root directory")
    parser.add_argument("--no-backup", action="store_true", help="Skip creating git backup")
    parser.add_argument("--verify-only", action="store_true", help="Only verify cleanup, don't clean")
    
    args = parser.parse_args()
    
    cleaner = GitHistoryCleaner(args.repo_root)
    
    if args.verify_only:
        return cleaner.verify_cleanup()
    
    success = cleaner.clean_history(create_backup=not args.no_backup)
    
    if success:
        cleaner.verify_cleanup()
    
    return success

if __name__ == "__main__":
    exit(0 if main() else 1) 