# 📘 Compiler

An educational **compiler implementation in Python** that demonstrates the fundamental stages of compiler design, including **lexical analysis** and **syntax analysis**.  
This project is intended for learning, experimentation, and academic use.

---

## 🧠 Overview

This repository contains a basic compiler that processes source code through multiple compilation phases.  
The main goal of the project is to provide a **clear and modular implementation** of compiler concepts suitable for computer engineering and software development students.

Currently implemented phases:

- **Lexical Analysis (Scanner)**
- **Syntax Analysis (Parser)**

The project structure allows future expansion to include:
- Semantic analysis
- Intermediate code generation
- Code optimization
- Target code generation

---

## 🚀 Features

- Written in **Python** for simplicity and readability
- Modular and well-structured design
- Clear separation between compiler phases
- Easy to extend for additional compilation stages
- Suitable for academic projects and coursework

---

## 📁 Project Structure

    Compiler/
    │
    ├── Lexical Analysis/     # Tokenization and scanning logic
    ├── Syntax Analysis/      # Grammar rules and parsing logic
    ├── main.py               # Compiler entry point
    └── README.md

---

## 🔧 Requirements

- Python **3.7** or higher

If a `requirements.txt` file exists, install dependencies using:

    pip install -r requirements.txt

Otherwise, no external libraries are required.

---

## ▶️ Usage

Run the compiler using:

    python main.py <source_file>

### Example

    python main.py examples/test.code

---

## ⚙️ Compilation Stages

### 1️⃣ Lexical Analysis
- Reads the source code as raw text
- Converts characters into tokens (keywords, identifiers, operators, literals, etc.)
- Detects invalid or unknown symbols

### 2️⃣ Syntax Analysis
- Receives tokens from the lexical analyzer
- Validates program structure using grammar rules
- Builds a parse tree or syntax representation
- Reports syntax errors with meaningful messages

---

## 📌 Example Output

    Lexical analysis started...
    ✔ Tokens generated successfully

    Syntax analysis started...
    ✔ Program parsed successfully

    Compilation finished with no errors.

---

## 🛠️ Future Improvements

- Add semantic analysis phase
- Generate intermediate representation (IR)
- Implement basic optimizations
- Add error recovery mechanisms
- Improve documentation and examples

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a new branch (`feature/your-feature-name`)
3. Commit your changes
4. Open a Pull Request

Please keep code clean and well-documented.

---

## 📄 License

This project is released under the **MIT License**.  
You are free to use, modify, and distribute it for educational and personal purposes.

---

## 👨‍💻 Author

**Erfan Shahbazzadeh**  
Computer Engineer & Software Developer
