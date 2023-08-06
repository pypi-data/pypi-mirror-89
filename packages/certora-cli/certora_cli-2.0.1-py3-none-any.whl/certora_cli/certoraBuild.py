#!/usr/bin/env python3

import json
import os
import sys
from Crypto.Hash import keccak
import shutil
import traceback
import re
import ast
from collections import OrderedDict
from certora_cli.certoraUtils import debug_print_  # type: ignore
from certora_cli.certoraUtils import safe_create_dir, run_cmd, get_file_basename, get_file_extension, \
    read_from_conf, handle_file_list, current_conf_to_file
from certora_cli.certoraUtils import OPTION_SOLC, OPTION_SOLC_ARGS, OPTION_SOLC_MAP, OPTION_PATH, OPTION_OUTPUT, \
    OPTION_OUTPUT_FOLDER, OPTION_OUTPUT_VERIFY, OPTION_VERIFY, OPTION_ASSERT, OPTION_LINK, OPTION_STRUCT_LINK, \
    OPTION_PACKAGES, \
    OPTION_PACKAGES_PATH, DEFAULT_CONF, OPTION_ADDRESS, OPTION_LINK_CANDIDATES, fatal_error, is_windows, \
    remove_and_recreate_dir, getcwd, as_posix
from certora_cli.certoraUtils import legal_build_args, check_legal_args, nestedOptionHack, sanitize_path

from typing import Any, Dict, List, Tuple, Union


def print_usage() -> None:  # TODO use the macros in print usage as well?
    print("""Usage:
       If no arguments, read from default.conf
       Otherwise:
       [file[:contractName] ...] or CONF_FILE.conf
       [--cache NAME]
       [--output OUTPUT_FILE_NAME (default: .certora_build)]
       [--output_folder OUTPUT_FOLDER_NAME (default: .certora_config)]
       [--link [contractName:slotNumOrFieldName=contractName ...]]
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
       [--debug]
       [--help]""")


BUILD_IS_LIBRARY = False


def is_hex_or_dec(s: str) -> bool:
    """
    :param s: A string
    :return: True if it a decimal or hexadecimal number
    """
    try:
        int(s, 16)
        return True
    except ValueError:
        return False


def is_hex(number: str) -> bool:
    """
    :param number: A string
    :return: True if the number is a hexadecimal number:\
        - Starts with 0
        - second character is either x or X
        - all other characters are digits 0-9, letters a-f or A-F
    """
    match = re.search(r'^0[xX][0-9a-fA-F]+$', number)
    return match is not None


def exit_if_not_library(code: int) -> None:
    if BUILD_IS_LIBRARY:
        return
    else:
        sys.exit(code)


def fatal_error_if_not_library(msg: str) -> None:
    if BUILD_IS_LIBRARY:
        print(msg)
        raise Exception(msg)
    else:
        fatal_error(msg)


DEBUG = False


def debug_print(s: str) -> None:
    debug_print_(s, DEBUG)


class InputConfig:
    def __init__(self, args: List[str]) -> None:
        self.args = args  # type: List[str]
        self.parsed_options = {"solc": "solc"}  # type: Dict[str, Any]
        self.solc_mappings = {}  # type: Dict[str, str]
        self.files = []  # type: List[str]
        self.fileToContractName = {}  # type: Dict[str, str]
        self.load_input(self.get_options_start_idx(self.get_options()))

    def get_options(self) -> List[Tuple[int, Any]]:
        enumerated_args = [(i, arg) for i, arg in enumerate(self.args)]
        debug_print("Enumerated args %s" % (enumerated_args))
        options = list(filter(lambda x: (x[1].startswith("--")), enumerated_args))
        debug_print("Options indices %s" % (options))
        return options

    @staticmethod
    def get_options_start_idx(options: List[Tuple[int, Any]]) -> int:
        # Figure out indices where there are options
        if len(options) > 0:
            first_option_idx = options[0][0]
        else:
            first_option_idx = -1
        debug_print("First option index is %s" % first_option_idx)
        return first_option_idx

    def load_input(self, first_option_idx: int) -> None:
        if first_option_idx == -1 and len(self.args) == 0:
            debug_print("Will read from default.conf")
            read_from_conf(DEFAULT_CONF, self.parsed_options, self.files, self.fileToContractName)
            print("Building verification environment for files: %s" % (self.files,))
        elif self.args[0].endswith(".conf"):
            if first_option_idx != -1 and len(self.args[:first_option_idx]) != 1:
                fatal_error_if_not_library(
                    "When passing a conf file, can only pass options, not additional files: %s" % (self.args[1:]))
            debug_print("Will read from conf file %s" % (self.args[0]))
            read_from_conf(self.args[0], self.parsed_options, self.files, self.fileToContractName)
            print("Building verification environment for files: %s" % (self.files,))
        else:
            file_list = self.args[0:first_option_idx]
            handle_file_list(file_list, self.files, self.fileToContractName)

            print("Building verification environment for files: %s" % (self.files,))
            # FROM THIS POINT ONWARD, files & fileToContractName DOES NOT CHANGE

        # Process options and override
        self.process_all_options(self.get_options())

        # HANDLE OPTION DEFAULTS
        self.process_defaults()

        # FROM THIS POINT ONWARD, parsed_options and solc_mappings are not changed!

    def update_config(self, name: str, value: Any) -> None:
        self.parsed_options[name] = value

    # Process options - may override those from conf file
    @staticmethod
    def process_option(option: Tuple[int, str], value: Any) -> Tuple[str, str]:
        debug_print("Processing option %s with value %s" % (option, value))
        option_name = option[1][2:]
        # normalize for non-list options
        if option_name in ["solc", "path", "packages_path", "output", "output_folder", "solc_map", "cache"]:
            if len(value) != 1:
                print("Error: option {} should not take more than 1 value, got {}".format(option_name, value))
                print_usage()
                exit_if_not_library(1)
            value = value[0]
        elif option_name in ["packages"]:
            value = ' '.join(value)
        elif option_name in ["address"]:
            def split_tuple(s: str) -> Tuple[str, str]:
                x, y = s.split(":", 2)
                return x, y

            value = dict(map(split_tuple, value))
        elif option_name in [OPTION_ASSERT]:
            if isinstance(value, bool) and value:
                fatal_error_if_not_library("Error: must specify which contract to check assertions for")

        return (option_name, value)

    def process_all_options(self, options: List[Tuple[int, Any]]) -> None:
        for optionIdx, option in enumerate(options):
            debug_print("Working on option %d %s out of %d" % (optionIdx + 1, option, len(options)))
            if optionIdx + 1 < len(options):
                nextOption = options[optionIdx + 1]
                if nextOption[0] == option[0] + 1:
                    self.update_config(*self.process_option(option, True))
                else:
                    optionParams = self.args[option[0] + 1:nextOption[0]]
                    self.update_config(*self.process_option(option, optionParams))
            else:
                if option[0] + 1 < len(self.args):
                    value = self.args[option[0] + 1:]
                    self.update_config(*self.process_option(option, value))
                else:
                    self.update_config(*self.process_option(option, [True]))

        debug_print("Options: %s" % (self.parsed_options))

    def process_defaults(self) -> None:
        # Add default for "output"
        if OPTION_OUTPUT not in self.parsed_options:
            self.parsed_options[OPTION_OUTPUT] = ".certora_build"

        # Add default for "output_folder"
        if OPTION_OUTPUT_FOLDER not in self.parsed_options:
            self.parsed_options[OPTION_OUTPUT_FOLDER] = ".certora_config"

        if OPTION_OUTPUT_VERIFY not in self.parsed_options:
            self.parsed_options[OPTION_OUTPUT_VERIFY] = ".certora_verify"

        # Add default for "path"
        if OPTION_PATH not in self.parsed_options:
            self.parsed_options[OPTION_PATH] = "%s/contracts/,%s" % (getcwd(), getcwd())
        self.parsed_options[OPTION_PATH] = ','.join(
            [sanitize_path(os.path.abspath(p)) for p in self.parsed_options[OPTION_PATH].split(",")])

        # Add default packages path
        if OPTION_PACKAGES_PATH not in self.parsed_options:
            self.parsed_options[OPTION_PACKAGES_PATH] = \
                os.getenv("NODE_PATH", "%s/node_modules" % (getcwd()))

        # If packages were not specified, try to find them from package.json, if it exists
        if OPTION_PACKAGES not in self.parsed_options:
            try:
                with open("package.json", "r") as package_json_file:
                    package_json = json.load(package_json_file)
                    deps = set(list(package_json["dependencies"].keys()) if "dependencies" in package_json else
                               list(package_json["devDependencies"].keys()) if "devDependencies" in package_json
                               else list())  # May need both
                    # Don't know which ones we need, so we take them all
                    # solidity_deps = [k for k in deps.keys() if k.find("solidity") != -1]
                    # debug_print("Solidity dependencies: %s" % (solidity_deps))

                    packages_path = self.parsed_options[OPTION_PACKAGES_PATH]
                    packages_to_pass_list = ["%s=%s/%s" % (package, packages_path, package) for package in deps]
                    packages_to_pass = ' '.join(packages_to_pass_list)
                    debug_print("Packages to pass: %s" % (packages_to_pass))
                    self.parsed_options[OPTION_PACKAGES] = packages_to_pass
            except EnvironmentError:
                ex_type, ex_value, _ = sys.exc_info()
                debug_print("Failed in processing package.json: %s,%s" % (ex_type, ex_value))

        # Add default for addresses - empty
        if OPTION_ADDRESS not in self.parsed_options:
            self.parsed_options[OPTION_ADDRESS] = {}

        if OPTION_SOLC_MAP in self.parsed_options:
            solcmaps = self.parsed_options[OPTION_SOLC_MAP]
            split = solcmaps.split(",")
            for solcmap in split:
                contract = solcmap.rsplit("=")[0]
                solcver = solcmap.rsplit("=")[1]
                debug_print("Adding solc mapping from %s to %s" % (contract, solcver))
                self.solc_mappings[contract] = solcver

        if OPTION_SOLC_ARGS in self.parsed_options:
            solcargs = self.parsed_options[OPTION_SOLC_ARGS]

            '''
            Lines below convert from format "  ['--solc-version', 'istanbul']"
            to
            "--solc-version istanbul"
            '''
            solcargs = [ast.literal_eval(k.strip()) for k in solcargs]
            solcargs = [item for sublist in solcargs for item in sublist]

            normalized = ' '.join(map(lambda x: x.replace("'", ""), solcargs))
            self.parsed_options[OPTION_SOLC_ARGS] = normalized

    # Utils
    def get_certora_config_dir(self) -> str:
        return self.parsed_options[OPTION_OUTPUT_FOLDER]


