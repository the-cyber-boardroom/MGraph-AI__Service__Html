from unittest                                                                   import TestCase
from osbot_utils.utils.Objects                                                  import base_classes
from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from osbot_utils.testing.__                                                     import __
from mgraph_ai_service_html.html__fast_api.schemas.Schema__Html__Requests      import Schema__Dict__To__Text__Nodes__Response


class test_Schema__Dict__To__Text__Nodes__Response(TestCase):
    
    def test__init__(self):                                      # Test auto-initialization
        with Schema__Dict__To__Text__Nodes__Response() as _:
            assert type(_)         is Schema__Dict__To__Text__Nodes__Response
            assert base_classes(_) == [Type_Safe, object]
            assert _.obj()         == __(text_nodes        = {}   ,
                                         total_nodes       = 0    ,
                                         max_depth_reached = False)
    
    def test__with_text_nodes(self):                             # Test with text node data
        text_nodes = {
            'hash123': {'text': 'Hello', 'tag': 'p'},
            'hash456': {'text': 'World', 'tag': 'div'}
        }
        
        with Schema__Dict__To__Text__Nodes__Response(text_nodes        = text_nodes,
                                                     total_nodes       = 2        ,
                                                     max_depth_reached = False    ) as _:
            assert _.text_nodes        == text_nodes
            assert _.total_nodes       == 2
            assert _.max_depth_reached is False
            
            assert _.obj() == __(text_nodes        = text_nodes,
                                 total_nodes       = 2         ,
                                 max_depth_reached = False     )
    
    def test__with_max_depth_reached(self):                      # Test max_depth_reached flag
        with Schema__Dict__To__Text__Nodes__Response(text_nodes        = {}  ,
                                                     total_nodes       = 0   ,
                                                     max_depth_reached = True) as _:
            assert _.max_depth_reached is True
