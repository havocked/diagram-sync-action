import os
from diagram_sync.confluence_client import ConfluenceClient
from diagram_sync.utils import extract_diagrams_section, build_diagrams_section

def main():
    """
    Main entry point for syncing diagrams to Confluence.
    """
    confluence_page_id = os.environ["CONFLUENCE_PAGE_ID"]
    diagrams_dir = os.environ.get("DIAGRAMS_DIR", "docs/diagrams")

    client = ConfluenceClient()

    # 1. Get current page content
    page = client.get_page(confluence_page_id)
    body = page["body"]["storage"]["value"]
    title = page["title"]
    version = page["version"]["number"]
    space_id = page["spaceId"]

    # 2. Extract or create Diagrams section
    new_diagrams = build_diagrams_section(diagrams_dir, client, confluence_page_id)
    updated_body = extract_diagrams_section(body, new_diagrams)

    # 3. Update page if changed
    if updated_body != body:
        client.update_page(confluence_page_id, title, updated_body, version, space_id)
        print("Confluence page updated.")
    else:
        print("No changes detected.")

if __name__ == "__main__":
    main() 