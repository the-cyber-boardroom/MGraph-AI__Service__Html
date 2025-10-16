from osbot_fast_api.api.routes.Fast_API__Routes                                         import Fast_API__Routes
from starlette.responses                                                                   import HTMLResponse
from mgraph_ai_service_html.html__fast_api.core.Html__Direct__Transformations              import Html__Direct__Transformations
from mgraph_ai_service_html.html__fast_api.schemas.Schema__Html__Transformations           import Schema__Hashes__To__Html__Request
from osbot_utils.helpers.html.transformers.Html__To__Html_Dict                             import STRING__SCHEMA_NODES, STRING__SCHEMA_TEXT
from typing                                                                                import Dict


class Routes__Hashes(Fast_API__Routes):                         # Hash reconstruction
    tag                        : str                       = 'hashes'
    html_direct_transformations: Html__Direct__Transformations = None
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_direct_transformations = Html__Direct__Transformations()
    
    def to__html(self, request: Schema__Hashes__To__Html__Request
                  ) -> HTMLResponse:
        modified_dict = self._apply_hash_mapping(request.html_dict, request.hash_mapping)  # Merge hash_mapping into html_dict
        html          = self.html_direct_transformations.html_dict__to__html(modified_dict)  # Reconstruct HTML
        
        return HTMLResponse(content=html, status_code=200)
    
    def _apply_hash_mapping(self, html_dict      : Dict         ,  # Apply hash replacements
                                  hash_mapping   : Dict[str, str]
                            ) -> Dict:
        if not isinstance(html_dict, dict):
            return html_dict
        
        result = html_dict.copy()                                # Create copy to avoid modifying original
        
        if result.get("type") == STRING__SCHEMA_TEXT:            # If this is a text node, check if we should replace it
            data = result.get("data", "")
            if data in hash_mapping:
                result["data"] = hash_mapping[data]
        
        if STRING__SCHEMA_NODES in result:                       # Recursively process children
            result[STRING__SCHEMA_NODES] = [
                self._apply_hash_mapping(child, hash_mapping)
                for child in result[STRING__SCHEMA_NODES]
            ]
        
        return result
    
    def setup_routes(self):
        self.add_route_post(self.to__html)
