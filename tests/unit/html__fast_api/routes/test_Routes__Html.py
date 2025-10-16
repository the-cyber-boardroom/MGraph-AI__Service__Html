from unittest                                                                 import TestCase
from fastapi.testclient                                                       import TestClient
from mgraph_ai_service_html.html__fast_api.Html__Fast_API                     import Html__Fast_API


class test_Routes__Html(TestCase):                               # Test HTML transformation routes
    
    @classmethod
    def setUpClass(cls):
        with Html__Fast_API() as api:
            api.setup()
            cls.app    = api.app()
            cls.client = TestClient(cls.app)
    
    def test__to__dict(self):                                    # Test atomic parsing
        html = "<html><body><p>Test</p></body></html>"
        
        response = self.client.post('/html/to/dict', 
                                   json={'html': html})
        
        assert response.status_code == 200
        result = response.json()
        
        assert 'html_dict'  in result
        assert 'node_count' in result
        assert result['node_count'] > 0
    
    def test__to__html(self):                                    # Test round-trip
        html = "<html><body><p>Test</p></body></html>"
        
        response = self.client.post('/html/to/html',
                                   json={'html': html})
        
        assert response.status_code == 200
        reconstructed = response.text
        
        assert '<p>Test</p>' in reconstructed                    # Should contain original content
    
    def test__to__text__nodes(self):                             # Test extraction
        html = "<html><body><p>Hello</p><span>World</span></body></html>"
        
        response = self.client.post('/html/to/text/nodes',
                                   json={'html': html})
        
        assert response.status_code == 200
        result = response.json()
        
        assert 'text_nodes'  in result
        assert 'total_nodes' in result
        assert result['total_nodes'] == 2                        # "Hello" and "World"
        
        text_nodes = result['text_nodes']                        # Verify hash structure
        for hash_value, node_data in text_nodes.items():
            assert 'original_text' in node_data
            assert 'tag'           in node_data
            assert len(hash_value) == 10                         # Default hash size
    
    def test__to__html__hashes(self):                            # Test hash replacement
        html = "<html><body><p>Test Content</p></body></html>"
        
        response = self.client.post('/html/to/html/hashes',
                                   json={'html': html})
        
        assert response.status_code == 200
        html_with_hashes = response.text
        
        assert 'Test Content' not in html_with_hashes            # Original text replaced
        assert '<p>' in html_with_hashes                         # Structure preserved
    
    def test__to__html__xxx(self):                               # Test xxx masking
        html = "<html><body><p>Secret Text</p></body></html>"
        
        response = self.client.post('/html/to/html/xxx',
                                   json={'html': html})
        
        assert response.status_code == 200
        html_with_xxx = response.text
        
        assert 'Secret Text' not in html_with_xxx                # Original text hidden
        assert 'xxxxxx' in html_with_xxx                         # Replaced with x's
        assert '<p>' in html_with_xxx                            # Structure preserved
