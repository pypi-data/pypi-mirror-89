from dataclasses import dataclass
from pathlib import Path
import typing
from typing import ClassVar, List, Tuple, Union

from parsimonious import NodeVisitor  # type: ignore
from parsimonious.expressions import Compound, OneOf, Optional, Sequence, TokenMatcher, ZeroOrMore  # type: ignore

from .scanner import scan
from .parser import parse_header


@dataclass
class Type:
    def size_bytes(self, declarations: List['Declaration']) -> int:
        raise NotImplementedError('type.size_bytes() on ' + str(type(self)) + ' not implemented')


@dataclass
class Expression:
    def type(self, declarations: List['Declaration']) -> Type:
        raise NotImplementedError('expression.type() on ' + str(type(self)) + ' not implemented')


@dataclass
class ConstantExpression(Expression):
    value: str

    def type(self, _: List['Declaration']) -> Type:
        if self.value.startswith('"'):
            return PointerType(ConstType(BasicType('char')))
        elif self.value.startswith("'"):
            return BasicType('char')
        elif self.value in ['true', 'false']:
            return BasicType('bool')
        elif '.' in self.value:
            return BasicType('float?') # TODO infer size
        else:
            return BasicType('int?') # TODO infer size and signedness


@dataclass
class VariableExpression(Expression):
    name: str

    def type(self, declarations: List['Declaration']) -> Type:
        for decl in declarations:
            if decl.name == self.name:
                if isinstance(decl, VariableDeclaration):
                    return decl.type
                elif isinstance(decl, VariableDefinition):
                    return decl.type
                elif isinstance(decl, FunctionDeclaration) or isinstance(decl, FunctionDefinition):
                    return FunctionType(decl.return_type, [arg.type for arg in decl.args])
        raise KeyError('unknown variable ' + self.name)


@dataclass
class AddExpression(Expression):
    term1: Expression
    term2: Expression


@dataclass
class SubtractExpression(Expression):
    term1: Expression
    term2: Expression


@dataclass
class MultiplyExpression(Expression):
    factor1: Expression
    factor2: Expression


@dataclass
class StructPointerElementExpression(Expression):
    base: Expression
    element: str

    def type(self, declarations: List['Declaration']) -> Type:
        base_type = self.base.type(declarations)
        assert isinstance(base_type, PointerType)
        assert isinstance(base_type.target, BasicType)
        hopefully_struct, struct_name = base_type.target.name.split(' ')
        assert hopefully_struct == 'struct'
        for decl in declarations:
            if isinstance(decl, StructDeclaration) and decl.name == struct_name:
                if decl.fields is None:
                    raise KeyError('struct ' + struct_name + ' is opaque')
                for elem in decl.fields:
                    if elem.name == self.element:
                        return elem.type
                raise KeyError('element ' + self.element + ' not found in struct ' + struct_name)
        raise KeyError('struct ' + struct_name + ' not found')


@dataclass
class ArrayIndexExpression(Expression):
    array: Expression
    index: Expression


@dataclass
class FunctionCallExpression(Expression):
    function: Expression
    arguments: List[Expression]


@dataclass
class LogicalNotExpression(Expression):
    body: Expression


@dataclass
class NegativeExpression(Expression):
    body: Expression


@dataclass
class AddressOfExpression(Expression):
    body: Expression


@dataclass
class SizeofExpression(Expression):
    body: Union[Type, Expression]


@dataclass
class ComparisonExpression(Expression):
    value1: Expression
    op: str
    value2: Expression


@dataclass
class BasicType(Type):
    name: str

    def size_bytes(self, declarations: List['Declaration']) -> int:
        if self.name == 'uint8':
            return 1
        elif self.name == 'uintsize':
            return 8
        elif self.name.startswith('struct'):
            _, struct_name = self.name.split(' ')
            for decl in declarations:
                if isinstance(decl, StructDeclaration) and decl.name == struct_name:
                    if decl.fields is None:
                        raise KeyError('struct ' + struct_name + ' is opaque')
                    return sum(field.type.size_bytes(declarations) for field in decl.fields)
        raise NotImplementedError('size of ' + str(self) + ' not yet found')


@dataclass
class ConstType(Type):
    target: Type


@dataclass
class PointerType(Type):
    target: Type

    def size_bytes(self, declarations: List['Declaration']) -> int:
        return 8 # TODO figure out 32 bit vs 64 bit


