from bs4 import BeautifulSoup
import os
import fitz  # PyMuPDF

def parse_file_content(file_path: str, content: bytes) -> str:
    """
    Parses file content based on extension.
    Supports HTML, Markdown, Text, JSON, and PDF files.
    Returns a string representation of the content.
    """
    filename = os.path.basename(file_path)
    ext = os.path.splitext(filename)[1].lower()
    
    if ext == '.html':
        soup = BeautifulSoup(content, 'html.parser')
        # Remove scripts and styles for cleaner embedding
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text(separator=' ', strip=True)
        return f"File: {filename}\nType: HTML\nContent: {text}"
    
    elif ext == '.pdf':
        try:
            # Open PDF from bytes
            pdf_document = fitz.open(stream=content, filetype="pdf")
            text = ""
            
            # Extract text from each page
            for page_num in range(pdf_document.page_count):
                page = pdf_document[page_num]
                text += page.get_text()
            
            pdf_document.close()
            return f"File: {filename}\nType: PDF\nContent: {text.strip()}"
        except Exception as e:
            print(f"Error parsing PDF {filename}: {e}")
            return f"File: {filename}\nType: PDF\nContent: (Error extracting PDF content)"
    
    elif ext in ['.md', '.txt', '.json']:
        return f"File: {filename}\nType: Text\nContent: {content.decode('utf-8')}"
    
    else:
        return f"File: {filename}\nType: Unknown\nContent: (Skipped binary or unsupported file)"

def clean_html_for_llm(html_content: str) -> str:
    """
    Cleans HTML content to reduce token usage for LLM processing.
    Preserves structure (IDs, classes, inputs) but removes scripts, styles, SVGs, and comments.
    """
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove heavy tags that aren't needed for Selenium selectors
        for tag in soup(["script", "style", "svg", "noscript", "meta", "link"]):
            tag.decompose()
            
        # Remove comments
        from bs4 import Comment
        for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
            comment.extract()
            
      
        return str(soup)
    except Exception as e:
        print(f"Error cleaning HTML: {e}")
        return html_content
