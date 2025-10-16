from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe
from osbot_utils.type_safe.primitives.domains.http.safe_str.Safe_Str__Html          import Safe_Str__Html
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash  import Safe_Str__Hash
from osbot_utils.type_safe.primitives.core.Safe_UInt                                 import Safe_UInt
from typing                                                                          import Dict


class Schema__Html__To__Html__Request(Type_Safe):               # Round-trip validation
    html: Safe_Str__Html                                         # HTML to validate


class Schema__Html__To__Html__Hashes__Request(Type_Safe):       # Visual debug
    html     : Safe_Str__Html                                    # Raw HTML content
    max_depth: Safe_UInt = 256                                   # Maximum traversal depth


class Schema__Html__To__Html__Xxx__Request(Type_Safe):          # Privacy mask
    html     : Safe_Str__Html                                    # Raw HTML content
    max_depth: Safe_UInt = 256                                   # Maximum traversal depth


class Schema__Html__To__Lines__Request(Type_Safe):              # Formatted output
    html: Safe_Str__Html                                         # Raw HTML content


class Schema__Hashes__To__Html__Request(Type_Safe):             # Merge external modifications
    html_dict   : Dict                                           # Original structure
    hash_mapping: Dict[Safe_Str__Hash, str]                      # {hash: replacement_text}
