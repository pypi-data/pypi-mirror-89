import dataclasses
from dataclasses import dataclass
from functools import singledispatch
from typing import List

from .ast import ImplementationFile, FunctionDefinition, ExpressionStatement, FunctionCallExpression, \
    VariableExpression, ConstantExpression, ReturnStatement, BasicType, IfStatement, ComparisonExpression, \
    AddExpression, StructPointerElementExpression, Declaration, PointerType, StructDeclaration, VariableDefinition, \
    MultiplyExpression, LogicalNotExpression, DirectAssignment, UpdateAssignment, SizeofExpression, Expression, \
    ConstType, ArrayIndexExpression, ArrayType, NegativeExpression, SubtractExpression, AddressOfExpression


@dataclass
class SsaResult:
    data: List[str]
    code: List[str]

    def __add__(self, other: 'SsaResult') -> 'SsaResult':
        if not isinstance(other, SsaResult):
            return NotImplemented
        return SsaResult(self.data + other.data, self.code + other.code)

    def __radd__(self, other: 'SsaResult'):
        if not isinstance(other, SsaResult):
            return NotImplemented
        self.data += other.data
        self.code += other.code


@dataclass
class CompileContext:
    declarations: List[Declaration]
    next_data: int = 0
    next_temp: int = 0
    next_label: int = 0


def build_ssa(file: ImplementationFile) -> str:
    result = compile_to_ssa(file, CompileContext(file.get_declarations()))
    data = '\n'.join(result.data)
    code = '\n'.join(result.code)
    return data + '\n\n' + code


@singledispatch
def compile_to_ssa(target, context: CompileContext) -> SsaResult:
    raise NotImplementedError('unannotated compile on ' + str(type(target)))


@compile_to_ssa.register
def _(target: ImplementationFile, context: CompileContext):
    result = SsaResult([], [])
    for target in target.contents:
        result += compile_to_ssa(target, context)
    return result


@compile_to_ssa.register
def _(target: FunctionDefinition, context: CompileContext) -> SsaResult:
    result = SsaResult([], [])
    context = dataclasses.replace(context, declarations=target.args + context.declarations)
    for statement in target.body:
        result += compile_to_ssa(statement, context)
        if isinstance(statement, Declaration):
            context = dataclasses.replace(context, declarations=[statement]+context.declarations)
    if not result.code[-1].startswith('ret'):
        result.code.append('ret')
    code = ['    ' + instr for instr in result.code]
    # TODO types
    args = ','.join(f"l %{x.name}" for x in target.args)
    ret_type = ''
    if target.return_type != BasicType('void'):
        ret_type = 'l'
    code = [f"export function {ret_type} ${target.name}({args}) {{", "@start", *code, "}"]
    return SsaResult(result.data, code)


@compile_to_ssa.register
def _(target: ExpressionStatement, context: CompileContext) -> SsaResult:
    return compile_to_ssa(target.body, context)


@compile_to_ssa.register
def _(target: FunctionCallExpression, context: CompileContext) -> SsaResult:
    assert isinstance(target.function, VariableExpression)
    result = SsaResult([], [])
    args = []
    for i, expr in enumerate(target.arguments):
        result += compile_to_ssa(expr, context)
        arg_dest = context.next_temp - 1
        args += [f"l %t{arg_dest}"]
    result_dest = context.next_temp
    context.next_temp += 1
    # TODO size
    result.code.append(f"%t{result_dest} =l call ${target.function.name}({','.join(args)})")
    return result


@compile_to_ssa.register
def _(target: ConstantExpression, context: CompileContext) -> SsaResult:
    if target.type(context.declarations) == PointerType(ConstType(BasicType('char'))):
        data_dest = context.next_data
        context.next_data += 1
        data = [f"data $data{data_dest} = {{ b {target.value}, b 0 }}"]
        temp = context.next_temp
        context.next_temp += 1
        code = [f"%t{temp} =l copy $data{data_dest}"]
    elif target.type(context.declarations) == BasicType('char'):
        value = target.value.strip("'")
        if len(value) == 1:
            value = ord(value)
        elif value == r'\0':
            value = 0
        else:
            raise NotImplementedError('escape sequence ' + value)
        data = []
        temp = context.next_temp
        context.next_temp += 1
        code = [f"%t{temp} =l copy {value}"]
    elif target.type(context.declarations) == BasicType('bool'):
        data = []
        temp = context.next_temp
        context.next_temp += 1
        if target.value == 'true':
            value = 1
        else:
            value = 0
        code = [f"%t{temp} =l copy {value}"]
    elif target.type(context.declarations) == BasicType('int?'):
        assert not target.value.startswith('0b')
        assert not target.value.startswith('0B')
        assert not target.value.startswith('0o')
        assert not target.value.startswith('0x')
        assert not target.value.startswith('0X')
        assert not target.value.startswith('0f')
        assert not target.value.startswith('0F')
        assert '.' not in target.value
        assert not target.value.startswith("'")
        data = []
        temp = context.next_temp
        context.next_temp += 1
        code = [f"%t{temp} =l copy {target.value}"]
    else:
        raise NotImplementedError('compiling ' + str(target))
    return SsaResult(data, code)