@dataclass
class ArrayType(Type):
    contents: Type
    size: Expression


@dataclass
class FunctionType(Type):
    return_type: Type
    args: List[Type]


@dataclass
class HeaderFileElement:
    pass


@dataclass
class ImplementationFileElement:
    pass


@dataclass
class Statement:
    pass


@dataclass
class EmptyStatement(Statement):
    pass


@dataclass
class FragileStatement(Statement):
    body: Statement


@dataclass
class ExpressionStatement(Statement):
    body: Expression


@dataclass
class IfStatement(Statement):
    condition: Expression
    then: List[Statement]
    els: typing.Optional[List[Statement]]


@dataclass
class SwitchStatement(Statement):
    expression: Expression
    body: List[Union[typing.Optional[Expression], Statement]]


@dataclass
class WhileStatement(Statement):
    condition: Expression
    body: List[Statement]


@dataclass
class DoWhileStatement(Statement):
    condition: Expression
    body: List[Statement]


@dataclass
class Declaration:
    name: str


@dataclass
class VariableDeclaration(Declaration, HeaderFileElement):
    """Represents the declaration of a variable."""
    type: Type


@dataclass
class VariableDefinition(Declaration, HeaderFileElement, ImplementationFileElement, Statement):
    """Represents the definition of a variable."""
    type: Type
    value: Expression


@dataclass
class AssignmentStatement(Statement):
    pass


@dataclass
class ForStatement(Statement):
    init: List[VariableDefinition]
    condition: Expression
    update: List[AssignmentStatement]


@dataclass
class ContinueStatement(Statement):
    pass


@dataclass
class BreakStatement(Statement):
    pass


@dataclass
class ReturnStatement(Statement):
    body: typing.Optional[Expression]


@dataclass
class DirectAssignment(AssignmentStatement):
    destination: Expression
    value: Expression


@dataclass
class UpdateAssignment(AssignmentStatement):
    destination: Expression
    operation: str
    value: Expression

    def deconstruct(self) -> DirectAssignment:
        if self.operation == '+=':
            return DirectAssignment(self.destination, AddExpression(self.destination, self.value))
        elif self.operation == '*=':
            return DirectAssignment(self.destination, MultiplyExpression(self.destination, self.value))
        else:
            raise NotImplementedError('UpdateAssignment deconstruct with ' + self.operation)


@dataclass
class CrementAssignment(AssignmentStatement):
    destination: Expression
    operation: str


@dataclass
class StructDeclaration(Declaration, HeaderFileElement, ImplementationFileElement):
    """Represents the declaration of a struct type."""
    fields: typing.Optional[List[VariableDeclaration]]


@dataclass
class EnumDeclaration(Declaration, HeaderFileElement, ImplementationFileElement):
    """Represents the declaration of an enum type."""
    values: List[Tuple[str, typing.Optional[int]]]


@dataclass
class UnionDeclaration(Declaration, HeaderFileElement, ImplementationFileElement):
    """Represents the declaration of a union type."""
    tag: typing.Optional[VariableDeclaration]
    cases: Union[List[VariableDeclaration], List[Tuple[Expression, typing.Optional[VariableDeclaration]]]]


@dataclass
class FunctionDeclaration(Declaration, HeaderFileElement):
    """Represents the declaration of a function."""
    return_type: Type
    args: List[VariableDeclaration]


@dataclass
class FunctionDefinition(Declaration, HeaderFileElement, ImplementationFileElement):
    """Represents the definition of a function."""
    return_type: Type
    args: List[VariableDeclaration]
    body: List[Statement]


@dataclass
class HeaderFile:
    grammar: ClassVar[str] = "HeaderFile <- IncludeStatement* HeaderFileElement+"
    includes: List['HeaderFile']
    contents: List[HeaderFileElement]

    def get_declarations(self) -> List[Declaration]:
        included_declarations = [x.get_declarations() for x in self.includes]
        own_declarations: List[Declaration] = [x for x in self.contents if isinstance(x, Declaration)]
        all_declarations = included_declarations + [own_declarations]
        return [x for l in all_declarations for x in l]


