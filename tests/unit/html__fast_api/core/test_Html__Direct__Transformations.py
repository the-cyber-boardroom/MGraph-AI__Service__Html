from unittest                                                                   import TestCase

from osbot_utils.testing.__ import __
from osbot_utils.utils.Objects import base_classes, obj
from mgraph_ai_service_html.html__fast_api.core.Html__Direct__Transformations   import Html__Direct__Transformations
from osbot_utils.type_safe.Type_Safe                                            import Type_Safe


class test_Html__Direct__Transformations(TestCase):

    @classmethod
    def setUpClass(cls):                                         # ONE-TIME setup for expensive operations
        cls.transformations = Html__Direct__Transformations()

    def test__init__(self):                                      # Test auto-initialization
        with Html__Direct__Transformations() as _:
            assert type(_)         is Html__Direct__Transformations
            assert base_classes(_) == [Type_Safe, object]

    def test__html__to__html_dict(self):                         # Test HTML parsing to dict structure
        html = "<html><body><p>Test Content</p></body></html>"

        with self.transformations as _:
            html_dict = _.html__to__html_dict(html)

            assert isinstance(html_dict, dict)  is True
            assert 'tag'                        in html_dict
            assert 'nodes'                      in html_dict
            assert html_dict['tag']             == 'html'
            assert obj(html_dict)               == __( tag   = 'html',
                                                       attrs = __(),
                                                       nodes = [__(tag   = 'body',
                                                                   attrs = __(),
                                                                   nodes = [__(tag   = 'p'  ,
                                                                               attrs = __() ,
                                                                               nodes = [__(type = 'TEXT'        ,
                                                                                           data = 'Test Content')])])])

    def test__html__to__html_dict__empty(self):                  # Test with empty HTML
        html = ""
        with self.transformations as _:
            assert _.html__to__html_dict(html) is None


    def test__html__to__html_dict__complex(self):                # Test with nested structure
        html = """
        <html>
            <head><title>Test Page</title></head>
            <body>
                <div class="container">
                    <p id="intro">Hello World</p>
                    <ul>
                        <li>Item 1</li>
                        <li>Item 2</li>
                    </ul>
                </div>
            </body>
        </html>
        """

        with self.transformations as _:
            html_dict = _.html__to__html_dict(html)

            assert html_dict['tag'] == 'html'
            assert len(html_dict.get('nodes', [])) > 0
            #assert obj(html_dict) == ....                  # we can't do this due to issue with obj() where the 'class' variable name is used as a python variable name (which doesn't compile)

            assert html_dict == {'attrs': {},
                                 'nodes': [{'attrs': {},
                                            'nodes': [{'attrs': {},
                                                       'nodes': [{'data': 'Test Page', 'type': 'TEXT'}],
                                                       'tag': 'title'}],
                                            'tag': 'head'},
                                           {'attrs': {},
                                            'nodes': [{'attrs': {'class': 'container'},
                                                       'nodes': [{'attrs': {'id': 'intro'},
                                                                  'nodes': [{'data': 'Hello World',
                                                                             'type': 'TEXT'}],
                                                                  'tag': 'p'},
                                                                 {'attrs': {},
                                                                  'nodes': [{'attrs': {},
                                                                             'nodes': [{'data': 'Item 1',
                                                                                        'type': 'TEXT'}],
                                                                             'tag': 'li'},
                                                                            {'attrs': {},
                                                                             'nodes': [{'data': 'Item 2',
                                                                                        'type': 'TEXT'}],
                                                                             'tag': 'li'}],
                                                                  'tag': 'ul'}],
                                                       'tag': 'div'}],
                                            'tag': 'body'}],
                                 'tag': 'html'}


    def test__html_dict__to__html(self):                         # Test HTML reconstruction from dict
        original_html = "<html><body><p>Test</p></body></html>"

        with self.transformations as _:
            html_dict     = _.html__to__html_dict(original_html)
            reconstructed = _.html_dict__to__html(html_dict)

            assert isinstance(reconstructed, str)
            assert '<p>Test</p>' in reconstructed
            assert 'html'        in reconstructed.lower()
            assert 'body'        in reconstructed.lower()

    def test__html_dict__to__html__preserves_structure(self):    # Test structure preservation
        original_html = """
        <html>
            <body>
                <div>
                    <p>First</p>
                    <p>Second</p>
                </div>
            </body>
        </html>
        """

        with self.transformations as _:
            html_dict     = _.html__to__html_dict(original_html)
            reconstructed = _.html_dict__to__html(html_dict)

            assert 'First'  in reconstructed
            assert 'Second' in reconstructed
            assert '<div>'  in reconstructed or '<div' in reconstructed

    def test__html__to__lines(self):                             # Test line formatting
        html = "<html><body><p>Test</p></body></html>"

        with self.transformations as _:
            lines = _.html__to__lines(html)

            assert isinstance(lines, str)
            assert 'html' in lines
            assert 'body' in lines
            assert 'p'    in lines
            assert '\n'   in lines                               # Should have line breaks
            assert lines == 'html\n    └── body\n        └── p\n            └── TEXT: Test'

    def test__html__to__lines__empty(self):                      # Test with empty HTML
        html = ""

        with self.transformations as _:
            lines = _.html__to__lines(html)
            assert isinstance(lines, str)

    def test__html_dict__to__text_nodes(self):                   # Test text node extraction
        html = "<html><body><p>Hello</p><span>World</span></body></html>"

        with self.transformations as _:
            html_dict  = _.html__to__html_dict(html)
            text_nodes = _.html_dict__to__text_nodes(html_dict)

            assert isinstance(text_nodes, dict)
            assert len(text_nodes) == 2                          # "Hello" and "World"

            for hash_value, node_data in text_nodes.items():     # Verify structure
                assert 'text' in node_data
                assert 'tag'  in node_data
                assert len(hash_value) == 10                     # Default hash size

    def test__html_dict__to__text_nodes__with_max_depth(self):   # Test depth limiting
        html = "<html><body><div><div><div><p>Deep</p></div></div></div></body></html>"

        with self.transformations as _:
            html_dict = _.html__to__html_dict(html)

            text_nodes_deep    = _.html_dict__to__text_nodes(html_dict, max_depth=256)
            text_nodes_shallow = _.html_dict__to__text_nodes(html_dict, max_depth=2)

            assert isinstance(text_nodes_deep, dict)
            assert isinstance(text_nodes_shallow, dict)

    def test__html_dict__to__text_nodes__filters_script_style(self): # Test script/style filtering
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

        with self.transformations as _:
            html_dict  = _.html__to__html_dict(html)
            text_nodes = _.html_dict__to__text_nodes(html_dict)

            has_visible_text = any('Visible Text' in node.get('text', '')
                                  for node in text_nodes.values())
            has_script_text  = any('alert' in node.get('text', '')
                                  for node in text_nodes.values())
            has_style_text   = any('color: red' in node.get('text', '')
                                  for node in text_nodes.values())

            assert has_visible_text is True                      # Should capture visible text
            assert has_script_text  is False                     # Should NOT capture script
            assert has_style_text   is False                     # Should NOT capture style

    def test__round_trip__simple(self):                          # Test full round-trip
        original = "<html><body><p>Test</p></body></html>"

        with self.transformations as _:
            html_dict     = _.html__to__html_dict(original)
            reconstructed = _.html_dict__to__html(html_dict)

            assert '<p>Test</p>' in reconstructed
            assert reconstructed  == ('<!DOCTYPE html>\n'
                                      '<html>\n'
                                      '    <body>\n'
                                      '        <p>Test</p>\n'
                                      '    </body>\n'
                                      '</html>\n')

    def test__round_trip__with_attributes(self):                 # Test attributes preservation
        original = '<html><body><p class="test" id="para">Text</p></body></html>'

        with self.transformations as _:
            html_dict     = _.html__to__html_dict(original)
            reconstructed = _.html_dict__to__html(html_dict)

            assert 'Text' in reconstructed
            assert 'class' in reconstructed or 'id' in reconstructed  # At least one attribute

    def test__round_trip__nested_lists(self):                    # Test complex nesting
        original = """\
<!DOCTYPE html>
<html>
    <body>
        <ul>
            <li>Item 1
                <ul>
    <li>Sub 1</li>
    <li>Sub 2</li>
</ul></li>
            <li>Item 2</li>
        </ul>
    </body>
</html>
"""

        with self.transformations as _:
            html_dict     = _.html__to__html_dict(original)
            reconstructed = _.html_dict__to__html(html_dict)

            assert 'Item 1' in reconstructed
            assert 'Sub 1'  in reconstructed
            assert 'Sub 2'  in reconstructed
            assert 'Item 2' in reconstructed
            assert reconstructed == original        # todo BUG: note the aligment issue with the ul

    def test__text_extraction__whitespace_handling(self):        # Test whitespace stripping
        html = "<html><body><p>  Trimmed  </p><span>   Text   </span></body></html>"

        with self.transformations as _:
            html_dict  = _.html__to__html_dict(html)
            text_nodes = _.html_dict__to__text_nodes(html_dict)

            assert list(text_nodes.values()) == [{'text': '  Trimmed  ', 'tag': 'p'},
                                                 {'text': '   Text   ', 'tag': 'span'}]

    def test__text_extraction__empty_text_nodes(self):           # Test empty node handling
        html = "<html><body><p></p><span>  </span><div>Text</div></body></html>"

        with self.transformations as _:
            html_dict  = _.html__to__html_dict(html)
            text_nodes = _.html_dict__to__text_nodes(html_dict)

            assert len(text_nodes) == 1                          # Only "Text" should be captured