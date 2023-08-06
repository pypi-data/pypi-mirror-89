#!/usr/bin/env python3

import os
import sys
import subprocess
import traceback
from certora_cli.certoraUtils import read_from_conf, get_certora_root_directory  # type: ignore
from certora_cli.certoraUtils import OPTION_CACHE, DEFAULT_CONF
from certora_cli.certoraUtils import nestedOptionHack, debug_print_
from certora_cli.certoraUtils import sanitize_path, prepare_call_args
from certora_cli.certoraUtils import legal_run_args, check_legal_args, CloudVerification, checkResultsFromFile
from certora_cli.certoraUtils import is_windows
from certora_cli.certoraUtils import CERTORA_BUILD, CERTORA_VERIFY
from certora_cli.certoraUtils import which
from certora_cli.certoraUtils import warning_print
import argparse
import re
import ast
import pkg_resources
from typing import Dict, List, Optional, Tuple, Any, Union, Set

# a list of valid environments to be used when running remotely
VALID_ENVS = ["--staging", "--cloud"]
JAR_PATH_KEY = "jar_path"
JAVA_ARGS_KEY = "java_args"
BUILD_SCRIPT_PATH_KEY = "build_script_path"
TOOL_OUTPUT_LOCAL = "toolOutput"

RUN_IS_LIBRARY = False
DEBUG = False
DEFAULT_CLOUD_ENV = 'production'
DEFAULT_STAGING_ENV = 'master'


def get_version() -> str:
    """
    :return: The version of the Certora CLI's python package in format XX.YY
    :raises pkg_resources.DistributionNotFound if the 'certora-cli' python package is somehow not found
    """
    try:
        version = pkg_resources.get_distribution("certora-cli").version
        return version
    except pkg_resources.DistributionNotFound:
        return "couldn't find certora-cli distributed package"


def print_version() -> None:
    print("certora-cli", get_version())


def exit_if_not_library(code: int) -> None:
    # Uri - we can use our own exception...
    if RUN_IS_LIBRARY:
        return
    else:
        sys.exit(code)


def debug_print(s: str) -> None:
    # TODO: We should have a logger for this - Uri
    debug_print_(s, DEBUG)


def print_usage() -> None:
    # TODO: Can be auto-generated - Uri
    print("""Usage:
       [file[:contractName] ...] or CONF_FILE.conf or TAC_FILE.tac
       [--link [contractName:slot=contractName ...]]
       [--verify [contractName:specName ...] (space separated)]
       [--solc SOLC_EXEC (default: solc)] or [--solc_map [name=solc,..]]
       [--settings [flag1,...,k1=v1,...]]
       For example,
       ContractA.sol ContractB.sol --link ContractA:b=ContractB --verify ContractA:verifyingRules.spec --solc solc5
       [--help]
       [--help-advanced]""",
          flush=True)


def print_advanced_usage() -> None:
    print("""Usage:
       If no arguments, read from default.conf
       Otherwise:
       [file[:contractName] ...] or CONF_FILE.conf or TAC_FILE.tac
       [--settings [flag1,...,k1=v1,...]]
       [--cache NAME]
       [--output OUTPUT_FILE_NAME (default: .certora_build)]
       [--output_folder OUTPUT_FOLDER_NAME (default: .certora_config)]
       [--link [contractName:slot=contractName ...]]
       [--address [contractName:address ...] (default: auto-assigned)]
       [--path ALLOWED_PATH (default: $PWD/contracts/)]
       [--packages_path PATH (default: $NODE_PATH)] or [--packages [name=path,...]]
       [--solc SOLC_EXEC (default: solc)] or [--solc_map [name=solc,..]]
       [--solc_args 'SOLC_ARGS' (default: none. wrap in quotes, may need to escape)]
       [--verify [contractName:specName ...] (space separated)]
       [--assert [contractName, ...]]
       [--dont_fetch_sources]
       [--iscygwin]
       [--varmap]
       [--build PATH_TO_BUILD_SCRIPT (default: $CERTORA/certoraBuild.py)]
       [--jar JAR_FULL_PATH (full path to jar including name)]
       [--javaArgs 'JAVA_ARGS']
       [--toolOutput PATH (only in local mode)]
       [--disableLocalTypeChecking]
       [--debug]
       [--help]
       [--staging/cloud [environment] (run on the amazon server, default environment is production)]""",
          flush=True)


def run_cmd(cmd: str, overrideExitcode: bool, customErrorMessage: Optional[str] = None) -> None:
    args = None
    try:
        args = prepare_call_args(cmd)
        exitcode = subprocess.call(args, shell=False)
        if exitcode:
            debug_print(str(args))
            default_msg = "Failed to run %s, exitcode %d" % (' '.join(args), exitcode)
            if customErrorMessage is not None:
                debug_print(default_msg)
                print(customErrorMessage, flush=True)
            else:
                print(default_msg, flush=True)
            debug_print("Path is %s" % (os.getenv("PATH"),))
            if not overrideExitcode:
                exit_if_not_library(1)
        else:
            debug_print("Exitcode %d" % (exitcode,))
    except Exception:
        debug_print(str(args))
        #  debug_print(traceback.format_exc())
        default_msg = "Failed to run %s" % (cmd,)
        if customErrorMessage is not None:
            debug_print(default_msg)
            print(customErrorMessage, flush=True)
        else:
            print(default_msg, flush=True)
        debug_print(str(sys.exc_info()))
        exit_if_not_library(1)


