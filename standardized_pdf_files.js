// Standardized PDF file paths using the new naming convention
// Original: pdfs/unit1/1.2_quiz.pdf -> New: pdfs/unit1/unit1_section1.2_quiz.pdf

// To use these standardized paths:
// 1. Rename your PDF files using the standardize_filenames.py script
// 2. Replace the PDF paths in your index.html file with these standardized paths

const pdfFiles = [
    {
        id: "1-1",
        name: "Topic 1.1",
        description: "Introducing Statistics: What Can We Learn from Data?",
        videos: [
            {
                url: "https://apclassroom.collegeboard.org/d/708w9bpk60?sui=33,1",
                altUrl: "https://drive.google.com/file/d/1wEbNmDM4KBUWvvoRoQIgIYKYWxG3x6Cv/view?usp=drive_link",
                completed: false,
                completionDate: null
            }
        ],
        quizzes: [],
        current: false
    },
    {
        id: "1-2",
        name: "Topic 1.2",
        description: "The Language of Variation: Variables",
        videos: [
            {
                url: "https://apclassroom.collegeboard.org/d/o7atnjt521?sui=33,1",
                altUrl: "https://drive.google.com/file/d/1cJ3a5DSlZ0w3vta901HVyADfQ-qKVQcD/view?usp=drive_link",
                completed: false,
                completionDate: null
            }
        ],
        quizzes: [
            {
                questionPdf: "pdfs/unit1/unit1_section1.2_quiz.pdf",
                answersPdf: "pdfs/unit1/unit1_section1.2_answers.pdf",
                quizId: "1-2_q1",
                completed: false,
                completionDate: null
            }
        ],
        current: false
    },
    {
        id: "1-3",
        name: "Topic 1.3",
        description: "Representing a Categorical Variable with Tables",
        videos: [
            {
                url: "https://apclassroom.collegeboard.org/d/5umo3jmlhy?sui=33,1",
                altUrl: "https://drive.google.com/file/d/1F9_jLryrjHyXUN21eZmNHrTIGATBhhDw/view?usp=drive_link",
                completed: false,
                completionDate: null
            }
        ],
        quizzes: [
            {
                questionPdf: "pdfs/unit1/unit1_section1.3_quiz.pdf",
                answersPdf: "pdfs/unit1/unit1_section1.3_answers.pdf",
                quizId: "1-3_q1",
                completed: false,
                completionDate: null
            }
        ],
        current: false
    },
    {
        id: "1-4",
        name: "Topic 1.4",
        description: "Representing a Categorical Variable with Graphs",
        videos: [
            {
                url: "https://apclassroom.collegeboard.org/d/nnomwwtzqc?sui=33,1",
                altUrl: "https://drive.google.com/file/d/1vo3zsZu4wZAAkf-fPTuCmKXudgs0Gnl4/view?usp=drive_link",
                completed: false,
                completionDate: null
            },
            {
                url: "https://apclassroom.collegeboard.org/d/yd2t974opr?sui=33,1",
                altUrl: "https://drive.google.com/file/d/1Hp7GWdTzjPQNvcAnnrrt_QYXV27gCEHh/view?usp=drive_link",
                completed: false,
                completionDate: null
            }
        ],
        quizzes: [
            {
                questionPdf: "pdfs/unit1/unit1_section1.4_quiz.pdf",
                answersPdf: "pdfs/unit1/unit1_section1.4_answers.pdf",
                quizId: "1-4_q1",
                completed: false,
                completionDate: null
            }
        ],
        current: false
    },
    {
        id: "1-5",
        name: "Topic 1.5",
        description: "Representing a Quantitative Variable with Graphs",
        videos: [
            {
                url: "https://apclassroom.collegeboard.org/d/o142s0yu7e?sui=33,1",
                altUrl: "https://drive.google.com/file/d/1jlopxNducZRaqXtU9c2NvXxq_tGK90ue/view?usp=drive_link",
                completed: false,
                completionDate: null
            }
        ],
        quizzes: [
            {
                questionPdf: "pdfs/unit1/unit1_section1.5_quiz.pdf",
                answersPdf: "pdfs/unit1/unit1_section1.5_answers.pdf",
                quizId: "1-5_q1",
                completed: false,
                completionDate: null
            }
        ],
        current: false
    },
    {
        id: "1-6",
        name: "Topic 1.6",
        description: "Describing the Distribution of a Quantitative Variable",
        videos: [
            {
                url: "https://apclassroom.collegeboard.org/d/q0wwgrkzqb?sui=33,1",
                altUrl: "https://drive.google.com/file/d/1oWGqzk4meQ6HuXE-mTDHMStp-qOGDUZJ/view?usp=drive_link",
                completed: false,
                completionDate: null
            }
        ],
        quizzes: [
            {
                questionPdf: "pdfs/unit1/unit1_section1.6_quiz.pdf",
                answersPdf: "pdfs/unit1/unit1_section1.6_answers.pdf",
                quizId: "1-6_q1",
                completed: false,
                completionDate: null
            }
        ],
        current: false
    },
    {
        id: "1-7",
        name: "Topic 1.7",
        description: "Summary Statistics for a Quantitative Variable",
        videos: [
            {
                url: "https://apclassroom.collegeboard.org/d/99bxa5glos?sui=33,1",
                altUrl: "https://drive.google.com/file/d/1JpzXso3aZ8P8MXQ8b8f1kpjlq_ciaQCK/view?usp=drive_link",
                completed: false,
                completionDate: null
            },
            {
                url: "https://apclassroom.collegeboard.org/d/99h7sgooy8?sui=33,1",
                altUrl: "https://drive.google.com/file/d/1_LYoOie55jPT2tM-o3spuiqbVxga9VPv/view?usp=drive_link",
                completed: false,
                completionDate: null
            }
        ],
        quizzes: [
            {
                questionPdf: "pdfs/unit1/unit1_section1.7_quiz.pdf",
                answersPdf: "pdfs/unit1/unit1_section1.7_answers.pdf",
                quizId: "1-7_q1",
                completed: false,
                completionDate: null
            }
        ],
        current: false
    },
    {
        id: "1-8",
        name: "Topic 1.8",
        description: "Graphical Representations of Summary Statistics",
        videos: [
            {
                url: "https://apclassroom.collegeboard.org/d/rm76rrgb3t?sui=33,1",
                altUrl: "https://drive.google.com/file/d/1sKc6XpjX5RUjGv5wbjUl7R1QEYLXG6W8/view?usp=drive_link",
                completed: false,
                completionDate: null
            }
        ],
        quizzes: [
            {
                questionPdf: "pdfs/unit1/unit1_section1.8_quiz.pdf",
                answersPdf: "pdfs/unit1/unit1_section1.8_answers.pdf",
                quizId: "1-8_q1",
                completed: false,
                completionDate: null
            }
        ],
        current: false
    },
    {
        id: "1-9",
        name: "Topic 1.9",
        description: "Comparing Distributions of a Quantitative Variable",
        videos: [
            {
                url: "https://apclassroom.collegeboard.org/d/27s7exmq1d?sui=33,1",
                altUrl: "https://drive.google.com/file/d/1zUev1tHzgJLMi337FjuxY49siAJJf_w8/view?usp=drive_link",
                completed: false,
                completionDate: null
            }
        ],
        quizzes: [
            {
                questionPdf: "pdfs/unit1/unit1_section1.9_quiz.pdf",
                answersPdf: "pdfs/unit1/unit1_section1.9_answers.pdf",
                quizId: "1-9_q1",
                completed: false,
                completionDate: null
            }
        ],
        current: false
    },
    {
        id: "1-10",
        name: "Topic 1.10",
        description: "The Normal Distribution",
        videos: [
            {
                url: "https://apclassroom.collegeboard.org/d/0ps3pcvbfn?sui=33,1",
                altUrl: "https://drive.google.com/file/d/1vTOitP631CGaZJMJjE6VVw53kiOa0zGv/view?usp=drive_link",
                completed: false,
                completionDate: null
            },
            {
                url: "https://apclassroom.collegeboard.org/d/wualxc69hl?sui=33,1",
                altUrl: "https://drive.google.com/file/d/1UF7VafU4agY3JcxHnp61EEjpOv959wZ8/view?usp=drive_link",
                completed: false,
                completionDate: null
            },
            {
                url: "https://apclassroom.collegeboard.org/d/3fev7ihoms?sui=33,1",
                altUrl: "https://drive.google.com/file/d/1aYbhplXukoDHOpWYCNG5OOTGVYZOcyCV/view?usp=drive_link",
                completed: false,
                completionDate: null
            }
        ],
        quizzes: [
            {
                questionPdf: "pdfs/unit1/unit1_section1.10_quiz.pdf",
                answersPdf: "pdfs/unit1/unit1_section1.10_answers.pdf",
                quizId: "1-10_q1",
                completed: false,
                completionDate: null
            }
        ],
        current: false
    },
    {
        id: "1-capstone",
        name: "Unit 1 Progress Check",
        description: "Capstone Assessment",
        videos: [],
        quizzes: [
            {
                questionPdf: "pdfs/unit1/unit1_pc_frq_quiz.pdf",
                answersPdf: "pdfs/unit1/unit1_pc_frq_answers.pdf",
                quizId: "1-capstone_q1",
                completed: false,
                completionDate: null
            },
            {
                questionPdf: "pdfs/unit1/unit1_pc_mcq_parta_answers.pdf",
                answersPdf: null,
                quizId: "1-capstone_q2",
                completed: false,
                completionDate: null
            },
            {
                questionPdf: "pdfs/unit1/unit1_pc_mcq_partb_answers.pdf",
                answersPdf: null,
                quizId: "1-capstone_q3",
                completed: false,
                completionDate: null
            }
        ],
        isCapstone: true,
        current: false
    },
]; 