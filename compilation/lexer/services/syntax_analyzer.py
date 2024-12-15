# compilation/lexer/services/syntax_analyzer.py
class SyntaxAnalyzer:
    def __init__(self):
        self.current_token_index = 0
        self.tokens = []
        self.errors = []
        self.has_end = False

    def analyze(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.errors = []
        self.has_end = False
        
        try:
            ast = self.parse_program()
            
            # Vérification supplémentaire pour Snk_End
            if not self.has_end:
                self.errors.append("Program must end with 'Snk_End'")
                
            return {
                'ast': ast,
                'structure': self.get_program_structure(),
                'valid': len(self.errors) == 0,
                'errors': self.errors
            }
        except Exception as e:
            self.errors.append(str(e))
            return {
                'ast': None,
                'structure': [],
                'valid': False,
                'errors': self.errors
            }

    def parse_program(self):
        ast = {'type': 'Program', 'body': []}
        
        # Vérifier Snk_Begin
        if not self.match_token('KEYWORD', 'Snk_Begin'):
            self.errors.append("Program must start with 'Snk_Begin'")
            return ast

        # Parser le corps du programme
        while self.current_token_index < len(self.tokens):
            token = self.current_token()
            if not token:
                break
                
            if token.type == 'KEYWORD' and token.value == 'Snk_End':
                self.has_end = True
                self.advance()
                break
                
            statement = self.parse_statement()
            if statement:
                ast['body'].append(statement)

        # Vérification finale de Snk_End déplacée dans analyze()
        return ast

    def parse_statement(self):
        token = self.current_token()
        
        if not token:
            return None
            
        if token.type == 'KEYWORD':
            if token.value in ['Snk_Int', 'Snk_Real', 'Snk_Strg']:
                return self.parse_variable_declaration()
            elif token.value == 'Set':
                return self.parse_assignment()
            elif token.value == 'if':
                return self.parse_if_statement()
            elif token.value == 'Snk_Print':
                return self.parse_print_statement()
                
        self.errors.append(f"Line {token.line}: Unexpected token {token.value}")
        self.advance()
        return None

    def parse_variable_declaration(self):
        var_type = self.current_token().value  # Snk_Int, Snk_Real, ou Snk_Strg
        self.advance()
        
        if not self.current_token() or self.current_token().type != 'IDENTIFIER':
            self.errors.append(f"Line {self.current_token().line}: Expected identifier after {var_type}")
            return None
            
        name = self.current_token().value
        line = self.current_token().line
        self.advance()
        
        # Vérifier le terminateur #
        if not self.match_token('END_INSTRUCTION'):
            self.errors.append(f"Line {line}: Missing terminator '#' after variable declaration")
            
        return {
            'type': 'VariableDeclaration',
            'var_type': var_type,
            'name': name,
            'line': line
        }

    def parse_assignment(self):
        self.advance()  # Skip 'Set'
        
        if not self.current_token() or self.current_token().type != 'IDENTIFIER':
            self.errors.append(f"Line {self.current_token().line}: Expected identifier after 'Set'")
            return None
            
        target = self.current_token().value
        line = self.current_token().line
        self.advance()
        
        if not self.match_token('OPERATOR', '='):
            self.errors.append(f"Line {line}: Expected '=' in assignment")
            return None
            
        value = self.parse_expression()
        
        if not self.match_token('END_INSTRUCTION'):
            self.errors.append(f"Line {line}: Missing terminator '#' after assignment")
            
        return {
            'type': 'Assignment',
            'target': target,
            'value': value,
            'line': line
        }

    def parse_if_statement(self):
        self.advance()  # Skip 'if'
        line = self.current_token().line
        
        condition = self.parse_expression()
        
        if not self.match_token('END_INSTRUCTION'):
            self.errors.append(f"Line {line}: Missing terminator '#' after if condition")
            
        body = []
        while self.current_token() and not self.current_token().value in ['else', 'end']:
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
                
        else_body = []
        if self.match_token('KEYWORD', 'else'):
            while self.current_token() and self.current_token().value != 'end':
                stmt = self.parse_statement()
                if stmt:
                    else_body.append(stmt)
                    
        if not self.match_token('KEYWORD', 'end'):
            self.errors.append(f"Line {line}: Missing 'end' for if statement")
            
        if not self.match_token('END_INSTRUCTION'):
            self.errors.append(f"Line {line}: Missing terminator '#' after end")
            
        return {
            'type': 'IfStatement',
            'condition': condition,
            'body': body,
            'else_body': else_body,
            'line': line
        }

    def parse_print_statement(self):
        self.advance()  # Skip 'Snk_Print'
        line = self.current_token().line
        
        value = self.parse_expression()
        
        if not self.match_token('END_INSTRUCTION'):
            self.errors.append(f"Line {line}: Missing terminator '#' after print statement")
            
        return {
            'type': 'PrintStatement',
            'value': value,
            'line': line
        }

    def parse_expression(self):
        left = self.parse_term()
        
        if not left:
            return None
            
        token = self.current_token()
        if token and token.type == 'OPERATOR' and token.value in ['>', '<', '>=', '<=', '==', '!=']:
            operator = token.value
            self.advance()
            right = self.parse_term()
            if right:
                return {
                    'type': 'BinaryOperation',
                    'operator': operator,
                    'left': left,
                    'right': right,
                    'line': token.line
                }
        
        return left

    def parse_term(self):
        left = self.parse_factor()
        
        if not left:
            return None
            
        token = self.current_token()
        if token and token.type == 'OPERATOR' and token.value in ['+', '-']:
            operator = token.value
            self.advance()
            right = self.parse_factor()
            if right:
                return {
                    'type': 'BinaryOperation',
                    'operator': operator,
                    'left': left,
                    'right': right,
                    'line': token.line
                }
        
        return left

    def parse_factor(self):
        left = self.parse_primary()
        
        if not left:
            return None
            
        token = self.current_token()
        if token and token.type == 'OPERATOR' and token.value in ['*', '/']:
            operator = token.value
            self.advance()
            right = self.parse_primary()
            if right:
                return {
                    'type': 'BinaryOperation',
                    'operator': operator,
                    'left': left,
                    'right': right,
                    'line': token.line
                }
        
        return left

    def parse_primary(self):
        token = self.current_token()
        if not token:
            return None
            
        if token.type in ['INTEGER', 'REAL']:
            value = float(token.value) if token.type == 'REAL' else int(token.value)
            self.advance()
            return {'type': 'Literal', 'value': value, 'line': token.line}
            
        elif token.type == 'STRING':
            value = token.value
            self.advance()
            return {'type': 'Literal', 'value': value, 'line': token.line}
            
        elif token.type == 'IDENTIFIER':
            value = token.value
            self.advance()
            return {'type': 'Variable', 'name': value, 'line': token.line}
            
        self.errors.append(f"Line {token.line}: Unexpected token in expression: {token.value}")
        self.advance()
        return None

    def match_token(self, expected_type, expected_value=None):
        token = self.current_token()
        if token and token.type == expected_type:
            if expected_value is None or token.value == expected_value:
                self.advance()
                return True
        return False

    def current_token(self):
        if self.current_token_index < len(self.tokens):
            return self.tokens[self.current_token_index]
        return None

    def advance(self):
        self.current_token_index += 1

    def get_program_structure(self):
        structure = []
        for token in self.tokens:
            structure.append(f"{token.type}: {token.value}")
        return structure