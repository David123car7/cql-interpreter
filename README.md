# CQL Interpreter

This project consists of developing an interpreter for the **CQL (Comma Query Language)**, a query language inspired by SQL designed to operate on CSV files. The interpreter is implemented in Python using the [PLY (Python Lex-Yacc)](https://www.dabeaz.com/ply/) library.
> **Academic Context**  
> This application was developed as part of the “Language Processing” course in the second year of the degree in Computer Systems Engineering (Licenciatura em Engenharia de Sistemas Informáticos) at Instituto Politécnico do Cávado e do Ave.

## 📚 Description

The main goal is to allow users to perform data query and manipulation operations on CSV files using SQL-like commands. The features include:

- **Table import and export**: `IMPORT TABLE`, `EXPORT TABLE`
- **Queries**: `SELECT` with support for `WHERE` and `LIMIT` clauses
- **Table manipulation**: `CREATE TABLE`, `RENAME TABLE`, `DISCARD TABLE`
- **Procedures**: defining and executing procedures with `PROCEDURE` and `CALL`
- **Comments**: support for single-line and multi-line comments

## 🛠️ Technologies Used

- [Python 3.x](https://www.python.org/)
- [PLY (Python Lex-Yacc)](https://www.dabeaz.com/ply/)

## 🚀 How to Run

1. **Clone the repository:**

   ```bash
   git clone https://github.com/David123car7/cql-interpreter.git

   
2. **Install dependencies::**

   ```bash
   pip install ply
   
3. **Run the interpreter No File:**
   
      ```bash
   python cql_interpreter.py

4. **Run the interpreter With File:**
   
      ```bash
   python cql_interpreter.py files/entrada.fca