def parse_settings_arg(settingsArg: str) -> List[str]:
    """
        This function parses a settings arg string.
        Commas ',' separate different settings.
        Since commas can appear inside values (like for method choice, '-m'),
        we need to ignore commas that appear within parenthesis.
        It's not a regular property, so we just parse this string.
        This is done by iterating over the characters and maintaining whether we're
        reading the key (assumed that it can't have commas) (IS_KEY),
                the value (which may have commas only within parenthesis) (not IS_KEY),
                in-between (comma for key only, or '=' for key-value properties),
                where we are in the portion (key/value) (idxPortion),
                the current key (KEY) or value (VALUE),
                where we are in the string (idxString),
                how many parenthesis we didn't close yet (COUNT_PAREN)
    """
    debug_print("Parsing {}".format(settingsArg))
    COUNT_PAREN = 0
    IS_KEY = True
    idxString = 0
    idxPortion = 0
    KEY = ""
    VALUE = ""
    args_list = []
    while idxString < len(settingsArg):
        ch = settingsArg[idxString]
        # debug_print("handling char {}".format(ch))
        if IS_KEY:
            if ch == '(' or ch == ')':
                print("""Error: Cannot contain parenthesis in key,
                got {} in index {} of {}""".format(ch, idxString, settingsArg))
                exit_if_not_library(1)

            if idxPortion == 0:
                if ch != '-':
                    print("Error: parsing settings {}, expected '-', got '{}' at character {}".format(settingsArg, ch,
                                                                                                      idxString))
                    exit_if_not_library(1)
                KEY = "-"
                idxPortion += 1
                idxString += 1
                continue

            if idxPortion > 0:
                if ch == '=':
                    debug_print("Got key {}".format(KEY))
                    IS_KEY = False
                    idxPortion = 0
                    idxString += 1
                elif ch == ',':
                    KEY += " "
                    # Still key, but no value
                    debug_print("Adding {}".format(KEY))
                    args_list.append(KEY)
                    KEY = ""
                    idxPortion = 0
                    idxString += 1
                else:
                    KEY += ch
                    if idxString + 1 == len(settingsArg):  # finishing
                        debug_print("Adding {}".format(KEY))
                        args_list.append(KEY)
                    idxPortion += 1
                    idxString += 1
            continue

        # Here: is handling VALUE
        if not IS_KEY:
            if ch == '(':
                COUNT_PAREN += 1
            if ch == ')':
                COUNT_PAREN -= 1

            if COUNT_PAREN < 0:
                print("Error: Unbalanced parenthesis in {}".format(settingsArg))
                exit_if_not_library(1)

            if (ch == "," and COUNT_PAREN == 0) or idxString + 1 == len(settingsArg):
                # done with this pair
                if ch != ",":
                    VALUE += ch  # close parenthesis probably

                if COUNT_PAREN > 0:
                    print("Error: Cannot close value {} if parenthesis are unbalanced".format(VALUE))
                    exit_if_not_library(1)

                debug_print("Adding {} {}".format(KEY, VALUE))
                args_list.append("{} {}".format(KEY, VALUE))
                IS_KEY = True
                KEY = ""
                VALUE = ""
                idxPortion = 0
                idxString += 1
            else:
                VALUE += ch
                idxString += 1
                idxPortion += 1

    return args_list


def parse_args(args: List[str]) -> Tuple[List[str], Dict[str, Any], List[str], Dict[str, Any], Dict[str, Any]]:
    run_args = []  # type: List[str]
    build_args = []  # type: List[str]
    script_args = {}  # type: Dict[str, Any]
    timers = {}  # type: Dict[str, Any]
    script_args[JAVA_ARGS_KEY] = ""
    custom_args = {}  # type: Dict[str, Any]

    i = 0

    while i < len(args):
        current_arg = args[i]
        current_potential_value = args[i + 1] if len(args) > i + 1 else None
        if current_arg in VALID_ENVS:  # when it's production --cloud or no flag
            script_args["env"] = current_arg[2:]
            # add branches to the PROD environment
            if (current_arg in ["--staging", "--cloud"] and current_potential_value is not None and not
               current_potential_value.startswith("-")):
                i += 1
                script_args["branch"] = current_potential_value
        elif current_arg == "--settings":
            i += 1  # inc for the settings
            if current_potential_value is not None:
                settingsList = parse_settings_arg(current_potential_value)
                run_args.extend(settingsList)
                # script_args["settings"] = current_potential_value
                if "settings" in script_args:
                    script_args["settings"].extend(settingsList)
                else:
                    script_args["settings"] = settingsList
            else:
                print("--settings requires an argument", flush=True)
                exit_if_not_library(1)
        elif current_arg == "--jar":
            script_args[JAR_PATH_KEY] = ""
            if current_potential_value and not current_potential_value.startswith("-"):
                script_args[JAR_PATH_KEY] = current_potential_value
                i += 1
        elif current_arg == "--javaArgs":
            if current_potential_value and not current_potential_value.startswith("-"):
                normalized = ''.join(map(lambda x: x.replace("\"", ""), current_potential_value))
                old = script_args[JAVA_ARGS_KEY]
                if old != "":
                    script_args[JAVA_ARGS_KEY] = old + " " + normalized
                else:
                    script_args[JAVA_ARGS_KEY] = normalized
                i += 1
        elif current_arg == "--build":
            i += 1  # inc for the path
            script_args[BUILD_SCRIPT_PATH_KEY] = current_potential_value
        elif current_arg == "--key":
            i += 1
            script_args["key"] = current_potential_value
        elif current_arg == "--toolOutput" and current_potential_value is not None:
            i += 1
            script_args[TOOL_OUTPUT_LOCAL] = current_potential_value
            run_args.extend(["-json", current_potential_value])
        elif current_arg == "--msg" and current_potential_value is not None:
            i += 1
            script_args["msg"] = current_potential_value
            if len(script_args["msg"]) > 100:
                warning_print("notification message is too long. Only the first 100 characters will be used")
                script_args["msg"] = script_args["msg"][:100]
        elif current_arg in ["--queue_wait_minutes", "--max_poll_minutes", "--log_query_frequency_seconds",
                             "--max_attempts_to_fetch_output", "--delay_fetch_output_seconds"] and \
                current_potential_value is not None:
            i += 1
            try:
                timers[current_arg] = int(current_potential_value)
            except ValueError:
                warning_print("wrong timer type. Removing {}".format(current_arg), flush=True)
        elif current_arg in ["--disableLocalTypeChecking"]:
            custom_args["disableLocalTypeChecking"] = True
        else:
            build_args.append(current_arg)

        i += 1

    if len(build_args) == 0 or (build_args[0].endswith(".conf") or build_args[0].startswith("--")):
        # No build args (default.conf) or first build arg ends with .conf or starts with -- (an option)
        files = []  # type: List[str]
        fileToContractName = {}  # type: Dict[str, str]
        parsed_options = {"solc": "solc"}

        if len(build_args) == 0:
            conf_file = DEFAULT_CONF
        else:
            conf_file = build_args[0]

        read_from_conf(conf_file, parsed_options, files, fileToContractName)

        if OPTION_CACHE in parsed_options:
            build_args.append("--cache")
            build_args.append(parsed_options[OPTION_CACHE])

    return build_args, script_args, run_args, timers, custom_args


