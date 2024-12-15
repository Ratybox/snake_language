# compilation/lexer/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services.lexical_analyzer import LexicalAnalyzer
from .services.syntax_analyzer import SyntaxAnalyzer
from .services.semantic_analyzer import SemanticAnalyzer

class CompileView(APIView):
    def post(self, request):
        code = request.data.get('code', '')
        
        if not code.strip().endswith('Snk_End'):
            return Response({
                'success': False,
                'errors': ["Program must end with 'Snk_End'"],
                'lexical_analysis': None,
                'syntax_analysis': None,
                'semantic_analysis': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Analyse lexicale
            lexical_analyzer = LexicalAnalyzer()
            tokens, lexical_errors = lexical_analyzer.analyze(code)
            
            if lexical_errors:
                return Response({
                    'success': False,
                    'errors': lexical_errors,
                    'lexical_analysis': [token.to_dict() for token in tokens],
                    'syntax_analysis': None,
                    'semantic_analysis': None
                }, status=status.HTTP_400_BAD_REQUEST)

            # Analyse syntaxique
            syntax_analyzer = SyntaxAnalyzer()
            syntax_result = syntax_analyzer.analyze(tokens)
            
            if not syntax_result['valid']:
                return Response({
                    'success': False,
                    'errors': syntax_result['errors'],
                    'lexical_analysis': [token.to_dict() for token in tokens],
                    'syntax_analysis': syntax_result,
                    'semantic_analysis': None
                }, status=status.HTTP_400_BAD_REQUEST)

            # Analyse sémantique
            semantic_analyzer = SemanticAnalyzer()
            semantic_result = semantic_analyzer.analyze(syntax_result['ast'])
            
            return Response({
                'success': semantic_result['valid'],
                'errors': semantic_result['errors'],
                'lexical_analysis': [token.to_dict() for token in tokens],
                'syntax_analysis': syntax_result,
                'semantic_analysis': semantic_result
            }, status=status.HTTP_200_OK if semantic_result['valid'] else status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({
                'success': False,
                'errors': [str(e)],
                'lexical_analysis': None,
                'syntax_analysis': None,
                'semantic_analysis': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)