# Bin Scripts Documentation

This directory contains utility scripts for managing git worktrees integrated with Linear issue tracking.

## Scripts Overview

### mkwt - Make Worktree
Creates a new git worktree for a Linear ticket with automatic branch naming and environment setup.

### rmwt - Remove Worktree  
Safely removes a git worktree after work is complete, with checks for uncommitted changes and branch merge status.

### gbn - Get Branch Name
Generates a standardized git branch name from a Linear ticket ID by fetching the ticket title and formatting it according to project conventions. The name "gbn" is short for "get-branch-name".

## Dependencies

### Required Dependencies

1. **Git** (2.15+)
   - Required for worktree functionality
   - Check version: `git --version`

2. **Bash** (4.0+)
   - Required for script execution
   - Check version: `bash --version`

3. **uv** (Python package manager)
   - Required for Python environment setup
   - Install: `curl -LsSf https://astral.sh/uv/install.sh | sh`
   - Or via Homebrew: `brew install uv`
   - Documentation: https://github.com/astral-sh/uv

4. **Linear CLI** (@egcli/lr)
   - Required for fetching Linear ticket information
   - Install: `npm install -g @egcli/lr`
   - Or via yarn: `yarn global add @egcli/lr`
   - Documentation: https://github.com/evangodon/linear-cli

### Optional Dependencies

1. **direnv**
   - Automatically loads environment variables from .envrc
   - Install: `brew install direnv`
   - Not required but recommended for automatic environment activation

2. **Claude Code CLI**
   - Can be used instead of Linear CLI for fetching branch names
   - Install from: https://claude.ai/code
   - Currently commented out in favor of Linear CLI

## Setup Instructions

### 1. Install Dependencies

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Linear CLI (requires Node.js)
npm install -g @egcli/lr

# Optional: Install direnv
brew install direnv
```

### 2. Configure Linear CLI

Before using the scripts, you need to initialize the Linear CLI with your API key:

```bash
# Initialize Linear CLI
linear init

# Follow the prompts to:
# 1. Enter your Linear API key (get from https://linear.app/settings/api)
# 2. Select your workspace
# 3. Optionally set a default team
```

### 3. Make Scripts Executable

```bash
chmod +x mkwt rmwt gbn
```

### 4. Configure Symlinks (Optional)

Create a `wt.rc` file in your repository root to specify which files should be symlinked to worktrees:

```bash
# Example wt.rc
SYMLINK_FILES="
.envrc
.env.local
"
```

If no `wt.rc` exists, the script will skip creating symlinks.

## Usage

### Creating a Worktree

```bash
# From anywhere in the repository
./bin/mkwt ROY-123

# This will:
# 1. Pull latest changes from main
# 2. Fetch branch name from Linear ticket using gbn
# 3. Create a worktree at ../todoish-roy-123
# 4. Set up Python environment with uv
# 5. Create symlinks for configured files
# 6. Navigate to the new worktree
# 7. Activate the Python environment
```

### Removing a Worktree

```bash
# From within the worktree directory
./bin/rmwt

# This will:
# 1. Check for uncommitted changes
# 2. Verify if branch is merged to main
# 3. Navigate back to main repository
# 4. Remove the worktree
# 5. Optionally delete the remote branch
# 6. Prune worktree list
```

#### Dry Run Mode

Test what would happen without making changes:

```bash
./bin/rmwt --dry-run
```

### Getting a Branch Name

```bash
# Get a standardized branch name for a Linear ticket
./bin/gbn ROY-123

# Output: farmisen/roy-123-implement-feature-name

# Use in branch creation:
git checkout -b $(./bin/gbn ROY-123)
```

## Environment Variables

- `CLAUDE_HOME`: Path to Claude CLI installation (default: `~/.claude/local`)
- `VIRTUAL_ENV`: Automatically set when entering a worktree with Python environment

## Troubleshooting

### Linear CLI Issues

**Problem**: "No config found" error  
**Solution**: Run `linear init` to set up your API key

**Problem**: Cannot fetch branch name  
**Solution**: Ensure you have access to the Linear ticket and your API key has proper permissions

### Python Environment Issues

**Problem**: uv command not found  
**Solution**: Install uv using the installation instructions above

**Problem**: Virtual environment not activating  
**Solution**: 
- If using direnv, ensure it's installed and hooked into your shell
- Run `direnv allow` in the worktree directory
- Manually activate with `source .venv/bin/activate`

### Worktree Issues

**Problem**: "Worktree already exists" error  
**Solution**: Either navigate to the existing worktree or remove it first with `rmwt`

**Problem**: Cannot remove worktree  
**Solution**: Use `git worktree remove --force <path>` if the directory was manually deleted

## Notes

- Worktrees are created in the parent directory with the pattern `todoish-<ticket-slug>`
- Each worktree gets its own Python virtual environment at `.venv`
- The scripts ensure you're always on the main branch before creating new worktrees
- Branch names follow the format: `farmisen/<ticket-id>-<description>`