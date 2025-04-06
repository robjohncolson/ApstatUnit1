#!/usr/bin/env python3

import re
import os

# Fix the file path for Windows
# Use raw string to handle backslashes properly
file_path = r"C:\Users\ColsonR\Downloads\apstat\unit 1\index.html"

# Function to find all occurrences of a function definition with line numbers
def find_function_definitions(file_path, function_name):
    print(f"Searching for '{function_name}' in {file_path}")
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        # Use regex to find function definitions
        pattern = rf'async\s+function\s+{function_name}\s*\(\)'
        
        # Get line numbers by splitting content into lines
        lines = content.split('\n')
        
        results = []
        for i, line in enumerate(lines, 1):
            if re.search(pattern, line):
                # Found a function definition
                print(f"Found '{function_name}' at line {i}: {line.strip()}")
                
                # Find the function's closing brace by tracking opening/closing braces
                brace_count = 0
                start_line = i
                end_line = i
                
                # Start from the function definition line
                for j, check_line in enumerate(lines[i-1:], i):
                    # Count opening and closing braces
                    open_braces = check_line.count('{')
                    close_braces = check_line.count('}')
                    
                    if open_braces > 0 and brace_count == 0:
                        # First opening brace found
                        brace_count += open_braces
                    else:
                        brace_count += open_braces - close_braces
                    
                    # If braces are balanced, we've found the end
                    if brace_count <= 0 and j > i and check_line.strip():
                        end_line = j
                        break
                
                # Look for the function comment (usually above the function)
                comment_line = i - 1
                comment_text = ""
                if comment_line > 0 and '//' in lines[comment_line-1]:
                    comment_text = lines[comment_line-1].strip()
                
                # Extract content snippet (first few lines of function body)
                content_start = max(i, i+1)  # Skip function signature
                content_end = min(end_line, content_start + 5)  # Include more lines to catch Supabase
                content_snippet = '\n'.join(lines[content_start-1:content_end])
                
                # Store the complete information
                results.append({
                    'start_line': start_line,
                    'end_line': end_line,
                    'comment': comment_text,
                    'content_snippet': content_snippet,
                    'length': end_line - start_line + 1
                })
                
                # Also look for "supabaseClient" in the full function body
                full_function = '\n'.join(lines[start_line-1:end_line])
                has_supabase = "supabaseClient" in full_function
                results[-1]['uses_supabase'] = has_supabase
        
        return results
    
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

# Find all calculateDynamicQuota function definitions
results = find_function_definitions(file_path, "calculateDynamicQuota")

# Display results summary
if results:
    print("\nFound", len(results), "implementations of calculateDynamicQuota:")
    
    for i, result in enumerate(results, 1):
        print(f"\nFunction #{i}:")
        print(f"  Lines: {result['start_line']} to {result['end_line']} (Length: {result['length']} lines)")
        print(f"  Comment: {result['comment']}")
        print(f"  First few lines:")
        print(f"  {result['content_snippet']}")
        
        # Look for Supabase client query
        if result['uses_supabase']:
            print("  ✓ This version queries Supabase (correct version)")
        else:
            print("  ✗ This version does NOT query Supabase (likely incorrect version)")
        
    print("\nRecommendation:")
    # Sort by whether they use Supabase
    correct_versions = [r for r in results if r['uses_supabase']]
    incorrect_versions = [r for r in results if not r['uses_supabase']]
    
    if correct_versions:
        for r in correct_versions:
            print(f"  - KEEP function at lines {r['start_line']}-{r['end_line']} (uses Supabase)")
    
    if incorrect_versions:
        for r in incorrect_versions:
            print(f"  - DELETE function at lines {r['start_line']}-{r['end_line']} (doesn't use Supabase)")
            
            # Find leading comment for the incorrect function
            if r['comment']:
                comment_line = r['start_line'] - 1
                print(f"    Also delete comment at line {comment_line}: {r['comment']}")
    
    print("\nExample edit command to remove incorrect function:")
    if incorrect_versions:
        incorrect = incorrect_versions[0]
        comment_line = incorrect['start_line'] - 1 if incorrect['comment'] else None
        
        # Create line range for deletion
        start_del = comment_line if comment_line else incorrect['start_line']
        end_del = incorrect['end_line']
        
        print(f"\n  1. Open index.html in a text editor")
        print(f"  2. Delete lines {start_del} to {end_del}")
        print(f"  3. Save the file")
    
    print("\nNote: This script does not modify any files. Use the line numbers above to edit the file manually.")
else:
    print("No implementations of calculateDynamicQuota found.") 