@dataclass
class ImplementationFile:
    includes: List[HeaderFile]
    contents: List[ImplementationFileElement]

    def get_declarations(self) -> List[Declaration]:
        included_declarations = [x.get_declarations() for x in self.includes]
        own_declarations: List[Declaration] = [x for x in self.contents if isinstance(x, Declaration)]
        all_declarations = included_declarations + [own_declarations]
        return [x for l in all_declarations for x in l]


# noinspection PyPep8Naming,PyMethodMayBeStatic,PyUnusedLocal
class ASTBuilder(NodeVisitor):
    def __init__(self, include_folders):
        self.include_folders = include_folders

    def visit_HeaderFile(self, node, visited_children) -> HeaderFile:
        includes, elements = visited_children
        return HeaderFile(includes, elements)

    def visit_ImplementationFile(self, node, visited_children) -> ImplementationFile:
        includes, elements = visited_children
        return ImplementationFile(includes, elements)

    def visit_IncludeStatement(self, node, visited_children) -> HeaderFile:
        include, included_header, semicolon = visited_children
        assert include.type == 'include'
        assert included_header.type == 'string_literal'
        included_header = included_header.data.strip('"')
        assert semicolon.type == ';'
        for include_folder in self.include_folders:
            header = Path(include_folder) / included_header
            if header.exists():
                with open(header, 'r', encoding='utf-8') as header_file:
                    header_text = header_file.read()
                header_parse_tree = parse_header(scan(header_text))
                return self.visit(header_parse_tree)
        raise FileNotFoundError(included_header)

    def visit_NormalStructDefinition(self, node, visited_children) -> StructDeclaration:
        struct, name, lbrace, fields, rbrace = visited_children
        assert struct.type == 'struct'
        assert name.type == 'identifier'
        name = name.data
        assert lbrace.type == '{'
        assert rbrace.type == '}'
        return StructDeclaration(name, fields)

    def visit_OpaqueStructDefinition(self, node, visited_children) -> StructDeclaration:
        opaque, struct, name, semi = visited_children
        assert opaque.type == 'opaque'
        assert struct.type == 'struct'
        assert name.type == 'identifier'
        name = name.data
        assert semi.type == ';'
        return StructDeclaration(name, None)

    def visit_EnumDefinition(self, node, visited_children) -> EnumDeclaration:
        enum, name, lbrace, first_member, extra_members, trailing_comma, rbrace = visited_children
        assert enum.type == 'enum'
        assert name.type == 'identifier'
        name = name.data
        assert lbrace.type == '{'
        assert rbrace.type == '}'
        values = [first_member]
        for _, v in extra_members:
            values.append(v)
        return EnumDeclaration(name, values)

    def visit_EnumMember(self, node, visited_children) -> Tuple[str, typing.Optional[Expression]]:
        name, equals_value = visited_children
        assert name.type == 'identifier'
        name = name.data
        if equals_value is None:
            return name, None
        _, value = equals_value
        return name, value

    def visit_RobustUnionDefinition(self, node, visited_children) -> UnionDeclaration:
        union, name, lbrace, tag, body, rbrace = visited_children
        assert union.type == 'union'
        assert name.type == 'identifier'
        name = name.data
        assert lbrace.type == '{'
        assert rbrace.type == '}'
        expected_tagname, body = body
        if tag.name != expected_tagname:
            raise NameError(f"tag {tag} does not match switch argument {expected_tagname}")
        if not isinstance(body, list):
            body = [body]
        return UnionDeclaration(name, tag, body)

    def visit_UnionBody(self, node, visited_children) -> Tuple[str, List[Tuple[Expression, typing.Optional[VariableDeclaration]]]]:
        switch, lparen, tag, rparen, lbrace, body, rbrace = visited_children
        assert switch.type == 'switch'
        assert lparen.type == '('
        assert rparen.type == ')'
        assert lbrace.type == '{'
        assert rbrace.type == '}'
        return tag.data, body

    def visit_UnionBodySet(self, node, visited_children) -> Tuple[Expression, typing.Optional[VariableDeclaration]]:
        cases, var = visited_children
        if isinstance(cases, list):
            cases = cases[0]
        if isinstance(var, VariableDeclaration):
            return cases, var
        else:
            return cases, None

    def visit_CaseSpecifier(self, node, visited_children) -> Expression:
        while isinstance(visited_children, list) and len(visited_children) == 1:
            visited_children = visited_children[0]
        # TODO don't explode on 'default:'
        case, expr, colon = visited_children
        return expr

    def visit_FragileUnionDefinition(self, node, visited_children) -> UnionDeclaration:
        fragile, union, name, lbrace, body, rbrace = visited_children
        assert fragile.type == 'fragile'
        assert union.type == 'union'
        assert name.type == 'identifier'
        name = name.data
        assert lbrace.type == '{'
        assert rbrace.type == '}'
        return UnionDeclaration(name, None, body)

    def visit_FunctionDeclaration(self, node, visited_children) -> FunctionDeclaration:
        signature, semi = visited_children
        assert semi.type == ';'
        return signature

    def visit_VariableDefinition(self, node, visited_children) -> VariableDefinition:
        type, name, eq, value, semi = visited_children
        assert name.type == 'identifier'
        name = name.data
        assert eq.type == '='
        assert semi.type == ';'
        return VariableDefinition(name, type, value)

    def visit_VariableDeclaration(self, node, visited_children) -> VariableDeclaration:
        type, name, semi = visited_children
        assert name.type == 'identifier'
        name = name.data
        assert semi.type == ';'
        return VariableDeclaration(name, type)

    def visit_FunctionDefinition(self, node, visited_children) -> FunctionDefinition:
        signature, body = visited_children
        return FunctionDefinition(signature.name, signature.return_type, signature.args, body)

    def visit_FunctionSignature(self, node, visited_children) -> FunctionDeclaration:
        return_type, name, lparen, args, rparen = visited_children
        assert name.type == 'identifier'
        name = name.data
        assert lparen.type == '('
        if args is None:
            args = []
        assert rparen.type == ')'
        return FunctionDeclaration(name, return_type, args)

    def visit_SignatureArguments(self, node, visited_children) -> List[VariableDeclaration]:
        first_type, first_name, rest, comma = visited_children
        result = [VariableDeclaration(first_name.data, first_type)]
        for comma, ty, name in rest:
            result.append(VariableDeclaration(name.data, ty))
        return result

    def visit_IfStatement(self, node, visited_children):
        kwd, lparen, condition, rparen, then, els = visited_children
        assert kwd.type == 'if'
        assert lparen.type == '('
        assert rparen.type == ')'
        if els is not None:
            kwd, els = els
            assert kwd.type == 'else'
        return IfStatement(condition, then, els)

    def visit_ReturnStatement(self, node, visited_children):
        ret, body, semi = visited_children
        assert ret.type == 'return'
        assert semi.type == ';'
        return ReturnStatement(body)

    def visit_DirectAssignmentBody(self, node, visited_children):
        dest, eq, value = visited_children
        assert eq.type == '='
        return DirectAssignment(dest, value)

    def visit_UpdateAssignmentBody(self, node, visited_children):
        dest, op, value = visited_children
        return UpdateAssignment(dest, op.type, value)

    def visit_AssignmentStatement(self, node, visited_children):
        assignment, semi = visited_children
        assert semi.type == ';'
        return assignment

    def visit_ExpressionStatement(self, node, visited_children):
        expression, semi = visited_children
        assert semi.type == ';'
        return ExpressionStatement(expression)

    def visit_BasicType(self, node, visited_children) -> Type:
        while isinstance(visited_children, list) and len(visited_children) == 1:
            visited_children = visited_children[0]
        if isinstance(visited_children, list):
            if len(visited_children) == 3:
                # parenthesized!
                lparen, ty, rparen = visited_children
                assert lparen.type == '('
                assert rparen.type == ')'
                return ty
            else:
                category, name = visited_children
                category = category.type
                assert name.type == 'identifier'
                name = name.data
                return BasicType(f"{category} {name}")
        return BasicType(visited_children.type)

    def visit_ConstType(self, node, visited_children) -> ConstType:
        const, contents = visited_children
        assert const.type == 'const'
        return ConstType(contents)

    def visit_FunctionType(self, node, visited_children):
        raise NotImplementedError('function types')

    def visit_ArrayType(self, node, visited_children) -> ArrayType:
        contents, lbracket, size, rbracket = visited_children
        assert lbracket.type == '['
        assert rbracket.type == ']'
        return ArrayType(contents, size)

    def visit_PointerType(self, node, visited_children) -> PointerType:
        contents, splat = visited_children
        assert splat.type == '*'
        return PointerType(contents)

    def visit_Block(self, node, visited_children) -> List[Expression]:
        lbrace, body, rbrace = visited_children
        assert lbrace.type == '{'
        assert rbrace.type == '}'
        return body

    def visit_AtomicExpression(self, node, visited_children) -> Expression:
        if isinstance(visited_children, list) and len(visited_children) == 3:
            lparen, body, rparen = visited_children
            assert lparen.type == '('
            assert rparen.type == ')'
            return body
        body = visited_children
        while isinstance(body, list):
            body = body[0]
        if body.type == 'identifier':
            return VariableExpression(body.data)
        if body.type == 'constant':
            return ConstantExpression(body.data)
        if body.type in ['true', 'false']:
            return ConstantExpression(body.type)
        if body.type == 'string_literal':
            return ConstantExpression(body.data)
        raise NotImplementedError('atomic expression ' + repr(body))

    def visit_StructPointerElementSuffix(self, node, visited_children):
        separator, element = visited_children
        assert separator.type == '->'
        return lambda base: StructPointerElementExpression(base, element.data)

    def visit_CommasExpressionList(self, node, visited_children):
        first, rest, comma = visited_children
        result = [first]
        for comma, next in rest:
            result.append(next)
        return result

    def visit_FunctionCallSuffix(self, node, visited_children):
        lparen, args, rparen = visited_children
        assert lparen.type == '('
        assert rparen.type == ')'
        if args is None:
            args = []
        return lambda base: FunctionCallExpression(base, args)

    def visit_ArrayIndexSuffix(self, node, visited_children):
        lbracket, index, rbracket = visited_children
        assert lbracket.type == '['
        assert rbracket.type == ']'
        return lambda base: ArrayIndexExpression(base, index)

    def visit_ObjectExpression(self, node, visited_children) -> Expression:
        if isinstance(visited_children, list):
            base, suffix = visited_children[0]
            if len(suffix) > 0:
                for suffix in suffix:
                    base = suffix(base)
            return base
        raise NotImplementedError('array/struct literals')

    def visit_NegativeExpression(self, node, visited_children):
        minus, body = visited_children
        assert minus.type == '-'
        return NegativeExpression(body)

    def visit_AddressOfExpression(self, node, visited_children):
        ampersand, body = visited_children
        assert ampersand.type == '&'
        return AddressOfExpression(body)

    def visit_LogicalNotExpression(self, node, visited_children):
        bang, body = visited_children
        assert bang.type == '!'
        return LogicalNotExpression(body)

    def visit_SizeofExpression(self, node, visited_children):
        sizeof, argument = visited_children[0]
        assert sizeof.type == 'sizeof'
        return SizeofExpression(argument)

    def visit_TermExpression(self, node, visited_children) -> Expression:
        base, suffix = visited_children
        if suffix is not None:
            for op, factor in suffix:
                if op.type == '*':
                    base = MultiplyExpression(base, factor)
                else:
                    raise NotImplementedError('term suffix ' + op)
        return base

    def visit_ArithmeticExpression(self, node, visited_children) -> Expression:
        base, suffix = visited_children
        if suffix is not None:
            for op, term in suffix:
                if op.type == '+':
                    base = AddExpression(base, term)
                elif op.type == '-':
                    base = SubtractExpression(base, term)
                else:
                    raise NotImplementedError('arithmetic suffix ' + op)
        return base

    def visit_GreaterEqExpression(self, node, visited_children):
        value1, op, value2 = visited_children
        assert op.type == '>='
        return ComparisonExpression(value1, '>=', value2)

    def visit_LessEqExpression(self, node, visited_children):
        value1, op, value2 = visited_children
        assert op.type == '<='
        return ComparisonExpression(value1, '<=', value2)

    def generic_visit(self, node, visited_children):
        if isinstance(node.expr, TokenMatcher):
            return node.text[0]
        if isinstance(node.expr, OneOf):
            return visited_children[0]
        if isinstance(node.expr, Optional):
            if len(visited_children) == 0:
                return None
            return visited_children[0]
        if isinstance(node.expr, Sequence) and node.expr.name != '':
            raise NotImplementedError('visit for sequence ' + str(node.expr))
        if isinstance(node.expr, Compound):
            return visited_children
        print(node.expr)
        return super(ASTBuilder, self).generic_visit(node, visited_children)


def build_ast(parse_tree, include_dirs):
    builder = ASTBuilder(include_dirs)
    return builder.visit(parse_tree)
