import pytest
import os
import shutil
import subprocess
from pathlib import Path

@pytest.fixture
def repo_root(tmp_path):
    """
    Creates a mock repository structure.
    """
    # Create structure
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()
    vendor_dir = tmp_path / "vendor"
    vendor_dir.mkdir()
    
    # Copy the actual ai script
    original_script = Path(__file__).parent.parent / "bin" / "ai"
    shutil.copy(original_script, bin_dir / "ai")
    
    # Make executable
    (bin_dir / "ai").chmod(0o755)
    
    # Create dummy skills
    (skills_dir / "personal-skill").mkdir()
    (skills_dir / "personal-skill" / "SKILL.md").write_text("# Personal Skill")

    # Skill name that would have broken the old python3 -c string interpolation
    (skills_dir / "bad'skill").mkdir()
    (skills_dir / "bad'skill" / "SKILL.md").write_text("# Personal Skill With Quote")
    
    (vendor_dir / "community-repo").mkdir()
    (vendor_dir / "community-repo" / "skills").mkdir()
    (vendor_dir / "community-repo" / "skills" / "community-skill").mkdir()
    (vendor_dir / "community-repo" / "skills" / "community-skill" / "SKILL.md").write_text("# Community Skill")

    # Vendor skill provided as a single markdown file (skill.md)
    (vendor_dir / "community-repo" / "skills" / "md-skill.md").write_text("# Vendor Markdown Skill")
    
    return tmp_path

@pytest.fixture
def ai_cmd(repo_root):
    """
    Returns the path to the mocked ai command.
    """
    return str(repo_root / "bin" / "ai")
