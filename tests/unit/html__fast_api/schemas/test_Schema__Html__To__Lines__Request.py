from unittest                                                                            import TestCase
from osbot_utils.utils.Objects                                                           import base_classes
from osbot_utils.type_safe.Type_Safe                                                     import Type_Safe
from osbot_utils.testing.__                                                              import __
from mgraph_ai_service_html.html__fast_api.schemas.html.Schema__Html__To__Lines__Request import Schema__Html__To__Lines__Request


class test_Schema__Html__To__Lines__Request(TestCase):
    
    def test__init__(self):                                      # Test auto-initialization
        with Schema__Html__To__Lines__Request() as _:
            assert type(_)         is Schema__Html__To__Lines__Request
            assert base_classes(_) == [Type_Safe, object]
            assert _.obj()         == __(html='')
    
    def test__with_html(self):                                   # Test with HTML content
        html = "<div><p>Line formatting</p></div>"
        
        with Schema__Html__To__Lines__Request(html=html) as _:
            assert _.html  == html
            assert _.obj() == __(html=html)
