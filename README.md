# Agentic Dotfiles (2026)

A centralized, local hub for managing AI agent skills and custom instructions across multiple platforms (Claude Code, OpenAI Codex, Google Antigravity).

## 🚀 Overview

Just like personal dotfiles for your shell, **Agentic Dotfiles** provides a "Universal Multi-Brain" workflow. It centralizes your opinionated AI prompts and vendor-provided community skills, allowing you to selectively inject them into projects.

### Key Benefits
- **DRY (Don't Repeat Yourself):** Edit a prompt once in `~/.agentic-dotfiles` and it updates everywhere.
- **Zero Context Dilution:** Inject only the skills needed for the current task (Principle of Least Privilege).
- **Tool Agnostic:** Cross-compatible with Claude (`CLAUDE.md`), Codex (`.agents/`), and Antigravity (`.agent/`).
- **Manifest Tracking:** Uses `.agentic.json` to manage project-specific skill state robustly.

---

## 🏗 Architecture

```text
~/.agentic-dotfiles/
├── bin/
│   └── ai                 # The CLI tool (Bash + Python)
├── skills/                # Your personal/private skills
│   ├── capture/
│   ├── handoff/
│   └── ...
├── vendor/                # Community skills (Git Submodules)
│   └── (optional downloads)
├── tests/                 # Pytest suite
└── .venv/                 # Local test environment
```

---

## 🛠 Installation

1. **Clone the repo:**
   ```bash
   git clone <your-repo-url> ~/.agentic-dotfiles
   cd ~/.agentic-dotfiles
   ```

2. **Add to your PATH:**
   Add this to your `~/.zshrc` or `~/.bashrc`:
   ```bash
   export PATH="$HOME/.agentic-dotfiles/bin:$PATH"
   ```

3. **Verify:**
   ```bash
   ai list
   ```

---

## 📖 Usage Guide

### 1. Initialize a Project
Run this in any new project root to set up the universal directory structure and symlinks.
```bash
ai init
```

### 2. Add Skills
Inject specific brains from your hub into the current project.
```bash
ai add rust-analyzer custom-deploy
```

### 3. Sync Fresh Clones
If you clone a project that already has an `.agentic.json` manifest, restore all skill symlinks instantly:
```bash
ai install
```

### 4. Remove Skills
Clean up the AI's context when a task is finished.
```bash
ai remove rust-analyzer
```

---

## 🧭 Recommended Pattern (2026)

Use a two-layer model:

- **`agentic-dotfiles` = personal layer**
  - Keep reusable generic skills and private preferences here.
  - This is your local AI toolbox.

- **`project B` = team layer**
  - Commit only project-critical instructions (for example `AGENTS.md`).
  - Do not commit generated local runtime artifacts: `.agent/`, `.agents/`, `CLAUDE.md`, `.claude/`.
  - Keep `.agentic.json` local by default; optionally commit `.agentic.json.example` for opt-in onboarding.

### Practical Workflow in Project B

```bash
ai init
ai add <skills>
# later, on fresh clones (if .agentic.json is present):
ai install
```

Copy skills into `project B` only when they are truly project-specific and must be identical for all contributors. Keep generic skills in `agentic-dotfiles`.

---

## 🧪 Testing

The repository includes a comprehensive `pytest` suite to ensure the CLI remains robust across platforms.

```bash
source .venv/bin/activate
pytest tests
```

---

## 📄 License
MIT
