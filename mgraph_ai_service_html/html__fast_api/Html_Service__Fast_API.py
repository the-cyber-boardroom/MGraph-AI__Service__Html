from osbot_fast_api.api.routes.Routes__Set_Cookie                   import Routes__Set_Cookie
from osbot_fast_api_serverless.fast_api.Serverless__Fast_API        import Serverless__Fast_API
from osbot_fast_api_serverless.fast_api.routes.Routes__Info         import Routes__Info
from mgraph_ai_service_html.config                                  import FAST_API__TITLE, FAST_API__DESCRIPTION
from mgraph_ai_service_html.html__fast_api.routes.Routes__Admin     import Routes__Admin
from mgraph_ai_service_html.html__fast_api.routes.Routes__Dict      import Routes__Dict
from mgraph_ai_service_html.html__fast_api.routes.Routes__Hashes    import Routes__Hashes
from mgraph_ai_service_html.html__fast_api.routes.Routes__Html      import Routes__Html
from mgraph_ai_service_html.utils.Version                           import version__mgraph_ai_service_html


class Html_Service__Fast_API(Serverless__Fast_API):                     # Main FastAPI application

    def setup(self):
        with self.config as _:
            _.name           = FAST_API__TITLE
            _.version        = version__mgraph_ai_service_html
            _.description    = FAST_API__DESCRIPTION
        return super().setup()


    def setup_routes(self):
        self.add_routes(Routes__Html      )                     # HTML transformation routes
        self.add_routes(Routes__Dict      )                     # Dict operation routes
        self.add_routes(Routes__Hashes    )                     # Hash reconstruction routes
        self.add_routes(Routes__Info      )                     # Service info
        self.add_routes(Routes__Set_Cookie)                     # Utility routes
        self.add_routes(Routes__Admin     )
