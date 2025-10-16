from unittest                                                                   import TestCase
from osbot_utils.utils.Objects                                                  import base_classes
from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from osbot_utils.testing.__                                                     import __
from mgraph_ai_service_html.html__fast_api.schemas.Schema__Html__Requests      import Schema__Html__To__Html__Xxx__Request


class test_Schema__Html__To__Html__Xxx__Request(TestCase):
    
    def test__init__(self):                                      # Test auto-initialization
        with Schema__Html__To__Html__Xxx__Request() as _:
            assert type(_)         is Schema__Html__To__Html__Xxx__Request
            assert base_classes(_) == [Type_Safe, object]
            assert _.obj()         == __(html      = ''  ,
                                         max_depth = 256 )
    
    def test__with_html_and_depth(self):                         # Test with values
        html      = "<p>Text to mask</p>"
        max_depth = 64
        
        with Schema__Html__To__Html__Xxx__Request(html      = html     ,
                                                  max_depth = max_depth) as _:
            assert _.html      == html
            assert _.max_depth == max_depth
