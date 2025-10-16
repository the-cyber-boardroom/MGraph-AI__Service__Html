from unittest                                                                               import TestCase
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash          import Safe_Str__Hash
from osbot_utils.utils.Objects                                                              import base_classes
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.testing.__                                                                 import __
from mgraph_ai_service_html.html__fast_api.schemas.hashes.Schema__Hashes__To__Html__Request import Schema__Hashes__To__Html__Request


class test_Schema__Hashes__To__Html__Request(TestCase):
    
    def test__init__(self):                                      # Test auto-initialization
        with Schema__Hashes__To__Html__Request() as _:
            assert type(_)         is Schema__Hashes__To__Html__Request
            assert base_classes(_) == [Type_Safe, object]
            assert _.obj()         == __(html_dict    = __()      ,
                                         hash_mapping = __()      )
    
    def test__with_data(self):                                   # Test with mapping data
        html_dict    = {'tag': 'p', 'data': 'abcd123456'}
        hash_mapping = {'abcd123456': 'Replaced Text'}
        
        with Schema__Hashes__To__Html__Request(html_dict    = html_dict   ,
                                               hash_mapping = hash_mapping) as _:
            assert _.html_dict    == html_dict
            assert _.hash_mapping == {Safe_Str__Hash('abcd123456'): 'Replaced Text'}
            
            assert _.obj() == __(html_dict=__(tag='p', data='abcd123456'),
                                 hash_mapping=__(abcd123456='Replaced Text'))
    
    def test__with_multiple_mappings(self):                      # Test multiple hash replacements
        html_dict = {'tag': 'div'}
        hash_mapping = {'1abcd12345': 'Text A',
                        '2abcd12345': 'Text B',
                        '3abcd12345': 'Text C'}
        
        with Schema__Hashes__To__Html__Request(html_dict    = html_dict   ,
                                               hash_mapping = hash_mapping) as _:
            assert len(_.hash_mapping) == 3
            assert _.hash_mapping['1abcd12345'] == 'Text A'
            assert _.hash_mapping['2abcd12345'] == 'Text B'
            assert _.hash_mapping['3abcd12345'] == 'Text C'
    
    def test__serialization_round_trip(self):                    # Test JSON round-trip
        html_dict    = {'tag': 'span', 'data': 'abcd123456'}
        hash_mapping = {'abcd123456': 'New Content'}
        
        with Schema__Hashes__To__Html__Request(html_dict    = html_dict   ,
                                               hash_mapping = hash_mapping) as original:
            json_data = original.json()
            
            with Schema__Hashes__To__Html__Request.from_json(json_data) as restored:
                assert restored.obj() == original.obj()
