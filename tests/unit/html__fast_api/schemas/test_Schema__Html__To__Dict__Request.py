from unittest                                                                           import TestCase
from osbot_utils.utils.Objects                                                          import base_classes
from osbot_utils.type_safe.Type_Safe                                                    import Type_Safe
from osbot_utils.testing.__                                                             import __
from mgraph_ai_service_html.html__fast_api.schemas.html.Schema__Html__To__Dict__Request import Schema__Html__To__Dict__Request


class test_Schema__Html__To__Dict__Request(TestCase):
    
    def test__init__(self):                                      # Test auto-initialization
        with Schema__Html__To__Dict__Request() as _:
            assert type(_)         is Schema__Html__To__Dict__Request
            assert base_classes(_) == [Type_Safe, object]
            assert _.obj()         == __(html='')                # Empty string default
    
    def test__with_html_content(self):                           # Test with HTML content
        html = "<html><body><p>Test</p></body></html>"
        
        with Schema__Html__To__Dict__Request(html=html) as _:
            assert _.html  == html
            assert _.obj() == __(html=html)
    
    def test__serialization_round_trip(self):                    # Test JSON round-trip
        html = "<html><body>Test</body></html>"
        
        with Schema__Html__To__Dict__Request(html=html) as original:
            json_data = original.json()
            
            with Schema__Html__To__Dict__Request.from_json(json_data) as restored:
                assert restored.obj() == original.obj()
