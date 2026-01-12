# SalmanBappi's Aniyomi Extensions Repository

This is a dedicated repository for custom Aniyomi/Anikku extensions, primarily focusing on BDIX-based streaming services and local content providers.

## How to Add to Aniyomi / Anikku

To use these extensions in Aniyomi or Anikku:

1.  Open **Aniyomi** or **Anikku**.
2.  Go to **Settings** -> **Browse** -> **Extension repositories**.
3.  Click **Add**.
4.  Enter the following URL:
    ```
    https://raw.githubusercontent.com/salmanbappi/extensions-repo/main/index.min.json
    ```
5.  After adding, you can find the extensions in the **Extensions** tab under the **Anime** category.

## Available Extensions

Currently, this repository hosts the following extensions:

- **DhakaFlix / DhakaFlix 2**: Support for DhakaFlix (BDIX) streaming.
- **InfoMedia**: Multi-language content provider (Rebranded from MediaServer).
- **FtpBd**: Support for FtpBd.net.
- **Dflix**: Support for Dflix streaming.
- **Nagordola**: Support for Nagordola content.
- **Udvash**: Support for Udvash educational content.
- **Bas Play**: Support for Bas Play streaming.
- **Amader FTP**: Support for Amader FTP.
- **Cineplex BD**: Support for Cineplex BD movies and series.

## Technical Maintenance Notes (Jan 2026 Fixes)

The following critical issues were resolved to ensure compatibility with **Anikku** and **Mihon**:

1.  **Source ID Stability**: All extensions now use **hardcoded 64-bit Long IDs** in the Kotlin source files. This prevents extensions from becoming "Obsolete" when renamed or moved.
2.  **Author Metadata**: Added the `author` field to `build.gradle` and `AndroidManifest.xml`. This allows Anikku to correctly display the developer name (`@salmanbappi`).
3.  **Signing Fingerprint**: Standardized all extensions to use a consistent release keystore. The repository metadata (`repo.json`) is synchronized with the SHA-256 fingerprint: `c7ebe223044970f2f9738f600dc25c180d3ed03994e088aaf5709338c57b93af`.
4.  **Metadata Synchronization**: The `generate_repo.py` script was updated to ensure the `sources` array in `index.min.json` perfectly matches the IDs hardcoded in the APKs.
5.  **Cineplex BD Fix**: Corrected a configuration error where release builds were using a debug signing key.

## Technical Information

- **Repository Website**: [https://github.com/salmanbappi/extensions-repo](https://github.com/salmanbappi/extensions-repo)

## Maintenance

This repository is automatically updated via GitHub Actions. When a new version of an extension is built in its respective repository, it is pushed here, and the `index.min.json` is regenerated.