def get_cache_key(args: List[str]) -> Optional[str]:
    if "--cache" in args:
        location_of_cache = args.index("--cache")
        if location_of_cache + 1 >= len(args):
            print("Did not provide cache key", flush=True)
            exit_if_not_library(1)
            return None
        else:
            return args[location_of_cache + 1]
    else:
        return None


def get_cache_param(cache_arg: Optional[str]) -> str:
    if cache_arg is not None:
        return " -cache %s" % cache_arg
    else:
        return ""


def is_tac_file(filename: str) -> bool:
    return filename.endswith(".tac")


def run_local_type_check(args: Dict[str, Any]) -> None:
    # Should even run local type checking? by default yes, but allow opt-out
    if "disableLocalTypeChecking" in args and args["disableLocalTypeChecking"]:
        print("Local checks of specification files disabled. It is recommended to enable the checks.")
        return

    # Check if java exists on the machine
    java = which("java")
    if java is None:
        print(
            "`java` is not installed. It is highly recommended to install Java to check specification files locally.")
        return  # if user doesn't have java installed, user will have to wait for remote type checking

    # Find path to typechecker jar
    local_certora_path = sanitize_path(
        os.path.join(os.path.split(__file__)[0], "certora_jars", "Typechecker.jar"))
    installed_certora_path = sanitize_path(
        os.path.join(os.path.split(__file__)[0], "..", "certora_jars", "Typechecker.jar"))
    path_to_typechecker = local_certora_path if os.path.isfile(local_certora_path) else installed_certora_path
    # if typechecker jar does not exist, we just skip this step
    if not os.path.isfile(path_to_typechecker):
        print("Error: Could not run type checker locally.", flush=True)
        return

    # args to typechecker
    build_file = CERTORA_BUILD
    verify_file = CERTORA_VERIFY
    debug_print("Path to typechecker is {}".format(path_to_typechecker))
    typecheck_cmd = "java -jar {} {} {}".format(path_to_typechecker, build_file, verify_file)

    # run it - exit with code 1 if failed
    run_cmd(typecheck_cmd, False, "Failed to compile spec file")


def main_with_args(args: List[str], isLibrary: bool = False, actualResultExpectedPath: Union[str, None] = None) -> None:
    get_args(args)  # Parse arguments
    # TODO: use parsed arguments

    # FIXME: actualResultExpectedPath is not used
    global RUN_IS_LIBRARY
    RUN_IS_LIBRARY = isLibrary
    global DEBUG
    try:
        if len(args) == 0:
            print_usage()
            exit_if_not_library(1)

        if "--debug" in sys.argv:
            DEBUG = True

        nestedOptionHack(args)

        if "--help" in args:
            print_usage()
            exit_if_not_library(1)

        if "--help-advanced" in args:
            print_advanced_usage()
            exit_if_not_library(1)

        check_legal_args(args, legal_run_args)
        build_args, script_args, run_args, timers, custom_args = parse_args(args)

        is_only_tac = is_tac_file(build_args[0])

        cache_arg = get_cache_key(build_args)
        if cache_arg is not None:
            run_args.append(get_cache_param(cache_arg))
            script_args[OPTION_CACHE] = cache_arg

        if BUILD_SCRIPT_PATH_KEY in script_args:
            build_script_path = sanitize_path(script_args[BUILD_SCRIPT_PATH_KEY])
            print("Running with custom build script" + build_script_path)
        else:
            build_script_path = "certoraBuild.py"

        if len(build_args) > 0:
            build_cmd = "%s %s" % (build_script_path, ' '.join(build_args))
        else:
            build_cmd = build_script_path

        # When a TAC file is provided, no build arguments will be processed
        if not is_only_tac:
            print("Building: %s" % (build_cmd,), flush=True)
            if BUILD_SCRIPT_PATH_KEY in script_args:
                run_cmd(build_cmd, False)
            else:
                from certora_cli.certoraBuild import main_with_args  # type: ignore
                main_with_args(build_args, isLibrary)

        defaultPath = "%s/emv.jar" % (sanitize_path(get_certora_root_directory()),)
        if JAR_PATH_KEY in script_args or (os.path.exists(defaultPath) and "env" not in script_args):
            jar_path = (
                script_args[JAR_PATH_KEY] if JAR_PATH_KEY in script_args and script_args[JAR_PATH_KEY]
                else defaultPath)
            if is_only_tac:
                run_args.insert(0, build_args[0])
            if JAVA_ARGS_KEY in script_args:
                java_args = script_args[JAVA_ARGS_KEY]
                check_cmd = " ".join(["java", java_args, "-jar", jar_path] + run_args)
            else:
                check_cmd = " ".join(["java", "-jar", jar_path] + run_args)
            print("Running: %s" % (check_cmd,), flush=True)
            compareWithToolOutput = TOOL_OUTPUT_LOCAL in script_args
            run_cmd(check_cmd, compareWithToolOutput)
            debug_print("Running the verifier like this:\n %s" % (check_cmd,))
            if compareWithToolOutput:
                print("Comparing tool output to expected:")
                result = checkResultsFromFile(script_args[TOOL_OUTPUT_LOCAL])
                if result:
                    exit_if_not_library(0)
                else:
                    exit_if_not_library(1)
        else:
            # In cloud mode, we first run a local type checker
            run_local_type_check(custom_args)
            script_args["buildArgs"] = ' '.join(args)
            script_args["version"] = get_version()

            if len(timers) > 0:  # at least one timer is supplied
                cv = CloudVerification(timers)
            else:
                cv = CloudVerification()
            result = cv.cliVerify(script_args)
            if result:
                exit_if_not_library(0)
            else:
                exit_if_not_library(1)

    except Exception:
        print("Encountered an error running Certora Prover", flush=True)
        if DEBUG:
            print(traceback.format_exc(), flush=True)
        exit_if_not_library(1)
    except KeyboardInterrupt:
        print('Interrupted', flush=True)


'''
########################################################################################################################
############################################### Argument types #########################################################
########################################################################################################################
'''


def type_non_negative_integer(string: str) -> str:
    """
    :param string: A string
    :return: The same string, if it represents a decimal integer
    :raises argparse.ArgumentTypeError if the string does not represent a non-negative decimal integer
    """
    if not re.match(r'^\d+$', string):
        raise argparse.ArgumentTypeError('expected a non-negative integer, instead given ' + string)
    return string


