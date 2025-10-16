from osbot_utils.type_safe.Type_Safe                                                    import Type_Safe
from osbot_utils.type_safe.primitives.domains.http.safe_str.Safe_Str__Html             import Safe_Str__Html
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash     import Safe_Str__Hash
from osbot_utils.type_safe.primitives.core.Safe_UInt                                    import Safe_UInt
from typing                                                                             import Dict

# ============ Atomic Operation Schemas ============

class Schema__Html__To__Dict__Request(Type_Safe):                # Parse HTML to dict
    html: Safe_Str__Html                                         # Raw HTML content (1MB limit)

class Schema__Html__To__Dict__Response(Type_Safe):               # Parsed structure
    html_dict    : Dict                                          # Full html_dict structure
    node_count   : Safe_UInt                                     # Total nodes in tree
    max_depth    : Safe_UInt                                     # Deepest nesting level

class Schema__Dict__To__Html__Request(Type_Safe):                # Reconstruct HTML
    html_dict: Dict                                              # html_dict structure

class Schema__Dict__To__Text__Nodes__Request(Type_Safe):         # Extract text nodes
    html_dict: Dict                                              # html_dict structure
    max_depth: Safe_UInt = 256                                   # Maximum traversal depth

class Schema__Dict__To__Text__Nodes__Response(Type_Safe):        # Extracted nodes
    text_nodes       : Dict[Safe_Str__Hash, Dict]                # {hash: {text, tag}}
    total_nodes      : Safe_UInt                                 # Number of text nodes
    max_depth_reached: bool                                      # Hit depth limit?

# ============ Compound Operation Schemas ============

class Schema__Html__To__Text__Nodes__Request(Type_Safe):         # One-shot extraction
    html     : Safe_Str__Html                                    # Raw HTML content
    max_depth: Safe_UInt = 256                                   # Maximum traversal depth

class Schema__Html__To__Html__Request(Type_Safe):                # Round-trip validation
    html: Safe_Str__Html                                         # HTML to validate

class Schema__Html__To__Html__Hashes__Request(Type_Safe):        # Visual debug
    html     : Safe_Str__Html                                    # Raw HTML content
    max_depth: Safe_UInt = 256                                   # Maximum traversal depth

class Schema__Html__To__Html__Xxx__Request(Type_Safe):           # Privacy mask
    html     : Safe_Str__Html                                    # Raw HTML content
    max_depth: Safe_UInt = 256                                   # Maximum traversal depth

class Schema__Html__To__Lines__Request(Type_Safe):               # Formatted output
    html: Safe_Str__Html                                         # Raw HTML content

class Schema__Dict__To__Lines__Request(Type_Safe):               # Format dict as lines
    html_dict: Dict                                              # html_dict structure

# ============ Hash Reconstruction Schema ============

class Schema__Hashes__To__Html__Request(Type_Safe):              # Merge external modifications
    html_dict   : Dict                                           # Original structure
    hash_mapping: Dict[Safe_Str__Hash, str]                      # {hash: replacement_text}
