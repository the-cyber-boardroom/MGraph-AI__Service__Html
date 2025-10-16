from unittest                                                             import TestCase
from osbot_utils.utils.Objects                                            import base_classes
from osbot_utils.type_safe.Type_Safe                                      import Type_Safe
from mgraph_ai_service_html.html__fast_api.core.Html__Extract_Text_Nodes  import Html__Extract_Text_Nodes, DEFAULT_MAX_DEPTH
from osbot_utils.helpers.html.transformers.Html__To__Html_Dict            import Html__To__Html_Dict


class test_Html__Extract_Text_Nodes(TestCase):

    def test__init__(self):                                      # Test auto-initialization
        with Html__Extract_Text_Nodes() as _:
            assert type(_)         is Html__Extract_Text_Nodes
            assert base_classes(_) == [Type_Safe, object]

            assert _.html_dict          is None                  # Not yet set
            assert _.text_elements      == {}                    # Empty dict
            assert _.text_elements__raw == {}                    # Empty dict
            assert _.hash_size          == 10                    # Default hash size
            assert _.captures           == 0                     # No captures yet
            assert _.max_depth          == DEFAULT_MAX_DEPTH     # Default max depth

    def test__capture_text(self):                                # Test text capture with hash
        with Html__Extract_Text_Nodes() as _:
            text = "Hello World"
            tag  = "p"

            hash_value = _.capture_text(text, tag)

            assert len(hash_value)  == _.hash_size               # Hash is correct length
            assert hash_value       in _.text_elements
            assert hash_value       in _.text_elements__raw
            assert _.text_elements__raw[hash_value] == text
            assert _.text_elements[hash_value]      == {'text': text, 'tag': tag}
            assert _.captures                       == 1

    def test__capture_text__multiple(self):                      # Test multiple captures
        with Html__Extract_Text_Nodes() as _:
            hash1 = _.capture_text("First",  "p")
            hash2 = _.capture_text("Second", "div")
            hash3 = _.capture_text("Third",  "span")

            assert len(_.text_elements)      == 3
            assert len(_.text_elements__raw) == 3
            assert _.captures                == 3
            assert hash1 != hash2 != hash3                       # Different hashes

    def test__capture_text__same_text_different_tags(self):      # Test same text in different tags
        with Html__Extract_Text_Nodes() as _:
            text  = "Repeated Text"
            hash1 = _.capture_text(text, "p")
            hash2 = _.capture_text(text, "div")

            assert hash1 == hash2                                # Same text = same hash
            assert _.text_elements[hash1]['tag'] == "div"        # Last tag wins
            assert _.captures                    == 2            # Both captured

    def test__traverse__simple_text_node(self):                  # Test simple traversal
        html      = "<p>Hello</p>"
        html_dict = Html__To__Html_Dict(html=html).convert()

        with Html__Extract_Text_Nodes() as _:
            _.html_dict = html_dict
            _.traverse(html_dict, depth=0, parent_tag=None)

            assert _.captures      == 1
            assert len(_.text_elements) == 1

            for hash_value, node_data in _.text_elements.items():
                assert node_data['text'] == 'Hello'
                assert node_data['tag']  == 'p'

    def test__traverse__nested_structure(self):                  # Test nested HTML traversal
        html = """
        <div>
            <p>First</p>
            <span>Second</span>
            <div>
                <p>Third</p>
            </div>
        </div>
        """
        html_dict = Html__To__Html_Dict(html=html).convert()

        with Html__Extract_Text_Nodes() as _:
            _.html_dict = html_dict
            _.traverse(html_dict, depth=0, parent_tag=None)

            assert _.captures           == 3                     # Three text nodes
            assert len(_.text_elements) == 3

            texts = [node['text'] for node in _.text_elements.values()]
            assert 'First'  in texts
            assert 'Second' in texts
            assert 'Third'  in texts

    def test__traverse__filters_script_tags(self):               # Test script tag filtering
        html = """
        <html>
            <body>
                <script>alert('test');</script>
                <p>Visible</p>
            </body>
        </html>
        """
        html_dict = Html__To__Html_Dict(html=html).convert()

        with Html__Extract_Text_Nodes() as _:
            _.html_dict = html_dict
            _.traverse(html_dict, depth=0, parent_tag=None)

            texts = [node['text'] for node in _.text_elements.values()]
            assert 'Visible' in texts
            assert 'alert'   not in str(texts)                   # Script content not captured

    def test__traverse__filters_style_tags(self):                # Test style tag filtering
        html = """
        <html>
            <head>
                <style>body { color: red; }</style>
            </head>
            <body>
                <p>Content</p>
            </body>
        </html>
        """
        html_dict = Html__To__Html_Dict(html=html).convert()

        with Html__Extract_Text_Nodes() as _:
            _.html_dict = html_dict
            _.traverse(html_dict, depth=0, parent_tag=None)

            texts = [node['text'] for node in _.text_elements.values()]
            assert 'Content' in texts
            assert 'color'   not in str(texts)                   # Style content not captured

    def test__traverse__respects_max_depth(self):                # Test max depth limiting
        html = """
        <div>                           
            <div>                       
                <div>                   
                    <div>               
                        <div>           
                            <p>Deep</p> 
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
        html_dict = Html__To__Html_Dict(html=html).convert()

        with Html__Extract_Text_Nodes() as _:
            _.html_dict = html_dict
            _.max_depth = 3                                      # Limit depth
            _.traverse(html_dict, depth=0, parent_tag=None)

            assert _.captures == 0                               # Should not reach text at depth 5

    def test__traverse__strips_whitespace(self):                 # Test whitespace stripping
        html = """
        <div>
            <p>  Text with spaces  </p>
            <span>    </span>
            <p>Another</p>
        </div>
        """
        html_dict = Html__To__Html_Dict(html=html).convert()

        with Html__Extract_Text_Nodes() as _:
            _.html_dict = html_dict
            _.traverse(html_dict, depth=0, parent_tag=None)

            texts = [node['text'] for node in _.text_elements.values()]
            assert '  Text with spaces  ' in texts                   # Original text preserved
            assert 'Another'              in texts
            assert _.captures             == 2                       # Whitespace-only span not captured

    def test__extract_from_html_dict(self):                      # Test new extraction method
        html = "<html><body><p>Test</p><div>Content</div></body></html>"
        html_dict = Html__To__Html_Dict(html=html).convert()

        with Html__Extract_Text_Nodes() as _:
            text_nodes = _.extract_from_html_dict(html_dict)

            assert isinstance(text_nodes, dict)
            assert len(text_nodes) == 2                          # "Test" and "Content"

            for hash_value, node_data in text_nodes.items():
                assert 'text' in node_data
                assert 'tag'  in node_data
                assert len(hash_value) == 10

    def test__extract_from_html_dict__with_custom_max_depth(self): # Test with custom max depth
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

        with Html__Extract_Text_Nodes() as _:
            text_nodes_deep    = _.extract_from_html_dict(html_dict, max_depth=256)

        with Html__Extract_Text_Nodes() as _:
            text_nodes_shallow = _.extract_from_html_dict(html_dict, max_depth=2)

        assert len(text_nodes_deep)    == 1                      # Should capture deep text
        assert len(text_nodes_shallow) == 0                      # Should NOT capture at depth 2

    def test__extract_from_html_dict__empty_html(self):          # Test with empty HTML
        html      = ""
        html_dict = Html__To__Html_Dict(html=html).convert()

        with Html__Extract_Text_Nodes() as _:
            text_nodes = _.extract_from_html_dict(html_dict)

            assert isinstance(text_nodes, dict)
            assert len(text_nodes) == 0

    def test__extract_from_html_dict__complex_structure(self):   # Test with complex real-world HTML
        html = """
        <html>
            <head>
                <title>Test Page</title>
            </head>
            <body>
                <header>
                    <h1>Main Title</h1>
                    <nav>
                        <a href="#">Link 1</a>
                        <a href="#">Link 2</a>
                    </nav>
                </header>
                <main>
                    <article>
                        <h2>Article Title</h2>
                        <p>First paragraph with some text.</p>
                        <p>Second paragraph with more content.</p>
                        <ul>
                            <li>List item 1</li>
                            <li>List item 2</li>
                        </ul>
                    </article>
                </main>
                <footer>
                    <p>Footer text</p>
                </footer>
            </body>
        </html>
        """
        html_dict = Html__To__Html_Dict(html=html).convert()

        with Html__Extract_Text_Nodes() as _:
            text_nodes = _.extract_from_html_dict(html_dict)

            assert len(text_nodes) >= 8                          # Multiple text nodes

            all_text = ' '.join(node['text'] for node in text_nodes.values())
            assert 'Main Title'      in all_text
            assert 'Article Title'   in all_text
            assert 'First paragraph' in all_text
            assert 'List item 1'     in all_text
            assert 'Footer text'     in all_text

    def test__hash_stability(self):                              # Test hash consistency
        text = "Consistent Text"

        with Html__Extract_Text_Nodes() as _:
            hash1 = _.capture_text(text, "p")

        with Html__Extract_Text_Nodes() as _:
            hash2 = _.capture_text(text, "div")

        assert hash1 == hash2                                    # Same text = same hash

    def test__hash_uniqueness(self):                             # Test hash uniqueness
        with Html__Extract_Text_Nodes() as _:
            hash1 = _.capture_text("Text 1", "p")
            hash2 = _.capture_text("Text 2", "p")
            hash3 = _.capture_text("Text 3", "p")

            hashes = {hash1, hash2, hash3}
            assert len(hashes) == 3                              # All different

    def test__tag_preservation(self):                            # Test tag information preservation
        html = """
        <div>
            <p>Para text</p>
            <span>Span text</span>
            <a href="#">Link text</a>
        </div>
        """
        html_dict = Html__To__Html_Dict(html=html).convert()

        with Html__Extract_Text_Nodes() as _:
            text_nodes = _.extract_from_html_dict(html_dict)

            tags = [node['tag'] for node in text_nodes.values()]
            assert 'p'    in tags
            assert 'span' in tags
            assert 'a'    in tags

    def test__performance__large_html(self):                     # Test with large HTML
        html_parts = ["<div>"]
        for i in range(100):                                     # Create 100 paragraphs
            html_parts.append(f"<p>Paragraph {i}</p>")
        html_parts.append("</div>")
        html = "".join(html_parts)

        html_dict = Html__To__Html_Dict(html=html).convert()

        with Html__Extract_Text_Nodes() as _:
            text_nodes = _.extract_from_html_dict(html_dict)

            assert len(text_nodes) == 100                        # All paragraphs captured