def type_jar(filename: str) -> str:
    if not os.path.isfile(filename):
        raise argparse.ArgumentTypeError("file " + filename + " does not exist.")
    if not os.access(filename, os.X_OK):
        raise argparse.ArgumentTypeError("no execute permission for jar file " + filename)

    basename = os.path.basename(filename)  # extract file name from path.
    # NOTE: expects Linux file paths, all Windows file paths will fails the check below!
    if re.search(r"^\w+\.jar$", basename):
        # Base file name can contain only alphanumeric characters or underscores
        return filename

    raise argparse.ArgumentTypeError("file " + filename + " is not of type .jar")


def type_readable_file(filename: str) -> str:
    if not os.path.exists(filename):
        raise argparse.ArgumentTypeError("file " + filename + " not found")
    if os.path.isdir(filename):
        raise argparse.ArgumentTypeError(filename + " is a directory and not a file")
    if not os.access(filename, os.R_OK):
        raise argparse.ArgumentTypeError("no read permissions for " + filename)
    return filename


def type_executable(filename: str) -> str:
    if is_windows() and not re.search(r"\.exe$", filename):
        filename += ".exe"

    common_mistakes_suffixes = ['sol', 'conf', 'tac', 'spec', 'cvl']
    for suffix in common_mistakes_suffixes:
        if re.search(r'^[^.]+\.' + suffix + '$', filename):
            raise argparse.ArgumentTypeError("wrong solidity executable given: " + filename)

    # TODO: find a better way to iterate over all directories in path
    for dirname in os.environ['PATH'].split(os.pathsep) + [os.getcwd()]:
        candidate = os.path.join(dirname, filename)
        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            return filename

    raise argparse.ArgumentTypeError("solidity executable " + filename + " not found in path")


def type_dir(dirname: str) -> str:
    if not os.path.exists(dirname):
        raise argparse.ArgumentTypeError("path " + dirname + " does not exist")
    if os.path.isfile(dirname):
        raise argparse.ArgumentTypeError(dirname + " is a file and not a directory")
    if not os.access(dirname, os.R_OK):
        raise argparse.ArgumentTypeError("no read permissions to " + dirname)
    return dirname


def type_tool_output_path(filename: str) -> str:
    if os.path.isdir(filename):
        raise argparse.ArgumentTypeError("--toolOutputPath " + filename + " is a directory")
    if os.path.isfile(filename):
        warning_print("--toolOutPutpath " + filename + " file already exists")
        if not os.access(filename, os.W_OK):
            raise argparse.ArgumentTypeError('No permission to rewrite --toolOutPutpath file ' + filename)
    else:
        try:
            with open(filename, 'w') as f:
                f.write('try')
            os.remove(filename)
        except (ValueError, IOError, OSError) as e:
            raise argparse.ArgumentTypeError("could not create --toolOutputPath file " + filename +
                                             ". Error: " + str(e))

    return filename


def type_list(candidate: str) -> List[str]:
    """
    Verifies the argument can be evaluated by python as a list
    """
    v = ast.literal_eval(candidate)
    if type(v) is not list:
        raise argparse.ArgumentTypeError("Argument \"" + str(candidate) + "\" is not a list")
    return v


def type_input_file(file: str) -> str:
    # [file[:contractName] ...] or CONF_FILE.conf or TAC_FILE.tac
    if '.sol' in file:
        if not re.search(r'^.+\.sol(:[^.:]+)?$', file):
            raise argparse.ArgumentTypeError("Bad input file format of " + file + ". Expected <contract_path>:<alias>")

        if ':' in file:
            file_path, alias = file.split(':')
            if not re.search(r'^\w+$', alias):
                raise argparse.ArgumentTypeError("file alias " + alias +
                                                 " can contain only alphanumeric characters or underscores")
        else:
            file_path = file

        type_readable_file(file_path)
        base_name = os.path.basename(file_path)[0:-4]  # get Path's leaf name and remove the trailing .sol
        if not re.search(r'^\w+$', base_name):
            raise argparse.ArgumentTypeError("file name " + file +
                                             " can contain only alphanumeric characters or underscores")
        return file

    if file.endswith('.tac') or file.endswith('.conf'):
        type_readable_file(file)
        return file

    raise argparse.ArgumentTypeError("input file " + file + " is not in one of the supported types (.sol, .tac, .conf)")


def type_verify_arg(candidate: str) -> str:
    if not re.search(r'^\w+:[^:]+\.(spec|cvl)$', candidate):
        # Regex: name has only one ':', has at least one letter before, one letter after and ends in .spec
        raise argparse.ArgumentTypeError("argument " + candidate + " for --verify option is in incorrect form. "
                                                                   "Must be formatted contractName:specName.spec")
    spec_file = candidate.split(':')[1]
    type_readable_file(spec_file)

    return candidate


def type_link_arg(link: str) -> str:
    if not re.search(r'^\w+:\w+=\w+$', link):
        raise argparse.ArgumentTypeError("Link argument " + link + " must be of the form contractA:slot=contractB"
                                                                   "or contractA:slot=<number>")
    return link


def type_struct_link(link: str) -> str:
    search_res = re.search(r'^\w+:([^:=]+)=\w+$', link)
    # We do not require firm form of slot number so we can give more informative warnings

    if search_res is None:
        raise argparse.ArgumentTypeError("Struct link argument " + link +
                                         " must be of the form contractA:number=contractB")
    try:
        parsed_int = int(search_res[1], 0)  # an integer or a hexadecimal
        if parsed_int < 0:
            raise argparse.ArgumentTypeError("struct link slot number negative at " + link)
    except ValueError:
        raise argparse.ArgumentTypeError("Struct link argument " + link +
                                         " must be of the form contractA:number=contractB")
    return link


def type_alias(contract: str) -> str:
    if not re.match(r'^\w+$', contract):
        raise argparse.ArgumentTypeError("contract alias " + contract +
                                         " can include only alphanumeric characters or underscores")
    return contract


def type_package(package: str) -> str:
    if not re.search("^[^=]+=[^=]+", package):
        raise argparse.ArgumentTypeError("a package must have the form name=path")
    path = package.split('=')[1]
    if not os.path.isdir(path):
        raise argparse.ArgumentTypeError("Package path " + path + " does not exist")
    if not os.access(path, os.R_OK):
        raise argparse.ArgumentTypeError("No read permissions for for packages directory " + path)
    return package


