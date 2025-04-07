import re

# Read the file
with open('index_modified.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the main issue at line 3137-3139
pattern = r'const linkText = topic\.isCapstone && topic\.quizzes\.length > 1\s*\?\s*\(index === 0.*?MCQ Part B PDF"\)'
replacement = 'const linkText = topic.isCapstone && topic.quizzes.length > 1\n                            ? (quiz.quizId === "1-capstone_q1" ? "FRQ Questions PDF" : quiz.quizId === "1-capstone_q2" ? "MCQ Part A PDF" : "MCQ Part B PDF")'

# Count occurrences before replacement
original_count = len(re.findall(pattern, content))
print(f"Found {original_count} instances of the pattern to replace")

# Apply the replacement
modified_content = re.sub(pattern, replacement, content)

# Count occurrences after replacement to verify
remaining_count = len(re.findall(pattern, modified_content))
print(f"After replacement: {remaining_count} instances remaining")

if original_count > 0 and remaining_count == 0:
    print("Changes successfully prepared")
    
    # Write to a new file to avoid direct modification
    with open('index_fixed.html', 'w', encoding='utf-8') as f:
        f.write(modified_content)
    print("Fixed version saved to index_fixed.html")
    
    # Print out the instructions for manual replacement
    print("\nTo apply the fix:")
    print("1. Review index_fixed.html to verify the changes")
    print("2. If satisfied, you can rename index_fixed.html to index_modified.html")
else:
    print("No changes made or pattern not found exactly as expected") 