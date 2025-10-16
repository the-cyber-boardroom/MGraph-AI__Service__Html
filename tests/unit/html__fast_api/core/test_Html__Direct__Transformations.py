from unittest                                                                          import TestCase
from mgraph_ai_service_html.html__fast_api.core.Html__Direct__Transformations          import Html__Direct__Transformations


class test_Html__Direct__Transformations(TestCase):             # Test direct HTML transformations
    
    @classmethod
    def setUpClass(cls):
        cls.transformations = Html__Direct__Transformations()
    
    def test__html__to__html_dict(self):                         # Test HTML parsing
        html = "<html><body><p>Test</p></body></html>"
        
        html_dict = self.transformations.html__to__html_dict(html)
        
        assert isinstance(html_dict, dict)
        assert 'tag' in html_dict
        assert html_dict['tag'] == 'html'
    
    def test__html_dict__to__html(self):                         # Test HTML reconstruction
        html      = "<html><body><p>Test</p></body></html>"
        html_dict = self.transformations.html__to__html_dict(html)
        
        reconstructed = self.transformations.html_dict__to__html(html_dict)
        
        assert isinstance(reconstructed, str)
        assert '<p>Test</p>' in reconstructed
    
    def test__html__to__lines(self):                             # Test line formatting
        html = "<html><body><p>Test</p></body></html>"
        
        lines = self.transformations.html__to__lines(html)
        
        assert isinstance(lines, str)
        assert 'html' in lines
        assert 'body' in lines
        assert 'p' in lines
    
    def test__html_dict__to__text_nodes(self):                   # Test text node extraction
        html      = "<html><body><p>Hello</p><span>World</span></body></html>"
        html_dict = self.transformations.html__to__html_dict(html)
        
        text_nodes = self.transformations.html_dict__to__text_nodes(html_dict)
        
        assert isinstance(text_nodes, dict)
        assert len(text_nodes) == 2                              # "Hello" and "World"
        
        for hash_value, node_data in text_nodes.items():         # Verify structure
            assert 'original_text' in node_data
            assert 'tag'           in node_data