def type_settings_arg(settings: str) -> str:
    """
    Gets a string representing flags to be passed to another tool via --settings, in the form '-a,-b=2[,..]'
    @raise argparse.ArgumentTypeError
    """
    debug_print("settings pre-parsing= " + str(settings))
    settings = settings.lstrip()

    '''
    Split by commas UNLESS the commas are inside parenthesis, for example:
    "-b=2, -assumeUnwindCond, -rule=bounded_supply, -m=withdrawCollateral(uint256, uint256), -regressionTest"

    will become:
    ['-b=2',
    '-assumeUnwindCond',
    '-rule=bounded_supply',
    '-m=withdrawCollateral(uint256, uint256)',
    '-regressionTest']
    '''
    flags = re.split(r',(?![^()]*\))\s*', settings)
    '''
    Regex explanation:
    We want to match a comma.
    ?! is a negative lookahead. We do not match the comma if there is any number of non-parenthesis characters
    ending in a closing parenthesis.
    We also strip all whitespaces following commas, if any
    '''

    debug_print("settings after-split= " + str(settings))
    for flag in flags:
        debug_print("checking setting " + str(flag))
        if not re.search('^-[^-=]+(=[^-=]+)?', flag):
            raise argparse.ArgumentTypeError("illegal argument in --settings: " + flag)
    return settings


def type_java_arg(java_args: str) -> str:
    if not re.search('^".+"$', java_args):
        raise argparse.ArgumentTypeError('java argument must be wrapped in "", instead found ' + java_args)
    return java_args


def type_address(candidate: str) -> str:
    if not re.search(r'^[^:]+:\d+$', candidate):
        # Regex: name has only one ':', has at least one letter before, one letter after and ends in .spec
        raise argparse.ArgumentTypeError("argument " + candidate + " of --address option is in incorrect form. "
                                         "Must be formatted <contractName>:<non-negative number>")
    return candidate


def check_files_input(file_list: List[str]) -> None:
    """
    Verifies that correct input was inserted as input to files.
    As argparser verifies the files exist, and the correctness of the format, we only check if only a single operation
    mode was used.
    The allowed disjoint cases are:
    1. Use a single .conf file
    2. Use a single .tac file
    3. Use any number of [contract.sol:nickname ...] (at least one is guaranteed by argparser)
    @param file_list: A list of strings representing file paths
    @raise argparse.ArgumentTypeError if more than one of the modes above was used
    """
    num_files = len(file_list)
    if num_files > 1:  # if there is a single file, there cannot be a mix between file types
        for file in file_list:
            if '.tac' in file:
                raise argparse.ArgumentTypeError('Only a single .tac file can be used, given ' + str(num_files) +
                                                 ' files')
            if '.conf' in file:
                raise argparse.ArgumentTypeError('Only a single .conf file can be used, given ' + str(num_files) +
                                                 ' files')


def _get_natural_alias(contract: str) -> str:
    """
    Gets a path to a .sol file and returns its natural alias. The natural alias is basename of the path of the file,
    without file type suffix.
    For example:
    /Test/opyn/vault.sol has the alias vault.sol
    @param contract: A path to a .sol file
    @return: The natural alias of a contract file
    """
    contract = contract.split('/')[-1]  # Breaking path
    contract = contract.split('.')[0]
    return contract


def warn_verify_file_args(files: List[str]) -> Set[str]:
    """
    Verifies all file inputs are legal. If they are not, throws an exception.
    If there are any redundancies or duplication, warns the user.
    Otherwise, returns a set of all legal file aliases.
    @param files: A list of string of form: [contract.sol[:natural_alias] ...]
    @return: A set of strings, which are all recognized file aliases
    """

    """
    The logic is complex, and better shown by examples.
    Legal use cases:
    1. A.sol B.sol
        -> returns (A, B)
    2. A.sol:a B.sol:b C.sol
        -> returns (A, a, B, b, C)
    3. A.sol:B B.sol:c
        -> The contract names do not collide

    Warning cases:
    4. A.sol:a A.sol  # Should be an error
        -> A.sol is redundant
    5. A.sol A.sol:a  # Should be an error
        -> A.sol is redundant
    6. A.sol:a A.sol:a
        -> A.sol is redundant
    7. A.sol:A
        -> alias A is redundant

    Illegal cases:
    8. A.sol:a A.sol:b
        -> Cannot give two aliases to the same file
    9. A.sol:a B.sol:a
        -> Two files cannot have the same natural_alias
    10. ../A.sol A.sol
        -> Cannot use two files which have the same name
    11. A.sol:B B.sol
        -> Cannot use two files which have the same name

    Warning are printed only if the case is legal
    @raise argparse.ArgumentTypeError in an illegal case (see above)
    """
    if len(files) == 1 and (files[0].endswith(".conf") or files[0].endswith(".tac")):
        return set()  # No legal file aliases

    declared_contracts = set()
    all_warnings = set()

    contract_to_file: Dict[str, str] = dict()
    file_to_contract: Dict[str, str] = dict()

    for f in files:
        if ':' in f:
            filepath = f.split(':')[0]
            contract_name = f.split(':')[1]
            natural_contract_name = _get_natural_alias(filepath)
            if contract_name == natural_contract_name:
                all_warnings.add("contract name " + contract_name + " is the same as the file name and can be omitted")
        else:
            filepath = f
            contract_name = _get_natural_alias(filepath)

        if filepath in file_to_contract:
            if contract_name != file_to_contract[filepath]:
                raise argparse.ArgumentTypeError(
                    "file " + filepath + " was given two different aliases: " + file_to_contract[
                        filepath] + " and " + contract_name)
            else:
                all_warnings.add("file argument " + f + " is redundant")

        if contract_name in contract_to_file and contract_to_file[contract_name] != filepath:
            # A.sol:a B.sol:a
            raise argparse.ArgumentTypeError("a contract named " + contract_name + " was declared twice for files " +
                                             contract_to_file[contract_name] + ", " + filepath)

        contract_to_file[contract_name] = filepath
        file_to_contract[filepath] = contract_name
        declared_contracts.add(contract_name)

    for warning in all_warnings:
        warning_print(warning)
    return declared_contracts


