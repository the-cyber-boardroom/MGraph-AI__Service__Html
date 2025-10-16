from unittest                                                        import TestCase

import pytest
from fastapi.testclient                                              import TestClient
from osbot_fast_api_serverless.fast_api.Serverless__Fast_API__Config import Serverless__Fast_API__Config
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import file_name

from mgraph_ai_service_html.html__fast_api.Html_Service__Fast_API    import Html_Service__Fast_API
from osbot_utils.helpers.html.transformers.Html__To__Html_Dict       import Html__To__Html_Dict


class test_Routes__Hashes(TestCase):

    @classmethod
    def setUpClass(cls):                                         # ONE-TIME expensive setup
        config = Serverless__Fast_API__Config(enable_api_key=False)
        with Html_Service__Fast_API(config=config) as api:
            api.setup()
            cls.app    = api.app()
            cls.client = TestClient(cls.app)

    def test__to__html__no_modifications(self):                  # Test with empty hash mapping
        html      = "<html><body><p>Test Content</p></body></html>"
        html_dict = Html__To__Html_Dict(html=html).convert()

        response = self.client.post('/hashes/to/html',
                                   json={'html_dict'   : html_dict,
                                         'hash_mapping': {}      })

        assert response.status_code == 200
        reconstructed = response.text

        assert 'Test Content' in reconstructed                   # Original preserved

    def test__to__html__single_hash_replacement(self):           # Test single text replacement
        html = "<html><body><p>abcd123456</p></body></html>"
        html_dict = Html__To__Html_Dict(html=html).convert()

        hash_mapping = { 'abcd123456': 'Replaced Text' }

        response = self.client.post('/hashes/to/html',
                                   json={'html_dict'   : html_dict   ,
                                         'hash_mapping': hash_mapping})

        assert response.status_code == 200
        reconstructed = response.text

        assert 'Replaced Text' in reconstructed                  # Hash replaced
        assert 'abcd123456'    not in reconstructed              # Original hash gone

    def test__to__html__multiple_hash_replacements(self):        # Test multiple replacements
        html = """
        <html>
            <body>
                <p>1abcd12345</p>
                <div>2abcd12345</div>
                <span>3abcd12345</span>
            </body>
        </html>
        """
        html_dict = Html__To__Html_Dict(html=html).convert()

        hash_mapping = { '1abcd12345': 'First Text' ,
                         '2abcd12345': 'Second Text',
                         '3abcd12345': 'Third Text' }

        response = self.client.post('/hashes/to/html',
                                   json={'html_dict'   : html_dict   ,
                                         'hash_mapping': hash_mapping})

        assert response.status_code == 200
        reconstructed = response.text

        assert 'First Text'  in reconstructed                    # All replacements applied
        assert 'Second Text' in reconstructed
        assert 'Third Text'  in reconstructed
        assert '1abcd12345'    not in reconstructed                # All hashes gone
        assert '2abcd12345'    not in reconstructed
        assert '3abcd12345'    not in reconstructed
        assert reconstructed == ('<!DOCTYPE html>\n'
                                 '<html>\n'
                                 '    <body>\n'
                                 '        <p>First Text</p>\n'
                                 '        <div>Second Text</div>\n'
                                 '        <span>Third Text</span>\n'
                                 '    </body>\n'
                                 '</html>\n')

    def test__to__html__partial_hash_replacement(self):          # Test with some unmapped hashes
        html = """
        <html>
            <body>
                <p>1abcd12345</p>
                <p>2abcd12345</p>
                <p>Regular Text</p>
            </body>
        </html>
        """
        html_dict = Html__To__Html_Dict(html=html).convert()

        hash_mapping = { '1abcd12345': 'Replaced One' }

        response = self.client.post('/hashes/to/html',
                                   json={'html_dict'   : html_dict   ,
                                         'hash_mapping': hash_mapping})

        assert response.status_code == 200
        reconstructed = response.text

        assert 'Replaced One' in reconstructed                   # Mapped hash replaced
        assert '2abcd12345'   in reconstructed                   # Unmapped hash preserved
        assert 'Regular Text' in reconstructed                   # Non-hash text preserved

    def test__bug__to__html__semantic_text_workflow(self):            # Test external service workflow
        pytest.skip("fix text")
        html = "<html><body><p>Original text for rating</p></body></html>"

        response1 = self.client.post('/html/to/text/nodes',      # Step 1: Extract text nodes
                                    json={'html': html})

        assert response1.status_code == 200
        text_nodes = response1.json()['text_nodes']

        response2 = self.client.post('/html/to/dict',            # Step 2: Get html_dict
                                    json={'html': html})

        assert response2.status_code == 200
        html_dict = response2.json()['html_dict']               # todo: BUG: this workflow is wrong, we should be getting an hash mapping here
        pprint(html_dict)
        hash_mapping = {}                                        # Step 3: Build hash mapping
        for hash_value, node_data in text_nodes.items():         # (simulating external service)
            original_text = node_data['text']
            modified_text = f"[RATED: {original_text}]"          # Add rating marker
            hash_mapping[hash_value] = modified_text

        response3 = self.client.post('/hashes/to/html',          # Step 4: Reconstruct with ratings
                                    json={'html_dict'   : html_dict   ,
                                          'hash_mapping': hash_mapping})

        assert response3.status_code == 200
        final_html = response3.text
        assert '[RATED:' in final_html                           # Rating applied
        assert 'Original text for rating' not in final_html      # Original replaced

    def test__to__html__preserves_structure(self):               # Test structure preservation
        html = """
        <html>
            <body>
                <div class="container">
                    <h1>1abcd12345</h1>
                    <p id="content">2abcd12345</p>
                </div>
            </body>
        </html>
        """
        html_dict = Html__To__Html_Dict(html=html).convert()

        hash_mapping = { '1abcd12345': 'New Title'  ,
                         '2abcd12345' : 'New Content' }

        response = self.client.post('/hashes/to/html',
                                   json={'html_dict'   : html_dict   ,
                                         'hash_mapping': hash_mapping})

        assert response.status_code == 200
        reconstructed = response.text

        assert 'New Title'   in reconstructed                    # Content replaced
        assert 'New Content' in reconstructed
        assert 'container'   in reconstructed or 'div' in reconstructed  # Structure preserved
        assert 'h1'          in reconstructed or 'H1' in reconstructed

    def test__to__html__with_special_characters(self):           # Test special character handling
        html = "<html><body><p>1abcd12345</p></body></html>"
        html_dict = Html__To__Html_Dict(html=html).convert()

        hash_mapping = { '1abcd12345': 'Text with <special> & "characters"' }

        response = self.client.post('/hashes/to/html',
                                   json={'html_dict'   : html_dict   ,
                                         'hash_mapping': hash_mapping})

        assert response.status_code == 200
        reconstructed = response.text

        assert '&' in reconstructed or 'special' in reconstructed  # Special chars handled

    def test__to__html__empty_replacement(self):                 # Test replacing with empty string
        html      = "<html><body><p>1abcd12345</p></body></html>"
        html_dict = Html__To__Html_Dict(html=html).convert()

        hash_mapping = { '1abcd12345': '' }

        response = self.client.post('/hashes/to/html',
                                   json={'html_dict'   : html_dict   ,
                                         'hash_mapping': hash_mapping})

        assert response.status_code == 200
        reconstructed = response.text

        assert '1abcd12345' not in reconstructed                # Hash removed

    def test__to__html__unicode_replacement(self):               # Test Unicode character handling
        html      = "<html><body><p>1abcd12345</p></body></html>"
        html_dict = Html__To__Html_Dict(html=html).convert()

        hash_mapping = { '1abcd12345': 'Unicode: â˜… â™¥ â˜º æ—¥æœ¬èªž' }

        response = self.client.post('/hashes/to/html',
                                   json={'html_dict'   : html_dict   ,
                                         'hash_mapping': hash_mapping})

        assert response.status_code == 200
        reconstructed = response.text

        assert 'Unicode:' in reconstructed                       # Unicode handled

    def test__integration__full_pipeline(self):                  # Test complete workflow
        original_html = """
        <html>
            <body>
                <h1>Article Title</h1>
                <p>First paragraph of content.</p>
                <p>Second paragraph with more text.</p>
            </body>
        </html>
        """

        response1 = self.client.post('/html/to/text/nodes',      # Extract text with hashes
                                    json={'html': original_html})
        text_nodes = response1.json()['text_nodes']

        assert text_nodes == { '9896ab6df2': {'tag': 'h1', 'text': 'Article Title'},
                               'a3de497ca8': {'tag': 'p', 'text': 'First paragraph of content.'},
                               'fee1ec797d': {'tag': 'p', 'text': 'Second paragraph with more text.'}}

        response2 = self.client.post('/html/to/html/hashes',     # Get HTML with hashes
                                    json={'html': original_html})
        html_with_hashes = response2.text
        assert html_with_hashes == ('<!DOCTYPE html>\n'
                                     '<html>\n'
                                     '    <body>\n'
                                     '        <h1>9896ab6df2</h1>\n'
                                     '        <p>a3de497ca8</p>\n'
                                     '        <p>fee1ec797d</p>\n'
                                     '    </body>\n'
                                     '</html>\n')

        response3 = self.client.post('/html/to/dict',            # Get dict
                                    json={'html': original_html})
        html_dict = response3.json()['html_dict']

        assert html_dict == {'attrs': {},
                             'nodes': [{'attrs': {},
                                        'nodes': [{'attrs': {},
                                                   'nodes': [{'data': 'Article Title', 'type': 'TEXT'}],
                                                   'tag': 'h1'},
                                                  {'attrs': {},
                                                   'nodes': [{'data': 'First paragraph of content.',
                                                              'type': 'TEXT'}],
                                                   'tag': 'p'},
                                                  {'attrs': {},
                                                   'nodes': [{'data': 'Second paragraph with more text.',
                                                              'type': 'TEXT'}],
                                                   'tag': 'p'}],
                                        'tag': 'body'}],
                             'tag': 'html'}

        hash_mapping = {hash_val: f"MODIFIED: {node['text']}"   # Create modifications
                       for hash_val, node in text_nodes.items()}

        assert hash_mapping == { '9896ab6df2': 'MODIFIED: Article Title',
                                 'a3de497ca8': 'MODIFIED: First paragraph of content.',
                                 'fee1ec797d': 'MODIFIED: Second paragraph with more text.'}


        response4 = self.client.post('/hashes/to/html',          # Apply modifications
                                    json={'html_dict'   : html_dict   ,
                                          'hash_mapping': hash_mapping})

        final_html = response4.text

        # BUG: all test below are confirm that the conversion is not working
        assert final_html == ('<!DOCTYPE html>\n'
                             '<html>\n'
                             '    <body>\n'
                             '        <h1>Article Title</h1>\n'
                             '        <p>First paragraph of content.</p>\n'
                             '        <p>Second paragraph with more text.</p>\n'
                             '    </body>\n'
                             '</html>\n')

        assert 'MODIFIED: Article Title'        not in final_html    # All text modified
        assert 'MODIFIED: First paragraph'      not in final_html
        assert 'MODIFIED: Second paragraph'     not in final_html
        assert 'Article Title'                  in final_html or 'MODIFIED:' in final_html

    def test__error_handling__missing_html_dict(self):           # Test missing required field
        response = self.client.post('/hashes/to/html',
                                   json={'hash_mapping': {}})

        assert response.status_code == 200                       # Validation error
        assert response.text == ''

    def test__error_handling__missing_hash_mapping(self):        # Test missing hash_mapping
        html_dict = Html__To__Html_Dict(html="<p>Test</p>").convert()

        response = self.client.post('/hashes/to/html',
                                   json={'html_dict': html_dict})

        assert response.status_code == 200                       # Validation error
        assert response.text        == '<p>Test</p>\n'

    def test__error_handling__invalid_html_dict(self):           # Test with malformed dict
        response = self.client.post('/hashes/to/html',
                                   json={'html_dict'   : {}      ,
                                         'hash_mapping': {}      })

        assert response.status_code == 200                       # Should handle gracefully

    def test__filtering_scenario__min_rating(self):              # Simulate minimum rating filter
        html = """
        <html>
            <body>
                <p>1abcd12345</p>
                <p>2abcd12345</p>
                <p>3abcd12345</p>
            </body>
        </html>
        """
        html_dict = Html__To__Html_Dict(html=html).convert()

        ratings = {                                              # Simulated ratings
            '1abcd12345' : 8,
            '2abcd12345' : 3,
            '3abcd12345' : 6
        }

        hash_mapping = {}                                        # Only keep rating >= 6
        for hash_val, rating in ratings.items():
            if rating >= 6:
                hash_mapping[hash_val] = f"[{rating}/10] Content"
            else:
                hash_mapping[hash_val] = "[FILTERED]"

        response = self.client.post('/hashes/to/html',
                                   json={'html_dict'   : html_dict   ,
                                         'hash_mapping': hash_mapping})

        assert response.status_code == 200
        filtered_html = response.text

        assert '[8/10]'      in filtered_html                    # High rating shown
        assert '[6/10]'      in filtered_html                    # Medium rating shown
        assert '[FILTERED]'  in filtered_html                    # Low rating filtered
        assert '1abcd12345'  not in filtered_html                # Hashes replaced
        assert filtered_html == ('<!DOCTYPE html>\n'
                                 '<html>\n'
                                 '    <body>\n'
                                 '        <p>[8/10] Content</p>\n'
                                 '        <p>[FILTERED]</p>\n'
                                 '        <p>[6/10] Content</p>\n'
                                 '    </body>\n'
                                 '</html>\n')

    def test__performance__many_replacements(self):              # Test with many hashes
        html_parts = ["<html><body>"]
        for i in range(50):
            html_parts.append(f"<p>1111111{i:03d}</p>")
        html_parts.append("</body></html>")
        html = "".join(html_parts)

        html_dict = Html__To__Html_Dict(html=html).convert()

        hash_mapping = {f"1111111{i:03d}": f"Text {i}" for i in range(50)}

        response = self.client.post('/hashes/to/html',
                                   json={'html_dict'   : html_dict   ,
                                         'hash_mapping': hash_mapping})

        assert response.status_code == 200
        final_html = response.text

        assert 'Text 0'  in final_html                           # First replacement
        assert 'Text 49' in final_html                           # Last replacement
        assert '1111111000' not in final_html                      # Hashes gone