import os
import requests
from typing import Dict, Any

class ConfluenceClient:
    """
    Client for interacting with Confluence Cloud REST API v2.
    """
    def __init__(self):
        """
        Initialize the client using environment variables for configuration.
        """
        self.base_url = os.environ["CONFLUENCE_URL"].rstrip('/')
        self.api_token = os.environ["CONFLUENCE_TOKEN"]
        self.user_email = os.environ["CONFLUENCE_USER"]
        self.session = requests.Session()
        self.session.auth = (self.user_email, self.api_token)
        self.session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json"
        })

    def get_page(self, page_id: str) -> Dict[str, Any]:
        """
        Fetch a Confluence page by ID.
        :param page_id: The Confluence page ID
        :return: Page data as a dictionary
        """
        url = f"{self.base_url}/api/v2/pages/{page_id}"
        try:
            resp = self.session.get(url)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to fetch page {page_id}: {e}")

    def update_page(self, page_id: str, title: str, body_storage: str, version: int, space_id: str) -> Dict[str, Any]:
        """
        Update a Confluence page.
        :param page_id: The Confluence page ID
        :param title: The page title
        :param body_storage: The new page content in storage format
        :param version: The current version number
        :param space_id: The space ID
        :return: Updated page data as a dictionary
        """
        url = f"{self.base_url}/api/v2/pages/{page_id}"
        payload = {
            "id": page_id,
            "status": "current",
            "title": title,
            "spaceId": space_id,
            "body": {
                "representation": "storage",
                "value": body_storage
            },
            "version": {
                "number": version + 1
            }
        }
        try:
            resp = self.session.put(url, json=payload)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to update page {page_id}: {e}")

    def upload_attachment(self, page_id: str, file_path: str, file_name: str) -> dict:
        """
        Upload an attachment to a Confluence page.
        """
        url = f"{self.base_url}/api/v2/pages/{page_id}/attachments"
        with open(file_path, 'rb') as f:
            files = {'file': (file_name, f)}
            resp = self.session.post(url, files=files)
            resp.raise_for_status()
            return resp.json() 