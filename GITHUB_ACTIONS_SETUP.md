# GitHub Actions Setup for BookStack Import

This document explains how to set up the automated BookStack import using GitHub Actions.

## Overview

The GitHub Actions workflow automatically:
1. Pulls content from your BookStack instance
2. Processes it according to your navigation configuration
3. Updates the website content
4. Commits and pushes the changes back to the repository

## Setup Instructions

### 1. Configure GitHub Secrets

You need to add the following secrets to your GitHub repository:

1. Go to your repository on GitHub
2. Click on **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret** and add each of the following:

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `BOOKSTACK_BASE_URL` | Base URL of your BookStack instance | `https://wiki.example.com` |
| `BOOKSTACK_TOKEN_ID` | API Token ID from BookStack | `abc123def456` |
| `BOOKSTACK_TOKEN_SECRET` | API Token Secret from BookStack | `xyz789uvw012` |
| `BOOKSTACK_SHELF_SLUG` | Slug of the shelf to import | `my-website-content` |

### 2. Get BookStack API Credentials

To get your BookStack API credentials:

1. Log into your BookStack instance as an admin
2. Go to **Settings** → **API Tokens**
3. Click **Create Token**
4. Give it a name (e.g., "GitHub Actions Import")
5. Copy the **Token ID** and **Token Secret**
6. Add these to your GitHub secrets

### 3. Find Your Shelf Slug

To find your shelf slug:

1. Go to your BookStack shelf
2. Look at the URL: `https://your-bookstack.com/shelves/your-shelf-slug`
3. The slug is the part after `/shelves/`

## Workflow Configuration

The workflow is configured in `.github/workflows/bookstack-import.yml` and runs:

- **Daily at 6 AM UTC** (scheduled)
- **When manually triggered** (workflow_dispatch)
- **When changes are pushed** to the python directory or workflow file

### Customizing the Schedule

To change when the workflow runs, edit the cron expression in the workflow file:

```yaml
schedule:
  - cron: '0 6 * * *'  # Daily at 6 AM UTC
```

Common cron patterns:
- `'0 */6 * * *'` - Every 6 hours
- `'0 9 * * 1-5'` - 9 AM UTC, Monday through Friday
- `'0 0 * * 0'` - Weekly on Sunday at midnight UTC

### Manual Triggering

You can manually trigger the workflow:

1. Go to your repository on GitHub
2. Click **Actions**
3. Select **BookStack Import** workflow
4. Click **Run workflow**

## Local Development

For local development and testing:

### 1. Set Up Environment File

```bash
cd python
cp .env.example .env
# Edit .env with your actual values
```

### 2. Test Environment Setup

```bash
python load_env.py
```

### 3. Run Import Locally

```bash
python bookstack-import.py
```

## Workflow Steps Explained

1. **Checkout repository**: Downloads the latest code
2. **Set up Python**: Installs Python 3.11
3. **Install dependencies**: Installs required Python packages
4. **Run BookStack import**: Executes the import script with secrets as environment variables
5. **Commit and push changes**: Automatically commits any changes and pushes them back

## Troubleshooting

### Workflow Fails with "Missing environment variables"

- Check that all four secrets are set in GitHub repository settings
- Verify the secret names match exactly (case-sensitive)

### Workflow Fails with "API Error"

- Verify your BookStack URL is correct and accessible
- Check that your API tokens are valid and not expired
- Ensure the shelf slug exists and is accessible with your API credentials

### No Changes Committed

- The workflow only commits if there are actual changes to the website content
- Check the workflow logs to see if the import ran successfully
- Verify your navigation configuration is correct

### Permission Errors

The workflow needs write permissions to push changes. This should be enabled by default, but if you encounter issues:

1. Go to **Settings** → **Actions** → **General**
2. Under **Workflow permissions**, select **Read and write permissions**

## Security Considerations

- API tokens are stored as encrypted GitHub secrets
- The workflow only has access to the repository it's running in
- Tokens are never logged or exposed in workflow output
- Consider using a dedicated BookStack user account with minimal permissions

## Monitoring

To monitor the workflow:

1. Go to **Actions** tab in your repository
2. Click on individual workflow runs to see detailed logs
3. Set up notifications for workflow failures in your GitHub settings

## Advanced Configuration

### Custom Navigation Configuration

The workflow uses the `navigation_config.json` file in the python directory. To customize:

1. Edit the file directly in the repository, or
2. Use the management script locally and commit changes:

```bash
python manage_navigation.py add my-book-slug my-folder
git add python/navigation_config.json
git commit -m "Update navigation configuration"
git push
```

### Multiple Environments

To set up different configurations for different environments (e.g., staging vs production), you can:

1. Create separate workflow files
2. Use different secret names
3. Use different navigation configuration files
