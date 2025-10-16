from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe
from osbot_utils.type_safe.primitives.domains.http.safe_str.Safe_Str__Html          import Safe_Str__Html
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash  import Safe_Str__Hash
from osbot_utils.type_safe.primitives.core.Safe_UInt                                 import Safe_UInt
from typing                                                                          import Dict


class Schema__Dict__To__Html__Request(Type_Safe):               # Reconstruct HTML
    html_dict: Dict                                              # html_dict structure


class Schema__Dict__To__Text__Nodes__Request(Type_Safe):        # Extract text nodes
    html_dict: Dict                                              # html_dict structure
    max_depth: Safe_UInt = 256                                   # Maximum traversal depth


class Schema__Dict__To__Text__Nodes__Response(Type_Safe):       # Extracted nodes
    text_nodes       : Dict[Safe_Str__Hash, Dict]                # {hash: {text, tag}}
    total_nodes      : Safe_UInt                                 # Number of text nodes
    max_depth_reached: bool                                      # Hit depth limit?


class Schema__Dict__To__Lines__Request(Type_Safe):              # Formatted output
    html_dict: Dict                                              # html_dict structure
