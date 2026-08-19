# <p align="center">Custom Extension Repository</p>

<p align="center">
  <a href="https://github.com/salmanbappi/sb-extensions-source">
    <img src="https://img.shields.io/github/directory-file-count/salmanbappi/sb-extensions-source/src/all?label=Total%20Extensions&style=for-the-badge&color=7c3aed&logo=github" alt="Total Extensions" />
  </a>
  <a href="https://github.com/salmanbappi/extensions-repo">
    <img src="https://img.shields.io/badge/dynamic/json?query=count&label=Views&color=7c3aed&style=for-the-badge&url=https%3A%2F%2Fapi.counterapi.dev%2Fv1%2Fsalmanbappi%2Fextensions-repo%2Fup" alt="Repository Views" />
  </a>
  <a href="https://discord.gg/G6g4vBmcXp">
    <img src="https://img.shields.io/badge/Discord-Join%20Server-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Discord" />
  </a>
  <a href="https://github.com/salmanbappi/extensions-repo/actions/workflows/update.yml">
    <img src="https://img.shields.io/github/actions/workflow/status/salmanbappi/extensions-repo/update.yml?branch=main&label=Build%20Status&style=for-the-badge&logo=github-actions" alt="Build Status" />
  </a>
</p>

<p align="center">
  A premium, fully-automated repository for custom app extensions.<br>
  Providing secure and high-speed access to a collection of media extensions and content sources.
</p>

---

## 📲 Setup Guide

Adding this repository to your app is quick and easy:

```mermaid
graph TD
    A[Open Application] --> B[Go to Settings > Browse]
    B --> C[Select Extension Repositories]
    C --> D[Tap Add and enter Repository URL]
    D --> E[Install extensions from the browse tab]
    style A fill:#7c3aed,stroke:#2563eb,stroke-width:2px,color:#fff
    style E fill:#10b981,stroke:#059669,stroke-width:2px,color:#fff
```

1. Open the application on your device.
2. Go to **Settings** ➔ **Browse** ➔ **Extension repositories**.
3. Tap **Add** and paste the following repository index URL:
   ```text
   https://raw.githubusercontent.com/salmanbappi/extensions-repo/main/index.min.json
   ```
4. Navigate to the extensions section to view and install all available extensions.

---

## 💬 Community & Support

Have questions, suggestions, or need help setting up? Join our Discord server to connect with the community and get support:

<p align="center">
  <a href="https://discord.gg/G6g4vBmcXp">
    <img src="https://img.shields.io/badge/Discord-Join%20Server-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Discord Server" />
  </a>
</p>

---

## 🛠️ Repository Specifications

| Specification | Value / Details |
| :--- | :--- |
| **Source Monorepo** | [salmanbappi/sb-extensions-source](https://github.com/salmanbappi/sb-extensions-source) |
| **Repository Index** | [salmanbappi/extensions-repo](https://github.com/salmanbappi/extensions-repo) |
| **Automation** | Rebuilt instantly via **GitHub Actions** workflows |

---

## ⚙️ Maintenance & Updates
This repository is automatically updated whenever new extension versions are compiled in the source monorepo. The CI/CD pipelines automate the extraction, index mapping, and repository metadata regeneration to ensure you always receive the latest releases.