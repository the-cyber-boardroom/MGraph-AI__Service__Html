import re
import pytest
from unittest                                                        import TestCase
from fastapi.testclient                                              import TestClient
from osbot_fast_api_serverless.fast_api.Serverless__Fast_API__Config import Serverless__Fast_API__Config
from osbot_utils.testing.__                                          import __
from osbot_utils.testing.__helpers                                   import obj
from osbot_utils.utils.Misc                                          import list_set
from mgraph_ai_service_html.html__fast_api.Html_Service__Fast_API    import Html_Service__Fast_API


class test_Routes__Html__to__Hashes__to__Html__client(TestCase):

    @classmethod
    def setUpClass(cls):
        config = Serverless__Fast_API__Config(enable_api_key=False)
        with Html_Service__Fast_API(config=config) as api:
            api.setup()
            cls.app    = api.app()
            cls.client = TestClient(cls.app)

    def test__http_post__to__dict__hashes__returns_200(self):                       # Test basic HTTP POST success
        payload = { "html"      : "<p>Test</p>" ,
                    "max_depth" : 256           }

        response = self.client.post("/html/to/dict/hashes", json=payload)

        assert response.status_code            == 200
        data = response.json()
        assert "html_dict"           in data
        assert "text_hashes_mapping" in data
        assert "node_count"          in data
        assert "max_depth"           in data
        assert "total_text_hashes"   in data
        assert "max_depth_reached"   in data

        assert obj(data) == __( html_dict           = __( tag   = 'p'                     ,
                                                           attrs = __()                  ,
                                                           nodes = [ __( type = 'TEXT'   ,
                                                                        data = '0cbc6611f5' ) ] ) ,
                                 text_hashes_mapping = __( _0cbc6611f5 = 'Test' )         ,
                                 node_count          = 2                                  ,
                                 max_depth           = 1                                  ,
                                 total_text_hashes   = 1                                  ,
                                 max_depth_reached   = False                              )

    def test__http_post__to__dict__hashes__with_complex_html(self): # Test complex HTML structure
        payload = {
            "html": """
                <div>
                    <h1>Title</h1>
                    <p>Paragraph with <strong>bold</strong> text</p>
                    <ul>
                        <li>Item 1</li>
                        <li>Item 2</li>
                    </ul>
                </div>
            """,
            "max_depth": 256
        }

        response = self.client.post("/html/to/dict/hashes", json=payload)

        assert response.status_code                      == 200
        data = response.json()
        assert data["total_text_hashes"]                 >= 4    # Title, Paragraph, Item 1, Item 2
        assert type(data["text_hashes_mapping"])         is dict
        assert len(data["text_hashes_mapping"])          == data["total_text_hashes"]

        assert obj(data)                                 == __( html_dict    = __( tag   = 'div' ,
                                                                                   attrs = __()    ,
                                                                                   nodes = [ __( tag    = 'h1' ,
                                                                                                 attrs  = __()  ,
                                                                                                 nodes  = [ __( type  = 'TEXT'          ,
                                                                                                                data  = 'b78a322350' ) ] ) ,
                                                                                              __( tag   = 'p'   ,
                                                                                                  attrs = __()  ,
                                                                                                  nodes = [ __( type  = 'TEXT'          ,
                                                                                                                data  = '47b74c884c' )   ,
                                                                                                            __( tag   = 'strong'       ,
                                                                                                                attrs = __()            ,
                                                                                                                nodes = [ __( type = 'TEXT'          ,
                                                                                                                              data = '69dcab4a73' ) ] ) ,
                                                                                                            __( type  = 'TEXT'          ,
                                                                                                                data  = 'ea1f576750' ) ] ) ,
                                                                                              __( tag   = 'ul'  ,
                                                                                                  attrs = __()  ,
                                                                                                  nodes = [ __( tag   = 'li'           ,
                                                                                                                attrs = __()            ,
                                                                                                                nodes = [ __( type = 'TEXT'          ,
                                                                                                                              data = 'f59e6f3afd' ) ] ) ,
                                                                                                            __( tag   = 'li'           ,
                                                                                                                attrs = __()            ,
                                                                                                                nodes = [ __( type = 'TEXT'          ,
                                                                                                                              data = '9eda28f018' ) ] ) ] ) ] ) ,
                                                         text_hashes_mapping = __(  b78a322350  = 'Title'           ,
                                                                                   _47b74c884c  = 'Paragraph with ' ,
                                                                                   _69dcab4a73  = 'bold'            ,
                                                                                    ea1f576750  = ' text'           ,
                                                                                    f59e6f3afd  = 'Item 1'          ,
                                                                                   _9eda28f018  = 'Item 2'          ) ,
                                                         node_count          = 13                                 ,
                                                         max_depth           = 3                                  ,
                                                         total_text_hashes   = 6                                  ,
                                                         max_depth_reached   = False                              )


    def test__http_post__to__dict__hashes__validates_schema(self):                  # Test schema validation
        payload = { "max_depth": 256}

        response = self.client.post("/html/to/dict/hashes", json=payload)

        assert response.status_code == 200                                           # empty dict handled ok

        assert response.json() == { 'html_dict'           : {} ,
                                     'max_depth'          : 0  ,
                                     'max_depth_reached'  : False ,
                                     'node_count'         : 0  ,
                                     'text_hashes_mapping': {} ,
                                     'total_text_hashes'  : 0  }


    def test__http_post__to__dict__hashes__default_max_depth(self): # Test max_depth default value
        payload = {
            "html": "<p>Test</p>"
        }

        response = self.client.post("/html/to/dict/hashes", json=payload)

        assert response.status_code                      == 200
        data = response.json()
        assert data["max_depth"]                         <= 256  # Uses default

    def test__http_post__to__text__hashes__returns_200(self):    # Test lightweight endpoint
        payload = {
            "html"      : "<p>Test</p>",
            "max_depth" : 256
        }

        response = self.client.post("/html/to/text/hashes", json=payload)

        assert response.status_code                      == 200
        data = response.json()
        assert "text_hashes_mapping" in data
        assert "total_text_hashes"   in data
        assert "max_depth_reached"   in data
        assert "html_dict"           not in data                 # Lightweight response
        assert "node_count"          not in data

    def test__http_post__to__text__hashes__lightweight_response(self): # Test minimal response
        payload = {
            "html": "<div><p>Test</p><span>Content</span></div>"
        }

        response = self.client.post("/html/to/text/hashes", json=payload)

        assert response.status_code                      == 200
        data = response.json()

        assert len(data)                                 == 3    # Only 3 fields
        assert "text_hashes_mapping" in data
        assert "total_text_hashes"   in data
        assert "max_depth_reached"   in data

    def test__http_post__to__text__hashes__ignores_non_valid_data(self): # Test schema validation
        payload = { "invalid_field": "value" }

        response = self.client.post("/html/to/text/hashes", json=payload)

        assert response.status_code == 200
        assert response.json()      == {'max_depth_reached': False, 'text_hashes_mapping': {}, 'total_text_hashes': 0}

    def test__e2e__complete_workflow_via_http(self):             # Test complete workflow via HTTP
        extract_payload = { "html": "<p>Original text</p>" }
        extract_response = self.client.post("/html/to/dict/hashes", json=extract_payload)
        assert extract_response.status_code              == 200
        extract_data = extract_response.json()

        modified_mapping = {}
        for hash_value, original_text in extract_data["text_hashes_mapping"].items():
            modified_mapping[hash_value] = "Modified text"

        reconstruct_payload = { "html_dict"    : extract_data["html_dict"],
                                "hash_mapping" : modified_mapping }
        reconstruct_response = self.client.post("/hashes/to/html", json=reconstruct_payload)

        assert reconstruct_response.status_code          == 200
        reconstructed_html = reconstruct_response.text
        assert "Modified text" in reconstructed_html
        assert "Original text" not in reconstructed_html

        assert reconstructed_html == '<p>Modified text</p>\n'

    def test__e2e__workflow_with_multiple_nodes(self):           # Test multiple text nodes
        extract_payload = {
            "html": "<div><p>First</p><span>Second</span><p>Third</p></div>"
        }
        extract_response = self.client.post("/html/to/dict/hashes", json=extract_payload)
        extract_data = extract_response.json()

        assert extract_data["total_text_hashes"]         == 3

        modified_mapping = {}
        for hash_value, text in extract_data["text_hashes_mapping"].items():
            modified_mapping[hash_value] = f"NEW_{text}"

        reconstruct_payload = {
            "html_dict"    : extract_data["html_dict"],
            "hash_mapping" : modified_mapping
        }
        reconstruct_response = self.client.post("/hashes/to/html", json=reconstruct_payload)

        reconstructed_html = reconstruct_response.text
        assert "NEW_First"  in reconstructed_html
        assert "NEW_Second" in reconstructed_html
        assert "NEW_Third"  in reconstructed_html

        assert reconstructed_html == ('<div>\n'
                                      '    <p>NEW_First</p>\n'
                                      '    <span>NEW_Second</span>\n'
                                      '    <p>NEW_Third</p>\n'
                                      '</div>\n')

    def test__e2e__workflow_preserves_html_structure(self):      # Test structure preservation
        original_html = """\
<div class="container">
    <h1 id="title">Heading</h1>
    <p class="content">Paragraph</p>
</div>
"""
        extract_payload = {"html": original_html}
        extract_response = self.client.post("/html/to/dict/hashes", json=extract_payload)
        extract_data = extract_response.json()

        modified_mapping = extract_data["text_hashes_mapping"]  # Keep original

        reconstruct_payload = { "html_dict"    : extract_data["html_dict"],
                                "hash_mapping" : modified_mapping }
        reconstruct_response = self.client.post("/hashes/to/html", json=reconstruct_payload)

        reconstructed_html = reconstruct_response.text
        assert "container" in reconstructed_html
        assert "title"     in reconstructed_html
        assert "content"   in reconstructed_html
        assert "Heading"   in reconstructed_html
        assert "Paragraph" in reconstructed_html

        assert reconstructed_html == ('<div class="container">\n'
                                      '    <h1 id="title">Heading</h1>\n'
                                      '    <p class="content">Paragraph</p>\n'
                                      '</div>\n')
        assert reconstructed_html == original_html

    def test__openapi_docs__show_new_endpoints(self):            # Test OpenAPI documentation
        response = self.client.get("/openapi.json")

        assert response.status_code                      == 200
        openapi_spec = response.json()

        paths = openapi_spec.get("paths", {})
        assert "/html/to/dict/hashes" in paths
        assert "/html/to/text/hashes" in paths

        assert "post" in paths["/html/to/dict/hashes"]
        assert "post" in paths["/html/to/text/hashes"]

    def test__openapi_docs__correct_tags(self):                  # Test endpoint tags
        response = self.client.get("/openapi.json")
        openapi_spec = response.json()

        paths = openapi_spec["paths"]
        dict_hashes_endpoint = paths["/html/to/dict/hashes"]["post"]
        text_hashes_endpoint = paths["/html/to/text/hashes"]["post"]

        assert "html" in dict_hashes_endpoint.get("tags", [])
        assert "html" in text_hashes_endpoint.get("tags", [])

    def test__openapi_docs__request_schemas_defined(self):       # Test request schemas
        response = self.client.get("/openapi.json")
        openapi_spec = response.json()

        components = openapi_spec.get("components", {})
        schemas    = components.get("schemas", {})

        assert list_set(schemas) == [ 'HTTPValidationError',
                                      'Schema__Dict__To__Html__Request__BaseModel',
                                      'Schema__Dict__To__Text__Nodes__Request__BaseModel',
                                      'Schema__Dict__To__Tree_View__Request__BaseModel',
                                      'Schema__Hashes__To__Html__Request__BaseModel',
                                      'Schema__Html__To__Dict__Hashes__Request__BaseModel',
                                      'Schema__Html__To__Dict__Request__BaseModel',
                                      'Schema__Html__To__Html__Hashes__Request__BaseModel',
                                      'Schema__Html__To__Html__Request__BaseModel',
                                      'Schema__Html__To__Html__Xxx__Request__BaseModel',
                                      'Schema__Html__To__Text__Hashes__Request__BaseModel',
                                      'Schema__Html__To__Text__Nodes__Request__BaseModel',
                                      'Schema__Html__To__Tree_View__Request__BaseModel',
                                      'Schema__Set_Cookie__BaseModel',                              # BUG! Where are the response classes, like the "Schema__Html__To__Dict__Hashes__Response" + "__BaseModel"
                                      'ValidationError']
        assert "Schema__Html__To__Dict__Hashes__Request" + "__BaseModel" in schemas         # we need to add the __BaseModel, since these are the autogenerated classes
        assert "Schema__Html__To__Text__Hashes__Request" + "__BaseModel" in schemas

    def test__bug__openapi_docs__response_schemas_defined(self):      # Test response schemas
        response = self.client.get("/openapi.json")
        openapi_spec = response.json()

        components = openapi_spec.get("components", {})
        schemas    = components.get("schemas", {})

        assert "Schema__Html__To__Dict__Hashes__Response" + "__BaseModel" not in schemas            # BUG: current version of Fast_API (v0.29.0) is not returning the schema for the response objects
        assert "Schema__Html__To__Text__Hashes__Response" + "__BaseModel" not in schemas            # BUG: current version of Fast_API (v0.29.0) is not returning the schema for the response objects

    def test__existing_endpoints__still_work(self):              # Test existing endpoints not broken
        response = self.client.post("/html/to/dict", json={"html": "<p>Test</p>"})
        assert response.status_code                      == 200

        response = self.client.post("/html/to/html", json={"html": "<p>Test</p>"})
        assert response.status_code                      == 200

        response = self.client.post("/html/to/text/nodes", json={"html": "<p>Test</p>"})
        assert response.status_code                      == 200

        response = self.client.post("/html/to/tree/view", json={"html": "<p>Test</p>"})
        assert response.status_code                      == 200

    def test__performance__dict__hashes__reasonable_time(self):  # Test performance
        items = "".join([f"<li>Item {i}</li>" for i in range(100)])
        html  = f"<ul>{items}</ul>"
        payload = {"html": html}

        import time
        start    = time.time()
        response = self.client.post("/html/to/dict/hashes", json=payload)
        elapsed  = time.time() - start

        assert response.status_code                      == 200
        assert elapsed                                   <  5.0  # Within 5 seconds

    def test__performance__text__hashes__faster_than_dict__hashes(self): # Test lightweight speed
        items = "".join([f"<li>Item {i}</li>" for i in range(50)])
        html  = f"<ul>{items}</ul>"
        payload = {"html": html}

        import time

        start       = time.time()
        self.client.post("/html/to/dict/hashes", json=payload)
        dict_elapsed = time.time() - start

        start       = time.time()
        self.client.post("/html/to/text/hashes", json=payload)
        text_elapsed = time.time() - start

        assert text_elapsed                              <  dict_elapsed * 1.5

    def test__error__invalid_html_type(self):                    # Test invalid HTML type
        payload = { "html": 12345 }

        response = self.client.post("/html/to/dict/hashes", json=payload)

        assert response.status_code                      == 400  # Validation error
        assert response.json()  == {'detail': [{ 'input': 12345,
                                                 'loc': ['body', 'html'],
                                                 'msg': 'Input should be a valid string',
                                                 'type': 'string_type'}]}

    def test__error__negative_max_depth(self):                   # Test negative max_depth
        payload = { "html"      : "<p>Test</p>",
                    "max_depth" : -1 }

        error_message = "Safe_UInt must be >= 0, got -1"
        with pytest.raises(ValueError, match=re.escape(error_message)):
            self.client.post("/html/to/dict/hashes", json=payload)


    def test__error__extremely_large_max_depth(self):            # Test large max_depth value
        payload = { "html"      : "<p>Test</p>",
                    "max_depth" : 999999       }

        response = self.client.post("/html/to/dict/hashes", json=payload)

        assert response.status_code         == 200  #                            Should still work
        data = response.json()
        assert data["max_depth_reached"]    == False
        assert data                         == { 'html_dict'           : { 'attrs' : {}                                         ,
                                                                           'nodes' : [ { 'data': '0cbc6611f5', 'type': 'TEXT' } ],
                                                                           'tag'   : 'p'                                         } ,
                                                 'max_depth'           : 1                                                       ,
                                                 'max_depth_reached'   : False                                                  ,
                                                 'node_count'          : 2                                                       ,
                                                 'text_hashes_mapping' : { '0cbc6611f5': 'Test' }                                ,
                                                 'total_text_hashes'   : 1                                                       }
