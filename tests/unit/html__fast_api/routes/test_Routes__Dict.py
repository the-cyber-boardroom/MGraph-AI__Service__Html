from unittest                                                       import TestCase
from fastapi.testclient                                             import TestClient
from mgraph_ai_service_html.html__fast_api.Html_Service__Fast_API   import Html_Service__Fast_API
from osbot_utils.helpers.html.transformers.Html__To__Html_Dict      import Html__To__Html_Dict


class test_Routes__Dict(TestCase):

    @classmethod
    def setUpClass(cls):                                         # ONE-TIME expensive setup
        with Html_Service__Fast_API() as api:
            api.setup()
            cls.app    = api.app()
            cls.client = TestClient(cls.app)

    def test__to__html(self):                                    # Test HTML reconstruction from dict
        html      = "<html><body><p>Test</p></body></html>"
        html_dict = Html__To__Html_Dict(html=html).convert()

        response = self.client.post('/dict/to/html',
                                   json={'html_dict': html_dict})

        assert response.status_code == 200
        reconstructed = response.text

        assert isinstance(reconstructed, str)
        assert '<p>Test</p>' in reconstructed

    def test__to__html__complex_structure(self):                 # Test with nested structure
        html = """
        <html>
            <body>
                <div>
                    <h1>Title</h1>
                    <p>First paragraph</p>
                    <p>Second paragraph</p>
                </div>
            </body>
        </html>
        """
        html_dict = Html__To__Html_Dict(html=html).convert()

        response = self.client.post('/dict/to/html',
                                   json={'html_dict': html_dict})

        assert response.status_code == 200
        reconstructed = response.text

        assert 'Title'           in reconstructed
        assert 'First paragraph' in reconstructed
        assert 'Second paragraph' in reconstructed

    def test__to__html__with_attributes(self):                   # Test attribute preservation
        html = '<html><body><div class="container" id="main"><p>Content</p></div></body></html>'
        html_dict = Html__To__Html_Dict(html=html).convert()

        response = self.client.post('/dict/to/html',
                                   json={'html_dict': html_dict})

        assert response.status_code == 200
        reconstructed = response.text

        assert 'Content' in reconstructed
        assert 'class' in reconstructed or 'id' in reconstructed  # Attributes preserved

    def test__to__text__nodes(self):                             # Test text node extraction from dict
        html = "<html><body><p>Hello</p><span>World</span></body></html>"
        html_dict = Html__To__Html_Dict(html=html).convert()

        response = self.client.post('/dict/to/text/nodes',
                                   json={'html_dict': html_dict})

        assert response.status_code == 200
        result = response.json()

        assert 'text_nodes'        in result
        assert 'total_nodes'       in result
        assert 'max_depth_reached' in result
        assert result['total_nodes'] == 2                        # "Hello" and "World"

        text_nodes = result['text_nodes']
        for hash_value, node_data in text_nodes.items():
            assert 'text' in node_data
            assert 'tag'  in node_data
            assert len(hash_value) == 10                         # Default hash size

    def test__to__text__nodes__with_max_depth(self):             # Test max_depth parameter
        html = """
        <div>
            <div>
                <div>
                    <p>Deep Text</p>
                </div>
            </div>
        </div>
        """
        html_dict = Html__To__Html_Dict(html=html).convert()

        response_deep = self.client.post('/dict/to/text/nodes',
                                        json={'html_dict': html_dict, 'max_depth': 256})

        response_shallow = self.client.post('/dict/to/text/nodes',
                                           json={'html_dict': html_dict, 'max_depth': 2})

        assert response_deep.status_code    == 200
        assert response_shallow.status_code == 200

        result_deep    = response_deep.json()
        result_shallow = response_shallow.json()

        assert result_deep['total_nodes']    == 1                # Should capture deep text
        assert result_shallow['total_nodes'] == 0                # Should NOT capture

    def test__to__text__nodes__multiple_text_nodes(self):        # Test multiple text extractions
        html = """
        <html>
            <body>
                <h1>Heading</h1>
                <p>Paragraph 1</p>
                <p>Paragraph 2</p>
                <div>
                    <span>Span text</span>
                    <a href="#">Link text</a>
                </div>
            </body>
        </html>
        """
        html_dict = Html__To__Html_Dict(html=html).convert()

        response = self.client.post('/dict/to/text/nodes',
                                   json={'html_dict': html_dict})

        assert response.status_code == 200
        result = response.json()

        assert result['total_nodes'] == 5                        # 5 text nodes

        all_text = ' '.join(node['text'] for node in result['text_nodes'].values())
        assert 'Heading'     in all_text
        assert 'Paragraph 1' in all_text
        assert 'Paragraph 2' in all_text
        assert 'Span text'   in all_text
        assert 'Link text'   in all_text

    def test__to__lines(self):                                   # Test line formatting from dict
        html      = "<html><body><p>Test</p></body></html>"
        html_dict = Html__To__Html_Dict(html=html).convert()

        response = self.client.post('/dict/to/lines',
                                   json={'html_dict': html_dict})

        assert response.status_code == 200
        lines = response.text

        assert isinstance(lines, str)
        assert 'html' in lines
        assert 'body' in lines
        assert 'p'    in lines
        assert '\n'   in lines                                   # Should have line breaks

    def test__to__lines__nested_structure(self):                 # Test with complex HTML
        html = """
        <html>
            <body>
                <div>
                    <ul>
                        <li>Item 1</li>
                        <li>Item 2</li>
                    </ul>
                </div>
            </body>
        </html>
        """
        html_dict = Html__To__Html_Dict(html=html).convert()

        response = self.client.post('/dict/to/lines',
                                   json={'html_dict': html_dict})

        assert response.status_code == 200
        lines = response.text

        assert 'ul' in lines
        assert 'li' in lines

    def test__round_trip__dict_to_html_to_dict(self):            # Test round-trip consistency
        original_html = "<html><body><p>Test</p></body></html>"
        html_dict_1   = Html__To__Html_Dict(html=original_html).convert()

        response = self.client.post('/dict/to/html',             # Dict → HTML
                                   json={'html_dict': html_dict_1})

        assert response.status_code == 200
        reconstructed_html = response.text

        html_dict_2 = Html__To__Html_Dict(html=reconstructed_html).convert()  # HTML → Dict

        assert html_dict_1.get('tag') == html_dict_2.get('tag')  # Structure preserved

    def test__workflow__caching_scenario(self):                  # Test typical caching workflow
        original_html = "<html><body><p>Content</p></body></html>"

        html_dict = Html__To__Html_Dict(html=original_html).convert()  # Step 1: Parse (cacheable)

        response1 = self.client.post('/dict/to/html',            # Step 2: Reconstruct
                                    json={'html_dict': html_dict})

        response2 = self.client.post('/dict/to/text/nodes',      # Step 3: Extract text
                                    json={'html_dict': html_dict})

        response3 = self.client.post('/dict/to/lines',           # Step 4: Format
                                    json={'html_dict': html_dict})

        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response3.status_code == 200

        assert 'Content' in response1.text
        assert response2.json()['total_nodes'] == 1
        assert 'p' in response3.text

    def test__error_handling__empty_dict(self):                  # Test with empty dict
        response = self.client.post('/dict/to/html',
                                   json={'html_dict': {}})

        assert response.status_code == 200                       # Should handle gracefully

    def test__error_handling__missing_html_dict(self):           # Test missing required field
        response = self.client.post('/dict/to/html',
                                   json={})

        assert response.status_code == 422                       # Validation error

    def test__error_handling__invalid_dict_structure(self):      # Test with malformed dict
        invalid_dict = {'invalid': 'structure'}

        response = self.client.post('/dict/to/html',
                                   json={'html_dict': invalid_dict})

        assert response.status_code == 200                       # Should handle gracefully

    def test__comparison__atomic_vs_compound(self):              # Compare atomic vs compound operations
        html = "<html><body><p>Test</p></body></html>"

        response_compound = self.client.post('/html/to/text/nodes',  # Compound: direct
                                            json={'html': html})

        html_dict = Html__To__Html_Dict(html=html).convert()     # Atomic: two-step
        response_atomic = self.client.post('/dict/to/text/nodes',
                                          json={'html_dict': html_dict})

        assert response_compound.status_code == 200
        assert response_atomic.status_code   == 200

        result_compound = response_compound.json()
        result_atomic   = response_atomic.json()

        assert result_compound['total_nodes'] == result_atomic['total_nodes']  # Same result

    def test__performance__large_dict(self):                     # Test with large dict
        html_parts = ["<html><body>"]
        for i in range(50):
            html_parts.append(f"<p>Paragraph {i}</p>")
        html_parts.append("</body></html>")
        html = "".join(html_parts)

        html_dict = Html__To__Html_Dict(html=html).convert()

        response = self.client.post('/dict/to/html',
                                   json={'html_dict': html_dict})

        assert response.status_code == 200
        reconstructed = response.text

        assert 'Paragraph 0'  in reconstructed
        assert 'Paragraph 49' in reconstructed

    def test__text_extraction__filters_script_style(self):       # Test script/style filtering
        html = """
        <html>
            <head>
                <style>body { color: blue; }</style>
                <script>console.log('test');</script>
            </head>
            <body>
                <p>Visible Content</p>
            </body>
        </html>
        """
        html_dict = Html__To__Html_Dict(html=html).convert()

        response = self.client.post('/dict/to/text/nodes',
                                   json={'html_dict': html_dict})

        assert response.status_code == 200
        result = response.json()

        all_text = ' '.join(node['text'] for node in result['text_nodes'].values())
        assert 'Visible Content' in all_text                     # Should capture
        assert 'console.log'     not in all_text                 # Should NOT capture script
        assert 'color: blue'     not in all_text                 # Should NOT capture style