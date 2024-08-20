---
title: Self-hosting SOFA
layout: doc
---

# Quick Start Guide: Self-Hosted SOFA

This guide helps you set up a self-hosted SOFA feed and website, starting with hosting on GitHub Pages. You have the option to use the GitHub web interface or clone the repository locally, make the necessary changes, and trigger the deployment workflows. Follow these steps to get everything up and running.

Guides for other platforms like GitLab will be added in the future.

## SOFA on GitHub (Web UI Only)

Set up your self-hosted SOFA feed and website in a few easy steps with GitHub's web interface. This guide is perfect for anyone looking to streamline their SOFA running via GitHub web UI.

### Step 1: Fork the SOFA Repository

1. **Fork the SOFA Repository**:

   - Visit the [SOFA repository](https://github.com/macadmins/sofa) on GitHub.
   - Click the "Fork" button in the top-right corner to create a copy under your GitHub account.

### Step 2: Configure Deployment Settings

#### Option 1: GitHub Pages Subdomain Deployment

**Edit `config.mts`**: To edit the file directly in GitHub's web interface, follow these steps:

1. Navigate to (`web/.vitepress/config.mts`) in your forked repository.
2. Click on the file config.mts.
3. Click on the pencil icon (✏️) to edit the file directly on the GitHub website.
4. Update the `base` section with your repository name:

    ```typescript
    import { defineConfig } from 'vitepress';

    export default defineConfig({
        base: '/sofa/', // Use 'sofa' here as shown or replace with your actual repository name if it's different
        title: 'SOFA - by Mac Admins Open Source',
    ```

5. Click "Commit changes" to save.

#### Option 2: Custom Domain Deployment

**No Changes Needed in `config.mts`**:

- If using a custom domain (e.g., `https://sofa.acme.com`), no changes are needed in the `config.mts` file.
  
- **Note**: You need to set up a CNAME file in your repository and configure DNS settings to point your domain to GitHub Pages. For more details, refer to the [GitHub Pages Custom Domain Guide](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site).

### Step 3: Edit the Workflow File

**Locate and Edit `run_docker_macos_workflow.yml`**:

1. In your repository, go to `.github/workflows/` and open `run_docker_macos_workflow.yml`.
2. Click the pencil icon (✏️) to edit.  
**Make the Following Changes**: To ensure the GitHub action works for self-hosted, remove the following unnecessary steps that may fail:
    - **Remove Un prettify jsons**:

        ```yaml
        - name: Un prettify jsons
        ```

    - **Remove S3cmd Setup**:

        ```yaml
        - name: Set up S3cmd cli tool
        ```

    - **Remove Gzipping JSON Files**:

        ```yaml
        - name: Create gzipped jsons
        ```

    - **Remove DigitalOcean Upload Steps**:

        ```yaml
        - name: Upload to Digital Ocean (Beta Feed)
        ```

        ```yaml
        - name: Upload to Digital Ocean (Production Feed)
        ```

3. **Commit Changes**:
   - Click "Commit changes" to save your edits.

### Step 4: Deploy and Verify

1. **Enable GitHub Pages**:
   - Go to **Settings - Pages** in your GitHub repository.
   - In the **Build and Deployment** section, and select **Source** - **GitHub Actions**.
   - It is also recommended to check the **Enforce HTTPS** box.

2. **Trigger the Workflow**:
   - Go to the "Actions" tab in your repository.
   - Select the workflow "macOS and iOS SOFA Scan" and click "Run workflow" to trigger it manually.
   - When that workflow has finished, it should automatically trigger the workflow "Deploy site to GitHub Pages".

3. **Verify the Deployment**:
   - After the workflow completes, check that the SOFA site is deployed correctly on your custom domain or GitHub Pages subdomain. A link to the site is shown in **Settings - Pages**.
   - Ensure that all data feeds and the VitePress site are accessible and functioning properly.

### Final Note

This guide covers the basics of setting up a self-hosted SOFA site on GitHub. Scheduled updates and the fetch CVE action details are out of the scope of this guide.

## SOFA on GitHub (Local Edits via Terminal/GitHub Desktop)

This guide shows you how to clone the SOFA repository locally with Terminal or GitHub Desktop, make your edits, and push the changes back to GitHub. It's ideal for users who prefer to work in a local development environment.

### Step 1: Fork the SOFA Repository

1. **Fork the SOFA Repository**:
   - Visit the [SOFA repository](https://github.com/macadmins/sofa) on GitHub.
   - Click the "Fork" button in the top-right corner to create a copy under your GitHub account.

### Step 2: Clone the Repository Locally

#### Option 1: Clone with GitHub Desktop

1. **Open GitHub Desktop**:
   - Go to the main page of your forked repository on GitHub.
   - Click the green "Code" button and select "Open with GitHub Desktop."
   - Follow the prompts to clone the repository to your local machine.

#### Option 2: Clone with Terminal

1. **Clone the Repository via Terminal**:
   - Copy the repository URL by clicking the green "Code" button and selecting the HTTPS URL.
   - Open your terminal and run:

     ```bash
     git clone https://github.com/your-username/sofa.git
     ```

   - Replace `your-username` with your GitHub username.

### Step 3: Configure Deployment Settings Locally

#### Option 1: GitHub Pages Subdomain Deployment

1. **Edit `config.mts`**:
   - Navigate to the `web/.vitepress/config.mts` file in your cloned repository using your text editor.
   - Modify the `base` option to match your repository name:

     ```typescript
     import { defineConfig } from 'vitepress';

     export default defineConfig({
       base: '/sofa/', // Use 'sofa' here as shown or replace with your actual repository name if it's different
       title: 'SOFA - by Mac Admins Open Source',
     ```

   - Save the file.

2. **Commit and Push Changes**:
   - Open your terminal in the repository directory and run, or use GitHub Desktop:

     ```bash
     git add config.mts
     git commit -m "Update base path for GitHub Pages deployment"
     git push
     ```

#### Option 2: Custom Domain Deployment

1. **No Changes Needed in `config.mts`**:
   - If using a custom domain (e.g., `https://sofa.acme.com`), no changes are needed in the `config.mts` file.

2. **Commit and Push (If Applicable)**:
   - If you made any changes, commit and push as shown above.

- **Note**: You need to set up a CNAME file in your repository and configure DNS settings to point your domain to GitHub Pages. For more details, refer to the [GitHub Pages Custom Domain Guide](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site).

### Step 4: Edit the "macOS and iOS SOFA Scan" Workflow File Locally

1. **Locate and Edit `run_docker_macos_workflow.yml`**:
   - Open the `.github/workflows/run_docker_macos_workflow.yml` file in your text editor.

2. **Make the Following Changes**:

   To ensure the GitHub Action works for self-hosted deployments, remove the following unnecessary steps that may fail:

   - **Remove Unprettify JSONs**:

     ```yaml
     - name: Unprettify JSONs
     ```

   - **Remove S3cmd Setup**:

     ```yaml
     - name: Set up S3cmd cli tool
     ```

   - **Remove Gzipping JSON Files**:

     ```yaml
     - name: Create gzipped jsons
     ```

   - **Remove DigitalOcean Upload Steps**:

     ```yaml
     - name: Upload to Digital Ocean (Beta Feed)
     ```

     ```yaml
     - name: Upload to Digital Ocean (Production Feed)
     ```

3. **Commit and Push Changes**:
   - In your terminal, run:

     ```bash
     git add .github/workflows/run_docker_macos_workflow.yml
     git commit -m "Refine workflow for self-hosted SOFA deployment"
     git push
     ```

### Step 5: Deploy and Verify

1. **Enable GitHub Pages**:
   - Go to **Settings - Pages** in your GitHub repository.
   - In the **Build and Deployment** section, and select **Source** - **GitHub Actions**.
   - It is also recommended to check the **Enforce HTTPS** box.

2. **Trigger the Workflow**:
   - Go to the "Actions" tab in your GitHub repository.
   - Select the workflow "macOS and iOS SOFA Scan" and click "Run workflow" to trigger it manually.
   - When that workflow has finished, it should automatically trigger the workflow "Deploy site to GitHub Pages".

3. **Verify the Deployment**:
   - After the workflow completes, check that the SOFA site is deployed correctly on your custom domain or GitHub Pages subdomain. A link to the site is shown in **Settings - Pages**.
   - Ensure that all data feeds and the VitePress site are accessible and functioning properly.

### Final Note

This guide covers the basics of setting up a self-hosted SOFA site on GitHub with local edits. Scheduled updates and the fetch CVE action details are out of the scope of this guide. Please refer to the relevant documentation for those advanced configurations.
