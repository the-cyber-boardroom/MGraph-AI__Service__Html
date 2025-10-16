from unittest                                                       import TestCase
from fastapi.testclient                                             import TestClient
from mgraph_ai_service_html.html__fast_api.Html_Service__Fast_API   import Html_Service__Fast_API


class test_Routes__Html(TestCase):

    @classmethod
    def setUpClass(cls):                                         # ONE-TIME expensive setup
        with Html_Service__Fast_API() as api:
            api.setup()
            cls.app    = api.app()
            cls.client = TestClient(cls.app)

    def test__to__dict(self):                                    # Test atomic HTML parsing
        html = "<html><body><p>Test Content</p></body></html>"

        response = self.client.post('/html/to/dict',
                                   json={'html': html})

        assert response.status_code == 200
        result = response.json()

        assert 'html_dict'  in result
        assert 'node_count' in result
        assert 'max_depth'  in result
        assert result['node_count'] > 0
        assert result['max_depth']  >= 0

        assert isinstance(result['html_dict'], dict)
        assert 'tag' in result['html_dict']

    def test__to__dict__empty_html(self):                        # Test with empty HTML
        html = ""

        response = self.client.post('/html/to/dict',
                                   json={'html': html})

        assert response.status_code == 200
        result = response.json()

        assert 'html_dict' in result

    def test__to__dict__complex_structure(self):                 # Test with complex nested HTML
        html = """
        <html>
            <head>
                <title>Test Page</title>
            </head>
            <body>
                <div class="container">
                    <h1>Title</h1>
                    <p>Paragraph 1</p>
                    <p>Paragraph 2</p>
                    <ul>
                        <li>Item 1</li>
                        <li>Item 2</li>
                    </ul>
                </div>
            </body>
        </html>
        """

        response = self.client.post('/html/to/dict',
                                   json={'html': html})

        assert response.status_code == 200
        result = response.json()

        assert result['node_count'] > 5                          # Multiple nodes
        assert result['max_depth']  > 2                          # Nested structure

    def test__to__html(self):                                    # Test round-trip validation
        html = "<html><body><p>Test</p></body></html>"

        response = self.client.post('/html/to/html',
                                   json={'html': html})

        assert response.status_code == 200
        reconstructed = response.text

        assert isinstance(reconstructed, str)
        assert '<p>Test</p>' in reconstructed
        assert 'html'        in reconstructed.lower()
        assert 'body'        in reconstructed.lower()

    def test__to__html__preserves_content(self):                 # Test content preservation
        html = """
        <html>
            <body>
                <h1>Main Heading</h1>
                <p>First paragraph with <strong>bold text</strong>.</p>
                <p>Second paragraph with <em>italic text</em>.</p>
            </body>
        </html>
        """

        response = self.client.post('/html/to/html',
                                   json={'html': html})

        assert response.status_code == 200
        reconstructed = response.text

        assert 'Main Heading'   in reconstructed
        assert 'First paragraph' in reconstructed
        assert 'Second paragraph' in reconstructed
        assert 'bold text'      in reconstructed
        assert 'italic text'    in reconstructed

    def test__to__text__nodes(self):                             # Test compound text extraction
        html = "<html><body><p>Hello</p><span>World</span></body></html>"

        response = self.client.post('/html/to/text/nodes',
                                   json={'html': html})

        assert response.status_code == 200
        result = response.json()

        assert 'text_nodes'        in result
        assert 'total_nodes'       in result
        assert 'max_depth_reached' in result
        assert result['total_nodes'] == 2                        # "Hello" and "World"

        text_nodes = result['text_nodes']
        assert isinstance(text_nodes, dict)

        for hash_value, node_data in text_nodes.items():         # Verify hash structure
            assert 'text' in node_data
            assert 'tag'  in node_data
            assert len(hash_value) == 10                         # Default hash size

    def test__to__text__nodes__with_custom_max_depth(self):      # Test max_depth parameter
        html = """
        <div>
            <div>
                <div>
                    <p>Deep Text</p>
                </div>
            </div>
        </div>
        """

        response_deep = self.client.post('/html/to/text/nodes',
                                        json={'html': html, 'max_depth': 256})

        response_shallow = self.client.post('/html/to/text/nodes',
                                           json={'html': html, 'max_depth': 2})

        assert response_deep.status_code    == 200
        assert response_shallow.status_code == 200

        result_deep    = response_deep.json()
        result_shallow = response_shallow.json()

        assert result_deep['total_nodes']    == 1                # Should capture deep text
        assert result_shallow['total_nodes'] == 0                # Should NOT capture

    def test__to__text__nodes__filters_script_style(self):       # Test script/style filtering
        html = """
        <html>
            <head>
                <style>body { color: red; }</style>
                <script>alert('test');</script>
            </head>
            <body>
                <p>Visible Text</p>
            </body>
        </html>
        """

        response = self.client.post('/html/to/text/nodes',
                                   json={'html': html})

        assert response.status_code == 200
        result = response.json()

        text_nodes = result['text_nodes']
        all_text = ' '.join(node['text'] for node in text_nodes.values())

        assert 'Visible Text' in all_text                        # Should capture visible
        assert 'alert'        not in all_text                    # Should NOT capture script
        assert 'color: red'   not in all_text                    # Should NOT capture style

    def test__to__lines(self):                                   # Test line formatting
        html = "<html><body><p>Test</p></body></html>"

        response = self.client.post('/html/to/lines',
                                   json={'html': html})

        assert response.status_code == 200
        lines = response.text

        assert isinstance(lines, str)
        assert 'html' in lines
        assert 'body' in lines
        assert 'p'    in lines
        assert '\n'   in lines                                   # Should have line breaks

    def test__to__lines__complex_structure(self):                # Test with nested HTML
        html = """
        <html>
            <body>
                <div>
                    <p>First</p>
                    <span>Second</span>
                </div>
            </body>
        </html>
        """

        response = self.client.post('/html/to/lines',
                                   json={'html': html})

        assert response.status_code == 200
        lines = response.text

        assert 'div'  in lines
        assert 'p'    in lines
        assert 'span' in lines

    def test__to__html__hashes(self):                            # Test hash replacement
        html = "<html><body><p>Test Content</p></body></html>"

        response = self.client.post('/html/to/html/hashes',
                                   json={'html': html})

        assert response.status_code == 200
        html_with_hashes = response.text

        assert 'Test Content' not in html_with_hashes            # Original text replaced
        assert '<p>'          in html_with_hashes                # Structure preserved
        assert '<body>'       in html_with_hashes or 'body' in html_with_hashes

    def test__to__html__hashes__multiple_text_nodes(self):       # Test multiple replacements
        html = """
        <html>
            <body>
                <p>First text</p>
                <div>Second text</div>
                <span>Third text</span>
            </body>
        </html>
        """

        response = self.client.post('/html/to/html/hashes',
                                   json={'html': html})

        assert response.status_code == 200
        html_with_hashes = response.text

        assert 'First text'  not in html_with_hashes             # All text replaced
        assert 'Second text' not in html_with_hashes
        assert 'Third text'  not in html_with_hashes
        assert '<p>'         in html_with_hashes                 # Structure preserved
        assert '<div>'       in html_with_hashes or 'div' in html_with_hashes

    def test__to__html__xxx(self):                               # Test xxx masking
        html = "<html><body><p>Secret Text</p></body></html>"

        response = self.client.post('/html/to/html/xxx',
                                   json={'html': html})

        assert response.status_code == 200
        html_with_xxx = response.text

        assert 'Secret Text' not in html_with_xxx                # Original text hidden
        assert 'xxxxxx'      in html_with_xxx                    # Replaced with x's
        assert '<p>'         in html_with_xxx                    # Structure preserved

    def test__to__html__xxx__preserves_spaces(self):             # Test space preservation
        html = "<html><body><p>Text With Spaces</p></body></html>"

        response = self.client.post('/html/to/html/xxx',
                                   json={'html': html})

        assert response.status_code == 200
        html_with_xxx = response.text

        assert 'Text With Spaces' not in html_with_xxx           # Original replaced

        import re
        xxx_pattern = re.search(r'xxxx xx xxxxxx', html_with_xxx)  # Pattern with spaces
        assert xxx_pattern is not None                           # Spaces preserved

    def test__to__html__xxx__multiple_paragraphs(self):          # Test multiple text nodes
        html = """
        <html>
            <body>
                <p>First paragraph here.</p>
                <p>Second paragraph here.</p>
            </body>
        </html>
        """

        response = self.client.post('/html/to/html/xxx',
                                   json={'html': html})

        assert response.status_code == 200
        html_with_xxx = response.text

        assert 'First paragraph'  not in html_with_xxx           # All text replaced
        assert 'Second paragraph' not in html_with_xxx
        assert 'xxx'              in html_with_xxx               # Has replacements

    def test__round_trip__simple(self):                          # Test complete round-trip
        original = "<html><body><p>Test</p></body></html>"

        response = self.client.post('/html/to/html',
                                   json={'html': original})

        assert response.status_code == 200
        roundtrip = response.text

        assert '<p>Test</p>' in roundtrip

    def test__round_trip__with_attributes(self):                 # Test attribute preservation
        original = '<html><body><p class="test" id="para">Content</p></body></html>'

        response = self.client.post('/html/to/html',
                                   json={'html': original})

        assert response.status_code == 200
        roundtrip = response.text

        assert 'Content' in roundtrip
        assert 'class' in roundtrip or 'id' in roundtrip         # At least one attribute

    def test__integration__dict_then_text_nodes(self):           # Test workflow: dict → text nodes
        html = "<html><body><p>Test</p></body></html>"

        response1 = self.client.post('/html/to/dict',            # Step 1: Get dict
                                    json={'html': html})

        assert response1.status_code == 200
        html_dict = response1.json()['html_dict']

        response2 = self.client.post('/dict/to/text/nodes',      # Step 2: Extract text
                                    json={'html_dict': html_dict})

        assert response2.status_code == 200
        result = response2.json()

        assert result['total_nodes'] >= 1

    def test__error_handling__invalid_json(self):                # Test invalid request
        response = self.client.post('/html/to/dict',
                                   json={})                      # Missing 'html' field

        assert response.status_code == 422                       # Validation error

    def test__error_handling__malformed_html(self):              # Test malformed HTML
        html = "<html><body><p>Unclosed paragraph"               # No closing tags

        response = self.client.post('/html/to/dict',
                                   json={'html': html})

        assert response.status_code == 200                       # Should still parse
        result = response.json()
        assert 'html_dict' in result

    def test__performance__large_html(self):                     # Test with large HTML
        html_parts = ["<html><body>"]
        for i in range(100):
            html_parts.append(f"<p>Paragraph {i} with some content here.</p>")
        html_parts.append("</body></html>")
        html = "".join(html_parts)

        response = self.client.post('/html/to/dict',
                                   json={'html': html})

        assert response.status_code == 200
        result = response.json()

        assert result['node_count'] >= 100                       # At least 100 paragraphs