import mgraph_ai_service_html__admin_ui
from unittest                                                               import TestCase
from fastapi                                                                import FastAPI
from osbot_fast_api.api.Fast_API                                            import ENV_VAR__FAST_API__AUTH__API_KEY__NAME, ENV_VAR__FAST_API__AUTH__API_KEY__VALUE
from osbot_fast_api.api.schemas.consts.consts__Fast_API                     import EXPECTED_ROUTES__SET_COOKIE
from osbot_fast_api_serverless.fast_api.routes.Routes__Info                 import ROUTES_PATHS__INFO
from osbot_fast_api_serverless.utils.Version                                import version__osbot_fast_api_serverless
from osbot_utils.utils.Env                                                  import get_env
from osbot_utils.utils.Files                                                import file_contents
from starlette.testclient                                                   import TestClient
from mgraph_ai_service_html.html__fast_api.Html_Service__Fast_API           import Html_Service__Fast_API, ROUTES_PATHS__CONSOLE
from mgraph_ai_service_html.html__fast_api.routes.Routes__Dict              import ROUTES_PATHS__DICT
from mgraph_ai_service_html.html__fast_api.routes.Routes__Hashes            import ROUTES_PATHS__HASHES
from mgraph_ai_service_html.html__fast_api.routes.Routes__Html              import ROUTES_PATHS__HTML
from tests.unit.Service__Fast_API__Test_Objs                                import setup__service_fast_api_test_objs, Service__Fast_API__Test_Objs, TEST_API_KEY__NAME


class test_Html_Service__Fast_API__client(TestCase):

    @classmethod
    def setUpClass(cls):
        with setup__service_fast_api_test_objs() as _:
            cls.service_fast_api_test_objs         = _
            cls.fast_api                           = cls.service_fast_api_test_objs.fast_api
            cls.client                             = cls.service_fast_api_test_objs.fast_api__client
            cls.client.headers[TEST_API_KEY__NAME] = ''

    def auth_headers(self):
        auth_key_name       = get_env(ENV_VAR__FAST_API__AUTH__API_KEY__NAME )
        auth_key_value      = get_env(ENV_VAR__FAST_API__AUTH__API_KEY__VALUE)
        auth_headers        = { auth_key_name: auth_key_value }
        return auth_headers

    def test__init__(self):
        with self.service_fast_api_test_objs as _:
            assert type(_)                  is Service__Fast_API__Test_Objs
            assert type(_.fast_api        ) is Html_Service__Fast_API
            assert type(_.fast_api__app   ) is FastAPI
            assert type(_.fast_api__client) is TestClient
            assert self.fast_api            == _.fast_api
            assert self.client              == _.fast_api__client

    def test__client__auth(self):
        path                = '/info/version'
        auth_key_name       = get_env(ENV_VAR__FAST_API__AUTH__API_KEY__NAME )
        auth_key_value      = get_env(ENV_VAR__FAST_API__AUTH__API_KEY__VALUE)
        headers             = {auth_key_name: auth_key_value}

        response__no_auth   = self.client.get(url=path, headers={})
        response__with_auth = self.client.get(url=path, headers=headers)

        assert response__no_auth.status_code   == 401
        assert response__no_auth.json()        == { 'data'   : None,
                                                    'error'  : None,
                                                    'message': 'Client API key is missing, you need to set it on a header or cookie',
                                                    'status' : 'error'}

        assert auth_key_name                   is not None
        assert auth_key_value                  is not None
        assert response__with_auth.status_code == 200
        assert response__with_auth.json()      ==  {'version': version__osbot_fast_api_serverless }

    def test__config_fast_api_routes(self):
        assert self.fast_api.routes_paths() == sorted(  ROUTES_PATHS__INFO          +
                                                        EXPECTED_ROUTES__SET_COOKIE +       # todo: fix this on OSBot-Fast-API since this should be ROUTES_PATHS__AUTH
                                                        ROUTES_PATHS__CONSOLE       +
                                                        ROUTES_PATHS__DICT          +
                                                        ROUTES_PATHS__HASHES        +
                                                        ROUTES_PATHS__HTML          )

    def test_path_static_folder(self):
        with self.fast_api as _:
            assert '/console' in _.routes_paths(expand_mounts=True)
            index_contents = file_contents(mgraph_ai_service_html__admin_ui.path + '/index.html')



        with self.client as _:

            response_1 = _.get('/console', headers=self.auth_headers(), follow_redirects=False)
            assert response_1.status_code == 307
            assert response_1.headers['Location'] == '/console/v0/v0.1.0/index.html'

            response_2 = _.get('/console/index.html', headers=self.auth_headers())

            assert response_2.status_code == 200
            assert response_2.text        == index_contents

            response_3 = _.get('/console', headers=self.auth_headers(), follow_redirects=True)
            assert response_3.status_code == 200
            assert "<title>HTML Service Dashboard - Admin UI</title>" in response_3.text
