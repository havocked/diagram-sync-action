# Diagram Sync to Confluence

This project automates the process of syncing PlantUML/C4 diagrams from your repository's `docs/diagrams/` folder to a Confluence Cloud page using the REST API v2. It is designed for seamless integration with CI/CD pipelines (e.g., GitHub Actions).

---

## Features
- **Automatic rendering**: Converts PlantUML files to SVG and PNG using PlantUML CLI.
- **Confluence integration**: Uploads diagrams as attachments and embeds them using the `plantumlcloud` macro.
- **Section management**: Updates or creates a "Diagrams" section in your Confluence page.
- **CI/CD ready**: Works out-of-the-box with GitHub Actions.
- **Modular, testable Python code**

---

## Prerequisites
- **Python 3.9+**
- **Java 17+** (required for PlantUML rendering)
- **[PlantUML CLI JAR](https://github.com/plantuml/plantuml/releases)** (downloaded automatically in CI)
- **Confluence Cloud account** with API access

---

## Setup

### 1. **Clone the repository**
```sh
git clone <your-repo-url>
cd <your-repo>
```

### 2. **Install dependencies**
We recommend using [Rye](https://github.com/astral-sh/rye) for Python dependency management:
```sh
rye sync
```

### 3. **Configure environment variables**
Create a `.env` file or set the following variables in your CI/CD secrets:
- `CONFLUENCE_URL`: Base URL (e.g. `https://your-domain.atlassian.net/wiki`)
- `CONFLUENCE_TOKEN`: API token (see [Atlassian API tokens](https://id.atlassian.com/manage-profile/security/api-tokens))
- `CONFLUENCE_USER`: Email of the bot/user
- `CONFLUENCE_PAGE_ID`: Page ID to update (see [How to find Confluence page ID](https://confluence.atlassian.com/doc/locate-a-page-id-163611.html))
- `DIAGRAMS_DIR`: (optional) Path to diagrams folder (default: `docs/diagrams`)

---

## Usage

### **Local Run**
1. Place your `.puml` or `.plantuml` files in `docs/diagrams/`.
2. Run the sync script:
   ```sh
   rye run python -m src.diagram_sync.sync
   ```
3. The script will:
   - Render diagrams to SVG/PNG
   - Upload them as attachments to your Confluence page
   - Update the "Diagrams" section with the correct macro

### **CI/CD (GitHub Actions)**
- The workflow `.github/workflows/diagram_sync.yml` will automatically:
  - Install Java and PlantUML
  - Run the sync script on push to `docs/diagrams/` or on manual dispatch
- Ensure your repository secrets are set for all required environment variables.

---

## How it works
1. **Rendering**: Each `.puml` file is rendered to SVG and PNG using the PlantUML CLI.
2. **Attachment**: The SVG and PNG files are uploaded as attachments to the specified Confluence page.
3. **Macro Embedding**: The PlantUML source is compressed, encoded, and embedded in a `plantumlcloud` macro in the Confluence page body, referencing the uploaded SVG.
4. **Section Update**: The "Diagrams" section of the page is created or updated with the new macros.

---

## Testing
Run tests with:
```sh
pytest
```

---

## Linting
Check code style with:
```sh
ruff check .
```

---

## Troubleshooting
- **Java/PlantUML errors**: Ensure Java 17+ is installed and `plantuml.jar` is present in the working directory.
- **Confluence API errors**: Double-check your API token, user email, and page ID.
- **No diagrams found**: Make sure your `.puml` files are in the correct directory (`docs/diagrams/` by default).
- **CI/CD issues**: Check the Actions logs for details and ensure all secrets are set.

---

## Contributing
Pull requests and issues are welcome! Please ensure code is tested and linted before submitting.

---

## License
[MIT](LICENSE) 