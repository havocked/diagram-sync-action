import os
import re
import zlib
import base64
import urllib.parse
import subprocess
from typing import List

def compress_and_encode_plantuml(source: str) -> str:
    """
    Compress, URI-encode, and base64-encode PlantUML source for the plantumlcloud macro.
    """
    encoded = urllib.parse.quote(source)
    compressed = zlib.compress(encoded.encode('utf-8'), level=9)[2:-4]
    b64 = base64.b64encode(compressed).decode('utf-8')
    return b64

def get_svg_size(svg_path: str) -> tuple[int, int]:
    """
    Extract width and height from an SVG file.
    """
    with open(svg_path, 'r') as f:
        content = f.read()
    width_match = re.search(r'width="([\d.]+)(pt|px)"', content)
    height_match = re.search(r'height="([\d.]+)(pt|px)"', content)
    if not width_match or not height_match:
        raise ValueError("SVG width/height not found")
    width, width_unit = width_match.groups()
    height, height_unit = height_match.groups()
    width = float(width)
    height = float(height)
    if width_unit == 'pt':
        width = width * 4 / 3
    if height_unit == 'pt':
        height = height * 4 / 3
    return int(round(width)), int(round(height))

def render_plantuml(input_path: str, output_dir: str):
    """
    Render a PlantUML file to SVG and PNG using the PlantUML CLI.
    """
    for ext in ['svg', 'png']:
        subprocess.run([
            'java', '-jar', 'plantuml.jar',
            f'-t{ext}', '-o', output_dir, input_path
        ], check=True)

def build_diagrams_section(diagrams_dir: str, confluence_client, default_page_id: str) -> str:
    """
    Build the Diagrams section using plantumlcloud macro and upload attachments.
    Uses the page ID from the diagram comment if present, otherwise uses the default_page_id.
    """
    diagrams = []
    for filename in os.listdir(diagrams_dir):
        if filename.endswith('.puml') or filename.endswith('.plantuml'):
            path = os.path.join(diagrams_dir, filename)
            base = os.path.splitext(filename)[0]
            with open(path, 'r') as f:
                source = f.read()
            # Parse page ID from diagram comment
            page_id = parse_page_id_from_diagram(source) or default_page_id
            # Render to SVG/PNG
            render_plantuml(path, diagrams_dir)
            svg_path = os.path.join(diagrams_dir, base + '.svg')
            png_path = os.path.join(diagrams_dir, base + '.png')
            # Upload attachments to the correct page
            confluence_client.upload_attachment(page_id, svg_path, base + '.svg')
            confluence_client.upload_attachment(page_id, png_path, base + '.png')
            # Get SVG size
            width, height = get_svg_size(svg_path)
            # Compress and encode
            data = compress_and_encode_plantuml(source)
            # Macro
            macro = (
                f'<ac:structured-macro ac:name="plantumlcloud">'
                f'<ac:parameter ac:name="toolbar">bottom</ac:parameter>'
                f'<ac:parameter ac:name="filename">{base}.svg</ac:parameter>'
                f'<ac:parameter ac:name="originalHeight">{height}</ac:parameter>'
                f'<ac:parameter ac:name="data">{data}</ac:parameter>'
                f'<ac:parameter ac:name="compressed">true</ac:parameter>'
                f'<ac:parameter ac:name="originalWidth">{width}</ac:parameter>'
                f'<ac:parameter ac:name="revision">1</ac:parameter>'
                f'</ac:structured-macro>'
            )
            diagrams.append(macro)
    if not diagrams:
        return '<h2>Diagrams</h2><p>No diagrams found.</p>'
    return '<h2>Diagrams</h2>' + ''.join(f'<p>{d}</p>' for d in diagrams)

def extract_diagrams_section(body: str, new_diagrams: str) -> str:
    """
    Replace or append the Diagrams section in the Confluence page body.
    :param body: Existing Confluence storage format body
    :param new_diagrams: New Diagrams section content
    :return: Updated body
    """
    import re
    # Look for <h2>Diagrams</h2> and everything after it
    pattern = r'(<h2>Diagrams</h2>)(.*?)(?=(<h2>|<h1>|$))'
    match = re.search(pattern, body, re.DOTALL)
    if match:
        # Replace the section
        start, end = match.span(2)
        return body[:start] + '\n' + new_diagrams[len('<h2>Diagrams</h2>'):] + body[end:]
    else:
        # Append at the end
        return body + '\n' + new_diagrams 

def parse_page_id_from_diagram(source: str) -> str | None:
    """
    Parse the Confluence page ID from a special comment in the PlantUML source.
    The comment format is: @confluence-page-id: 123456
    Returns the page ID as a string, or None if not found.
    """
    import re
    match = re.search(r"@confluence-page-id:\s*([0-9A-Za-z\-_]+)", source)
    if match:
        return match.group(1)
    return None 