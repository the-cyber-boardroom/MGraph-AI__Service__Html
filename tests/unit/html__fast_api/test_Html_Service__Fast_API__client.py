from unittest                                                               import TestCase
from fastapi                                                                import FastAPI
from osbot_fast_api.api.Fast_API                                            import ENV_VAR__FAST_API__AUTH__API_KEY__NAME, ENV_VAR__FAST_API__AUTH__API_KEY__VALUE
from osbot_fast_api.api.schemas.safe_str.Safe_Str__Fast_API__Route__Prefix  import Safe_Str__Fast_API__Route__Prefix
from osbot_utils.utils.Env                                                  import get_env
from starlette.testclient                                                   import TestClient
from mgraph_ai_service_html.html__fast_api.Html_Service__Fast_API           import Html_Service__Fast_API
from tests.unit.Service__Fast_API__Test_Objs                                import setup__service_fast_api_test_objs, Service__Fast_API__Test_Objs, TEST_API_KEY__NAME


class test_Html_Service__Fast_API__client(TestCase):

    @classmethod
    def setUpClass(cls):
        with setup__service_fast_api_test_objs() as _:
            cls.service_fast_api_test_objs         = _
            cls.fast_api                           = cls.service_fast_api_test_objs.fast_api
            cls.client                             = cls.service_fast_api_test_objs.fast_api__client
            cls.client.headers[TEST_API_KEY__NAME] = ''

    def test__init__(self):
        with self.service_fast_api_test_objs as _:
            assert type(_)                  is Service__Fast_API__Test_Objs
            assert type(_.fast_api        ) is Html_Service__Fast_API
            assert type(_.fast_api__app   ) is FastAPI
            assert type(_.fast_api__client) is TestClient
            assert self.fast_api            == _.fast_api
            assert self.client              == _.fast_api__client

    def test__client__auth(self):
        path                = '/info/health'
        auth_key_name       = get_env(ENV_VAR__FAST_API__AUTH__API_KEY__NAME )
        auth_key_value      = get_env(ENV_VAR__FAST_API__AUTH__API_KEY__VALUE)
        headers             = {auth_key_name: auth_key_value}

        response__no_auth   = self.client.get(url=path, headers={})
        response__with_auth = self.client.get(url=path, headers=headers)

        assert response__no_auth.status_code == 401
        assert response__no_auth.json()      == { 'data'   : None,
                                                  'error'  : None,
                                                  'message': 'Client API key is missing, you need to set it on a header or cookie',
                                                  'status' : 'error'}

        assert auth_key_name                 is not None
        assert auth_key_value                is not None
        #assert response__with_auth.json()    == ROUTES_INFO__HEALTH__RETURN_VALUE

    def test__config_fast_api_routes(self):
        # todo: refactor these route values to the respective Routes_* classes
        assert self.fast_api.routes_paths() == [ Safe_Str__Fast_API__Route__Prefix('/auth/set-auth-cookie'),
                                                 Safe_Str__Fast_API__Route__Prefix('/auth/set-cookie-form'),
                                                 Safe_Str__Fast_API__Route__Prefix('/dict/to/html'),
                                                 Safe_Str__Fast_API__Route__Prefix('/dict/to/lines'),
                                                 Safe_Str__Fast_API__Route__Prefix('/dict/to/text/nodes'),
                                                 Safe_Str__Fast_API__Route__Prefix('/hashes/to/html'),
                                                 Safe_Str__Fast_API__Route__Prefix('/html-service/{file_path:path}'),
                                                 Safe_Str__Fast_API__Route__Prefix('/html/to/dict'),
                                                 Safe_Str__Fast_API__Route__Prefix('/html/to/html'),
                                                 Safe_Str__Fast_API__Route__Prefix('/html/to/html/hashes'),
                                                 Safe_Str__Fast_API__Route__Prefix('/html/to/html/xxx'),
                                                 Safe_Str__Fast_API__Route__Prefix('/html/to/lines'),
                                                 Safe_Str__Fast_API__Route__Prefix('/html/to/text/nodes'),
                                                 Safe_Str__Fast_API__Route__Prefix('/info/version')]