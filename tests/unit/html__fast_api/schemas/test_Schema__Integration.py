from unittest                                                                   import TestCase
from mgraph_ai_service_html.html__fast_api.schemas.Schema__Html__Requests      import (
    Schema__Html__To__Dict__Request, Schema__Html__To__Dict__Response,
    Schema__Html__To__Text__Nodes__Request, Schema__Dict__To__Text__Nodes__Request,
    Schema__Dict__To__Text__Nodes__Response, Schema__Hashes__To__Html__Request
)


class test_Schema__Integration(TestCase):                       # Integration tests across schemas
    
    def test__request_response_chain(self):                      # Test typical request/response flow
        request = Schema__Html__To__Dict__Request(html="<p>Test</p>")
        
        response = Schema__Html__To__Dict__Response(
            html_dict  = {'tag': 'p', 'data': 'Test'},
            node_count = 1                            ,
            max_depth  = 1
        )
        
        assert request.html              == "<p>Test</p>"
        assert response.html_dict['tag'] == 'p'
    
    def test__text_extraction_workflow(self):                    # Test text extraction workflow
        request = Schema__Html__To__Text__Nodes__Request(
            html      = "<div><p>Hello</p></div>",
            max_depth = 256
        )
        
        response = Schema__Dict__To__Text__Nodes__Response(
            text_nodes = {
                'hash123': {'text': 'Hello', 'tag': 'p'}
            }                       ,
            total_nodes       = 1   ,
            max_depth_reached = False
        )
        
        assert request.html         == "<div><p>Hello</p></div>"
        assert response.total_nodes == 1
        assert 'hash123'            in response.text_nodes
    
    def test__hash_reconstruction_workflow(self):                # Test hash reconstruction
        dict_request = Schema__Dict__To__Text__Nodes__Request(
            html_dict = {'tag': 'p'},
            max_depth = 256
        )
        
        hash_request = Schema__Hashes__To__Html__Request(
            html_dict    = {'tag': 'p', 'data': 'HASH_ABC'},
            hash_mapping = {'HASH_ABC': 'Final Text'}
        )
        
        assert dict_request.html_dict['tag']        == 'p'
        assert hash_request.hash_mapping['HASH_ABC'] == 'Final Text'