@compile_to_ssa.register
def _(target: ReturnStatement, context: CompileContext) -> SsaResult:
    if target.body is None:
        return SsaResult([], ['ret'])
    result = compile_to_ssa(target.body, context)
    ret_val_dest = context.next_temp - 1
    result.code.append(f"ret %t{ret_val_dest}")
    return result


@compile_to_ssa.register
def _(target: IfStatement, context: CompileContext) -> SsaResult:
    result = compile_to_ssa(target.condition, context)
    condition_dest = context.next_temp - 1
    true_label = context.next_label
    context.next_label += 1
    false_label = context.next_label
    context.next_label += 1
    after_label = context.next_label
    context.next_label += 1
    result.code.append(f"jnz %t{condition_dest}, @l{true_label}, @l{false_label}")
    result.code.append(f"@l{true_label}")
    for statement in target.then:
        result += compile_to_ssa(statement, context)
    if not result.code[-1].startswith('ret'):
        result.code.append(f"jmp @l{after_label}")
    result.code.append(f"@l{false_label}")
    if target.els is not None:
        for statement in target.els:
            result += compile_to_ssa(statement, context)
    if not result.code[-1].startswith('ret'):
        result.code.append(f"jmp @l{after_label}")
    result.code.append(f"@l{after_label}")
    return result


@compile_to_ssa.register
def _(target: ComparisonExpression, context: CompileContext) -> SsaResult:
    result = compile_to_ssa(target.value1, context)
    value1_dest = context.next_temp - 1
    result += compile_to_ssa(target.value2, context)
    value2_dest = context.next_temp - 1
    result_dest = context.next_temp
    context.next_temp += 1
    # TODO types, and signedness
    if target.op == '==':
        op = "ceqw"
    elif target.op == '>=':
        op = "cugew"
    elif target.op == '<=':
        op = "culew"
    else:
        raise NotImplementedError('comparison ' + target.op)
    result.code.append(f"%t{result_dest} =l {op} %t{value1_dest}, %t{value2_dest}")
    return result


@compile_to_ssa.register
def _(target: AddExpression, context: CompileContext) -> SsaResult:
    result = compile_to_ssa(target.term1, context)
    value1_dest = context.next_temp - 1
    result += compile_to_ssa(target.term2, context)
    value2_dest = context.next_temp - 1
    result_reg = context.next_temp
    context.next_temp += 1
    # TODO make sure the types are correct
    result.code.append(f"%t{result_reg} =l add %t{value1_dest}, %t{value2_dest}")
    return result


@compile_to_ssa.register
def _(target: SubtractExpression, context: CompileContext) -> SsaResult:
    result = compile_to_ssa(target.term1, context)
    value1_dest = context.next_temp - 1
    result += compile_to_ssa(target.term2, context)
    value2_dest = context.next_temp - 1
    result_reg = context.next_temp
    context.next_temp += 1
    # TODO make sure the types are correct
    result.code.append(f"%t{result_reg} =l sub %t{value1_dest}, %t{value2_dest}")
    return result


@compile_to_ssa.register
def _(target: MultiplyExpression, context: CompileContext) -> SsaResult:
    result = compile_to_ssa(target.factor1, context)
    value1_dest = context.next_temp - 1
    result += compile_to_ssa(target.factor2, context)
    value2_dest = context.next_temp - 1
    result_reg = context.next_temp
    context.next_temp += 1
    # TODO make sure the types are correct
    result.code.append(f"%t{result_reg} =l mul %t{value1_dest}, %t{value2_dest}")
    return result


@compile_to_ssa.register
def _(target: VariableExpression, context: CompileContext) -> SsaResult:
    # TODO make sure any of this is reasonable
    result = context.next_temp
    context.next_temp += 1
    return SsaResult([], [f"%t{result} =l copy %{target.name}"])


