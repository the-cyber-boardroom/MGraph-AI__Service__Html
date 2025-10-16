from typing                                                         import Dict
from osbot_utils.helpers.html.transformers.Html__To__Html_Dict  import STRING__SCHEMA_NODES, STRING__SCHEMA_TEXT
from osbot_utils.helpers.html.transformers.Html_Dict__To__Html  import Html_Dict__To__Html
from osbot_utils.type_safe.Type_Safe                            import Type_Safe
from osbot_utils.utils.Misc                                     import str_md5


DEFAULT_MAX_DEPTH = 256                                          # Maximum tree traversal depth


class Html__Extract_Text_Nodes(Type_Safe):                      # Extract text nodes from HTML dict
    html_dict          : Dict = None                             # Can be set directly
    text_elements      : Dict                                    # Processed text elements
    text_elements__raw : Dict                                    # Raw text content
    hash_size          : int  = 10                               # Length of hash identifiers
    captures           : int  = 0                                # Number of text nodes found
    max_depth          : int  = 256                              # Maximum traversal depth
    
    def capture_text(self, text: str, tag: str) -> str:         # Create hash and store text node
        hash_value                      = str_md5(text)[:self.hash_size]
        self.text_elements__raw[hash_value] = text
        self.text_elements[hash_value] = dict(original_text = text,
                                              tag           = tag )
        self.captures += 1
        return hash_value

    def traverse(self, node        : Dict,                      # Recursively traverse HTML tree
                       depth       : int ,
                       parent_tag  : str
                 ) -> None:
        if depth > self.max_depth:
            return

        if not isinstance(node, dict):
            return

        if node.get("type") == STRING__SCHEMA_TEXT:             # Found text node
            data = node.get("data", "").strip()
            if data:
                if parent_tag not in ['style', 'script']:       # Skip script/style content
                    node['data'] = self.capture_text(node['data'], parent_tag)

        node_tag = node.get('tag')
        for child in node.get(STRING__SCHEMA_NODES, []):
            self.traverse(child, depth + 1, node_tag)

    def extract_from_html_dict(self, html_dict : Dict     ,     # NEW METHOD: Direct extraction
                                     max_depth  : int = 256
                                ) -> Dict:
        self.html_dict = html_dict
        self.max_depth = max_depth
        self.traverse(self.html_dict, depth=0, parent_tag=None)
        return self.text_elements
        
    def create_html_with_hashes_as_text(self) -> str:           # Replace text with hashes (visual debug)
        if not self.html_dict:
            raise ValueError("html_dict not set - call extract_from_html_dict first")

        html_with_hashes = Html_Dict__To__Html(root=self.html_dict).convert()
        return html_with_hashes

    def create_html_with_xxx_as_text(self) -> str:              # Replace text with xxx (privacy mask)
        html = self.create_html_with_hashes_as_text()
        for text_hash, text_element in self.text_elements.items():
            original_text   = text_element.get('original_text')
            text_to_replace = ''.join('x' if c != ' ' else ' ' for c in original_text)
            html            = html.replace(text_hash, text_to_replace)
        return html
