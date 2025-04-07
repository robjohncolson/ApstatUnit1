import re

# Read the file
with open('index_modified.html', 'r', encoding='utf-8') as f:
    content = f.read()
    lines = content.split('\n')

# Finding all instances of index-based capstone buttons
patterns = [
    r'topic\.isCapstone.*?\?\s*\(\s*index\s*===\s*0.*?MCQ Part B PDF',
    r'const linkText = topic\.isCapstone.*?index === 0.*?MCQ Part B PDF'
]

for pattern_idx, pattern in enumerate(patterns):
    print(f"\nSearching for pattern {pattern_idx + 1}:")
    matches = re.finditer(pattern, content, re.DOTALL)
    
    # Track found issues
    issues_found = False
    
    for match in matches:
        issues_found = True
        
        # Calculate line number
        line_num = content[:match.start()].count('\n') + 1
        
        # Get context (10 lines before and after)
        start_line = max(0, line_num - 10)
        end_line = min(len(lines), line_num + 10)
        
        print(f"\nIssue found at line {line_num}:")
        print(f"Context (lines {start_line}-{end_line}):")
        print("```")
        for i in range(start_line, end_line):
            prefix = "→ " if i == line_num - 1 else "  "
            print(f"{prefix}{i+1:4d} | {lines[i]}")
        print("```")
        
        # Extract the problematic code
        code_extract = match.group(0)
        print(f"\nReplacement needed for: ```{code_extract}```")
        
        # Suggest replacement (basic suggestion)
        suggested_replacement = code_extract.replace("index === 0", "quiz.quizId === \"1-capstone_q1\"")
        suggested_replacement = suggested_replacement.replace("index === 1", "quiz.quizId === \"1-capstone_q2\"")
        suggested_replacement = suggested_replacement.replace("index === 2", "quiz.quizId === \"1-capstone_q3\"")
        
        print(f"Suggested replacement: ```{suggested_replacement}```")
    
    if not issues_found:
        print("No issues found for this pattern.")

# Look for one more case - the compact view
compact_pattern = r'linkText = topic\.isCapstone.*?index === 0.*?MCQ Part B PDF'
matches = re.finditer(compact_pattern, content, re.DOTALL)

print("\nSearching for compact view pattern:")
issues_found = False

for match in matches:
    issues_found = True
    
    # Calculate line number
    line_num = content[:match.start()].count('\n') + 1
    
    # Get context (5 lines before and after)
    start_line = max(0, line_num - 5)
    end_line = min(len(lines), line_num + 5)
    
    print(f"\nCompact view issue found at line {line_num}:")
    print(f"Context (lines {start_line}-{end_line}):")
    print("```")
    for i in range(start_line, end_line):
        prefix = "→ " if i == line_num - 1 else "  "
        print(f"{prefix}{i+1:4d} | {lines[i]}")
    print("```")

if not issues_found:
    print("No compact view issues found.") 