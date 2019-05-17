# Quick hacky script to convert toyota tests to a friendlier format

from __future__ import print_function
import sys
import os

sys.path.extend(['.', '..'])

from pycparser import c_parser, c_ast, parse_file, c_generator

generator = c_generator.CGenerator()
to_output = {}
filename = None
basename = None
output_dir = None
log_dir = None

ignored = []

def is_valid_name(name):
    if name.startswith(basename) and len(name) >= len(basename) + 4:
        s = name[len(basename):len(basename)+4]
        return (s.startswith("_") and s[1:4].isdigit())
    return False

def get_test_number(name):
    if name.startswith(basename):
        s = name[len(basename)+1:]
        # Assuming number is 3 digits
        return s[:3]
    else:
        raise AssertionError("Oh no... unknown name %s" %(basename))

class Visitor(c_ast.NodeVisitor):
    def visit_FuncDef(self, node):
        global ignored
        global to_output
        if is_valid_name(node.decl.name):
            test_number = get_test_number(node.decl.name)
            c_string = generator.visit(node)
            if not test_number in to_output:
                to_output[test_number] = []
            to_output[test_number].append(c_string)
        else:
            ignored.append(node.decl.name)

    def visit_Typedef(self, node):
        global ignored
        global to_output

        if is_valid_name(node.name):
            test_number = get_test_number(node.name)
            c_string = generator.visit(node) + ";"
            if not test_number in to_output:
                to_output[test_number] = []
            to_output[test_number].append(c_string)
        else:
            ignored.append(node.name)

    def visit_Decl(self, node):
        global ignored
        global to_output

        if is_valid_name(node.name):
            test_number = get_test_number(node.name)
            c_string = generator.visit(node) + ";"
            if not test_number in to_output:
                to_output[test_number] = []
            to_output[test_number].append(c_string)
        else:
            ignored.append(node.name)

def show_func_defs(filename):
    ast = parse_file(filename, use_cpp=True,
                     cpp_args=r'-Iutils/fake_libc_include')
    v = Visitor()
    v.visit(ast)

def output_test(test_name):
    if not test_name in to_output:
        raise AssertionError ("Test %s not in to_output" %(test_name))

    of = open(os.path.join(output_dir, basename + "_" + test_name + ".c"), "w")

    # special case rand
    """
    if "rand" in ignored:
        of.write("int rand(void);\n")
    """

    of.write("#include <stdlib.h>\n")
    of.write("#include <stdint.h>\n")
    of.write("int idx, sink;\n")
    of.write("void *psink;\n")

    # Output test case
    for v in to_output[test_name]:
        of.write(v+ "\n")

    # We don't actually need this, but oh well:
    of.write("int main(void) {%s();}\n" %(basename + "_" + test_name))

    of.close()

if __name__ == "__main__":
    if len(sys.argv) > 3:
        filename = sys.argv[1]
        output_dir = sys.argv[2]
        log_dir = sys.argv[3]
        if not os.path.exists(output_dir):
            raise AssertionError("Output directory must exist")
        if not os.path.exists(log_dir):
            raise AssertionError("Log directory must exist")
    else:
        raise AssertionError("Provide filename and output dirname and log dir")
    basename = os.path.basename(os.path.normpath(filename)).rstrip(".c")
    show_func_defs(filename)

    for k in to_output:
        output_test(k)

    logfile = open(os.path.join(log_dir,basename + ".log"), "w")
    logfile.write(ignored.__str__() + "\n")
    logfile.close()

