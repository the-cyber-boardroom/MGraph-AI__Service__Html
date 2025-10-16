from unittest                                                                   import TestCase
from osbot_utils.utils.Objects                                                  import base_classes
from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from osbot_utils.testing.__                                                     import __
from mgraph_ai_service_html.html__fast_api.schemas.Schema__Html__Requests      import Schema__Hashes__To__Html__Request


class test_Schema__Hashes__To__Html__Request(TestCase):
    
    def test__init__(self):                                      # Test auto-initialization
        with Schema__Hashes__To__Html__Request() as _:
            assert type(_)         is Schema__Hashes__To__Html__Request
            assert base_classes(_) == [Type_Safe, object]
            assert _.obj()         == __(html_dict    = {}      ,
                                         hash_mapping = {}      )
    
    def test__with_data(self):                                   # Test with mapping data
        html_dict    = {'tag': 'p', 'data': 'HASH_123'}
        hash_mapping = {'HASH_123': 'Replaced Text'}
        
        with Schema__Hashes__To__Html__Request(html_dict    = html_dict   ,
                                               hash_mapping = hash_mapping) as _:
            assert _.html_dict    == html_dict
            assert _.hash_mapping == hash_mapping
            
            assert _.obj() == __(html_dict    = html_dict   ,
                                 hash_mapping = hash_mapping)
    
    def test__with_multiple_mappings(self):                      # Test multiple hash replacements
        html_dict = {'tag': 'div'}
        hash_mapping = {
            'HASH_A': 'Text A',
            'HASH_B': 'Text B',
            'HASH_C': 'Text C'
        }
        
        with Schema__Hashes__To__Html__Request(html_dict    = html_dict   ,
                                               hash_mapping = hash_mapping) as _:
            assert len(_.hash_mapping) == 3
            assert _.hash_mapping['HASH_A'] == 'Text A'
            assert _.hash_mapping['HASH_B'] == 'Text B'
            assert _.hash_mapping['HASH_C'] == 'Text C'
    
    def test__serialization_round_trip(self):                    # Test JSON round-trip
        html_dict    = {'tag': 'span', 'data': 'HASH_XYZ'}
        hash_mapping = {'HASH_XYZ': 'New Content'}
        
        with Schema__Hashes__To__Html__Request(html_dict    = html_dict   ,
                                               hash_mapping = hash_mapping) as original:
            json_data = original.json()
            
            with Schema__Hashes__To__Html__Request.from_json(json_data) as restored:
                assert restored.obj() == original.obj()