class SolidityType:
    def __init__(self,
                 base_type: str,  # The source code representation of the base type (e.g., the base type of A[][] is A)
                 components: List[Any],  # List[SolidityType]
                 array_dims: List[int],
                 # If this is an array, the i-th element is its i-th dimension size; -1 denotes a dynamic array
                 is_storage: bool,  # Whether it's a storage pointer (only applicable to library functions)
                 is_tuple: bool,  # Whether it's a tuple or a user-defined struct
                 is_address_alias: bool,  # Whether it's an alias of address type (e.g., contract, 'address payable')
                 is_uint8_alias: bool,  # Whether it's an alias of uint8 type (e.g., enum)
                 lib_canonical_signature: str = None
                 # If this is a library function param, this signature used to compute the sighash of the function
                 ):
        self.base_type = base_type
        self.components = components
        self.array_dims = array_dims
        self.is_storage = is_storage
        self.is_tuple = is_tuple
        self.is_address_alias = is_address_alias
        self.is_uint8_alias = is_uint8_alias
        self.lib_canonical_signature = lib_canonical_signature

    def asdict(self) -> Dict[str, Any]:
        return {
            "baseType": self.base_type,
            "components": [x.asdict() for x in self.components],
            "arrayDims": self.array_dims,
            "isStorage": self.is_storage,
            "isTuple": self.is_tuple,
            "isAddressAlias": self.is_address_alias,
            "isUint8Alias": self.is_uint8_alias
        }

    def __repr__(self) -> str:
        return repr(self.asdict())

    def array_dims_signature(self) -> str:
        return "".join([(lambda x: "[]" if (x == -1) else "[%d]" % x)(dim_size) for dim_size in self.array_dims[::-1]])

    def canonical_tuple_signature(self) -> str:
        return "(" + ",".join([x.signature() for x in self.components]) + ")"

    # Returns a signature in a "canonical form", namely without user-defined types and with decomposed struct members
    def signature(self) -> str:
        base_type_str = self.lib_canonical_signature if self.lib_canonical_signature is not None else (
            "uint8" if self.is_uint8_alias else (self.canonical_tuple_signature() if self.is_tuple else (
                "address" if self.is_address_alias else self.base_type)))
        return base_type_str + self.array_dims_signature() + (" storage" if self.is_storage else "")

    # Returns a signature with user-defined types
    def source_code_signature(self) -> str:
        return self.base_type + self.array_dims_signature() + (" storage" if self.is_storage else "")


class Func:
    def __init__(self,
                 name: str,
                 fullArgs: List[SolidityType],
                 returns: List[SolidityType],
                 sighash: str,
                 notpayable: bool,
                 isABI: bool,
                 stateMutability: Dict[str, str]
                 ):
        self.name = name
        self.fullArgs = fullArgs
        self.returns = returns
        self.sighash = sighash
        self.notpayable = notpayable
        self.isABI = isABI
        self.stateMutability = stateMutability
        self.sighashIsFromOtherName = any([a.lib_canonical_signature is not None for a in fullArgs])

    def asdict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "fullArgs": list(map(lambda x: x.asdict(), self.fullArgs)),
            "returns": list(map(lambda x: x.asdict(), self.returns)),
            "sighash": self.sighash,
            "notpayable": self.notpayable,
            "isABI": self.isABI,
            "stateMutability": self.stateMutability,
            "sighashIsFromOtherName": self.sighashIsFromOtherName
        }

    def __repr__(self) -> str:
        return repr(self.asdict())

    def signature(self) -> str:
        return Func.compute_signature(self.name, self.fullArgs, lambda x: x.signature())

    def source_code_signature(self) -> str:
        return Func.compute_signature(self.name, self.fullArgs, lambda x: x.source_code_signature())

    @staticmethod
    def compute_signature(
            name: str,
            args: List[SolidityType],
            signature_getter: Any
    ) -> str:
        return name + "(" + ",".join([signature_getter(x) for x in args]) + ")"


class ImmutableReference:
    def __init__(self,
                 offset: str,
                 length: str,
                 varname: str
                 ):
        self.offset = offset
        self.length = length
        self.varname = varname

    def asdict(self) -> Dict[str, Any]:
        return {
            "offset": self.offset,
            "length": self.length,
            "varname": self.varname
        }

    def __repr__(self) -> str:
        return repr(self.asdict())


class PresetImmutableReference(ImmutableReference):
    def __init__(self,
                 offset: str,
                 length: str,
                 varname: str,
                 value: str
                 ):
        ImmutableReference.__init__(self, offset, length, varname)
        self.value = value

    def asdict(self) -> Dict[str, Any]:
        dict = ImmutableReference.asdict(self)
        dict["value"] = self.value
        return dict

    def __repr__(self) -> str:
        return repr(self.asdict())


# Python3.5 to which we maintain backward-compatibility due to CI's docker image, does not support @dataclass
class ContractInSDC:
    def __init__(self,
                 name: str,
                 original_file: str,
                 file: str,
                 address: str,
                 methods: List[Any],
                 bytecode: str,
                 srcmap: str,
                 varmap: Any,
                 linkCandidates: Any,
                 storageLayout: Any,
                 immutables: List[ImmutableReference]
                 ):
        self.name = name
        self.original_file = original_file
        self.file = file
        self.address = address
        self.methods = methods
        self.bytecode = bytecode
        self.srcmap = srcmap
        self.varmap = varmap
        self.linkCandidates = linkCandidates
        self.storageLayout = storageLayout
        self.immutables = immutables

    def asdict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "original_file": self.original_file,
            "file": self.file,
            "address": self.address,
            "methods": list(map(lambda x: x.asdict(), self.methods)),
            "bytecode": self.bytecode,
            "srcmap": self.srcmap,
            "varmap": self.varmap,
            "linkCandidates": self.linkCandidates,
            "storageLayout": self.storageLayout,
            "immutables": list(map(lambda x: x.asdict(), self.immutables)),
        }

    def __repr__(self) -> str:
        return repr(self.asdict())


class SDC:
    def __init__(self,
                 primary_contract: str,
                 primary_contract_address: str,
                 sdc_origin_file: str,
                 original_srclist: Dict[Any, Any],
                 srclist: Dict[Any, Any],
                 sdc_name: str,
                 contracts: List[ContractInSDC],
                 library_addresses: List[str],
                 generated_with: str,
                 state: Dict[str, str],
                 structLinkingInfo: Dict[str, str]
                 ):
        self.primary_contract = primary_contract
        self.primary_contract_address = primary_contract_address
        self.sdc_origin_file = sdc_origin_file
        self.original_srclist = original_srclist
        self.srclist = srclist
        self.sdc_name = sdc_name
        self.contracts = contracts
        self.library_addresses = library_addresses
        self.generated_with = generated_with
        self.state = state
        self.structLinkingInfo = structLinkingInfo

    def asdict(self) -> Dict[str, Any]:
        return {
            "primary_contract": self.primary_contract,
            "primary_contract_address": self.primary_contract_address,
            "sdc_origin_file": self.sdc_origin_file,
            "original_srclist": self.original_srclist,
            "srclist": self.srclist,
            "sdc_name": self.sdc_name,
            "contracts": list(map(lambda x: x.asdict(), self.contracts)),
            "library_addresses": self.library_addresses,
            "generated_with": self.generated_with,
            "state": self.state,
            "structLinkingInfo": self.structLinkingInfo,
        }


