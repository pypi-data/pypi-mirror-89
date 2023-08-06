#
# Copyright (c) 2020 Carsten Igel.
#
# This file is part of rtcg
# (see https://github.com/carstencodes/rtcg).
#
# License: 3-clause BSD, see https://opensource.org/licenses/BSD-3-Clause
#

"""Creates a simple runtime function wrapper, that is typed.
"""

from dataclasses import dataclass, field
from typing import Iterable, Type, Any, Optional, Callable, Dict, List, Union


Primitive = Union[str, int, bool, float]
NoneType = type(None)


@dataclass
class Argument:
    """Represents a simple parameter of a function to generate."""

    name: str = field()
    type: Type = field()
    default_value: Optional[Primitive] = field(default=None)


@dataclass
class Decorator:
    """Represents a decorator to use for a function."""

    name: str = field()
    decorator_fn: Callable = field()
    arguments: List[Primitive] = field(default_factory=list)


def create_function(
        name: str,
        trampoline: Callable,
        *parameters: Argument,  # noqa: E999
        result_type: Type = NoneType,
        scope: Dict[str, Any] = None,
        decorators: List[Decorator] = None) -> Callable:
    """Creates a typed wrapper function.

    Args:
        name (str): The name of the function to generate.
        trampoline (Callable): The function to call
        result_type (Type, optional): The resulting type.
           Defaults to NoneType.
        scope (Dict[str, Any], optional): The scope of
           variables to use. Defaults to None.
        decorators (List[Decorator], optional): The list of
           decorators to use. Defaults to None.

    Returns:
        Callable: The wrapped function.
    """
    lines: List[str] = []
    local_scope = dict()
    if scope is not None:
        local_scope.update(**scope)

    __append_decorators(decorators, lines, local_scope)

    result: str = "None"
    if result_type is not NoneType:
        result = "_{}_ResultType".format(name)
        local_scope["_{}_ResultType".format(name)] = result_type

    params = __create_parameters_in_declaration(parameters, local_scope)

    lines.append("def __wrapped_function({}) -> {}:".format(params, result))
    __create_function_body(
        trampoline, parameters, result_type, lines, local_scope)

    code: str = "\n".join(lines)

    # pylint: disable=W0122
    exec(code, local_scope)
    result_fn = local_scope["__wrapped_function"]

    return result_fn


def __create_function_body(
        trampoline: Callable,
        parameters: Iterable[Argument],
        result_type: Optional[Type],
        lines: List[str],
        local_scope: Dict[str, Any]) -> None:
    indent = "    "
    if len(parameters) > 0:
        lines.append("{}_params = dict(".format(indent))
        for param in parameters:
            lines.append("{i}{i}{n} = {n},".format(i=indent, n=param.name))
        lines.append("{})".format(indent))
    else:
        lines.append(indent + "_params = {}")
    pre_statement = ""
    if result_type is not NoneType:
        pre_statement = "return "
    lines.append(
        "{}{}__trampoline_fn(**_params)".format(indent, pre_statement)
    )
    local_scope["__trampoline_fn"] = trampoline


def __create_parameters_in_declaration(
        parameters: Iterable[Argument],
        local_scope: Dict[str, Any]) -> str:
    params: str = ""
    if len(parameters) > 0:
        parameter_values: List[str] = []
        for param in parameters:
            value = param.name
            if param.type is not None:
                value = "{}: _{}_Type".format(value, param.name)
                local_scope["_{}_Type".format(param.name)] = param.type
            if param.default_value is not None:
                value = __format_value(param.default_value)
                value = "{} = {}".format(value, param.default_value)
            parameter_values.append(value)
        params = ", ".join(parameter_values)
    return params


def __append_decorators(
        decorators: Iterable[Argument],
        lines: List[str],
        local_scope: Dict[str, Any]) -> None:
    if decorators is not None and len(decorators) > 0:
        for decorator in decorators:
            value: str = "@{}".format(decorator.name)
            local_scope[decorator.name] = decorator.decorator_fn
            args = decorator.arguments
            if args is not None and len(args) > 0:
                value = "{}(".format(value)
                dec_args: List[str] = []
                for arg in decorator.arguments:
                    val: str = __format_value(arg)
                    dec_args.append(val)
                value = "{}{}".format(value, ", ".join(dec_args))
                value = "{})".format(value)
            lines.append(value)


def __format_value(arg: Primitive) -> str:
    """Formats a value to a string. If the value is a string,
       it will be enclosed with quotes.

    Args:
        arg (Primitive): The value to format.

    Returns:
        str: The formatted argument.
    """
    val: str = str(arg)
    if arg is str:
        val = '"{}"'.format(arg)

    return val
