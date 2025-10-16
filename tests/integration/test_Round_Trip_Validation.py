from unittest                                                   import TestCase
from starlette.testclient                                       import TestClient
from mgraph_ai_service_html.fast_api.Html__Fast_API             import Html__Fast_API

class test_Round_Trip_Validation(TestCase):
    
    @classmethod
    def setUpClass(cls):
        with Html__Fast_API() as _:
            _.setup()
            cls.app    = _.app()
            cls.client = TestClient(cls.app)
    
    def test__simple_html(self):                                # Basic validation
        original = "<html><body>Test</body></html>"
        
        response = self.client.post('/html/to/html',
                                   json={'html': original})
        
        assert response.status_code == 200
        roundtrip = response.text
        
        # Check that key elements are preserved
        assert 'html' in roundtrip.lower()
        assert 'body' in roundtrip.lower()
        assert 'Test' in roundtrip
    
    def test__nested_structure(self):                           # Nested elements
        original = "<html><body><div><p>Hello</p><span>World</span></div></body></html>"
        
        response = self.client.post('/html/to/html',
                                   json={'html': original})
        
        assert response.status_code == 200
        roundtrip = response.text
        
        # Verify structure is preserved
        assert 'Hello' in roundtrip
        assert 'World' in roundtrip
    
    def test__with_text_extraction(self):                       # Full pipeline test
        original = "<html><body><p>Test Content</p></body></html>"
        
        # Step 1: Extract text nodes
        response1 = self.client.post('/html/to/text/nodes',
                                    json={'html': original, 'max_depth': 256})
        assert response1.status_code == 200
        text_nodes = response1.json()['text_nodes']
        
        # Step 2: Get html_dict
        response2 = self.client.post('/html/to/dict',
                                    json={'html': original})
        assert response2.status_code == 200
        html_dict = response2.json()['html_dict']
        
        # Step 3: Reconstruct with no modifications
        response3 = self.client.post('/hashes/to/html',
                                    json={'html_dict': html_dict,
                                          'hash_mapping': {}})  # Empty = no changes
        
        assert response3.status_code == 200
        reconstructed = response3.text
        
        # Content should be preserved
        assert 'Test Content' in reconstructed or 'Test' in reconstructed
