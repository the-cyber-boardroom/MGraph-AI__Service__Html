from osbot_fast_api.api.routes.Fast_API__Routes                                                  import Fast_API__Routes
from starlette.responses                                                                                import HTMLResponse, PlainTextResponse
from mgraph_ai_service_html.html__fast_api.core.Html__Direct__Transformations                           import Html__Direct__Transformations
from mgraph_ai_service_html.html__fast_api.core.Html__Extract_Text_Nodes                                import Html__Extract_Text_Nodes
from mgraph_ai_service_html.html__fast_api.schemas.Schema__Html__To__Dict                               import Schema__Html__To__Dict__Request, Schema__Html__To__Dict__Response
from mgraph_ai_service_html.html__fast_api.schemas.Schema__Html__To__Text__Nodes                        import Schema__Html__To__Text__Nodes__Request, Schema__Html__To__Text__Nodes__Response
from mgraph_ai_service_html.html__fast_api.schemas.Schema__Html__Transformations                        import Schema__Html__To__Html__Request, Schema__Html__To__Html__Hashes__Request, Schema__Html__To__Html__Xxx__Request, Schema__Html__To__Lines__Request
from typing                                                                                             import Dict


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
                         ) -> Schema__Html__To__Text__Nodes__Response:
        html_dict  = self.html_direct_transformations.html__to__html_dict(request.html)
        text_nodes = self.html_direct_transformations.html_dict__to__text_nodes(html_dict, request.max_depth)
        
        return Schema__Html__To__Text__Nodes__Response(text_nodes        = text_nodes                                    ,
                                                       total_nodes       = len(text_nodes)                               ,
                                                       max_depth_reached = self._check_depth(html_dict, request.max_depth))
    
    def to__lines(self, request: Schema__Html__To__Lines__Request
                   ) -> PlainTextResponse:
        lines = self.html_direct_transformations.html__to__lines(request.html)
        return PlainTextResponse(content=lines)
    
    def to__html__hashes(self, request: Schema__Html__To__Html__Hashes__Request
                          ) -> HTMLResponse:
        html_dict  = self.html_direct_transformations.html__to__html_dict(request.html)
        
        extractor = Html__Extract_Text_Nodes()                   # Extract and replace with hashes
        extractor.extract_from_html_dict(html_dict, request.max_depth)
        html = extractor.create_html_with_hashes_as_text()
        
        return HTMLResponse(content=html, status_code=200)
    
    def to__html__xxx(self, request: Schema__Html__To__Html__Xxx__Request
                       ) -> HTMLResponse:
        html_dict  = self.html_direct_transformations.html__to__html_dict(request.html)
        
        extractor = Html__Extract_Text_Nodes()                   # Extract and replace with xxx
        extractor.extract_from_html_dict(html_dict, request.max_depth)
        html = extractor.create_html_with_xxx_as_text()
        
        return HTMLResponse(content=html, status_code=200)
    
    # ========== Helper Methods ==========
    
    def _count_nodes(self, html_dict: Dict) -> int:              # Count nodes in tree
        if not isinstance(html_dict, dict):
            return 0
        
        count = 1
        for child in html_dict.get('nodes', []):
            count += self._count_nodes(child)
        return count
        
    def _calculate_max_depth(self, html_dict: Dict, current_depth: int = 0) -> int:  # Find deepest nesting
        if not isinstance(html_dict, dict):
            return current_depth
        
        children = html_dict.get('nodes', [])
        if not children:
            return current_depth
        
        max_child_depth = current_depth
        for child in children:
            child_depth = self._calculate_max_depth(child, current_depth + 1)
            max_child_depth = max(max_child_depth, child_depth)
        
        return max_child_depth
        
    def _check_depth(self, html_dict: Dict, max_depth: int) -> bool:  # Hit depth limit?
        actual_depth = self._calculate_max_depth(html_dict)
        return actual_depth >= max_depth
    
    def setup_routes(self):
        self.add_route_post(self.to__dict         )              # Atomic operations
        self.add_route_post(self.to__html         )
        self.add_route_post(self.to__text__nodes  )              # Compound operations
        self.add_route_post(self.to__lines        )
        self.add_route_post(self.to__html__hashes )
        self.add_route_post(self.to__html__xxx    )
