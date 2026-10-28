# <p align="center">AniZen & Aniyomi Extension Repository</p>

<p align="center">
  <a href="https://raw.githubusercontent.com/salmanbappi/extensions-repo/main/index.min.json">
    <img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsalmanbappi%2Fextensions-repo%2Fmain%2Findex.min.json&query=%24.length&label=Total%20Extensions&style=for-the-badge&color=7c3aed&logo=android" alt="Total Extensions" />
  </a>
  <a href="https://github.com/salmanbappi/sb-extensions-source/actions/workflows/build_push.yml">
    <img src="https://img.shields.io/github/actions/workflow/status/salmanbappi/sb-extensions-source/build_push.yml?branch=master&label=CI%20Build&style=for-the-badge&logo=github-actions" alt="CI Build Status" />
  </a>
  <a href="https://discord.gg/G6g4vBmcXp">
    <img src="https://img.shields.io/badge/Discord-Join%20Community-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Discord Community" />
  </a>
  <a href="https://github.com/salmanbappi/extensions-repo">
    <img src="https://img.shields.io/badge/dynamic/json?query=count&label=Views&color=7c3aed&style=for-the-badge&url=https%3A%2F%2Fapi.counterapi.dev%2Fv1%2Fsalmanbappi%2Fextensions-repo%2Fup" alt="Repository Views" />
  </a>
</p>

<p align="center">
  Official distribution repository for <b>AniZen</b> and <b>Aniyomi</b> custom extension packages.<br>
  Compiled, verified, cryptographically signed, and deployed automatically via remote GitHub Actions CI.
</p>

---

## 📲 Setup Guide

Add this repository to your app in a few quick steps:

```mermaid
graph TD
    A[Open Application] --> B[Settings ➔ Browse]
    B --> C[Extension Repositories]
    C --> D[Tap Add Repository]
    D --> E[Paste Repository URL]
    E --> F[Browse & Install Extensions]
    style A fill:#7c3aed,stroke:#2563eb,stroke-width:2px,color:#fff
    style F fill:#10b981,stroke:#059669,stroke-width:2px,color:#fff
```

### Repository URLs

Depending on your client, you can use any of the following endpoints:

| Format / Target | URL |
| :--- | :--- |
| **Primary Index** | `https://raw.githubusercontent.com/salmanbappi/extensions-repo/main/index.min.json` |
| **Metadata Endpoint (`repo.json`)** | `https://raw.githubusercontent.com/salmanbappi/extensions-repo/main/repo.json` |
| **Web Catalog** | [https://salmanbappi.github.io/extensions-repo/](https://salmanbappi.github.io/extensions-repo/) |

#### Instructions:
1. Open **AniZen** or **Aniyomi**.
2. Navigate to **Settings** ➔ **Browse** ➔ **Extension repositories**.
3. Tap **Add repository** (+ icon) and paste the Primary Index URL:
   ```text
   https://raw.githubusercontent.com/salmanbappi/extensions-repo/main/index.min.json
   ```
4. Head back to the **Extensions** tab to search, install, and update your sources.

---

## 💬 Community & Support

Need assistance, want to request an extension, or looking to report a broken source? Join our official Discord community:

<p align="center">
  <a href="https://discord.gg/G6g4vBmcXp">
    <img src="https://img.shields.io/badge/Discord-Join%20Community%20Server-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Discord Server" />
  </a>
</p>

---

## 🛠️ Repository Specifications

| Specification | Value / Details |
| :--- | :--- |
| **Source Monorepo** | [salmanbappi/sb-extensions-source](https://github.com/salmanbappi/sb-extensions-source) |
| **Distribution Repo** | [salmanbappi/extensions-repo](https://github.com/salmanbappi/extensions-repo) |
| **API Architecture** | Extensions-lib API v16 baseline (Aniyomi v14–v17 & AniZen compatible) |
| **Languages Supported** | English (`en`), Bangla / BDIX (`bn`), Multi-language (`all`), Arabic (`ar`), Spanish (`es`) |
| **Automation Engine** | Fully automated remote CI/CD via GitHub Actions (`build_push.yml`) |
| **Signing Protocol** | Android APK v2/v3 scheme with SHA-256 trust pinning |

---

## ⚙️ Maintenance & Lifecycle

Extension packages and indices are rebuilt automatically on every commit to the source repository. Upstream changes trigger compilation, Dex code inspection (`Inspector.jar`), icon normalization, and SHA-256 fingerprint validation before deployment.
