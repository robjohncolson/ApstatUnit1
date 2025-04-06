#!/usr/bin/env python3

import sys
import re

def find_function_calls(file_path, function_name):
    try:
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # First look for direct function calls
        pattern1 = r'\b' + re.escape(function_name) + r'\(\);'
        
        # Also look for function calls in a variable or as a parameter
        pattern2 = r'\b' + re.escape(function_name) + r'\('
        
        lines = content.split('\n')
        actual_calls = []
        potential_calls = []
        
        for line_num, line in enumerate(lines, 1):
            # Find direct calls
            if re.search(pattern1, line):
                actual_calls.append((line_num, line.strip()))
            # Find potential calls
            elif re.search(pattern2, line) and not "function " + function_name in line:
                potential_calls.append((line_num, line.strip()))
        
        # Print results
        print(f"Found {len(actual_calls)} actual calls to {function_name}():")
        for line_num, line_text in actual_calls:
            print(f"Line {line_num}: {line_text}")
            
        print(f"\nFound {len(potential_calls)} potential references to {function_name}():")
        for line_num, line_text in potential_calls:
            print(f"Line {line_num}: {line_text}")
        
        return actual_calls, potential_calls
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return [], []

def find_function_definitions(file_path, function_names):
    try:
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        for function_name in function_names:
            # Look for function definition pattern
            pattern = r'function\s+' + re.escape(function_name) + r'\s*\([^)]*\)\s*\{'
            
            matches = re.finditer(pattern, content)
            found = False
            
            for match in matches:
                found = True
                start_pos = match.start()
                # Find the line number
                line_num = content[:start_pos].count('\n') + 1
                # Get a snippet of the function
                line_end = content.find('\n', start_pos)
                snippet = content[start_pos:line_end].strip()
                
                print(f"Found definition of {function_name} at line {line_num}:")
                print(f"  {snippet}")
                
                # Try to find the function body
                open_braces = 1
                pos = content.find('{', start_pos) + 1
                end_pos = pos
                
                while open_braces > 0 and pos < len(content):
                    if content[pos] == '{':
                        open_braces += 1
                    elif content[pos] == '}':
                        open_braces -= 1
                        if open_braces == 0:
                            end_pos = pos
                    pos += 1
                
                # Extract the first few lines of the function body
                body_snippet = content[start_pos:end_pos + 1]
                body_lines = body_snippet.split('\n')
                print(f"  Function body (first few lines):")
                for i, line in enumerate(body_lines[:5]):
                    print(f"    {line.strip()}")
                if len(body_lines) > 5:
                    print(f"    ... ({len(body_lines) - 5} more lines)")
                
            if not found:
                print(f"No definition found for function {function_name}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

def find_local_quota_function():
    file_path = "index.html"
    
    try:
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        # Variables to track function location
        found = False
        start_line = -1
        end_line = -1
        line_number = 0
        
        # Search for the function definition
        for i, line in enumerate(lines):
            line_number = i + 1  # 1-based line numbering
            
            if "function checkLocalQuota()" in line:
                found = True
                start_line = line_number - 1  # Include the comment line above
                
                # Find the end of the function (closing brace)
                for j in range(i, len(lines)):
                    if "}" in lines[j] and not found_nested_function(lines, i, j):
                        end_line = j + 1  # 1-based line number
                        break
                break
        
        if found:
            print(f"Found checkLocalQuota function in {file_path}:")
            print(f"  - Starts at line {start_line}")
            print(f"  - Ends at line {end_line}")
            print("\nFunction content:")
            for i in range(start_line - 1, end_line):
                print(f"{i+1}: {lines[i].rstrip()}")
            
            print("\nThis function can be safely removed since it's a placeholder and")
            print("has been replaced with checkDailyQuotaCompletion.")
        else:
            print(f"The checkLocalQuota function was not found in {file_path}.")
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def found_nested_function(lines, start, current):
    """Check if we're seeing a closing brace for a nested function or object"""
    open_braces = 0
    for i in range(start, current + 1):
        line = lines[i]
        open_braces += line.count('{')
        open_braces -= line.count('}')
    
    # If we've closed all braces, this is the end of our function
    return open_braces > 0

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = "index.html"  # Default path
    
    find_function_calls(file_path, "displayTodaysQuotaStatus")
    find_function_definitions(file_path, ["checkLocalQuota", "displayTodaysQuotaStatus"])
    find_local_quota_function()