class CertoraBuildGenerator:
    def __init__(self, input_config: InputConfig) -> None:
        self.input_config = input_config
        # SDCs describes the set of all 'Single Deployed Contracts' the solidity file whose contracts comprise a single
        # bytecode of interest. Which one it is - we don't know yet, but we make a guess based on the base filename.
        # An SDC corresponds to a single solidity file.
        self.SDCs = {}  # type: Dict[str, SDC]

        # Note that the the last '/' in config_path is important for solc to succeed, so it should be added
        self.config_path = "%s/%s" % (getcwd(), input_config.get_certora_config_dir())
        self.library_addresses = []  # type: List[str]

        # ASTs will be lazily loaded
        self.asts = {}  # type: Dict[str, Dict[str, Dict[int, Any]]]

        remove_and_recreate_dir(self.config_path)

        self.address_generator_idx = 0

    @staticmethod
    def CERTORA_CONTRACT_NAME() -> str:
        return "certora_contract_name"

    def collect_funcs(self, data: Dict[str, Any], contract_file: str,
                      contract_name: str, original_file: str) -> List[Func]:

        def collect_func_source_code_signatures_from_abi() -> List[str]:
            func_signatures = []
            abi = data["abi"]  # ["contracts"][contract_file][contract_name]["abi"]
            debug_print(abi)
            for f in filter(lambda x: x["type"] == "function", abi):
                inputs = f["inputs"]
                func_signatures.append(f["name"] + "(" + ",".join(
                    [input["internalType"] if "internalType" in input else input["type"] for input in inputs]) + ")")
            return func_signatures

        def get_getter_func_node_from_abi(state_var_name: str) -> Dict[str, Any]:
            abi = data["abi"]  # ["contracts"][contract_file][contract_name]["abi"]
            abi_getter_nodes = [g for g in
                                filter(lambda x: x["type"] == "function" and x["name"] == state_var_name, abi)]

            assert len(abi_getter_nodes) != 0, "Failed to find a getter function of the state variable" \
                                               " %s in the ABI" % state_var_name
            assert len(abi_getter_nodes) == 1, "Found multiple candidates for a getter function of the state variable" \
                                               " %s in the ABI" % state_var_name

            return abi_getter_nodes[0]

        def collect_array_type_from_abi_rec(type_str: str, dims: List[int]) -> str:
            outer_dim = re.findall(r"\[\d*\]$", type_str)
            if outer_dim:
                type_rstrip_dim = re.sub(r"\[\d*\]$", '', type_str)
                if len(outer_dim[0]) == 2:
                    dims.append(-1)  # dynamic array
                else:
                    assert len(outer_dim[0]) > 2, "Expected to find a fixed-size array, but found %s" % type_str
                    dims.append(int(re.findall(r"\d+", outer_dim[0])[0]))
                return collect_array_type_from_abi_rec(type_rstrip_dim, dims)
            return type_str

        # Returns (list of array dimensions' lengths, the base type of the array)
        def collect_array_type_from_abi(type_str: str) -> Tuple[List[int], str]:
            dims = []  # type: List[int]
            base_type = collect_array_type_from_abi_rec(type_str, dims)
            return dims, base_type

        # Gets the SolidityType of a function parameter (either input or output) from the ABI
        def get_solidity_type_from_abi(abi_param_entry: Dict[str, Any]) -> SolidityType:
            assert "type" in abi_param_entry, "Invalid ABI function parameter entry: %s" % abi_param_entry

            is_tuple = "components" in abi_param_entry and len(abi_param_entry["components"]) > 0
            if is_tuple:
                components = [get_solidity_type_from_abi(x) for x in abi_param_entry["components"]]
            else:
                components = []

            array_dims, base_type = collect_array_type_from_abi(abi_param_entry["type"])

            internalType_exists = "internalType" in abi_param_entry
            if internalType_exists:
                array_dims_internal, internal_base_type = collect_array_type_from_abi(abi_param_entry["internalType"])
                assert array_dims_internal == array_dims
                is_address_alias = base_type == "address" and internal_base_type != base_type
                is_uint8_alias = base_type == "uint8" and internal_base_type != base_type
            else:
                internal_base_type = ""
                is_address_alias = False
                is_uint8_alias = False

            return SolidityType(
                internal_base_type if internalType_exists else base_type,
                components,
                array_dims,
                False,  # ABI functions cannot have storage references as parameters
                is_tuple,
                is_address_alias,
                is_uint8_alias
            )

        def get_external_public_func_def_nodes(contract_file_ast: Dict[int, Any]) -> List[Dict[str, Any]]:
            fun_defs_in_file = [contract_file_ast[node_id] for node_id in filter(
                lambda node_id: "nodeType" in contract_file_ast[node_id] and
                                contract_file_ast[node_id]["nodeType"] == "FunctionDefinition" and
                                (("kind" in contract_file_ast[node_id] and
                                  contract_file_ast[node_id]["kind"] == "function") or
                                 ("isConstructor" in contract_file_ast[node_id] and
                                  contract_file_ast[node_id]["isConstructor"] is False and
                                  "name" in contract_file_ast[node_id] and
                                  contract_file_ast[node_id]["name"] != "")) and  # Not the fallback function (< solc6)
                                "visibility" in contract_file_ast[node_id] and
                                contract_file_ast[node_id]["visibility"] in ["public", "external"], contract_file_ast)]

            assert all(self.CERTORA_CONTRACT_NAME() in fd for fd in fun_defs_in_file)

            fun_defs_in_given_contract = [fd for fd in fun_defs_in_file if fd[self.CERTORA_CONTRACT_NAME()] == c_name]
            return fun_defs_in_given_contract

        def get_public_state_var_def_nodes(contract_file_ast: Dict[int, Any]) -> List[Dict[str, Any]]:
            public_var_defs_in_file = [contract_file_ast[node_id] for node_id in filter(
                lambda node_id: "nodeType" in contract_file_ast[node_id] and
                                contract_file_ast[node_id]["nodeType"] == "VariableDeclaration" and
                                "visibility" in contract_file_ast[node_id] and
                                contract_file_ast[node_id]["visibility"] == "public" and
                                "stateVariable" in contract_file_ast[node_id] and
                                contract_file_ast[node_id]["stateVariable"] is True, contract_file_ast)]

            assert all(self.CERTORA_CONTRACT_NAME() in vd for vd in public_var_defs_in_file)

            var_defs_in_given_contract = [vd for vd in public_var_defs_in_file if
                                          vd[self.CERTORA_CONTRACT_NAME()] == c_name]
            return var_defs_in_given_contract

        def is_library_def_node(file: str, node_ref: int) -> bool:
            contract_def_node = self.asts[original_file][file][node_ref]
            return "contractKind" in contract_def_node and contract_def_node["contractKind"] == "library"

        def get_contract_def_node_ref() -> int:
            contract_file_ast = self.asts[original_file][contract_file]
            contract_def_refs = [node_id for node_id in filter(
                lambda node_id: "nodeType" in contract_file_ast[node_id] and
                                contract_file_ast[node_id]["nodeType"] == "ContractDefinition" and
                                "name" in contract_file_ast[node_id] and
                                contract_file_ast[node_id]["name"] == contract_name, contract_file_ast)]

            assert len(contract_def_refs) != 0, "Failed to find a \"ContractDefinition\" ast node id for the contract" \
                                                " %s" % contract_name
            assert len(
                contract_def_refs) == 1, "Found multiple \"ContractDefinition\" ast node ids for the same contract" \
                                         " %s: %s" % (contract_name, contract_def_refs)
            return contract_def_refs[0]

        def retrieve_base_contracts_list_rec(base_contracts_queue: List[Any],
                                             base_contracts_lst: List[Tuple[str, str, bool]]) -> None:
            (curr_contract_file, curr_contract_def_node_ref) = base_contracts_queue.pop()

            curr_contract_def = self.asts[original_file][curr_contract_file][curr_contract_def_node_ref]
            assert "baseContracts" in curr_contract_def, "Got a \"ContractDefinition\" ast node without " \
                                                         "a \"baseContracts\" key: %s" % curr_contract_def
            for bc in curr_contract_def["baseContracts"]:
                assert "nodeType" in bc and bc["nodeType"] == "InheritanceSpecifier"
                assert "baseName" in bc and "referencedDeclaration" in bc["baseName"]
                next_bc_ref = bc["baseName"]["referencedDeclaration"]
                next_bc = get_contract_file_of(next_bc_ref)
                if next_bc not in base_contracts_lst:
                    base_contracts_lst.append((next_bc, self.asts[original_file][next_bc][next_bc_ref]["name"],
                                               is_library_def_node(next_bc, next_bc_ref)))
                    base_contracts_queue.insert(0, (next_bc, bc["baseName"]["referencedDeclaration"]))

            if base_contracts_queue:
                retrieve_base_contracts_list_rec(base_contracts_queue, base_contracts_lst)

        # For each base contract, returns (base_contract_file, base_contract_name)
        def retrieve_base_contracts_list() -> List[Tuple[str, str, bool]]:
            contract_def_node_ref = get_contract_def_node_ref()
            base_contracts_queue = [(contract_file, contract_def_node_ref)]
            base_contracts_lst = [
                (contract_file, contract_name, is_library_def_node(contract_file, contract_def_node_ref))]
            retrieve_base_contracts_list_rec(base_contracts_queue, base_contracts_lst)
            return base_contracts_lst

        def get_original_def_node(reference: int) -> Dict[str, Any]:
            return self.asts[original_file][get_contract_file_of(reference)][reference]

        def get_contract_file_of(reference: int) -> str:
            original_file_asts = self.asts[original_file]
            for contract in original_file_asts:
                if reference in original_file_asts[contract]:
                    return contract
            # error if got here
            fatal_error_if_not_library("Could not find reference AST node {}".format(reference))
            return ""

        def get_function_selector(f_entry: Dict[str, Any], f_name: str,
                                  input_types: List[SolidityType]) -> str:
            if "functionSelector" in f_entry:
                return f_entry["functionSelector"]

            f_base = Func.compute_signature(f_name, input_types, lambda x: x.signature())

            assert f_base in data["evm"]["methodIdentifiers"],\
                "Was about to compute the sighash of %s based on the signature %s.\nExpected this signature to appear" \
                " in \"methodIdentifiers\"." % (f_name, f_base)

            f_hash = keccak.new(digest_bits=256)
            f_hash.update(str.encode(f_base))

            result = f_hash.hexdigest()[0:8]
            expected_result = data["evm"]["methodIdentifiers"][f_base]

            assert expected_result == result,\
                "Computed the sighash %s of %s based on a (presumably) correct signature (%s), but got " \
                "an incorrect result. Expected result: %s" % (result, f_name, f_base, expected_result)

            return result

        # Returns the base type (node) of the specified array type, e.g., returns A for A[][3][]
        def collect_array_type_from_typeName_rec(typeName: Dict[str, Any], dims: List[int]) -> Dict[str, Any]:
            assert "nodeType" in typeName, "Expected a \"nodeType\" key, but got %s" % typeName
            if typeName["nodeType"] == "ArrayTypeName":
                if "length" in typeName:
                    length = typeName["length"]
                    if type(length) is dict and "value" in length:
                        dims.append(int(length["value"]))  # Fixed-size array
                    else:
                        dims.append(-1)  # Dynamic array
                else:  # Dynamic array (in solc7)
                    dims.append(-1)
                assert "baseType" in typeName, "Expected an array type with a \"baseType\" key, but got %s" % typeName
                return collect_array_type_from_typeName_rec(typeName["baseType"], dims)

            return typeName

        # Returns (list of array type dimensions, ast node of the array's base type).
        # E.g., Returns ([-1, 3, -1], A) for A[][3][].
        # If given a non-array type A, returns ([],A)
        def collect_array_type_from_typeName(typeName: Dict[str, Any]) -> Tuple[List[int], Dict[str, Any]]:
            assert "nodeType" in typeName, "Expected a \"nodeType\" key, but got %s" % typeName
            dims = []  # type: List[int]
            if typeName["nodeType"] == "ArrayTypeName":
                base_type_node = collect_array_type_from_typeName_rec(typeName, dims)
            else:
                base_type_node = typeName
            return dims, base_type_node

        def is_payable_address_type(base_type_node: Dict[str, Any]) -> bool:
            if "stateMutability" in base_type_node:
                assert "name" in base_type_node and base_type_node["name"] == "address", \
                    "Expected an address type, but got %s" % base_type_node

                assert base_type_node["stateMutability"] == "nonpayable" or \
                       base_type_node["stateMutability"] == "payable"

                return base_type_node["stateMutability"] == "payable"

            return False

        def get_solidityType_from_ast_param(p: Dict[str, Any]) -> SolidityType:
            assert "typeName" in p, "Expected a \"typeName\" key, but got %s" % p
            (array_dims, base_type_node) = collect_array_type_from_typeName(p["typeName"])

            base_type_is_user_defined = base_type_node["nodeType"] == "UserDefinedTypeName"
            lib_canonical_base_type_str = None  # Used to compute the function sighash in case of a library function
            if base_type_is_user_defined:
                orig_user_defined_type = get_original_def_node(base_type_node["referencedDeclaration"])
                is_valid_node = orig_user_defined_type is not None and "nodeType" in orig_user_defined_type
                is_struct = is_valid_node and orig_user_defined_type["nodeType"] == "StructDefinition"
                is_contract = is_valid_node and orig_user_defined_type["nodeType"] == "ContractDefinition"
                is_enum = is_valid_node and orig_user_defined_type["nodeType"] == "EnumDefinition"
                if c_is_lib:
                    if "canonicalName" in orig_user_defined_type:  # prefer the "canonicalName", if available
                        lib_canonical_base_type_str = orig_user_defined_type["canonicalName"]
                    elif "name" in orig_user_defined_type:
                        lib_canonical_base_type_str = orig_user_defined_type["name"]
            else:
                is_struct = False
                is_contract = False
                is_enum = False

            is_payable_address = is_payable_address_type(base_type_node)

            # For a struct parameter, recursively add a solidity type to its components list for each of its members.
            def collect_struct_member_types() -> List[SolidityType]:
                components = []
                if is_struct:
                    struct_def_node_id = base_type_node["referencedDeclaration"]
                    struct_def_node = get_original_def_node(struct_def_node_id)  # type: Dict[str, Any]
                    assert ("nodeType" in struct_def_node and struct_def_node["nodeType"] == "StructDefinition")

                    if not struct_def_node:
                        fatal_error("Expected to find a definition of {} in the contracts asts".format(
                            base_type_str))

                    # Proceed recursively on each member of the struct
                    components.extend(
                        [get_solidityType_from_ast_param(struct_member) for struct_member in
                         struct_def_node["members"]])

                return components

            base_type_str = base_type_node["typeDescriptions"]["typeString"]
            is_storage_ref = p["storageLocation"] == "storage"
            return SolidityType(base_type_str, collect_struct_member_types(), array_dims, is_storage_ref,
                                is_struct, is_contract or is_payable_address, is_enum, lib_canonical_base_type_str)

        abi_func_signatures = collect_func_source_code_signatures_from_abi()
        funcs = []
        abi_funcs_cnt = 0
        collected_func_selectors = set()
        base_contract_files = retrieve_base_contracts_list()  # List[str]
        for c_file, c_name, c_is_lib in base_contract_files:
            if c_is_lib:
                debug_print("%s is a library" % c_name)
            for func_def in get_external_public_func_def_nodes(self.asts[original_file][c_file]):
                func_name = func_def["name"]
                debug_print(func_name)
                params = [p for p in func_def["parameters"]["parameters"]]
                solidityType_args = [get_solidityType_from_ast_param(p) for p in params]

                func_selector = get_function_selector(func_def, func_name, solidityType_args)
                if func_selector in collected_func_selectors:
                    continue
                collected_func_selectors.add(func_selector)

                # Refer to https://github.com/OpenZeppelin/solidity-ast/blob/master/schema.json for more info
                return_params = func_def["returnParameters"]["parameters"]
                solidityType_outs = [get_solidityType_from_ast_param(p) for p in return_params]

                isABI = Func.compute_signature(
                    func_name, solidityType_args, lambda x: x.source_code_signature()
                ) in abi_func_signatures or Func.compute_signature(
                    func_name, solidityType_args, lambda x: x.signature()
                ) in abi_func_signatures

                func = Func(
                    func_name,
                    solidityType_args,
                    solidityType_outs,
                    func_selector,
                    func_def["stateMutability"] in ["nonpayable", "view", "pure"],
                    (not c_is_lib) and isABI,  # Always set library functions as non-ABI
                    {"keyword": func_def["stateMutability"]}
                )
                funcs.append(func)

                if not isABI:
                    debug_print(
                        "Added an instance of the function %s that is not part of the ABI"
                        % func.source_code_signature())
                else:
                    abi_funcs_cnt += 1

            # Add automatically generated getter functions for public state variables.
            for public_state_var in get_public_state_var_def_nodes(self.asts[original_file][c_file]):
                getter_name = public_state_var["name"]
                debug_print(getter_name)
                getter_abi_data = get_getter_func_node_from_abi(getter_name)

                params = [p for p in getter_abi_data["inputs"]]
                solidityType_args = [get_solidity_type_from_abi(p) for p in params]

                getter_selector = get_function_selector(public_state_var, getter_name, solidityType_args)
                if getter_selector in collected_func_selectors:
                    continue
                collected_func_selectors.add(getter_selector)

                return_params = [p for p in getter_abi_data["outputs"]]
                solidityType_outs = [get_solidity_type_from_abi(p) for p in return_params]

                if "payable" not in getter_abi_data:
                    isNotPayable = False
                else:  # Only if something is definitely non-payable, we treat it as such
                    isNotPayable = not getter_abi_data["payable"]

                if "stateMutability" not in getter_abi_data:
                    stateMutability = "nonpayable"
                else:
                    stateMutability = getter_abi_data["stateMutability"]
                    # in solc6 there is no json field "payable", so we infer that if stateMutability is view or pure,
                    # then we're also non-payable by definition
                    # (stateMutability is also a newer field)
                    if not isNotPayable and stateMutability in ["view", "pure", "nonpayable"]:
                        isNotPayable = True  # definitely not payable

                funcs.append(
                    Func(
                        getter_name,
                        solidityType_args,
                        solidityType_outs,
                        getter_selector,
                        isNotPayable,
                        True,
                        {"keyword": stateMutability}
                    )
                )
                abi_funcs_cnt += 1
                debug_print("Added an automatically generated getter function for %s" % getter_name)

        assert abi_funcs_cnt == len(abi_func_signatures), "There are functions in the ABI that were not added. " + \
            "Added functions: %s\n. Functions in ABI: %s" % ([f.source_code_signature() for f in funcs if f.isABI],
                                                             abi_func_signatures)
        return funcs

    def collect_srcmap(self, data: Dict[str, Any]) -> Any:
        return data["evm"]["deployedBytecode"]["sourceMap"]  # data["contracts"][contract]["srcmap-runtime"]

    def collect_varmap(self, contract: str, data: Dict[str, Any]) -> Any:
        return data["contracts"][contract]["local-mappings"]

    def collect_storage_layout(self, data: Dict[str, Any]) -> Any:
        return data.get("storageLayout", None)

    def get_standard_json_data(self, sdc_name: str) -> Dict[str, Any]:
        with open("%s/%s.standard.json.stdout" % (self.config_path, sdc_name)) as standard_json_str:
            json_obj = json.load(standard_json_str)
            return json_obj

    @staticmethod
    def address_as_str(address: Union[str, int]) -> str:
        if isinstance(address, str):
            return address
        return "%0.40x" % (address)

    def find_contract_address_str(self,
                                  contractFile: str,
                                  contractName: str,
                                  contracts_with_chosen_addresses: List[Tuple[int, Any]]) -> str:
        address_and_contracts = [e for e in contracts_with_chosen_addresses
                                 if e[1] == "%s:%s" % (contractFile, contractName)]
        if len(address_and_contracts) == 0:
            msg = "Failed to find a contract named %s in file %s. " \
                  "Please make sure there is a file named like the contract, " \
                  "or a file containing a contract with this name. Available contracts: %s" % \
                  (contractName, contractFile, ','.join(map(lambda x: x[1], contracts_with_chosen_addresses)))
            fatal_error_if_not_library(msg)
        address_and_contract = address_and_contracts[0]
        address = address_and_contract[0]
        contract = address_and_contract[1].split(":")[1]
        debug_print("Custom addresses: %s, looking for a match of %s from %s in %s" %
                    (self.input_config.parsed_options[OPTION_ADDRESS], address_and_contract, contract,
                     self.input_config.parsed_options[OPTION_ADDRESS].keys()))
        if contract in self.input_config.parsed_options[OPTION_ADDRESS].keys():
            address = self.input_config.parsed_options[OPTION_ADDRESS][contract]
        debug_print("Candidate addresses for %s is %s" % (contract, address))
        # Can't have more than one! Otherwise we will have conflicting same address for different contracts
        assert len(set(address_and_contracts)) == 1
        return self.address_as_str(address)

    def collect_and_link_bytecode(self,
                                  contract_name: str,
                                  contracts_with_chosen_addresses: List[Tuple[int, Any]],
                                  bytecode: str,
                                  links: Dict[str, Any]
                                  ) -> str:
        debug_print("Working on contract {}".format(contract_name))
        debug_print("Contracts with chosen addresses: %s" %
                    ([("0x%X" % x[0], x[1]) for x in contracts_with_chosen_addresses]))

        if links:
            # links are provided by solc as a map file -> contract -> (length, start)
            # flip the links from the "where" to the chosen contract address (based on file:contract).
            linked_bytecode = bytecode
            replacements = {}
            for link_file in links:
                for link_contract in links[link_file]:
                    for where in links[link_file][link_contract]:
                        replacements[where["start"]] = {"length": where["length"],
                                                        "address": self.find_contract_address_str(
                                                            link_file,
                                                            link_contract,
                                                            contracts_with_chosen_addresses)
                                                        }
            debug_print("Replacements %s" % (replacements))
            where_list = list(replacements.keys())
            where_list.sort()
            where_list.reverse()
            for where in where_list:
                offset = where * 2
                len = replacements[where]["length"] * 2
                addr = replacements[where]["address"]
                debug_print("replacing in {} of len {} with {}".format(offset, len, addr))
                linked_bytecode = "{}{}{}".format(
                    linked_bytecode[0:offset],
                    addr,
                    linked_bytecode[(offset + len):]
                )
                self.library_addresses.append(addr)
            return linked_bytecode

        return bytecode

    def get_relevant_solc(self, contract: str) -> str:
        if contract in self.input_config.solc_mappings:
            base = self.input_config.solc_mappings[contract]
        else:
            base = self.input_config.parsed_options[OPTION_SOLC]
        if is_windows() and not base.endswith(".exe"):
            base = base + ".exe"
        return base

    def get_extra_solc_args(self) -> str:
        if OPTION_SOLC_ARGS in self.input_config.parsed_options:
            return self.input_config.parsed_options[OPTION_SOLC_ARGS]
        else:
            return ""

    # when calling solc with the standard_json api, instead of passing it flags we pass it json
    # to request what we want--currently we only use this to retrieve storage layout as this
    # is the only way to do that, it would probably be good to migrate entirely to this API
    def standard_json(self, contract_file: str, remappings: List[str]) -> Dict[str, Any]:
        sources_dict = {contract_file: {"urls": [contract_file]}}
        solc_args = self.get_extra_solc_args()
        debug_print("Adding solc args {}".format(solc_args))
        settings_dict = {"remappings": remappings,
                         "outputSelection": {
                             "*": {
                                 "*": ["storageLayout", "abi", "evm.deployedBytecode", "evm.methodIdentifiers"],
                                 "": ["id", "ast"]
                             }
                         }
                         }

        def split_arg_hack(arg_name: str, args_: str) -> str:
            return args_.split(arg_name)[1].strip().split(" ")[0].strip()  # String-ops FTW

        EVM_VERSION = "--evm-version"
        OPTIMIZE = "--optimize"
        OPTIMIZE_RUNS = "--optimize-runs"

        if EVM_VERSION in solc_args:
            evmVersion = split_arg_hack(EVM_VERSION, solc_args)
            settings_dict["evmVersion"] = evmVersion
        if OPTIMIZE in solc_args or OPTIMIZE_RUNS in solc_args:
            enabled = OPTIMIZE in solc_args
            if OPTIMIZE_RUNS in solc_args:
                runs = int(split_arg_hack(OPTIMIZE_RUNS, solc_args))
                settings_dict["optimizer"] = {"enabled": enabled, "runs": runs}
            else:
                settings_dict["optimizer"] = {"enabled": enabled}

        result_dict = {"language": "Solidity", "sources": sources_dict, "settings": settings_dict}
        debug_print("Standard json input")
        debug_print(json.dumps(result_dict, indent=4))
        return result_dict

    def get_compilation_path(self, sdc_name: str) -> str:
        return "%s/%s" % (self.config_path, sdc_name)

    def build_srclist(self, data: Dict[str, Any], sdc_name: str) -> Tuple[Dict[str, Any], Dict[str, str]]:
        # srclist - important for parsing source maps
        srclist = {data["sources"][k]["id"]: k for k in data["sources"]}
        debug_print("Source list: %s" % (srclist,))

        fetched_srclist = {}

        map_idx_in_src_list_to_orig_file = {v: k for k, v in srclist.items()}
        for orig_file in map_idx_in_src_list_to_orig_file:
            idx_in_src_list = map_idx_in_src_list_to_orig_file[orig_file]
            if "dont_fetch_sources" not in self.input_config.parsed_options:
                # Copy contract_file to compilation path directory
                new_name = "%d_%s.%s" % (idx_in_src_list, get_file_basename(orig_file),
                                         get_file_extension(orig_file))
                shutil.copy2(orig_file,
                             '%s/%s' % (self.get_compilation_path(sdc_name), new_name))
                fetched_source = '%s/%s' % (sdc_name, new_name)
            else:
                fetched_source = orig_file

            fetched_srclist[idx_in_src_list] = fetched_source

        return (srclist, fetched_srclist)

    # This function fetches the AST provided by solc and flattens it so that each node_id is mapped to a dict object,
    # representing the node's contents.
    # contract_sources represents the AST. Every sub-object with an "id" key is an AST node.
    # The ast object is keyed by the original file for which we invoked solc
    def collect_asts(self, original_file: str, contract_sources: Dict[str, Dict[str, Any]]) -> None:

        def stamp_value_with_contract_name(popped_dict: Dict[str, Any], curr_value: Any) -> None:
            if isinstance(curr_value, dict):
                if popped_dict["nodeType"] == "ContractDefinition":
                    assert "name" in popped_dict
                    curr_value[self.CERTORA_CONTRACT_NAME()] = popped_dict["name"]
                elif self.CERTORA_CONTRACT_NAME() in popped_dict:
                    curr_value[self.CERTORA_CONTRACT_NAME()] = popped_dict[self.CERTORA_CONTRACT_NAME()]
            elif isinstance(curr_value, list):
                for node in curr_value:
                    stamp_value_with_contract_name(popped_dict, node)

        self.asts[original_file] = {}
        for c in contract_sources:
            debug_print("Adding ast of %s for %s" % (original_file, c))
            container = {}  # type: Dict[int, Any]
            self.asts[original_file][c] = container
            if "ast" not in contract_sources[c]:
                fatal_error_if_not_library(
                    "Invalid AST format for original file %s - got object that does not contain an \"ast\" %s" % (
                        original_file, contract_sources[c]))
            queue = [contract_sources[c]["ast"]]
            while queue:
                pop = queue.pop(0)
                if isinstance(pop, dict) and "id" in pop:
                    container[int(pop["id"])] = pop
                    for key, value in pop.items():
                        stamp_value_with_contract_name(pop, value)
                        if isinstance(value, dict):
                            queue.append(value)
                        if isinstance(value, list):
                            queue.extend(value)

    @staticmethod
    def get_node_from_asts(asts: Dict[str, Dict[str, Dict[int, Any]]], original_file: str, node_id: int) -> Any:
        debug_print("Available keys in ASTs: %s" % (asts.keys()))
        debug_print("Available keys in AST of original file: %s" % (asts[original_file].keys()))
        for contract_file in asts[original_file]:
            node = asts[original_file].get(contract_file, {}).get(node_id)
            if node is not None:
                debug_print("In original %s in contract file %s found for node id %d the node %s" % (
                    original_file, contract_file, node_id, node))
                return node  # Found the ast node of the given node_id
        return {}  # an ast node with the given node_id was not found

    def collect_immutables(self,
                           contract_data: Dict[str, Any],
                           original_file: str
                           ) -> List[ImmutableReference]:
        out = []
        immutableReferences = contract_data["evm"]["deployedBytecode"].get("immutableReferences", [])
        # Collect and cache the AST(s). We collect the ASTs of ALL contracts' files that appear in
        # contract_sources; the reason is that a key of an item in immutableReferences
        # is an id of an ast node that may belong to any of those contracts.
        debug_print("Got immutable references in %s: %s" % (original_file, immutableReferences))
        for astnode_id in immutableReferences:
            astnode = self.get_node_from_asts(self.asts, original_file, int(astnode_id))
            name = astnode.get("name", None)
            if name is None:
                fatal_error_if_not_library(
                    "immutable reference does not point to a valid ast node {} in {}, node id {}".format(
                        astnode,
                        original_file,
                        astnode_id
                    )
                )

            debug_print("Name of immutable reference is %s" % (name))
            for elem in immutableReferences[astnode_id]:
                out.append(ImmutableReference(elem["start"],
                                              elem["length"],
                                              name
                                              )
                           )
        return out

    def address_generator(self) -> int:
        # 12,14,04,06,00,04,10 is 0xce4604a aka certora.
        const = (12 * 2 ** 24 + 14 * 2 ** 20 + 4 * 2 ** 16 + 6 * 2 ** 12 + 0 + 4 * 2 ** 4 + 10 * 2 ** 0)
        address = const * 2 ** 100 + self.address_generator_idx
        # Don't forget for addresses there are only 160 bits
        self.address_generator_idx += 1
        return address

    def collect_for_file(self, file: str, file_index: int) -> SDC:
        primary_contract = self.input_config.fileToContractName[file]
        sdc_name = "%s_%d" % (file.split("/")[-1], file_index)
        compilation_path = self.get_compilation_path(sdc_name)
        safe_create_dir(compilation_path)

        solc_ver_to_run = self.get_relevant_solc(primary_contract)

        file_abs_path = as_posix(os.path.abspath(file))

        packages = self.input_config.parsed_options.get(OPTION_PACKAGES, "").split(" ")
        remappings = sorted(list(filter(lambda package: "=" in package, packages)), key=str.lower)
        paths_for_remappings = map(lambda remap: remap.split("=")[1], remappings)

        # ABI and bin-runtime cmds preparation
        if OPTION_PACKAGES in self.input_config.parsed_options:
            join_remappings = ','.join(paths_for_remappings)
            debug_print("Join remappings: %s" % (join_remappings))
            collect_cmd = "%s -o %s/ --overwrite --allow-paths %s,%s,. --standard-json" % \
                          (solc_ver_to_run, compilation_path, self.input_config.parsed_options[OPTION_PATH],
                           join_remappings)
        else:
            collect_cmd = "%s -o %s/ --overwrite --allow-paths %s,. --standard-json" % \
                          (solc_ver_to_run, compilation_path, self.input_config.parsed_options[OPTION_PATH])

        # Standard JSON

        standard_json_input = json.dumps(self.standard_json(file_abs_path, remappings)).encode("utf-8")
        run_cmd(collect_cmd, "%s.standard.json" % (sdc_name), self.config_path,
                input=standard_json_input, shell=False)

        debug_print("Collecting standard json: %s" % (collect_cmd))
        standard_json_data = self.get_standard_json_data(sdc_name)
        # debug_print("Standard json data")
        # debug_print(json.dumps(standard_json_data, indent=4))

        for error in standard_json_data.get("errors", []):
            # is an error not a warning
            if error.get("severity", None) == "error":
                debug_print("Error: standard-json invocation of solc encountered an error: {}"
                            .format(error))
                friendly_message = "Got error from {} of type {}:\n{}".format(solc_ver_to_run,
                                                                              error["type"],
                                                                              error["formattedMessage"])
                fatal_error_if_not_library(friendly_message)

        # load data
        # data = get_combined_json_data(sdc_name)
        data = standard_json_data  # Note we collected for just ONE file
        self.collect_asts(file, data["sources"])
        contracts_with_libraries = {}
        # Need to add all library dependencies that are in a different file:
        seen_link_refs = {file_abs_path}
        contract_work_list = [file_abs_path]
        while (contract_work_list):
            contract_file = contract_work_list.pop()
            contract_list = [c for c in data["contracts"][contract_file]]
            contracts_with_libraries[contract_file] = contract_list

            for contract_name in contract_list:
                contractObject = data["contracts"][contract_file][contract_name]
                linkRefs = contractObject["evm"]["deployedBytecode"]["linkReferences"]
                for linkRef in linkRefs:
                    if (linkRef not in seen_link_refs):
                        contract_work_list.append(linkRef)
                        seen_link_refs.add(linkRef)

        debug_print("Contracts in %s: %s" % (sdc_name, contracts_with_libraries[file_abs_path]))

        contracts_with_chosen_addresses = \
            [(self.address_generator(), "%s:%s" % (contract_file, contract_name)) for contract_file, contract_list in
             contracts_with_libraries.items() for contract_name in contract_list]  # type: List[Tuple[int, Any]]

        debug_print("Contracts with their chosen addresses: %s" % (contracts_with_chosen_addresses,))

        srclist, fetched_srclist = self.build_srclist(data, sdc_name)
        fetched_source = fetched_srclist[[idx for idx in srclist if srclist[idx] == contract_file][0]]
        contracts_in_sdc = []
        debug_print("finding primary contract address of %s:%s in %s" %
                    (file_abs_path, primary_contract, contracts_with_chosen_addresses))
        primary_contract_address = \
            self.find_contract_address_str(file_abs_path,
                                           primary_contract,
                                           contracts_with_chosen_addresses)
        debug_print("For contracts of primary {}".format(primary_contract))

        for contract_file, contract_list in contracts_with_libraries.items():
            for contract_name in contract_list:
                contract_in_sdc = self.get_contract_in_sdc(
                    contract_file,
                    contract_name,
                    contracts_with_chosen_addresses,
                    data,
                    fetched_source,
                    primary_contract,
                    file
                )
                contracts_in_sdc.append(contract_in_sdc)

        debug_print("Contracts in SDC %s: %s" % (sdc_name, contracts_in_sdc))
        # Need to deduplicate the library_addresses list without changing the order
        deduplicated_library_addresses = list(OrderedDict.fromkeys(self.library_addresses))
        sdc = SDC(primary_contract,
                  primary_contract_address,
                  file,
                  srclist,
                  fetched_srclist,
                  sdc_name,
                  contracts_in_sdc,
                  deduplicated_library_addresses,
                  ' '.join(sys.argv),
                  {},
                  {})
        self.library_addresses.clear()  # Reset library addresses
        return sdc

    def get_contract_in_sdc(self,
                            contract_file: str,
                            contract_name: str,
                            contracts_with_chosen_addresses: List[Tuple[int, Any]],
                            data: Dict[str, Any],
                            fetched_source: str,
                            primary_contract: str,
                            original_file: str
                            ) -> ContractInSDC:
        contract_data = data["contracts"][contract_file][contract_name]
        debug_print("Name,File of contract: %s, %s" % (contract_name, contract_file))
        funcs = self.collect_funcs(contract_data, contract_file, contract_name, original_file)
        debug_print("Functions of %s: %s" % (contract_name, funcs))
        srcmap = self.collect_srcmap(contract_data)
        debug_print("Source maps of %s: %s" % (contract_name, srcmap))
        if "varmap" in self.input_config.parsed_options:
            varmap = self.collect_varmap(contract_name, data)
            debug_print("Variable mappings of %s: %s" % (contract_name, varmap))
        else:
            varmap = ""
        bytecode_ = contract_data["evm"]["deployedBytecode"]["object"]
        bytecode = self.collect_and_link_bytecode(contract_name,
                                                  contracts_with_chosen_addresses,
                                                  bytecode_,
                                                  contract_data["evm"]["deployedBytecode"]["linkReferences"]
                                                  )
        if contract_name == primary_contract and len(bytecode) == 0:
            fatal_error_if_not_library("Error: Contract {} has no bytecode - is it abstract?"
                                       .format(contract_name))
        debug_print("linked bytecode for %s: %s" % (contract_name, bytecode))
        address = self.find_contract_address_str(contract_file,
                                                 contract_name,
                                                 contracts_with_chosen_addresses)
        storage_layout = \
            self.collect_storage_layout(contract_data)
        immutables = self.collect_immutables(contract_data, original_file)
        if OPTION_LINK_CANDIDATES in self.input_config.parsed_options:
            if contract_name in self.input_config.parsed_options[OPTION_LINK_CANDIDATES]:
                linkCandidates = self.input_config.parsed_options[OPTION_LINK_CANDIDATES][contract_name]
            else:
                linkCandidates = {}
        else:
            linkCandidates = {}
        return ContractInSDC(contract_name,
                             contract_file,
                             fetched_source,
                             address,
                             funcs,
                             bytecode,
                             srcmap,
                             varmap,
                             linkCandidates,
                             storage_layout,
                             immutables
                             )

    @staticmethod
    def get_sdc_key(contract: str, address: str) -> str:
        return "%s_%s" % (contract, address)

    @staticmethod
    def get_primary_contract_from_sdc(contracts: List[ContractInSDC], primary: str) -> List[ContractInSDC]:
        return [x for x in contracts if x.name == primary]

    def build(self) -> None:
        for i, f in enumerate(self.input_config.files):
            sdc = self.collect_for_file(f, i)

            # First, add library addresses as SDCs too (they should be processed first)
            debug_print("Libraries to add %s" % sdc.library_addresses)
            for library_address in sdc.library_addresses:
                library_contract_candidates = [contract for contract in sdc.contracts
                                               if contract.address == library_address]
                if len(library_contract_candidates) != 1:
                    fatal_error_if_not_library("Error: Expected to have exactly one library address for {}, got {}"
                                               .format(library_address, library_contract_candidates))

                library_contract = library_contract_candidates[0]
                debug_print("Found library contract %s" % (library_contract))
                # TODO: What will happen with libraries with libraries?
                sdc_lib = SDC(library_contract.name,
                              library_address,
                              library_contract.original_file,
                              sdc.original_srclist,
                              sdc.srclist,
                              "%s_%s" % (sdc.sdc_name, library_contract.name),
                              self.get_primary_contract_from_sdc(sdc.contracts, library_contract.name),
                              [],
                              sdc.generated_with,
                              {},
                              {})
                self.SDCs[self.get_sdc_key(sdc_lib.primary_contract, sdc_lib.primary_contract_address)] = sdc_lib

            # Filter out irrelevant contracts, now that we extracted the libraries, leave just the primary
            sdc.contracts = self.get_primary_contract_from_sdc(sdc.contracts, sdc.primary_contract)
            self.SDCs[self.get_sdc_key(sdc.primary_contract, sdc.primary_contract_address)] = sdc
        self.handle_links()
        self.handle_struct_links()

    def handle_links(self) -> None:
        # Link processing
        if OPTION_LINK in self.input_config.parsed_options:
            links = self.input_config.parsed_options[OPTION_LINK]
            for link in links:
                src, dst = link.split("=", 2)
                src_contract, reference_to_replace_with_link = src.split(":", 2)
                sources_to_update = self.get_matching_sdc_names_from_SDCs(src_contract)
                if len(sources_to_update) > 1:
                    fatal_error(
                        "Not expecting to find multiple SDC matches {} for {}".format(sources_to_update, src_contract))
                if len(sources_to_update) == 0:
                    fatal_error("No contract to link to with the name {}".format(src_contract))
                source_to_update = sources_to_update[0]
                # Primary contract name should match here
                if self.has_sdc_name_from_SDCs_starting_with(dst):
                    example_dst = self.get_one_sdc_name_from_SDCs(dst)  # Enough to pick one
                    dst_address = self.SDCs[example_dst].primary_contract_address
                else:
                    if is_hex(dst):
                        dst = re.sub(r'0[xX]', '', dst)
                        # The jar doesn't accept numbers with 0x prefix
                    dst_address = dst  # Actually, just a number

                # Decide how to link
                matching_immutable = list({(c, x.varname) for c in self.SDCs[source_to_update].contracts for x in
                                           c.immutables
                                           if
                                           x.varname == reference_to_replace_with_link and c.name == src_contract})
                if len(matching_immutable) > 1:
                    fatal_error(
                        "Not expecting to find multiple immutables with the name {}, got matches {}".format(
                            reference_to_replace_with_link, matching_immutable)
                    )
                """
                Three kinds of links, resolved in the following order:
                1. Immutables. We expect at most one pair of (src_contract, immutableVarName) that matches
                2. Field names. Allocated in the storage - we fetch their slot number. (TODO: OFFSET)
                3. Slot numbers in EVM. Requires knowledge about the Solidity compilation. (TODO: OFFSET)
                """
                debug_print("Candidate immutable names: {}".format(matching_immutable))
                debug_print("Reference to replace with link: {}".format(reference_to_replace_with_link))
                if len(matching_immutable) == 1 and reference_to_replace_with_link == matching_immutable[0][1]:
                    contract_match = matching_immutable[0][0]

                    def map_immut(immutable_reference: ImmutableReference) -> ImmutableReference:
                        if immutable_reference.varname == reference_to_replace_with_link:
                            return PresetImmutableReference(
                                immutable_reference.offset,
                                immutable_reference.length,
                                immutable_reference.varname,
                                dst_address
                            )
                        else:
                            return immutable_reference

                    contract_match.immutables = [map_immut(immutable_reference) for immutable_reference in
                                                 contract_match.immutables]

                    continue
                elif not reference_to_replace_with_link.isnumeric():
                    # TODO: we should parse hexadecimal strings with prefix 0x as integers
                    # We need to convert the string to a slot number
                    resolved_src_slot = self.resolve_slot(src_contract, reference_to_replace_with_link)
                else:
                    resolved_src_slot = reference_to_replace_with_link
                debug_print("Linking slot %s of %s to %s" % (resolved_src_slot, src_contract, dst))
                debug_print(' '.join(k for k in self.SDCs.keys()))

                debug_print("Linking %s (%s) to %s in slot %s" %
                            (src_contract, source_to_update, dst_address, resolved_src_slot))
                self.SDCs[source_to_update].state[resolved_src_slot] = dst_address

    def handle_struct_links(self) -> None:
        # struct link processing
        if OPTION_STRUCT_LINK in self.input_config.parsed_options:
            debug_print('handling struct linking')
            links = self.input_config.parsed_options[OPTION_STRUCT_LINK]
            for link in links:
                src, dst = link.split("=", 2)
                src_contract, reference_to_replace_with_link = src.split(":", 2)
                sources_to_update = self.get_matching_sdc_names_from_SDCs(src_contract)
                if len(sources_to_update) > 1:
                    fatal_error(
                        "Not expecting to find multiple SDC matches {} for {}".format(sources_to_update, src_contract))
                source_to_update = sources_to_update[0]
                # Primary contract name should match here
                if self.has_sdc_name_from_SDCs_starting_with(dst):
                    example_dst = self.get_one_sdc_name_from_SDCs(dst)  # Enough to pick one
                    dst_address = self.SDCs[example_dst].primary_contract_address
                else:
                    dst_address = dst  # Actually, just a number

                debug_print("STRUCT Reference to replace with link: {}".format(reference_to_replace_with_link))

                if not is_hex_or_dec(reference_to_replace_with_link):
                    # We need to convert the string to a slot number
                    fatal_error_if_not_library("error: struct link slot '%s' not a hexadecimal number" %
                                               reference_to_replace_with_link)
                else:
                    if is_hex(reference_to_replace_with_link):
                        reference_to_replace_with_link = re.sub(r'0[xX]', '', reference_to_replace_with_link)
                        # The jar doesn't accept numbers with 0x or 0X as prefix
                    resolved_src_slot = reference_to_replace_with_link
                debug_print("STRUCT Linking slot %s of %s to %s" % (resolved_src_slot, src_contract, dst))
                debug_print(' '.join(k for k in self.SDCs.keys()))

                debug_print("STRUCT Linking %s (%s) to %s in slot %s" %
                            (src_contract, source_to_update, dst_address, resolved_src_slot))
                self.SDCs[source_to_update].structLinkingInfo[resolved_src_slot] = dst_address

    def has_sdc_name_from_SDCs_starting_with(self, potential_contract_name: str) -> bool:
        candidates = self.get_matching_sdc_names_from_SDCs(potential_contract_name)
        return len(candidates) > 0

    def get_one_sdc_name_from_SDCs(self, contract: str) -> str:
        return [k for k, v in self.SDCs.items() if k.startswith("%s_00000000ce4604a" % (contract,))][0]

    def get_matching_sdc_names_from_SDCs(self, contract: str) -> List[str]:
        return [k for k, v in self.SDCs.items() if k.startswith("%s_00000000ce4604a" % (contract,))]

    # Returns the resolved slot number as hex without preceding 0x
    def resolve_slot(self, primary_contract: str, slot_name: str) -> str:
        # TODO: Don't run this command every time
        debug_print("Resolving slots for %s out of %s" % (primary_contract, self.SDCs.keys()))
        sdc = self.SDCs[self.get_one_sdc_name_from_SDCs(primary_contract)]  # Enough to pick one
        file = sdc.sdc_origin_file
        solc_ver_to_run = self.get_relevant_solc(primary_contract)
        solc_add_extra_args = self.get_extra_solc_args()

        if OPTION_PACKAGES in self.input_config.parsed_options:
            asm_collect_cmd = "%s %s -o %s/ --overwrite --asm --allow-paths %s %s %s" % \
                              (solc_ver_to_run, solc_add_extra_args, self.config_path,
                               self.input_config.parsed_options[OPTION_PATH],
                               self.input_config.parsed_options[OPTION_PACKAGES], file)
        else:
            asm_collect_cmd = "%s %s -o %s/ --overwrite --asm --allow-paths %s %s" % \
                              (solc_ver_to_run, solc_add_extra_args, self.config_path,
                               self.input_config.parsed_options[OPTION_PATH], file)
        run_cmd(asm_collect_cmd, "%s.asm" % (primary_contract), self.config_path, shell=False)
        with open("%s/%s.evm" % (self.config_path, primary_contract), "r") as asm_file:
            debug_print("Got asm %s" % (asm_file))
            saw_match = False
            candidate_slots = []
            for line in asm_file:
                if saw_match:
                    candidate_slots.append(line)
                    saw_match = False
                else:
                    regex = r'/\* "[a-zA-Z0-9./_\-:]+":[0-9]+:[0-9]+\s* %s \*/' % (slot_name,)
                    saw_match = re.search(regex, line) is not None
                    if saw_match:
                        debug_print("Saw match for %s on line %s" % (regex, line))
            debug_print("Candidate slots: %s" % (candidate_slots))
            normalized_candidate_slots = [x.strip() for x in candidate_slots]
            debug_print("Candidate slots: %s" % (normalized_candidate_slots))
            filtered_candidate_slots = [x for x in normalized_candidate_slots if x.startswith("0x")]
            set_candidate_slots = set(filtered_candidate_slots)
            debug_print("Set of candidate slots: %s" % (set_candidate_slots))
            if len(set_candidate_slots) == 1:
                # Auto detect base (should be 16 though thanks to 0x)
                slot_number = hex(int(list(set_candidate_slots)[0], 0))[2:]
                debug_print("Got slot number %s" % (slot_number))
            else:
                raise Exception("Failed to resolve slot for %s in %s, valid candidates: %s" %
                                (slot_name, primary_contract, set_candidate_slots))

        return slot_number


