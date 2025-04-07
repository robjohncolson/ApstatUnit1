# PDF Filename Standardizer

A set of Python tools to standardize PDF filename nomenclature across different unit directories.

## Tools Included

### 1. standardize_filenames.py
Analyzes and renames PDF files to follow a consistent naming pattern.

### 2. replace_pdf_files_array.py
Updates the `pdfFiles` array in your index.html with standardized file paths.

### 3. update_all_units_data.py
Updates the PDF paths in js/allUnitsData.js for multi-unit applications.

## Usage Process

1. First, run the filename standardizer to analyze your files:
   ```
   python standardize_filenames.py
   ```
   This will interactively guide you through standardizing your PDF filenames.

2. After renaming your files, update the references in your code:

   For single-unit pages:
   ```
   python replace_pdf_files_array.py
   ```
   This will replace the `pdfFiles` array in index.html with the standardized paths.
   
   For multi-unit applications:
   ```
   python update_all_units_data.py
   ```
   This will update the PDF paths in js/allUnitsData.js.

## Standardized Format

The scripts standardize filenames into these formats:

- Section Quizzes: `unit{unit}_section{section}_quiz.pdf`
- Section Answers: `unit{unit}_section{section}_answers.pdf`
- Unit Quizzes: `unit{unit}_{quiz_type}_{part_type}{part_name}.pdf`
- Unit Answers: `unit{unit}_{quiz_type}_{part_type}{part_name}_answers.pdf`

## Requirements

- Python 3.6+
- No external dependencies required

## Example

Before:
```
1.2_quiz.pdf
1.2_answers.pdf
...
unit1_pc_frq_quiz.pdf
```

After:
```
unit1_section1.2_quiz.pdf
unit1_section1.2_answers.pdf
...
unit1_pc_frq_quiz.pdf
```