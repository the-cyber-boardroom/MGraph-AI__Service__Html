from osbot_fast_api.api.routes.Fast_API__Routes                                                 import Fast_API__Routes
from starlette.responses                                                                        import HTMLResponse, PlainTextResponse
from typing                                                                                     import Dict
from mgraph_ai_service_html.html__fast_api.core.Html__Direct__Transformations                   import Html__Direct__Transformations
from mgraph_ai_service_html.html__fast_api.schemas.dict.Schema__Dict__To__Text__Nodes__Response import Schema__Dict__To__Text__Nodes__Response
from mgraph_ai_service_html.html__fast_api.schemas.html.Schema__Html__To__Dict__Request         import Schema__Html__To__Dict__Request
from mgraph_ai_service_html.html__fast_api.schemas.html.Schema__Html__To__Dict__Response        import Schema__Html__To__Dict__Response
from mgraph_ai_service_html.html__fast_api.schemas.html.Schema__Html__To__Html__Hashes__Request import Schema__Html__To__Html__Hashes__Request
from mgraph_ai_service_html.html__fast_api.schemas.html.Schema__Html__To__Html__Request         import Schema__Html__To__Html__Request
from mgraph_ai_service_html.html__fast_api.schemas.html.Schema__Html__To__Html__Xxx__Request    import Schema__Html__To__Html__Xxx__Request
from mgraph_ai_service_html.html__fast_api.schemas.html.Schema__Html__To__Lines__Request        import Schema__Html__To__Lines__Request
from mgraph_ai_service_html.html__fast_api.schemas.html.Schema__Html__To__Text__Nodes__Request  import Schema__Html__To__Text__Nodes__Request


class Routes__Html(Fast_API__Routes):                           # HTML transformation routes
    tag                        : str                       = 'html'
    html_direct_transformations: Html__Direct__Transformations = None
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_direct_transformations = Html__Direct__Transformations()
    
    # ========== Atomic Operations ==========
    
    def to__dict(self, request: Schema__Html__To__Dict__Request # Parse HTML to dict
                  ) -> Schema__Html__To__Dict__Response:
        html_dict  = self.html_direct_transformations.html__to__html_dict(request.html)
        node_count = self._count_nodes(html_dict)
        max_depth  = self._calculate_max_depth(html_dict)
        
        return Schema__Html__To__Dict__Response(html_dict  = html_dict  ,
                                                node_count = node_count ,
                                                max_depth  = max_depth  )
    
    def to__html(self, request: Schema__Html__To__Html__Request # Round-trip validation
                  ) -> HTMLResponse:
        html_dict = self.html_direct_transformations.html__to__html_dict(request.html)
        html      = self.html_direct_transformations.html_dict__to__html(html_dict)
        return HTMLResponse(content=html, status_code=200)
    
    # ========== Compound Operations ==========
    
    def to__text__nodes(self, request: Schema__Html__To__Text__Nodes__Request
                         ) -> Schema__Dict__To__Text__Nodes__Response:
        html_dict  = self.html_direct_transformations.html__to__html_dict(request.html)
        text_nodes = self.html_direct_transformations.html_dict__to__text_nodes(html_dict, request.max_depth)
        
        return Schema__Dict__To__Text__Nodes__Response(text_nodes        = text_nodes                            ,
                                                       total_nodes       = len(text_nodes)                       ,
                                                       max_depth_reached = self._check_depth(html_dict, request.max_depth))
    
    def to__lines(self, request: Schema__Html__To__Lines__Request
                   ) -> PlainTextResponse:
        lines = self.html_direct_transformations.html__to__lines(request.html)
        return PlainTextResponse(lines)
    
    def to__html__hashes(self, request: Schema__Html__To__Html__Hashes__Request
                          ) -> HTMLResponse:
        html_dict  = self.html_direct_transformations.html__to__html_dict(request.html)
        text_nodes = self.html_direct_transformations.html_dict__to__text_nodes(html_dict, request.max_depth)
        
        html_with_hashes = self._replace_text_with_hashes(html_dict, text_nodes)
        html = self.html_direct_transformations.html_dict__to__html(html_with_hashes)
        
        return HTMLResponse(content=html, status_code=200)
    
    def to__html__xxx(self, request: Schema__Html__To__Html__Xxx__Request
                       ) -> HTMLResponse:
        html_dict  = self.html_direct_transformations.html__to__html_dict(request.html)
        text_nodes = self.html_direct_transformations.html_dict__to__text_nodes(html_dict, request.max_depth)
        
        html_with_xxx = self._replace_text_with_xxx(html_dict, text_nodes)
        html = self.html_direct_transformations.html_dict__to__html(html_with_xxx)
        
        return HTMLResponse(content=html, status_code=200)
    
    # ========== Helper Methods ==========
    
    def _count_nodes(self, html_dict: Dict) -> int:             # Count nodes in tree
        def count_recursive(node):
            if not isinstance(node, dict):
                return 0
            count = 1
            for child in node.get('nodes', []):
                count += count_recursive(child)
            return count
        return count_recursive(html_dict)
        
    def _calculate_max_depth(self, html_dict: Dict) -> int:     # Find deepest nesting
        def depth_recursive(node, current_depth):
            if not isinstance(node, dict):
                return current_depth
            max_child_depth = current_depth
            for child in node.get('nodes', []):
                child_depth = depth_recursive(child, current_depth + 1)
                max_child_depth = max(max_child_depth, child_depth)
            return max_child_depth
        return depth_recursive(html_dict, 0)
        
    def _check_depth(self, html_dict: Dict, max_depth: int) -> bool:  # Hit depth limit?
        actual_depth = self._calculate_max_depth(html_dict)
        return actual_depth >= max_depth
        
    def _replace_text_with_hashes(self, html_dict: Dict, text_nodes: Dict) -> Dict:  # Replace text with hashes
        # Implementation: traverse html_dict, replace text with hashes
        # The text_nodes dict contains the mappings we need
        return html_dict  # Already modified during extraction
        
    def _replace_text_with_xxx(self, html_dict: Dict, text_nodes: Dict) -> Dict:  # Replace text with x's
        from osbot_utils.helpers.html.transformers.Html_Dict__To__Html import Html_Dict__To__Html
        html = Html_Dict__To__Html(root=html_dict).convert()
        for text_hash, text_element in text_nodes.items():
            original_text = text_element.get('text')
            text_to_replace = ''.join('x' if c != ' ' else ' ' for c in original_text)
            html = html.replace(text_hash, text_to_replace)
        # Convert back to dict
        from osbot_utils.helpers.html.transformers.Html__To__Html_Dict import Html__To__Html_Dict
        return Html__To__Html_Dict(html=html).convert()
    
    def setup_routes(self):
        self.add_route_post(self.to__dict         )             # Atomic operations
        self.add_route_post(self.to__html         )
        self.add_route_post(self.to__text__nodes  )             # Compound operations
        self.add_route_post(self.to__lines        )
        self.add_route_post(self.to__html__hashes )
        self.add_route_post(self.to__html__xxx    )
