from unittest                                                                            import TestCase
from osbot_utils.utils.Objects                                                           import base_classes
from osbot_utils.type_safe.Type_Safe                                                     import Type_Safe
from osbot_utils.testing.__                                                              import __
from mgraph_ai_service_html.html__fast_api.schemas.html.Schema__Html__To__Dict__Response import Schema__Html__To__Dict__Response


class test_Schema__Html__To__Dict__Response(TestCase):
    
    def test__init__(self):                                      # Test auto-initialization
        with Schema__Html__To__Dict__Response() as _:
            assert type(_)         is Schema__Html__To__Dict__Response
            assert base_classes(_) == [Type_Safe, object]
            assert _.obj()         == __(html_dict = __() ,
                                         node_count = 0   ,
                                         max_depth  = 0   )
    
    def test__with_data(self):                                   # Test with actual data
        html_dict  = {'tag': 'html', 'nodes': []}
        node_count = 5
        max_depth  = 3
        
        with Schema__Html__To__Dict__Response(html_dict  = html_dict ,
                                              node_count = node_count,
                                              max_depth  = max_depth ) as _:
            assert _.html_dict  == html_dict
            assert _.node_count == node_count
            assert _.max_depth  == max_depth
            
            assert _.obj() == __(html_dict=__(tag  =  'html',
                                              nodes = []   ),
                                 node_count=5,
                                 max_depth=3)
    
    def test__serialization_round_trip(self):                    # Test JSON round-trip
        html_dict = {'tag': 'p', 'data': 'test'}
        
        with Schema__Html__To__Dict__Response(html_dict  = html_dict,
                                              node_count = 10     ,
                                              max_depth  = 5      ) as original:
            json_data = original.json()
            
            with Schema__Html__To__Dict__Response.from_json(json_data) as restored:
                assert restored.obj() == original.obj()
