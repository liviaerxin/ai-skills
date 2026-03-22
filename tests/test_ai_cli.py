import pytest
import subprocess
import json
import os
from pathlib import Path

def run_cmd(cmd_list, cwd):
    """Run command and return output."""
    result = subprocess.run(
        cmd_list,
        cwd=str(cwd),
        capture_output=True,
        text=True
    )
    return result

def test_init(ai_cmd, tmp_path):
    """Verify init creates necessary directories and manifest."""
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    
    result = run_cmd([ai_cmd, "init"], project_dir)
    assert result.returncode == 0
    
    # Check directories
    assert (project_dir / ".agents" / "skills").is_dir()
    assert (project_dir / ".agents" / "agents").is_dir()
    assert (project_dir / ".claude").is_dir()
    
    # Check symlinks
    assert (project_dir / ".agent").is_symlink()
    assert (project_dir / "CLAUDE.md").is_symlink()
    
    # Check manifest
    manifest = project_dir / ".agentic.json"
    assert manifest.exists()
    assert json.loads(manifest.read_text()) == {"skills": []}

def test_add_personal_skill(ai_cmd, repo_root, tmp_path):
    """Verify adding a personal skill updates manifest and symlinks."""
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    run_cmd([ai_cmd, "init"], project_dir)
    
    # Add personal skill (defined in conftest.py)
    result = run_cmd([ai_cmd, "add", "personal-skill"], project_dir)
    assert result.returncode == 0
    assert "Added personal skill" in result.stdout
    
    # Check symlink
    skill_link = project_dir / ".agents" / "skills" / "personal-skill"
    assert skill_link.is_symlink()
    assert skill_link.resolve() == (repo_root / "skills" / "personal-skill")
    
    # Check manifest
    manifest = json.loads((project_dir / ".agentic.json").read_text())
    assert "personal-skill" in manifest["skills"]

def test_add_vendor_skill(ai_cmd, repo_root, tmp_path):
    """Verify adding a vendor skill updates manifest and symlinks."""
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    run_cmd([ai_cmd, "init"], project_dir)
    
    # Add vendor skill (defined in conftest.py)
    # The script searches for directory names recursively
    result = run_cmd([ai_cmd, "add", "community-skill"], project_dir)
    assert result.returncode == 0
    assert "Added community skill" in result.stdout
    
    # Check symlink
    skill_link = project_dir / ".agents" / "skills" / "community-skill"
    assert skill_link.is_symlink()
    assert skill_link.resolve() == (repo_root / "vendor" / "community-repo" / "skills" / "community-skill")
    
    # Check manifest
    manifest = json.loads((project_dir / ".agentic.json").read_text())
    assert "community-skill" in manifest["skills"]

def test_remove_skill(ai_cmd, repo_root, tmp_path):
    """Verify removing a skill cleans up symlinks and manifest."""
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    run_cmd([ai_cmd, "init"], project_dir)
    run_cmd([ai_cmd, "add", "personal-skill"], project_dir)
    
    result = run_cmd([ai_cmd, "remove", "personal-skill"], project_dir)
    assert result.returncode == 0
    assert "Removed skill" in result.stdout
    
    # Check symlink gone
    skill_link = project_dir / ".agents" / "skills" / "personal-skill"
    assert not skill_link.exists()
    
    # Check manifest update
    manifest = json.loads((project_dir / ".agentic.json").read_text())
    assert "personal-skill" not in manifest["skills"]

def test_install_from_manifest(ai_cmd, repo_root, tmp_path):
    """Verify install recreates symlinks from manifest."""
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    
    # Simulate a cloned repo with just a manifest
    (project_dir / ".agentic.json").write_text(json.dumps({"skills": ["personal-skill", "community-skill"]}))
    
    result = run_cmd([ai_cmd, "install"], project_dir)
    assert result.returncode == 0
    
    # Check symlinks created
    assert (project_dir / ".agents" / "skills" / "personal-skill").is_symlink()
    assert (project_dir / ".agents" / "skills" / "community-skill").is_symlink()

def test_list(ai_cmd, repo_root, tmp_path):
    """Verify list command output."""
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    run_cmd([ai_cmd, "init"], project_dir)
    run_cmd([ai_cmd, "add", "personal-skill"], project_dir)
    
    result = run_cmd([ai_cmd, "list"], project_dir)
    assert result.returncode == 0
    assert "Available Personal Skills" in result.stdout
    assert "personal-skill" in result.stdout
    assert "community-skill" in result.stdout
    assert "Active in Project" in result.stdout
