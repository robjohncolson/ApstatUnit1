import re
import json

def extract_pdf_paths_from_standardized(file_path):
    """Extract the PDF paths from standardized_pdf_files.js."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Extract the pdfFiles array
    array_pattern = r'const\s+pdfFiles\s*=\s*\[(.*?)\];'
    match = re.search(array_pattern, content, re.DOTALL)
    
    if not match:
        raise ValueError(f"Could not find pdfFiles array in {file_path}")
    
    # Create a mapping of topic IDs to their standardized PDF paths
    mapping = {}
    
    # Extract all topic objects
    topic_pattern = r'{(.*?id:\s*"([^"]+)".*?quizzes:\s*\[(.*?)\].*?)}'
    topics = re.finditer(topic_pattern, match.group(1), re.DOTALL)
    
    for topic_match in topics:
        topic_id = topic_match.group(2)
        quizzes_section = topic_match.group(3)
        
        # Extract questionPdf and answersPdf paths
        pdf_pattern = r'questionPdf:\s*"([^"]+)".*?answersPdf:\s*"?([^",}]+)?'
        pdf_matches = re.finditer(pdf_pattern, quizzes_section, re.DOTALL)
        
        topic_pdfs = []
        for pdf_match in pdf_matches:
            question_pdf = pdf_match.group(1) if pdf_match.group(1) != "null" else None
            answers_pdf = pdf_match.group(2) if pdf_match.group(2) and pdf_match.group(2) != "null" else None
            
            if question_pdf or answers_pdf:
                topic_pdfs.append({
                    "questionPdf": question_pdf,
                    "answersPdf": answers_pdf
                })
        
        if topic_pdfs:
            mapping[topic_id] = topic_pdfs
    
    return mapping

def update_all_units_data(file_path, pdf_mapping):
    """Update the js/allUnitsData.js file with standardized PDF paths."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Find each unit's topics array
    unit_pattern = r'unitId:\s*\'(unit\d+)\'.*?topics:\s*\[(.*?)\]'
    units = list(re.finditer(unit_pattern, content, re.DOTALL))
    
    # Store the modified content
    modified_content = content
    
    # Process each unit
    for unit_match in units:
        unit_id = unit_match.group(1)
        unit_number = unit_id.replace('unit', '')
        topics_section = unit_match.group(2)
        
        # Find each topic in this unit
        topic_pattern = r'{(.*?id:\s*"([^"]+)".*?quizzes:\s*\[(.*?)\].*?)}'
        topics = list(re.finditer(topic_pattern, topics_section, re.DOTALL))
        
        # Keep track of changes
        updated_topics_section = topics_section
        
        # Process each topic
        for topic_match in topics:
            topic_content = topic_match.group(1)
            topic_id = topic_match.group(2)
            quizzes_section = topic_match.group(3)
            
            # If we have standardized paths for this topic
            if topic_id in pdf_mapping:
                # Find and replace each PDF path
                for i, quiz_pdfs in enumerate(pdf_mapping[topic_id]):
                    # Find the quiz entry
                    quiz_pattern = r'({.*?questionPdf:\s*"[^"]*".*?answersPdf:\s*"?[^",}]*"?.*?})'
                    quiz_matches = list(re.finditer(quiz_pattern, quizzes_section, re.DOTALL))
                    
                    if i < len(quiz_matches):
                        quiz_content = quiz_matches[i].group(1)
                        updated_quiz_content = quiz_content
                        
                        # Update questionPdf
                        if quiz_pdfs.get("questionPdf"):
                            updated_quiz_content = re.sub(
                                r'(questionPdf:\s*")([^"]*)(")' if "null" not in quiz_content else r'(questionPdf:\s*)(null)',
                                r'\1' + quiz_pdfs["questionPdf"] + r'\3',
                                updated_quiz_content
                            )
                        
                        # Update answersPdf
                        if quiz_pdfs.get("answersPdf"):
                            updated_quiz_content = re.sub(
                                r'(answersPdf:\s*")([^"]*)(")' if "null" not in quiz_content else r'(answersPdf:\s*)(null)',
                                r'\1' + quiz_pdfs["answersPdf"] + r'\3',
                                updated_quiz_content
                            )
                        
                        # Replace in quizzes section
                        quizzes_section = quizzes_section.replace(quiz_content, updated_quiz_content)
                
                # Update topic with new quizzes section
                updated_topic_content = topic_match.group(0).replace(topic_match.group(3), quizzes_section)
                updated_topics_section = updated_topics_section.replace(topic_match.group(0), updated_topic_content)
        
        # Replace the original topics section in the content
        modified_content = modified_content.replace(topics_section, updated_topics_section)
    
    # Write the updated content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(modified_content)
    
    return True

def main():
    print("AllUnitsData PDF Paths Update Tool")
    print("=================================")
    
    try:
        # Extract PDF paths from standardized file
        source_file = "standardized_pdf_files.js"
        pdf_mapping = extract_pdf_paths_from_standardized(source_file)
        
        # Update PDF paths in allUnitsData.js
        target_file = "js/allUnitsData.js"
        update_all_units_data(target_file, pdf_mapping)
        
        print(f"✅ Successfully updated PDF paths in {target_file}")
        print(f"📝 Don't forget to rename your actual PDF files using standardize_filenames.py")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    main() 