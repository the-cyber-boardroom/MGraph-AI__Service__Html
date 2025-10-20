from unittest                                                                                       import TestCase
from osbot_utils.testing.__                                                                         import __
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash                  import Safe_Str__Hash
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                               import Type_Safe__Dict
from mgraph_ai_service_html.html__fast_api.routes.Routes__Hashes                                    import Routes__Hashes
from mgraph_ai_service_html.html__fast_api.routes.Routes__Html                                      import Routes__Html
from mgraph_ai_service_html.html__fast_api.schemas.html.Schema__Html__To__Dict__Hashes__Request     import Schema__Html__To__Dict__Hashes__Request
from mgraph_ai_service_html.html__fast_api.schemas.html.Schema__Html__To__Dict__Hashes__Response    import Schema__Html__To__Dict__Hashes__Response
from mgraph_ai_service_html.html__fast_api.schemas.html.Schema__Html__To__Text__Hashes__Request     import Schema__Html__To__Text__Hashes__Request
from mgraph_ai_service_html.html__fast_api.schemas.html.Schema__Html__To__Text__Hashes__Response    import Schema__Html__To__Text__Hashes__Response
from mgraph_ai_service_html.html__fast_api.schemas.hashes.Schema__Hashes__To__Html__Request         import Schema__Hashes__To__Html__Request


