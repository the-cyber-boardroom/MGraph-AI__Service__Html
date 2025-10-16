from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe
from osbot_utils.type_safe.primitives.domains.http.safe_str.Safe_Str__Html          import Safe_Str__Html
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash  import Safe_Str__Hash
from osbot_utils.type_safe.primitives.core.Safe_UInt                                 import Safe_UInt
from typing                                                                          import Dict


class Schema__Html__To__Text__Nodes__Request(Type_Safe):        # One-shot extraction
    html     : Safe_Str__Html                                    # Raw HTML content
    max_depth: Safe_UInt = 256                                   # Maximum traversal depth


class Schema__Html__To__Text__Nodes__Response(Type_Safe):       # Extracted nodes
    text_nodes       : Dict[Safe_Str__Hash, Dict]                # {hash: {text, tag}}
    total_nodes      : Safe_UInt                                 # Number of text nodes
    max_depth_reached: bool                                      # Hit depth limit?
