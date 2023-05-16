import os
import json
import PyPDF2
import io

def pdf_to_json(pdf_data):
    # Create a PDF reader object using the input pdf_data
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_data))

    # Extract text from the PDF file
    num_pages = len(pdf_reader.pages)
    content = ''
    metadata = {}

    if num_pages > 0:
        page = pdf_reader.pages[0]
        page_text = page.extract_text()
        if not page_text.startswith('INT.') and not page_text.startswith('EXT.'):
            metadata = page_text
        else:
            content += page_text

    for i in range(1, num_pages):
        page = pdf_reader.pages[i]
        content += page.extract_text()

    # Create a dictionary with the extracted text and metadata
    data = {
        'metadata': metadata,
        'content': content
    }

    # Return the dictionary
    return data
    
def txt_to_json(txt_content):
    data = {
        'content': txt_content
    }
    return data

def fountain_to_json(fountain_content):
    lines = fountain_content.split('\n')
    metadata = {}
    content = ''
    parsing_metadata = True
    current_metadata_key = None
    current_metadata_level = 0
    for line in lines:
        line = line.rstrip()
        if line.startswith(('Title:', 'Author:', 'Source:', 'Draft date:', 'Contact:', 'Copyright:')):
            # Metadata
            key, value = line.split(':', 1)
            current_metadata_key = key.strip()
            metadata[current_metadata_key] = value.strip()
            current_metadata_level = 0
        elif current_metadata_key is not None and line.startswith('\t'):
            # Metadata field continuation with indentation
            level = len(line) - len(line.lstrip('\t'))
            if level > current_metadata_level:
                # The line continues the previous metadata field
                metadata[current_metadata_key] += ' ' + line.lstrip('\t')
            elif level == current_metadata_level:
                # The line is a new line in the current metadata field
                metadata[current_metadata_key] += ' ' + line.lstrip('\t')
            else:
                # The line starts a new metadata field
                key, value = line.lstrip('\t').split(':', 1)
                current_metadata_key = key.strip()
                metadata[current_metadata_key] = value.strip()
                current_metadata_level = level
        else:
            # Content
            if parsing_metadata:
                # Skip lines until the first empty line after metadata
                if not line:
                    parsing_metadata = False
            else:
                # Append content lines
                content += line + '\n'
    # Replace newlines with spaces in metadata values
    for key, value in metadata.items():
        metadata[key] = value.replace('\n', ' ')
    data = {
        'metadata': metadata,
        'content': content
    }
    return data