class test_Routes__Html__to__Hashes__to__Html(TestCase):

    @classmethod
    def setUpClass(cls):                                         # ONE-TIME expensive setup
        cls.routes_html   = Routes__Html()
        cls.routes_hashes = Routes__Hashes()

    def test__to__dict__hashes__simple_html(self):               # Test simple HTML with single text node
        html    = "<p>Hello</p>"
        request = Schema__Html__To__Dict__Hashes__Request(html=html)

        response = self.routes_html.to__dict__hashes(request)

        assert type(response)                            is Schema__Html__To__Dict__Hashes__Response
        assert response.html_dict                        is not None
        assert type(response.text_hashes_mapping)        is Type_Safe__Dict
        assert response.total_text_hashes                >  0
        assert response.node_count                       >  0
        assert response.max_depth                        >= 0
        assert type(response.max_depth_reached)          is bool

        assert len(response.text_hashes_mapping)         == 1     # Single text node
        hash_value = list(response.text_hashes_mapping.keys())[0]
        assert len(hash_value)                           == 10    # Hash is 10 characters
        assert response.text_hashes_mapping[hash_value]  == "Hello"

    def test__to__dict__hashes__multiple_text_nodes(self):       # Test multiple text nodes
        html    = "<div><p>First</p><span>Second</span><p>Third</p></div>"
        request = Schema__Html__To__Dict__Hashes__Request(html=html)

        response = self.routes_html.to__dict__hashes(request)

        assert response.total_text_hashes                == 3
        assert len(response.text_hashes_mapping)         == 3

        text_values = list(response.text_hashes_mapping.values())
        assert "First"  in text_values
        assert "Second" in text_values
        assert "Third"  in text_values
        assert type(response) is Schema__Html__To__Dict__Hashes__Response
        assert response.obj() == __( html_dict           = __( tag   = 'div' ,
                                                               attrs = __()    ,
                                                               nodes = [ __( tag   = 'p'   ,
                                                                             attrs = __()  ,
                                                                             nodes = [ __( type = 'TEXT'          ,
                                                                                           data = '7fb55ed0b7' ) ] ) ,
                                                                         __( tag   = 'span' ,
                                                                             attrs = __()    ,
                                                                             nodes = [ __( type = 'TEXT'          ,
                                                                                          data = 'c22cf8376b' ) ] ) ,
                                                                         __( tag   = 'p'   ,
                                                                             attrs = __()  ,
                                                                             nodes = [ __( type = 'TEXT'          ,
                                                                                           data = '168909c0b6' ) ] ) ] ) ,
                                     text_hashes_mapping = __( _7fb55ed0b7 = 'First'  ,
                                                                c22cf8376b = 'Second' ,
                                                               _168909c0b6 = 'Third'  ) ,
                                     node_count          = 7                         ,
                                     max_depth           = 2                         ,
                                     total_text_hashes   = 3                         ,
                                     max_depth_reached   = False                     )

    def test__to__dict__hashes__nested_elements(self):           # Test deeply nested structure
        html    = "<div><div><div><p>Nested</p></div></div></div>"
        request = Schema__Html__To__Dict__Hashes__Request(html=html)

        response = self.routes_html.to__dict__hashes(request)

        assert response.total_text_hashes                == 1
        assert response.max_depth                        >  0
        assert "Nested" in response.text_hashes_mapping.values()

    def test__to__dict__hashes__empty_tags(self):                # Test empty tags produce no text nodes
        html    = "<div><p></p><span></span></div>"
        request = Schema__Html__To__Dict__Hashes__Request(html=html)

        response = self.routes_html.to__dict__hashes(request)

        assert response.total_text_hashes                == 0     # Empty tags create no text nodes
        assert len(response.text_hashes_mapping)         == 0

    def test__to__dict__hashes__special_characters(self):        # Test special characters preserved
        html    = '<p>Hello & "World" <span>\'Test\'</span></p>'
        request = Schema__Html__To__Dict__Hashes__Request(html=html)

        response = self.routes_html.to__dict__hashes(request)

        assert response.total_text_hashes                >  0
        text_values = list(response.text_hashes_mapping.values())
        assert any('&' in val or '"' in val or "'" in val for val in text_values)

    def test__to__dict__hashes__unicode_characters(self):        # Test Unicode support
        html    = "<p>Hello 世界 🌍</p>"
        request = Schema__Html__To__Dict__Hashes__Request(html=html)

        response = self.routes_html.to__dict__hashes(request)

        assert response.total_text_hashes                == 1
        text_value = list(response.text_hashes_mapping.values())[0]
        assert "世界" in text_value
        assert "🌍"  in text_value

    def test__to__dict__hashes__scripts_and_styles_ignored(self): # Test script/style filtering
        html = """
        <html>
            <head>
                <style>body { color: red; }</style>
                <script>console.log('test');</script>
            </head>
            <body>
                <p>Visible text</p>
            </body>
        </html>
        """
        request = Schema__Html__To__Dict__Hashes__Request(html=html)

        response = self.routes_html.to__dict__hashes(request)

        text_values = list(response.text_hashes_mapping.values())
        assert "Visible text"                            in text_values
        assert not any("color: red"  in val for val in text_values)
        assert not any("console.log" in val for val in text_values)

    def test__to__dict__hashes__max_depth_parameter(self):       # Test max_depth constraint
        html             = "<div><div><div><div><p>Deep</p></div></div></div></div>"
        request_shallow  = Schema__Html__To__Dict__Hashes__Request(html=html, max_depth=2)
        request_deep     = Schema__Html__To__Dict__Hashes__Request(html=html, max_depth=256)

        response_shallow = self.routes_html.to__dict__hashes(request_shallow)
        response_deep    = self.routes_html.to__dict__hashes(request_deep)

        assert response_shallow.max_depth_reached        == True
        assert response_deep.max_depth_reached           == False

    def test__to__dict__hashes__hash_format(self):               # Test hash format is valid
        html    = "<p>Test</p>"
        request = Schema__Html__To__Dict__Hashes__Request(html=html)

        response = self.routes_html.to__dict__hashes(request)

        for hash_value in response.text_hashes_mapping.keys():
            assert len(hash_value)                       == 10
            assert all(c in '0123456789abcdef' for c in hash_value.lower())

    def test__to__dict__hashes__whitespace_handling(self):       # Test whitespace preservation
        html    = "<p>  Text with   spaces  </p>"
        request = Schema__Html__To__Dict__Hashes__Request(html=html)

        response = self.routes_html.to__dict__hashes(request)

        assert response.total_text_hashes                == 1

    def test__to__text__hashes__simple_html(self):               # Test lightweight endpoint
        html    = "<p>Hello</p>"
        request = Schema__Html__To__Text__Hashes__Request(html=html)

        response = self.routes_html.to__text__hashes(request)

        assert type(response)                            is Schema__Html__To__Text__Hashes__Response
        assert type(response.text_hashes_mapping)        is Type_Safe__Dict
        assert response.total_text_hashes                >  0
        assert type(response.max_depth_reached)          is bool

        assert not hasattr(response, 'html_dict')                # No html_dict in lightweight response
        assert not hasattr(response, 'node_count')               # No node_count either

    def test__to__text__hashes__multiple_nodes(self):            # Test multiple nodes with lightweight response
        html    = "<div><p>First</p><span>Second</span></div>"
        request = Schema__Html__To__Text__Hashes__Request(html=html)

        response = self.routes_html.to__text__hashes(request)

        assert response.total_text_hashes                == 2
        text_values = list(response.text_hashes_mapping.values())
        assert "First"  in text_values
        assert "Second" in text_values

    def test__to__text__hashes__with_max_depth(self):            # Test max_depth with lightweight endpoint
        html    = "<div><div><div><p>Deep</p></div></div></div>"
        request = Schema__Html__To__Text__Hashes__Request(html=html, max_depth=2)

        response = self.routes_html.to__text__hashes(request)

        assert response.max_depth_reached                == True
        assert response.total_text_hashes                == 0     # Too deep

    def test__to__text__hashes__empty_html(self):                # Test empty HTML
        html    = ""
        request = Schema__Html__To__Text__Hashes__Request(html=html)

        response = self.routes_html.to__text__hashes(request)

        assert response.total_text_hashes                == 0
        assert len(response.text_hashes_mapping)         == 0

    def test__complete_workflow__extract_modify_reconstruct(self): # Test complete hash workflow
        original_html        = "<p>Original text</p>"
        extract_request      = Schema__Html__To__Dict__Hashes__Request(html=original_html)
        extract_response     = self.routes_html.to__dict__hashes(extract_request)
        original_hash        = list(extract_response.text_hashes_mapping.keys())[0]
        modified_mapping     = { original_hash: "Modified text" }
        reconstruct_request  = Schema__Hashes__To__Html__Request(html_dict    = extract_response.html_dict,
                                                                 hash_mapping = modified_mapping          )
        reconstruct_response = self.routes_hashes.to__html(reconstruct_request)
        reconstructed_html   = reconstruct_response.body.decode('utf-8')

        assert extract_response.total_text_hashes                  == 1
        assert extract_response.text_hashes_mapping[original_hash] == "Original text"
        assert "Modified text"                                     in reconstructed_html
        assert "Original text"                                 not in reconstructed_html
        assert reconstructed_html                                  == '<p>Modified text</p>\n'

    def test__complete_workflow__multiple_modifications(self):   # Test workflow with multiple mods
        original_html = "<div><p>First</p><span>Second</span><p>Third</p></div>"
        extract_request = Schema__Html__To__Dict__Hashes__Request(html=original_html)
        extract_response = self.routes_html.to__dict__hashes(extract_request)

        modified_mapping = {}
        for hash_value, original_text in extract_response.text_hashes_mapping.items():
            modified_mapping[hash_value] = f"NEW_{original_text}"

        reconstruct_request = Schema__Hashes__To__Html__Request(html_dict    = extract_response.html_dict,
                                                                hash_mapping = modified_mapping          )
        reconstruct_response = self.routes_hashes.to__html(reconstruct_request)

        reconstructed_html = reconstruct_response.body.decode('utf-8')
        assert "NEW_First"  in reconstructed_html
        assert "NEW_Second" in reconstructed_html
        assert "NEW_Third"  in reconstructed_html

    def test__complete_workflow__selective_modification(self):   # Test selective text modification
        original_html = "<div><p>Keep this</p><span>Modify this</span></div>"
        extract_request = Schema__Html__To__Dict__Hashes__Request(html=original_html)
        extract_response = self.routes_html.to__dict__hashes(extract_request)

        modified_mapping = {}
        for hash_value, original_text in extract_response.text_hashes_mapping.items():
            if original_text == "Modify this":
                modified_mapping[hash_value] = "CHANGED"
            else:
                modified_mapping[hash_value] = original_text         # Keep original

        assert extract_response.text_hashes_mapping == { Safe_Str__Hash('42d0b3e2a9'): 'Keep this'  ,
                                                         Safe_Str__Hash('eebe4f5462'): 'Modify this'}
        assert modified_mapping                     == { Safe_Str__Hash('42d0b3e2a9'): 'Keep this'  ,
                                                         Safe_Str__Hash('eebe4f5462'): 'CHANGED'    }
        reconstruct_request = Schema__Hashes__To__Html__Request(html_dict    = extract_response.html_dict,
                                                                hash_mapping = modified_mapping         )
        reconstruct_response = self.routes_hashes.to__html(reconstruct_request)

        reconstructed_html = reconstruct_response.body.decode('utf-8')
        assert "Keep this"   in reconstructed_html
        assert "CHANGED"     in reconstructed_html
        assert "Modify this" not in reconstructed_html

    def test__dict__hashes_vs_text__hashes__same_mapping(self):  # Verify both endpoints same mapping
        html         = "<p>Test</p><span>Content</span>"
        request_dict = Schema__Html__To__Dict__Hashes__Request(html=html)
        request_text = Schema__Html__To__Text__Hashes__Request(html=html)

        response_dict = self.routes_html.to__dict__hashes(request_dict)
        response_text = self.routes_html.to__text__hashes(request_text)

        assert response_dict.text_hashes_mapping         == response_text.text_hashes_mapping
        assert response_dict.total_text_hashes           == response_text.total_text_hashes

    def test__html_with_only_whitespace(self):                   # Test whitespace-only text
        html    = """<p>   </p><span>  
  </span>"""
        request = Schema__Html__To__Dict__Hashes__Request(html=html)

        response = self.routes_html.to__dict__hashes(request)

        assert response.total_text_hashes                == 0     # Whitespace stripped

    def test__malformed_html(self):                              # Test malformed HTML parsing
        html    = "<p>Unclosed paragraph<div>Nested wrong</p></div>"
        request = Schema__Html__To__Dict__Hashes__Request(html=html)

        response = self.routes_html.to__dict__hashes(request)

        assert response.total_text_hashes                >  0     # Should parse without error
        assert "Unclosed paragraph" in response.text_hashes_mapping.values() or \
               "Nested wrong"       in response.text_hashes_mapping.values()

    def test__very_large_html(self):                             # Test performance with large HTML
        items   = "".join([f"<li>Item {i}</li>" for i in range(100)])
        html    = f"<ul>{items}</ul>"
        request = Schema__Html__To__Dict__Hashes__Request(html=html)

        import time
        start    = time.time()
        response = self.routes_html.to__dict__hashes(request)
        elapsed  = time.time() - start

        assert response.total_text_hashes                == 100
        assert elapsed                                   <  5.0   # Complete in reasonable time

    def test__response_format_matches_hashes__to__html_requirements(self): # Test response format compatibility
        html    = "<p>Test</p>"
        request = Schema__Html__To__Dict__Hashes__Request(html=html)

        response = self.routes_html.to__dict__hashes(request)

        assert hasattr(response, 'html_dict')
        assert hasattr(response, 'text_hashes_mapping')

        hash_request = Schema__Hashes__To__Html__Request(
            html_dict    = response.html_dict,
            hash_mapping = response.text_hashes_mapping
        )
        assert hash_request                              is not None

    def test__text_hashes_mapping_is_dict_hash_to_str(self):     # Test mapping type correctness
        html    = "<p>Test</p>"
        request = Schema__Html__To__Dict__Hashes__Request(html=html)

        response = self.routes_html.to__dict__hashes(request)

        for key, value in response.text_hashes_mapping.items():
            assert type(key)                             is Safe_Str__Hash
            assert len(key)                              == 10                  # Hash length
            assert type(value)                           is str                 # Original text