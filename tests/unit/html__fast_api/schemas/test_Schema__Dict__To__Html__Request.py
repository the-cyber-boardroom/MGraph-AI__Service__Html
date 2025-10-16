from unittest                                                                           import TestCase
from osbot_utils.utils.Objects                                                          import base_classes
from osbot_utils.type_safe.Type_Safe                                                    import Type_Safe
from osbot_utils.testing.__                                                             import __
from mgraph_ai_service_html.html__fast_api.schemas.dict.Schema__Dict__To__Html__Request import Schema__Dict__To__Html__Request


class test_Schema__Dict__To__Html__Request(TestCase):
    
    def test__init__(self):                                      # Test auto-initialization
        with Schema__Dict__To__Html__Request() as _:
            assert type(_)         is Schema__Dict__To__Html__Request
            assert base_classes(_) == [Type_Safe, object]
            assert _.obj()         == __(html_dict=__())
    
    def test__with_html_dict(self):                              # Test with dict data
        html_dict = {'tag': 'html', 'nodes': [{'tag': 'body'}]}
        
        with Schema__Dict__To__Html__Request(html_dict=html_dict) as _:
            assert _.html_dict == html_dict
            assert _.obj()     == __(html_dict=__(tag='html', nodes=[__(tag='body')]))