class CertoraVerifyGenerator:
    def __init__(self, build_generator: CertoraBuildGenerator):
        self.build_generator = build_generator
        self.input_config = build_generator.input_config
        self.certora_verify_struct = []
        self.verify = {}  # type: Dict[str, List[str]]
        if OPTION_VERIFY in self.input_config.parsed_options or OPTION_ASSERT in self.input_config.parsed_options:
            if OPTION_VERIFY in self.input_config.parsed_options:
                verification_queries = self.input_config.parsed_options[OPTION_VERIFY]
                for verification_query in verification_queries:
                    vq_contract, vq_spec = verification_query.split(":", 2)
                    vq_spec = as_posix(os.path.abspath(vq_spec))  # get full abs path
                    if self.verify.get(vq_contract, None) is None:
                        self.verify[vq_contract] = []
                    self.verify[vq_contract].append(vq_spec)
                    self.certora_verify_struct.append(
                        {"type": "spec",
                         "primary_contract": vq_contract,
                         "specfile": self.get_path_to_spec(vq_contract, vq_spec)}
                    )

            if OPTION_ASSERT in self.input_config.parsed_options:
                for contractToCheckAssertsFor in self.input_config.parsed_options[OPTION_ASSERT]:
                    self.certora_verify_struct.append(
                        {"type": "assertion",
                         "primary_contract": contractToCheckAssertsFor}
                    )

        else:
            # if no --verify or --assert, remove verify json file
            try:
                os.remove('%s.json' % (self.input_config.parsed_options[OPTION_OUTPUT_VERIFY]))
            except OSError:
                pass

    def get_spec_idx(self, contract: str, spec: str) -> int:
        return self.verify[contract].index(spec)

    def get_path_to_spec(self, contract: str, spec: str) -> str:
        spec_basename = get_file_basename(spec)
        return "%s/%d_%s.spec" % (self.input_config.get_certora_config_dir(),
                                  self.get_spec_idx(contract, spec),
                                  spec_basename)

    def copy_specs(self) -> None:
        for contract, specs in self.verify.items():
            for spec in specs:
                shutil.copy2(spec, self.get_path_to_spec(contract, spec))

    def check(self) -> None:
        for contract in self.verify:
            if len(self.build_generator.get_matching_sdc_names_from_SDCs(contract)) == 0:
                fatal_error_if_not_library("Error: Could not find contract %s in contracts [%s]" %
                                           (contract, ','.join(map(lambda x: x[1].primary_contract,
                                                                   self.build_generator.SDCs.items())))
                                           )

    def dump(self) -> None:
        with open('%s.json' % (self.input_config.parsed_options[OPTION_OUTPUT_VERIFY]), 'w+') as output_file:
            json.dump(self.certora_verify_struct, output_file, indent=4, sort_keys=True)