def check_dedup_link_args(args: argparse.Namespace) -> None:
    """
    Detects contradicting definition of slots in link and throws.
    If no contradiction was found, removes duplicates, if exist.
    DOES NOT for file existence, format legality or anything else
    @param args: A namespace, where args.link includes a list of strings that are the link arguments
    @raise argparse.ArgumentTypeError if a slot was given two different definitions
    """
    dedup_links: Set[str] = set()
    double_def_warns = set()
    for link in args.link:
        for seen_link in dedup_links:
            slot = link.split('=')[0]
            if slot == seen_link.split('=')[0]:
                if link == seen_link:
                    double_def_warns.add("link " + link + " was defined multiple times")
                else:
                    raise argparse.ArgumentTypeError("slot " + slot + " was defined multiple times: " + link + ", " +
                                                     seen_link)

        dedup_links.add(link)

    for warning in double_def_warns:
        warning_print(warning)

    args.link = list(dedup_links)


def flatten_list(nested_list: Union[List[list], None]) -> Union[list, None]:
    """
    @param nested_list: A list of lists: [[a], [b, c], []]
    @return: a flat list, in our example [a, b, c]. If None was entered, returns None
    """
    if nested_list is None:
        return None
    return [item for sublist in nested_list for item in sublist]


def flatten_arg_lists(args: argparse.Namespace) -> None:
    """
    Flattens lists of lists arguments in a given namespace.
    For example,
    [[a], [b, c], []] -> [a, b, c]

    This is applicable to all options that can be used multiple times, and each time get multiple arguments.
    @param args: Namespace containing all command line arguments, generated by get_args()
    """
    layered_args_list = ['assert_contracts', 'verify', 'link']
    for args_list in layered_args_list:
        flat_list = flatten_list(getattr(args, args_list))
        setattr(args, args_list, flat_list)


def __remove_parsing_whitespace(arg_list: List[str]) -> None:
    """
    Removes all whitespaces added to args by __alter_args_before_argparse():
    1. A leading space before a dash (if added)
    2. space between commas
    :param arg_list: A list of options as strings.
    """
    for idx, arg in enumerate(arg_list):
        arg_list[idx] = arg.strip().replace(', ', ',')


def check_contract_name_arg_inputs(args: argparse.Namespace) -> None:
    """
    This function verifies that all options that expect to get contract names get valid contract names.
    If they do, nothing happens. If there an any error, an exception is thrown.
    @param args: Namespace containing all command line arguments, generated by get_args()
    @raise argparse.ArgumentTypeError if a file alias argument was expected, but not given.
    """
    contract_aliases = warn_verify_file_args(args.files)

    # we print the warnings at the end of this function, only if no errors were found. Each warning appears only once
    all_warnings = set()

    # Link arguments can be either: contractAlias:slot=contractAlias
    #   or contractAlias:slot=integer(decimal or hexadecimal)
    if args.link is not None:
        for link in args.link:
            executable = link.split(':')[0]
            executable = _get_natural_alias(executable)
            if executable not in contract_aliases:
                raise argparse.ArgumentTypeError("link " + link + " doesn't match any contract name")

            library_or_const = link.split('=')[1]
            try:
                parsed_int = int(library_or_const, 0)  # can be either a decimal or hexadecimal number
                if parsed_int < 0:
                    raise argparse.ArgumentTypeError("slot number is negative at " + link)
            except ValueError:
                library_name = _get_natural_alias(library_or_const)
                if library_name not in contract_aliases:
                    raise argparse.ArgumentTypeError("linked contract " + library_name +
                                                     " doesn't match any contract name")

        check_dedup_link_args(args)

    assert_args = set()
    if args.assert_contracts is not None:
        for assert_arg in args.assert_contracts:
            contract = _get_natural_alias(assert_arg)
            if contract not in contract_aliases:
                raise argparse.ArgumentTypeError("--assert argument " + contract + " doesn't match any contract name")
            if assert_arg in assert_args:
                all_warnings.add('--assert argument ' + assert_arg + ' was given multiple times')
            else:
                assert_args.add(assert_arg)

    args.assert_contracts = list(assert_args)

    verify_args = set()
    if args.verify is not None:
        for ver_arg in args.verify:
            contract = ver_arg.split(':')[0]
            contract = _get_natural_alias(contract)
            if contract not in contract_aliases:
                raise argparse.ArgumentTypeError("--verify argument " + contract + " doesn't match any contract name")

            if ver_arg in verify_args:
                all_warnings.add("the same verification was inserted multiple times: " + ver_arg)
            else:
                verify_args.add(ver_arg)

    # remove duplications:
    args.verify = list(verify_args)

    contract_to_address = dict()
    if args.address:
        for address_str in args.address:
            contract = address_str.split(':')[0]
            if contract not in contract_aliases:
                raise argparse.ArgumentTypeError("unrecognized contract in --address argument " + address_str)
            number = address_str.split(':')[1]
            if contract not in contract_to_address:
                contract_to_address[contract] = number
            elif contract_to_address[contract] != number:
                raise argparse.ArgumentTypeError('contract ' + contract + ' was given two different addresses: ' +
                                                 contract_to_address[contract] + " and " + number)
            else:
                all_warnings.add('address ' + number + ' for contract ' + contract + ' defined twice')

    if args.struct_link:
        contract_slot_to_contract = dict()
        for link in args.struct_link:
            location = link.split('=')[0]
            destination = link.split('=')[1]
            origin = location.split(":")[0]
            if origin not in contract_aliases:
                raise argparse.ArgumentTypeError("--struct link argument " + link + " is illegal: " + origin +
                                                 " is not a defined contract name")
            if destination not in contract_aliases:
                raise argparse.ArgumentTypeError("--struct link argument " + link + " is illegal: " + destination +
                                                 " is not a defined contract name")

            if location not in contract_slot_to_contract:
                contract_slot_to_contract[location] = destination
            elif contract_slot_to_contract[location] == destination:
                all_warnings.add("--structLink argument " + link + " appeared more than once")
            else:
                raise argparse.ArgumentTypeError(location + "  has two different definitions in --structLink: " +
                                                 contract_slot_to_contract[location] + " and  " + destination)

    for warning in all_warnings:
        warning_print(warning)


