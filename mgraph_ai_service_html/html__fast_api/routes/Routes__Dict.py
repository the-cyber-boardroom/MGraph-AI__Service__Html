from osbot_fast_api.api.routes.Fast_API__Routes                                         import Fast_API__Routes
from starlette.responses                                                                import HTMLResponse, PlainTextResponse
from mgraph_ai_service_html.core.Html__Direct__Transformations                          import Html__Direct__Transformations
from mgraph_ai_service_html.schemas.Schema__Html__Requests                              import Schema__Dict__To__Html__Request
from mgraph_ai_service_html.schemas.Schema__Html__Requests                              import Schema__Dict__To__Text__Nodes__Request, Schema__Dict__To__Text__Nodes__Response
from mgraph_ai_service_html.schemas.Schema__Html__Requests                              import Schema__Dict__To__Lines__Request

class Routes__Dict(Fast_API__Routes):                           # Dict-based operations
    tag                        : str                       = 'dict'
    html_direct_transformations: Html__Direct__Transformations = None
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_direct_transformations = Html__Direct__Transformations()
    
    def to__html(self, request: Schema__Dict__To__Html__Request # Reconstruct HTML
                  ) -> HTMLResponse:
        html = self.html_direct_transformations.html_dict__to__html(request.html_dict)
        return HTMLResponse(content=html, status_code=200)
    
    def to__text__nodes(self, request: Schema__Dict__To__Text__Nodes__Request
                         ) -> Schema__Dict__To__Text__Nodes__Response:
        text_nodes = self.html_direct_transformations.html_dict__to__text_nodes(request.html_dict, request.max_depth)
        
        return Schema__Dict__To__Text__Nodes__Response(text_nodes        = text_nodes       ,
                                                       total_nodes       = len(text_nodes)  ,
                                                       max_depth_reached = False            )  # TODO: implement depth check
    
    def to__lines(self, request: Schema__Dict__To__Lines__Request
                   ) -> PlainTextResponse:
        html = self.html_direct_transformations.html_dict__to__html(request.html_dict)
        lines = self.html_direct_transformations.html__to__lines(html)
        return PlainTextResponse(content=lines)
    
    def setup_routes(self):
        self.add_route_post(self.to__html       )
        self.add_route_post(self.to__text__nodes)
        self.add_route_post(self.to__lines      )
