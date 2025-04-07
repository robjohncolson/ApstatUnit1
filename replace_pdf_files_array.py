import re

def extract_pdf_files_array(file_path):
    """Extract the pdfFiles array content from a JavaScript file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        
    # Find the content between 'const pdfFiles = [' and the closing '];'
    pattern = r'const\s+pdfFiles\s*=\s*\[(.*?)\];'
    match = re.search(pattern, content, re.DOTALL)
    
    if match:
        return match.group(0)
    else:
        raise ValueError(f"Could not find pdfFiles array in {file_path}")

def replace_pdf_files_array(html_file_path, new_array_content):
    """Replace the pdfFiles array in the HTML file with new content."""
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    # Find and replace the pdfFiles array
    pattern = r'const\s+pdfFiles\s*=\s*\[(.*?)\];'
    new_html_content = re.sub(pattern, new_array_content, html_content, flags=re.DOTALL)
    
    # Check if replacement was successful
    if new_html_content == html_content:
        raise ValueError("Could not find pdfFiles array in the HTML file or no changes were made")
    
    with open(html_file_path, 'w', encoding='utf-8') as file:
        file.write(new_html_content)
    
    return True

def main():
    print("PDF Files Array Replacement Tool")
    print("===============================")
    
    try:
        # Extract the new pdfFiles array content
        source_file = "standardized_pdf_files.js"
        new_array_content = extract_pdf_files_array(source_file)
        
        # Replace pdfFiles array in the HTML file
        html_file = "index.html"
        replace_pdf_files_array(html_file, new_array_content)
        
        print(f"✅ Successfully replaced pdfFiles array in {html_file} with content from {source_file}")
        print(f"📝 Don't forget to rename your actual PDF files using standardize_filenames.py")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    main() 