def check_mode_of_operation(args: argparse.Namespace) -> None:
    """
    Ascertains we have only 1 mode of operation in use.
    The four modes are:
    1. There is a single .tac file
    2. There is a single .conf file
    3. --assert
    4. --verify

    This function ascertains there is no overlap between the modes. Correctness of each mode is checked in other
    functions.
    @param args: A namespace including all CLI arguments provided
    @raise an argparse.ArgumentTypeError when:
        1. .conf|.tac file is used with --assert|--verify flags
        2. when both --assert and --verify flags were given
        3. when the file is not .tac|.conf and neither --assert not --verify were used
    """
    assert args.files
    is_verifying = len(args.verify) > 0
    is_asserting = len(args.assert_contracts) > 0

    if is_verifying and is_asserting:
        raise argparse.ArgumentTypeError("only one option of --assert and --verify can be used")

    special_file_type = None

    if len(args.files) == 1:
        input_file = args.files[0]
        if re.search(r'\.tac$', input_file):
            special_file_type = '.tac'
        elif re.search(r'\.conf$', input_file):
            special_file_type = '.conf'

        if special_file_type is not None:
            if is_verifying:
                raise argparse.ArgumentTypeError("Option --verify cannot be used with a " + special_file_type +
                                                 " file " + input_file)
            if is_asserting:
                raise argparse.ArgumentTypeError("Option --assert cannot be used with a " + special_file_type +
                                                 " file " + input_file)

    if special_file_type is None and not is_asserting and not is_verifying:
        raise argparse.ArgumentTypeError("Must use either --assert or --verify option")


def check_packages_arguments(args: argparse.Namespace) -> None:
    """
    Performs checks on the --packages_path and --packages options.
    @param args: A namespace including all CLI arguments provided
    @raise an argparse.ArgumentTypeError if:
        1. both options --packages_path and --packages options were used
        2. in --packages the same name was given multiples paths
    """
    if args.packages and len(args.packages) > 0:
        if args.packages_path:
            raise argparse.ArgumentTypeError("Cannot use both --packages_path and --packages")

        package_name_to_path: Dict[str, str] = dict()
        for package_str in args.packages:
            package = package_str.split("=")[0]
            path = package_str.split("=")[1]
            if package in package_name_to_path:
                raise argparse.ArgumentTypeError("package " + package + " was given two paths: " +
                                                 package_name_to_path[package] + ", " + path)
            package_name_to_path[package] = path
    elif not args.packages_path:
        if 'NODE_PATH' in os.environ:
            args.packages_path = os.environ['NODE_PATH']
            debug_print("default package path used: " + os.environ['NODE_PATH'])
        else:
            debug_print("environment variable $NODE_PATH not defined, packages_path is None")


def check_deployment_args(args: argparse.Namespace) -> None:
    """
    Checks that the user didn't choose both --staging and --cloud
    @param args: A namespace including all CLI arguments provided
    @raise argparse.ArgumentTypeError if both --staging and --cloud options are present in args
    """
    if args.staging and args.cloud:
        raise argparse.ArgumentTypeError("you cannot use both --staging and --cloud")


class UniqueStore(argparse.Action):
    """
    This class makes the argparser throw an error for a given flag if it was inserted more than once
    """

    def __call__(self, parser: argparse.ArgumentParser, namespace: argparse.Namespace, values: Any,  # type: ignore
                 option_string: str) -> None:
        if getattr(namespace, self.dest, self.default) is not self.default:
            parser.error(option_string + " appears several times.")
        setattr(namespace, self.dest, values)


def __alter_args_before_argparse(args_list: List[str]) -> None:
    """
    This function is a hack so we can accept the old syntax and still use argparse.
    This function alters the CL input so that it will be parsed correctly by argparse.

    Currently, it fixes two issues:

    1. We want to accept --javaArgs '-a,-b'
    By argparse's default, it is parsed as two different arguments and not one string.
    The hack is to preprocess the arguments, replace the comma with a commaspace.

    2. A problem with --javaArgs -single_flag. The fix is to artificially add a space before the dash.

    NOTE: Must use remove_parsing_whitespace() to undo these changes on argparse.ArgumentParser.parse_args() ouput!
    :param args_list: A list of CLI options as strings
    """
    for idx, arg in enumerate(args_list):
        if isinstance(arg, str):
            if ',' in arg:
                args_list[idx] = arg.replace(",", ", ")
                arg = args_list[idx]
            if arg[0] == "-" and arg[1] != "-":  # fixes a problem with --javaArgs -single_flag
                args_list[idx] = " " + arg


def check_args_post_argparse(args: argparse.Namespace) -> None:
    """
    Performs checks over the arguments after basic argparse parsing

    argparse parses option one by one. This is the function that checks all relations between different options and
    arguments. We assume here that basic syntax was already checked.
    @param args: A namespace including all CLI arguments provided
    @raise argparse.ArgumentTypeError if input is illegal
    """
    if args.path is None:
        args.path = __default_path()
    check_files_input(args.files)
    check_contract_name_arg_inputs(args)
    check_mode_of_operation(args)
    check_packages_arguments(args)
    check_deployment_args(args)


def __default_path() -> str:
    path = os.path.join(os.getcwd(), "contracts")
    if os.path.isdir(path):
        return path
    return os.getcwd()


def pre_arg_fetching_checks(args_list: List[str]) -> None:
    """
    This function runs checks on the raw arguments before we attempt to read them with argparse.
    We also replace certain argument values so the argparser will accept them.
    NOTE: use remove_parsing_whitespace() on argparse.ArgumentParser.parse_args() output!
    :param args_list: A list of CL arguments
    :raises argparse.ArgumentTypeError if there are errors (see individual checks for more details):
        - There are wrong quotation marks “ in use
    """
    __check_no_pretty_quotes(args_list)
    __alter_args_before_argparse(args_list)


def __check_no_pretty_quotes(args_list: List[str]) -> None:
    """
    :param args_list: A list of CL arguments
    :raises argparse.ArgumentTypeError if there are wrong quotation marks “ in use (" are the correct ones)
    """
    for arg in args_list:
        if '“' in arg:
            raise argparse.ArgumentTypeError('Please replace “ with " quotation marks')


def handle_version_flag(args_list: List[str]) -> None:
    for arg in args_list:
        if arg == "--version":
            print_version()  # exits the program
            exit(0)


