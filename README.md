# SNAKE Language Compiler
## Screen Shots

![Image 1 Title](https://i.ibb.co/dK90kxB/1.png)

![Image 2 Title](https://i.ibb.co/WtVfHL8/2.png)

![Image 3 Title](https://i.ibb.co/ZJ6s5Z0/3.png)

![Image 4 Title](https://i.ibb.co/Zf7WRdk/4.png)

![Image 5 Title](https://i.ibb.co/yWJc1L0/5.png)


## Description
SNAKE is a custom programming language designed for demonstration purposes, with a simple structure and syntax. This project implements a compiler for SNAKE, capable of performing lexical, syntax, and semantic analysis of `.SNK` files written in the SNAKE language.

The compiler detects and reports:
- **Lexical errors:** Unrecognized tokens.
- **Syntax errors:** Miswritten instructions.
- **Semantic errors:** Type mismatches, undeclared variable usage, etc.

The application includes a web-based interface built with Django (backend), React (frontend), Tailwind CSS for styling, and Framer Motion for animations. RESTful APIs are used to communicate between the frontend and backend.

---

## Features
1. **Language Structure**:
   - Programs must start with `Snk_Begin` and end with `Snk_End`.
   - Each instruction must end with `#`.
   - Comments begin with `##`.
   - Variables:
     - Integer: `Snk_Int i, j, k #`
     - Real: `Snk_Real x3 #` (real numbers use a dot `.` as a separator)
     - String: `Snk_Strg`
   - Example: `Set i 33 #`
   - Keywords: `if`, `else`, `begin`, `end`, `Snk_Print "hello"`

2. **Analysis Phases**:
   - Lexical Analysis: Recognizes all tokens.
   - Syntax Analysis: Reports errors for incorrectly written instructions.
   - Semantic Analysis: Reports type incompatibilities and undeclared variable usage.

---

## Prerequisites
- Python 3.9+
- Node.js 16+
- npm or yarn
  
---

## Installation

### Backend Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/username/snake_language.git
   cd snake_language/compilation
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   ```

3. Start the server:
   ```bash
   python manage.py runserver
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd ../frontend
   ```

2. Install dependencies:
   ```bash
   npm i  # Or: yarn
   ```

3. Start the development server:
   ```bash
   npm start  # Or: yarn start
   ```

---

## Usage
1. Access the application at `http://localhost:3000`.
2. Upload a `.SNK` file containing your SNAKE program.
3. View the analysis results, including any detected lexical, syntax, or semantic errors.

---

## Example `.SNK` File
```snk
Snk_Begin
Snk_Int i, j #
Snk_Real x3 #
Set i 10 #
Set j 20 #
Set x3 30.5 #
Snk_Print "Sum: " ## This is a comment
Snk_End
```

---

## Technologies Used
- **Frontend**: React, Tailwind CSS, Framer-Motion
- **Backend**: Django
- **APIs**: RESTful API

---

## Contributions
Contributions are not welcome.

