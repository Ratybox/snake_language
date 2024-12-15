# compilation/lexer/services/semantic_analyzer.py
class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.errors = []

    def add_symbol(self, name, type, line):
        # Convertir les types Snk en types internes
        type_mapping = {
            'Snk_Int': 'int',
            'Snk_Real': 'real',
            'Snk_Strg': 'string'
        }
        internal_type = type_mapping.get(type, type)
        
        if name in self.symbols:
            self.errors.append(f"Line {line}: Variable '{name}' already declared")
        else:
            self.symbols[name] = {'type': internal_type, 'line': line}

    def get_symbol(self, name):
        return self.symbols.get(name)

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.errors = []

    def analyze(self, ast):
        if not ast:
            return {
                'valid': False,
                'symbol_table': {},
                'type_checking': 'failed',
                'scope_analysis': 'invalid',
                'errors': ['Invalid AST']
            }

        try:
            self.analyze_node(ast)
            
            return {
                'valid': len(self.errors) == 0 and len(self.symbol_table.errors) == 0,
                'symbol_table': self.symbol_table.symbols,
                'type_checking': 'passed' if len(self.errors) == 0 else 'failed',
                'scope_analysis': 'valid' if len(self.errors) == 0 else 'invalid',
                'errors': self.errors + self.symbol_table.errors
            }
        except Exception as e:
            self.errors.append(str(e))
            return {
                'valid': False,
                'symbol_table': {},
                'type_checking': 'failed',
                'scope_analysis': 'invalid',
                'errors': self.errors
            }

    def analyze_node(self, node):
        if isinstance(node, dict):
            if node['type'] == 'Program':
                for statement in node.get('body', []):
                    self.analyze_node(statement)
                    
            elif node['type'] == 'VariableDeclaration':
                self.check_variable_declaration(node)
                
            elif node['type'] == 'Assignment':
                self.check_assignment(node)
                
            elif node['type'] == 'BinaryOperation':
                return self.check_binary_operation(node)
                
            elif node['type'] == 'IfStatement':
                self.check_if_statement(node)
                
            elif node['type'] == 'PrintStatement':
                self.check_print_statement(node)

    def check_variable_declaration(self, node):
        name = node.get('name')
        var_type = node.get('var_type')
        line = node.get('line', 0)
        
        if name and var_type:
            self.symbol_table.add_symbol(name, var_type, line)

    def check_assignment(self, node):
        target = node.get('target')
        value = node.get('value')
        line = node.get('line', 0)
        
        if target:
            symbol = self.symbol_table.get_symbol(target)
            if not symbol:
                self.errors.append(f"Line {line}: Variable '{target}' not declared")
            elif value:
                value_type = self.get_expression_type(value)
                target_type = symbol['type']
                
                if not self.are_types_compatible(value_type, target_type):
                    self.errors.append(f"Line {line}: Type mismatch in assignment. Expected {target_type}, got {value_type}")

    def check_binary_operation(self, node):
        operator = node.get('operator')
        left = node.get('left')
        right = node.get('right')
        line = node.get('line', 0)
        
        if not (left and right):
            self.errors.append(f"Line {line}: Invalid binary operation")
            return None
            
        left_type = self.get_expression_type(left)
        right_type = self.get_expression_type(right)
        
        if operator in ['>', '<', '>=', '<=', '==', '!=']:
            if not self.are_types_compatible(left_type, right_type):
                self.errors.append(f"Line {line}: Cannot compare {left_type} with {right_type}")
            return 'bool'
            
        elif operator in ['+', '-', '*', '/']:
            if left_type in ['int', 'real'] and right_type in ['int', 'real']:
                return 'real' if 'real' in [left_type, right_type] else 'int'
            elif operator == '+' and 'string' in [left_type, right_type]:
                if left_type == right_type == 'string':
                    return 'string'
            self.errors.append(f"Line {line}: Invalid operation {operator} between {left_type} and {right_type}")
            
        return None

    def check_if_statement(self, node):
        condition = node.get('condition')
        if condition:
            condition_type = self.get_expression_type(condition)
            if condition_type != 'bool':
                self.errors.append(f"Line {node.get('line', 0)}: Condition must be a boolean expression")
                
        for stmt in node.get('body', []):
            self.analyze_node(stmt)
            
        for stmt in node.get('else_body', []):
            self.analyze_node(stmt)

    def check_print_statement(self, node):
        value = node.get('value')
        if value:
            self.get_expression_type(value)  # Vérifie juste que l'expression est valide

    def get_expression_type(self, expr):
        if isinstance(expr, dict):
            if expr['type'] == 'Literal':
                value = expr.get('value')
                if isinstance(value, int):
                    return 'int'
                elif isinstance(value, float):
                    return 'real'
                elif isinstance(value, str):
                    return 'string'
            elif expr['type'] == 'Variable':
                symbol = self.symbol_table.get_symbol(expr['name'])
                if symbol:
                    return symbol['type']
                self.errors.append(f"Line {expr.get('line', 0)}: Variable '{expr['name']}' not declared")
            elif expr['type'] == 'BinaryOperation':
                return self.check_binary_operation(expr)
        return None

    def are_types_compatible(self, type1, type2):
        if type1 == type2:
            return True
        if type1 in ['int', 'real'] and type2 in ['int', 'real']:
            return True
        return False