def __get_argparser() -> argparse.ArgumentParser:
    """

    :return: argparse.ArgumentParser with all relevant option arguments, types and logic
    """
    parser = argparse.ArgumentParser(prog="certora-cli arguments and options", allow_abbrev=False)
    parser.add_argument('files', type=type_input_file, nargs='+',
                        help='[contract.sol[:contractName] ...] or CONF_FILE.conf or TAC_FILE.tac')

    operation_args = parser.add_argument_group("mode of operation. Please choose one")
    # Must include exactly one of the options in this group
    operation_args.add_argument("--verify", nargs='+', type=type_verify_arg, action='append',
                                help='Matches specification files to contracts. '
                                     'For example: --verify [contractName:specName.spec ...]')
    operation_args.add_argument("--assert", nargs='+', dest='assert_contracts', type=type_alias, action='append',
                                help='The list of contracts to assert. Usage: --assert [contractName ...]')

    optional_args = parser.add_argument_group("optional arguments")
    optional_args.add_argument("--cache", help='name of cache to use', action=UniqueStore)
    optional_args.add_argument("--msg", help='Add a message description to your run', action=UniqueStore)
    optional_args.add_argument("--solc", type=type_executable, default='solc', action=UniqueStore,
                               help="path to the solidity compiler executable file")
    optional_args.add_argument("--solc_args", type=type_list, action=UniqueStore,
                               help="list of string arguments to pass for the solidity compiler, for example: "
                                    "\"['--optimize', '--optimize-runs', '200']\"")
    optional_args.add_argument("--link", nargs='+', type=type_link_arg, action='append',
                               help='Links a slot in a contract with another contract. Usage: ContractA:slot=ContractB')
    optional_args.add_argument("--address", nargs='+', type=type_address, action=UniqueStore,
                               help='Set an address manually. Default: automatic assignment by the python script.'
                                    'Format: <contractName>:<number>')
    optional_args.add_argument("--jar", type=type_jar, action=UniqueStore,
                               help="Path to the Certora prover's .jar file")
    optional_args.add_argument("--structLink", nargs='+', type=type_struct_link, action=UniqueStore, dest='struct_link',
                               help='linking a struct, <contractName>:<number>=<contractName>')
    optional_args.add_argument("--toolOutput", type=type_tool_output_path, action=UniqueStore,
                               help="Path to a directory at which tool output files will be saved")
    optional_args.add_argument("--path", type=type_dir, action=UniqueStore,
                               help='Use the given path as the root of the source tree instead of the root of the '
                                    'filesystem. Default: $PWD/contracts if exists, else $PWD')
    optional_args.add_argument("--javaArgs", type=type_java_arg, action='append', dest='java_args',
                               help='arguments to pass to the .jar file')
    optional_args.add_argument("--settings", type=type_settings_arg, action='append',
                               help='advanced settings. To view, use --advanced_help')

    # Package arguments (mutually exclusive)
    optional_args.add_argument("--packages_path", type=type_dir, action=UniqueStore,
                               help="Path to a directory including solidity packages (default: $NODE_PATH)")
    optional_args.add_argument("--packages", nargs='+', type=type_package, action=UniqueStore,
                               help='A mapping [package_name=path, ...]')

    # [--staging/cloud [environment] (run on the amazon server, default environment is production)]
    """
    Behavior:
    if --cloud is not used, args.cloud is None
    if --cloud is used without an argument, arg.cloud == DEFAULT_CLOUD_ENV (currently 'production')
    if --cloud is used with an argument, stores it under args.cloud
    same for --staging
    """
    optional_args.add_argument("--staging", nargs='?', action=UniqueStore, const=DEFAULT_CLOUD_ENV,
                               help="name of the environment to run on the amazon server")
    optional_args.add_argument("--cloud", nargs='?', action=UniqueStore, const=DEFAULT_CLOUD_ENV,
                               help="name of the environment to run on the amazon server")

    optional_args.add_argument("--debug", action='store_true', help="Use this flag to see debug prints")

    # --version was handled before, it is here just for the help message
    optional_args.add_argument('--version', action='version', help='show the tool version',
                               version='This message should never be reached')

    # Hidden flags

    # used for debugging command line option parsing.
    parser.add_argument('--check_args', action='store_true', help=argparse.SUPPRESS)

    # a setting for disabling the local type checking (e.g. if we have a bug in the jar published with the python and
    # want users to not get stuck and get the type checking from the cloud instead).
    parser.add_argument('--disableLocalTypeChecking', action='store_true', help=argparse.SUPPRESS)

    parser.add_argument('--queue_wait_minutes', type=type_non_negative_integer, action=UniqueStore,
                        help=argparse.SUPPRESS)
    parser.add_argument('--max_poll_minutes', type=type_non_negative_integer, action=UniqueStore,
                        help=argparse.SUPPRESS)
    parser.add_argument('--log_query_frequency_seconds', type=type_non_negative_integer, action=UniqueStore,
                        help=argparse.SUPPRESS)
    parser.add_argument('--max_attempts_to_fetch_output', type=type_non_negative_integer, action=UniqueStore,
                        help=argparse.SUPPRESS)
    parser.add_argument('--delay_fetch_output_seconds', type=type_non_negative_integer, action=UniqueStore,
                        help=argparse.SUPPRESS)
    return parser


def get_args(args_list: Union[List[str], None] = None) -> Union[None, argparse.Namespace]:
    if args_list is None:
        args_list = sys.argv

    '''
    Why do we handle --version before argparse?
    Because on some platforms, mainly CI tests, we cannot fetch the installed distribution package version of
    certora-cli. We want to calculate the version lazily, only when --version was invoked.
    We do it pre-argparse, because we do not care bout the input validity of anything else if we have a --version flag
    '''
    handle_version_flag(args_list)

    pre_arg_fetching_checks(args_list)
    parser = __get_argparser()

    # if there is a --help flag, we want to ignore all parsing errors, even those before it:
    for arg in args_list:
        if arg == '--help':
            parser.print_help()
            exit(0)

    cli_args = parser.parse_args(args_list)

    __remove_parsing_whitespace(args_list)

    flatten_arg_lists(cli_args)
    check_args_post_argparse(cli_args)

    debug_print("parsed args successfully.")
    debug_print("args= " + str(cli_args))
    if cli_args.check_args:
        exit(0)
    return cli_args


def main() -> None:
    main_with_args(sys.argv[1:])


if __name__ == '__main__':
    main()