@compile_to_ssa.register
def _(target: VariableDefinition, context: CompileContext) -> SsaResult:
    # TODO figure some shit out
    result = compile_to_ssa(target.value, context)
    result_dest = context.next_temp - 1
    result.code.append(f"%{target.name} =l copy %t{result_dest}")
    return result


@compile_to_ssa.register
def _(target: LogicalNotExpression, context: CompileContext) -> SsaResult:
    result = compile_to_ssa(target.body, context)
    inner_result_dest = context.next_temp - 1
    result_dest = context.next_temp
    context.next_temp += 1
    result.code.append(f"%t{result_dest} =l ceqw %t{inner_result_dest}, 0")
    return result


@compile_to_ssa.register
def _(target: NegativeExpression, context: CompileContext) -> SsaResult:
    return compile_to_ssa(SubtractExpression(ConstantExpression('0'), target.body), context)


@compile_to_ssa.register
def _(target: ArrayIndexExpression, context: CompileContext) -> SsaResult:
    result = compile_to_ssa(target.array, context)
    base = context.next_temp - 1
    result += compile_to_ssa(target.index, context)
    index = context.next_temp - 1
    array_type = target.array.type(context.declarations)
    if isinstance(array_type, PointerType):
        array_type = array_type.target
    assert isinstance(array_type, ArrayType)
    content_type = array_type.contents
    scale = content_type.size_bytes(context.declarations)
    offset = context.next_temp
    context.next_temp += 1
    address = context.next_temp
    context.next_temp += 1
    dest = context.next_temp
    context.next_temp += 1
    # TODO types
    result.code.append(f"%t{offset} =l mul %t{index}, {scale}")
    result.code.append(f"%t{address} =l add %t{base}, %t{offset}")
    result.code.append(f"%t{dest} =l loadl %t{address}")
    return result


@compile_to_ssa.register
def _(target: StructPointerElementExpression, context: CompileContext) -> SsaResult:
    result = compile_to_ssa(target.base, context)
    base_dest = context.next_temp - 1
    # hoooo boy.
    base_type = target.base.type(context.declarations)
    assert isinstance(base_type, PointerType)
    assert isinstance(base_type.target, BasicType)
    hopefully_struct, struct_name = base_type.target.name.split(' ')
    assert hopefully_struct == 'struct'
    target_struct = None
    for decl in context.declarations:
        if isinstance(decl, StructDeclaration) and decl.name == struct_name:
            if decl.fields is None:
                raise KeyError('struct ' + struct_name + ' is opaque')
            target_struct = decl
            break
    if target_struct is None:
        raise KeyError('struct ' + struct_name + ' not found')
    offset = 0
    for field in target_struct.fields:
        if field.name == target.element:
            break
        else:
            offset += field.type.size_bytes(context.declarations)
    temp = context.next_temp
    context.next_temp += 1
    result_dest = context.next_temp
    context.next_temp += 1
    # TODO types
    result.code.append(f"%t{temp} =l add %t{base_dest}, {offset}")
    result.code.append(f"%t{result_dest} =l loadl %t{temp}")
    return result


@compile_to_ssa.register
def _(target: AddressOfExpression, context: CompileContext) -> SsaResult:
    if isinstance(target.body, StructPointerElementExpression) or isinstance(target.body, ArrayIndexExpression):
        result = compile_to_ssa(target.body, context)
        result.code.pop()
        context.next_temp -= 1
    else:
        raise NotImplementedError('address of ' + str(type(target.body)))
    return result


@compile_to_ssa.register
def _(target: DirectAssignment, context: CompileContext) -> SsaResult:
    result = compile_to_ssa(target.value, context)
    result_dest = context.next_temp - 1
    if isinstance(target.destination, VariableExpression):
        raise NotImplementedError('assign directly to variable')
    elif isinstance(target.destination, StructPointerElementExpression) or isinstance(target.destination, ArrayIndexExpression):
        sub_result = compile_to_ssa(target.destination, context)
        last_instr = sub_result.code.pop()
        _, _, _, location = last_instr.split(' ')
        # TODO type
        sub_result.code.append(f"storel %t{result_dest}, {location}")
        result += sub_result
    else:
        raise NotImplementedError('assign to ' + str(type(target.destination)))
    return result


@compile_to_ssa.register
def _(target: UpdateAssignment, context: CompileContext) -> SsaResult:
    return compile_to_ssa(target.deconstruct(), context)


@compile_to_ssa.register
def _(target: SizeofExpression, context: CompileContext) -> SsaResult:
    target = target.body
    if isinstance(target, Expression):
        target = target.type(context.declarations)
    size = target.size_bytes(context.declarations)
    return compile_to_ssa(ConstantExpression(str(size)), context)
