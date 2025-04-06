#!/usr/bin/env python3

# This script analyzes an HTML file to find and fix duplicate function definitions
# It generates a new file with the fixes applied, without modifying the original

import os
import re

# Input and output file paths
input_file = "index.html"
output_file = "index.html.fixed"

# Function to extract regions from file
def extract_regions(filename, start_line, end_line):
    """Extract a region of text from file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        # Check bounds
        if start_line < 1:
            start_line = 1
        if end_line > len(lines):
            end_line = len(lines)
            
        # Extract the content (convert to 0-based indexing)
        return lines[start_line-1:end_line]
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

# Function to analyze file
def analyze_html_file(filename):
    """Find the conflicting calculateDynamicQuota functions"""
    print(f"Analyzing {filename}...")
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.readlines()
        
        # Find the duplicate function declarations
        function_pattern = r'async\s+function\s+calculateDynamicQuota\s*\(\)'
        
        function_lines = []
        for i, line in enumerate(content, 1):
            if re.search(function_pattern, line):
                function_lines.append(i)
                print(f"Found function declaration at line {i}: {line.strip()}")
        
        if len(function_lines) < 2:
            print(f"Found only {len(function_lines)} implementations - expected at least 2.")
            return None
            
        # Find the function bounds
        functions = []
        for start_line in function_lines:
            # Look for the previous comment line
            comment_line = start_line - 1
            while comment_line > 0 and '//' in content[comment_line-1]:
                comment_line -= 1
                
            # Find the end of the function
            brace_count = 0
            end_line = start_line
            
            for j in range(start_line, len(content)+1):
                if j == len(content)+1:
                    break
                    
                line = content[j-1]
                open_braces = line.count('{')
                close_braces = line.count('}')
                
                if open_braces > 0 and brace_count == 0:
                    brace_count = open_braces
                else:
                    brace_count += open_braces - close_braces
                
                if brace_count <= 0 and j > start_line and line.strip():
                    end_line = j
                    break
            
            # Check if the function uses Supabase
            function_content = ''.join(content[start_line-1:end_line])
            has_supabase = 'supabaseClient' in function_content
            
            functions.append({
                'start_line': comment_line if comment_line < start_line else start_line,
                'declaration_line': start_line,
                'end_line': end_line,
                'uses_supabase': has_supabase,
                'content': ''.join(content[start_line-1:end_line])
            })
        
        return {
            'functions': functions,
            'total_lines': len(content)
        }
        
    except Exception as e:
        print(f"Error analyzing file: {e}")
        return None

# Function to create a fixed file
def create_fixed_file(input_file, output_file, analysis):
    """Create a fixed file with the incorrect function removed"""
    if not analysis:
        print("No analysis data available")
        return False
        
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.readlines()
            
        # Group the functions by whether they use Supabase
        correct_functions = [f for f in analysis['functions'] if f['uses_supabase']]
        incorrect_functions = [f for f in analysis['functions'] if not f['uses_supabase']]
        
        if not correct_functions:
            print("No correct functions found (using Supabase)")
            return False
            
        if not incorrect_functions:
            print("No incorrect functions found (not using Supabase)")
            return False
            
        print(f"\nFound {len(correct_functions)} correct and {len(incorrect_functions)} incorrect functions")
        
        # Get the regions to remove
        regions_to_remove = []
        for func in incorrect_functions:
            regions_to_remove.append((func['start_line'], func['end_line']))
            print(f"Will remove lines {func['start_line']}-{func['end_line']}")
        
        # Sort and merge overlapping regions
        regions_to_remove.sort()
        merged_regions = []
        for region in regions_to_remove:
            if not merged_regions or region[0] > merged_regions[-1][1]:
                merged_regions.append(region)
            else:
                merged_regions[-1] = (merged_regions[-1][0], max(merged_regions[-1][1], region[1]))
        
        # Create the new content without the incorrect functions
        new_content = []
        last_end = 0
        
        for start, end in merged_regions:
            # Add content from last_end to start-1
            new_content.extend(content[last_end:start-1])
            last_end = end
            
        # Add the remaining content
        new_content.extend(content[last_end:])
        
        # Write to new file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(new_content)
            
        print(f"\nCreated fixed file: {output_file}")
        print(f"Original file: {input_file} is unchanged")
        
        return True
        
    except Exception as e:
        print(f"Error creating fixed file: {e}")
        return False

# Generate shell commands to apply the fix
def generate_shell_commands(input_file, output_file):
    """Generate commands that can be copy-pasted to apply the fix"""
    commands = []
    
    # Windows command
    commands.append(f"copy {output_file} {input_file}")
    
    # Unix/Mac command
    commands.append(f"mv {output_file} {input_file}")
    
    print("\nTo apply the fix, run ONE of these commands:")
    print("\nFor Windows:")
    print(f"  {commands[0]}")
    print("\nFor Unix/Mac:")
    print(f"  {commands[1]}")
    
    print("\nOr manually copy the content from the fixed file to the original.")

# Main function
def main():
    print(f"Analyzing HTML file: {input_file}")
    
    # Check if file exists
    if not os.path.isfile(input_file):
        print(f"Error: File not found: {input_file}")
        return
    
    # Analyze the file
    analysis = analyze_html_file(input_file)
    
    if analysis:
        print(f"\nTotal lines in file: {analysis['total_lines']}")
        print(f"Found {len(analysis['functions'])} implementations of calculateDynamicQuota")
        
        # Display function details
        for i, func in enumerate(analysis['functions'], 1):
            print(f"\nFunction #{i}:")
            print(f"  Lines: {func['start_line']} to {func['end_line']}")
            print(f"  Uses Supabase: {'Yes (correct)' if func['uses_supabase'] else 'No (incorrect)'}")
        
        # Create fixed file
        if create_fixed_file(input_file, output_file, analysis):
            generate_shell_commands(input_file, output_file)
    
if __name__ == "__main__":
    main() 