def main_with_args(args: List[str], isLibrary: bool = False) -> None:
    global BUILD_IS_LIBRARY
    BUILD_IS_LIBRARY = isLibrary
    global DEBUG

    try:
        if "--help" in args:
            print_usage()
            exit_if_not_library(1)

        if "--debug" in args:
            DEBUG = True

        nestedOptionHack(args)
        # Must check legal args after handling the solc args
        check_legal_args(args, legal_build_args)

        input_config = InputConfig(args)

        # Store current options
        current_conf_to_file(input_config.parsed_options, input_config.files, input_config.fileToContractName)

        # Start to collect information from solc
        certora_build_generator = CertoraBuildGenerator(input_config)
        certora_build_generator.build()

        # if OPTION_ADDRESS in parsed_options:
        #     manual_addresses = parsed_options[OPTION_ADDRESS]
        #     for address_assignment in manual_addresses:
        #         contract,address = address_assignment.split(":",2)
        #         debug_print("Setting address of %s to %s" %(contract,address))
        #         contracts_to_update = get_matching_sdc_names_from_SDCs(contract)
        #         for contract_to_update in contracts_to_update:
        #             debug_print("Setting address of %s (%s) to address %s" % (contract_to_update, contract, address))
        #             SDCs[contract_to_update]["address"] = address

        # Build certora_verify
        certora_verify_generator = CertoraVerifyGenerator(certora_build_generator)
        certora_verify_generator.check()
        certora_verify_generator.copy_specs()
        certora_verify_generator.dump()

        # Output
        if OPTION_OUTPUT in input_config.parsed_options:  # will never be false because of default
            with open('%s.json' % (input_config.parsed_options[OPTION_OUTPUT]), 'w+') as output_file:
                json.dump({k: v.asdict() for k, v in certora_build_generator.SDCs.items()},
                          output_file,
                          indent=4,
                          sort_keys=True)
        else:
            print("SDCs:")
            print(certora_build_generator.SDCs)

    except Exception:
        print("Encountered an error configuring the verification environment:")
        print(traceback.format_exc())
        print_usage()
        exit_if_not_library(1)


def main() -> None:
    main_with_args(sys.argv[1:])


if __name__ == '__main__':
    main()
