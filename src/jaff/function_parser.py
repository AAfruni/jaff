"""
This module contains code the parse auxiliary function files.
"""

from sympy import Function, parse_expr


#############################################################
def parse_error(line, fname, funcname=None):
    """
    Utility function to report parsing errors

    Parameters:
        line : string
            line that produced the parsing error
        fname : string
            file name that produced the parsing error
        funcname : string
            name of function that was being parsed when
            the error was encountered

    Returns:
        Nothing

    Raises:
        ValueError
    """

    if funcname is None:
        errstr = "file {:s}: encountered error when parsing line\n{:s}".format(
            fname, line
        )
    else:
        errstr = (
            "file {:s}: encountered error in parsing "
            "function {:s}; unparseable line\n"
            "{:s}".format(fname, funcname, line)
        )
    raise ValueError(errstr)


def strip_trailing_comments(line):
    """
    Strip trailing comments from a line

    Parameters:
        line : string
            the line to strip

    Returns
        str : string
            the stripped line
    """
    comment_start = line.find("#")
    if comment_start != -1:
        return line[:comment_start].rstrip()
    else:
        return line


#############################################################
def parse_func_declaration(line):
    """
    Parse a function declaration line

    Parameters:
        line : string
            the function declaration line

    Returns:
        funcname : string
            name of function
        funcargs : list
            list of sympy.Symbol objects giving function arguments

    Raises:
        ValueError, if the function declaration is not syntactically valid
    """

    # Make sure the line starts correctly
    if (
        not line.startswith("@function")
        and not line.startswith("@ratefunction")
        and not line.startswith("@deltaE")
        and not line.startswith("@heating_cooling_rate")
    ):
        raise ValueError

    # Remove leading @function or @
    if line.startswith("@function"):
        funcstring = line[len("@function") :].strip()
    else:
        funcstring = line[1:].strip()

    # Strip any trailing comments
    funcstring = strip_trailing_comments(funcstring)

    # Find leading parenthesis and extract function name
    firstparen = funcstring.find("(")
    if firstparen == -1:
        raise ValueError
    funcname = funcstring[:firstparen]

    # Make sure final character is a closing parenthesis,
    # then extract arguments
    if not funcstring.endswith(")"):
        raise ValueError

    # Extract list of arguments
    funcargs = funcstring[firstparen + 1 : -1].split(",")
    funcargs = [parse_expr(f.strip()) for f in funcargs if len(f.strip()) > 0]

    # Return
    return funcname, funcargs


def parse_funcfile(fname):
    """
    Parse a JAFF auxiliary function file

    Parameters:
        fname : string
            name of file to parse

    Returns:
        funcs : dict
            a dict whose keys are the names of functions and
            whose values are dicts containing the fields "def",
            "args", and "argcomments"; "def" contains a Sympy
            expression giving the function definition, "args"
            contains a list of Sympy.Symbols defining the
            arguments, "comments" is a string that captures any
            comments the follow the function definition,
            and "argcomments" is a list of strings capturing
            comments on the definitions of the arguments.

    Raises:
        IOError, if the file does not exist or cannot be parsed
    """

    # Prepare empty function and variables lists to return
    funcs = {}

    # Empty list of global variables to substitute
    global_symbols = []
    global_rules = []

    # Read through file
    acc_line = ""
    with open(fname) as fp:
        funcname = None
        for line in fp:
            # Strip whitespace
            line = line.strip()

            # Skip blank lines
            if len(line) == 0:
                continue

            # Check if this line ends with a backslash, indicating
            # continuation onto the next line; if so, just accumulate
            # and go to next line
            if line.endswith("\\"):
                acc_line += line[:-1] + " "
                continue
            else:
                line = acc_line + line
                acc_line = ""

            # Are we inside a function definition or not?
            if funcname is None:
                # Not in a function definition, so all we
                # should find are comment lines or lines that
                # start a function declaration
                if line[0] == "#":
                    continue  # Comment line
                elif (
                    line.startswith("@function")
                    or line.startswith("@ratefunction")
                    or line.startswith("@deltaE")
                    or line.startswith("@heating_cooling_rate")
                ):
                    # Function declaration line
                    try:
                        funcname, funcargs = parse_func_declaration(line)
                        funcarg_comments = {}
                        subst_symbols = []
                        subst_rules = []
                    except ValueError:
                        parse_error(line, fname)
                elif line.startswith("@var"):
                    # Global variable declaration line
                    try:
                        # Strip trailing comments
                        line = strip_trailing_comments(line)

                        # Strip the beginning @var
                        line = line[len("@var") :].strip()

                        # Split line at first = sign
                        splitline = line.split("=", maxsplit=1)
                        if len(splitline) != 2:
                            parse_error(line, fname, funcname)

                        # Construct global substitution rule
                        global_symbols.append(parse_expr(splitline[0]))
                        local_dict = {
                            str(k): v for k, v in zip(global_symbols[:-1], global_rules)
                        }
                        global_rules.append(
                            parse_expr(splitline[1], local_dict=local_dict)
                        )
                    except:
                        parse_error(line, fname, funcname)

                else:
                    parse_error(line, fname)

            else:
                # We are in a function definition; things we can find
                # here are (1) comments explaining what variables mean,
                # (2) substitution commands of the form x = y, (3)
                # return commands that end a function; anythin else is
                # an errror

                if line[0] == "#":
                    # This is a comment line; check if the comment
                    # starts with the name of one of our variables,
                    # and if so capture the rest of the line
                    comment = line[1:].strip()
                    for arg in funcargs:
                        argstr = str(arg)
                        if comment.startswith(argstr):
                            funcarg_comments[arg] = comment[len(argstr) :].strip()

                elif not line.startswith("return"):
                    # This should be a command line, of the form x = y;
                    # we need to capture this as a sympy substitution rule,
                    # which we will apply to the final function

                    # Strip trailing comments
                    line = strip_trailing_comments(line)

                    # Split line at first = sign
                    splitline = line.split("=", maxsplit=1)
                    if len(splitline) != 2:
                        parse_error(line, fname, funcname)
                    try:
                        subst_symbols.append(parse_expr(splitline[0]))
                        local_dict = {
                            str(k): v for k, v in zip(subst_symbols[:-1], subst_rules)
                        }
                        subst_rules.append(
                            parse_expr(splitline[1], local_dict=local_dict)
                        )
                    except:
                        parse_error(line, fname, funcname)

                else:
                    # This should be a return line, of the form return xxx;
                    # we need to capture the content of the function, apply
                    # any substitution rules we have to it, and then add
                    # the final result to the list of functions to be
                    # returned

                    # Strip trailing comments
                    line = strip_trailing_comments(line)

                    # Construct function definition
                    funcdef = parse_expr(
                        line[len("return") :].strip(),
                        local_dict={
                            str(k): v for k, v in zip(subst_symbols, subst_rules)
                        },
                    )

                    # Apply substitution rules, starting from final one and
                    # working backwards
                    for ss, sr in zip(subst_symbols[::-1], subst_rules[::-1]):
                        funcdef = funcdef.subs(ss, sr)

                    # Substitute in global variables
                    for ss, sr in zip(global_symbols[::-1], global_rules[::-1]):
                        funcdef = funcdef.subs(ss, sr)

                    # Record final results
                    funcs[funcname.lower()] = {
                        "def": funcdef,
                        "args": funcargs,
                        "argcomments": funcarg_comments,
                    }

                    # Reset state
                    funcname = None

    # Return list of functions
    return funcs
