# Push QA Agent to GitHub Repository
# Repository: https://github.com/Rishabh23112/OceanAI-QA.git

## Instructions

Run the following commands in your terminal (Git Bash, PowerShell, or Command Prompt):

```bash
# Step 1: Remove any existing remote (if applicable)
git remote remove origin

# Step 2: Add the new repository as remote
git remote add origin https://github.com/Rishabh23112/OceanAI-QA.git

# Step 3: Push to the repository
git push -u origin master
```

## What to Expect

When you run `git push -u origin master`, you will be prompted to authenticate:

1. **Username**: Enter your GitHub username
2. **Password**: Enter your Personal Access Token (NOT your GitHub password)

### How to Create a Personal Access Token

If you don't have a Personal Access Token:

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a name (e.g., "QA Agent Push")
4. Select scope: **repo** (Full control of private repositories)
5. Click "Generate token"
6. **Copy the token** (you won't see it again!)
7. Use this token as your password when pushing

## Alternative: Using GitHub CLI

If you have GitHub CLI installed, you can use:

```bash
gh auth login
git push -u origin master
```

## Verify the Push

After pushing, visit: https://github.com/Rishabh23112/OceanAI-QA

Your code should be visible there!
