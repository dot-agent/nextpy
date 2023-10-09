import pyparsing as pp

role_start_tag = pp.Suppress(pp.Optional(pp.White()) + pp.Literal("<|im_start|>"))
role_start_name = pp.Word(pp.alphanums + "_")("role_name")
role_kwargs = pp.Suppress(pp.Optional(" ")) + pp.Dict(pp.Group(pp.Word(pp.alphanums + "_") + pp.Suppress("=") + pp.QuotedString('"')))("kwargs")
role_start = (role_start_tag + role_start_name + pp.Optional(role_kwargs) + pp.Suppress("\n")).leave_whitespace()
role_end = pp.Suppress(pp.Literal("<|im_end|>"))
role_content = pp.Combine(pp.ZeroOrMore(pp.CharsNotIn("<") | pp.Literal("<") + ~pp.FollowedBy("|im_end|>")))("role_content")
role_group = pp.Group(role_start + role_content + role_end)("role_group").leave_whitespace()
partial_role_group = pp.Group(role_start + role_content)("role_group").leave_whitespace()
roles_grammar = pp.ZeroOrMore(role_group) + pp.Optional(partial_role_group) + pp.StringEnd()

# import pyparsing as pp

# role_start_tag = pp.Literal("<|im_start|>")
# role_start_name = pp.Word(pp.alphanums + "_")
# role_kwargs = pp.Dict(pp.Group(pp.Word(pp.alphanums + "_") + pp.Suppress("=") + pp.QuotedString('"')))
# role_start = role_start_tag + role_start_name + pp.Optional(role_kwargs) + pp.Suppress("\n")
# role_end = pp.Literal("<|im_end|>")
# role_content = pp.CharsNotIn("<|im_start|><|im_end|>")

# r'<\|im_start\|>([^\n]+)\n(.*?)(?=<\|im_end\|>|$)'

# define the syntax for the function definitions
start_functions = pp.Suppress(pp.Literal("## functions\n\nnamespace functions {\n\n"))
comment = pp.Combine(pp.Suppress(pp.Literal("//") + pp.Optional(" ")) + pp.restOfLine)
end_functions = pp.Suppress("} // namespace functions")
function_def_start = pp.Optional(comment)("function_description") + pp.Suppress(pp.Literal("type")) + pp.Word(pp.alphas + "_")("function_name") + pp.Suppress(pp.Literal("=") + pp.Literal("(_:") + pp.Literal("{"))
function_def_end = pp.Suppress(pp.Literal("})") + pp.Literal("=>") + pp.Literal("any;"))
parameter_type = (pp.Word(pp.alphas + "_")("simple_type") | pp.QuotedString('"')("enum_option") + pp.OneOrMore(pp.Suppress("|") + pp.QuotedString('"')("enum_option"))("enum")) + pp.Suppress(pp.Optional(","))
parameter_def = pp.Optional(comment)("parameter_description") + pp.Word(pp.alphas + "_")("parameter_name") + pp.Optional(pp.Literal("?"))("is_optional") + pp.Suppress(pp.Literal(":")) + pp.Group(parameter_type)("parameter_type")
function_def = function_def_start + pp.OneOrMore(pp.Group(parameter_def)("parameter")) + function_def_end
functions_def = start_functions + pp.OneOrMore(pp.Group(function_def)("function")) + end_functions
