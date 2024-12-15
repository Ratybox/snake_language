# compilation/lexer/services/lexical_analyzer.py
class Token:
    def __init__(self, type, value, line):
        self.type = type
        self.value = value
        self.line = line

    def to_dict(self):
        return {
            'type': self.type,
            'value': self.value,
            'line': self.line
        }

class LexicalAnalyzer:
    def __init__(self):
        self.keywords = {
            'Snk_Begin', 'Snk_End', 'Snk_Int', 'Snk_Real', 
            'Snk_Strg', 'Set', 'if', 'else', 'begin', 'end', 
            'Snk_Print'
        }
        self.operators = {'+', '-', '*', '/', '=', '<', '>', '<=', '>=', '==', '!='}
        
    def analyze(self, code):
        tokens = []
        errors = []
        current_line = 1
        i = 0
        has_end = False
        
        while i < len(code):
            char = code[i]
            
            # Gestion des espaces et nouvelles lignes
            if char.isspace():
                if char == '\n':
                    current_line += 1
                i += 1
                continue
                
            # Gestion des commentaires
            if char == '#' and i + 1 < len(code) and code[i + 1] == '#':
                while i < len(code) and code[i] != '\n':
                    i += 1
                continue
                
            # Fin d'instruction
            if char == '#':
                tokens.append(Token('END_INSTRUCTION', '#', current_line))
                i += 1
                continue
                
            # Identifiants et mots-clés
            if char.isalpha():
                identifier = ''
                start_pos = i
                while i < len(code) and (code[i].isalnum() or code[i] == '_'):
                    identifier += code[i]
                    i += 1
                if identifier in self.keywords:
                    tokens.append(Token('KEYWORD', identifier, current_line))
                    if identifier == 'Snk_End':
                        has_end = True
                else:
                    tokens.append(Token('IDENTIFIER', identifier, current_line))
                continue
                
            # Nombres (entiers et réels)
            if char.isdigit():
                number = ''
                start_pos = i
                dot_count = 0
                while i < len(code) and (code[i].isdigit() or code[i] == '.'):
                    if code[i] == '.':
                        dot_count += 1
                        if dot_count > 1:
                            errors.append(f"Line {current_line}: Invalid number format - multiple decimal points")
                            break
                    number += code[i]
                    i += 1
                try:
                    if '.' in number:
                        tokens.append(Token('REAL', float(number), current_line))
                    else:
                        tokens.append(Token('INTEGER', int(number), current_line))
                except ValueError:
                    errors.append(f"Line {current_line}: Invalid number format")
                continue
                
            # Chaînes de caractères
            if char == '"':
                string = ''
                i += 1
                start_pos = i
                while i < len(code) and code[i] != '"':
                    if code[i] == '\n':
                        errors.append(f"Line {current_line}: Unterminated string")
                        current_line += 1
                        break
                    string += code[i]
                    i += 1
                if i < len(code) and code[i] == '"':
                    tokens.append(Token('STRING', string, current_line))
                    i += 1
                else:
                    errors.append(f"Line {current_line}: Unterminated string")
                continue
                
            # Opérateurs
            if char in '+-*/=<>!':
                operator = char
                if i + 1 < len(code) and code[i:i+2] in self.operators:
                    operator = code[i:i+2]
                    i += 2
                else:
                    i += 1
                if operator in self.operators:
                    tokens.append(Token('OPERATOR', operator, current_line))
                else:
                    errors.append(f"Line {current_line}: Invalid operator '{operator}'")
                continue
                
            errors.append(f"Line {current_line}: Invalid character '{char}'")
            i += 1
            
        # Vérification de la structure du programme
        if not has_end:
            errors.append("Program must end with 'Snk_End'")
            
        return tokens, errors