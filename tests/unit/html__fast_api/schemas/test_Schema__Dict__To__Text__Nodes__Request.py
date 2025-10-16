from unittest                                                                   import TestCase
from osbot_utils.utils.Objects                                                  import base_classes
from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from osbot_utils.testing.__                                                     import __
from mgraph_ai_service_html.html__fast_api.schemas.Schema__Html__Requests      import Schema__Dict__To__Text__Nodes__Request


class test_Schema__Dict__To__Text__Nodes__Request(TestCase):
    
    def test__init__(self):                                      # Test auto-initialization with defaults
        with Schema__Dict__To__Text__Nodes__Request() as _:
            assert type(_)         is Schema__Dict__To__Text__Nodes__Request
            assert base_classes(_) == [Type_Safe, object]
            assert _.obj()         == __(html_dict = {}  ,
                                         max_depth = 256 )       # Default max_depth
    
    def test__with_custom_max_depth(self):                       # Test custom max_depth
        html_dict = {'tag': 'div'}
        max_depth = 50
        
        with Schema__Dict__To__Text__Nodes__Request(html_dict = html_dict,
                                                    max_depth = max_depth) as _:
            assert _.html_dict == html_dict
            assert _.max_depth == max_depth
            assert _.obj()     == __(html_dict = html_dict,
                                     max_depth = max_depth)
