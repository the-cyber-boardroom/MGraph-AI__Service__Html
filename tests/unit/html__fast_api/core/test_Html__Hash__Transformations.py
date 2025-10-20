import pytest
from unittest                                                                                       import TestCase
from osbot_utils.testing.__helpers                                                                  import obj
from osbot_utils.type_safe.primitives.core.Safe_UInt                                                import Safe_UInt
from osbot_utils.type_safe.primitives.domains.web.safe_str.Safe_Str__Html                           import Safe_Str__Html
from osbot_utils.testing.__                                                                         import __
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                               import Type_Safe__Dict
from mgraph_ai_service_html.html__fast_api.core.Html__Hash__Transformations                         import Html__Hash__Transformations
from mgraph_ai_service_html.html__fast_api.core.Html__Direct__Transformations                       import Html__Direct__Transformations
from mgraph_ai_service_html.html__fast_api.schemas.html.Schema__Html__To__Dict__Hashes__Response    import Schema__Html__To__Dict__Hashes__Response
from mgraph_ai_service_html.html__fast_api.schemas.html.Schema__Html__To__Text__Hashes__Response    import Schema__Html__To__Text__Hashes__Response


class test_Html__Hash__Transformations(TestCase):

    @classmethod
    def setUpClass(cls):                                         # ONE-TIME expensive setup
        cls.transformations = Html__Hash__Transformations()

    def test__init__(self):                                      # Test auto-initialization
        with Html__Hash__Transformations() as _:
            assert type(_)                                   is Html__Hash__Transformations
            assert type(_.html_direct_transformations)       is Html__Direct__Transformations

    def test__html__to__dict__hashes__simple_html(self):         # Test simple HTML with single text node
        html = Safe_Str__Html("<p>Hello</p>")

        response = self.transformations.html__to__dict__hashes(html)

        assert type(response)                                is Schema__Html__To__Dict__Hashes__Response
        assert response.html_dict                            is not None
        assert type(response.hash_mapping)                   is Type_Safe__Dict
        assert response.total_text_hashes                    == 1
        assert response.node_count                           >  0
        assert response.max_depth                            >= 0
        assert type(response.max_depth_reached)              is bool

        hash_value = list(response.hash_mapping.keys())[0]
        assert len(hash_value)                               == 10    # 10-char hash
        assert response.hash_mapping[hash_value]             == "Hello"
        assert response.json()                               == { 'html_dict'           : { 'attrs' : {}                                         ,
                                                                                            'nodes' : [ { 'data': '8b1a9953c4', 'type': 'TEXT' } ],
                                                                                            'tag'   : 'p'                                         } ,
                                                                   'max_depth'          : 1                                                       ,
                                                                   'max_depth_reached'  : False                                                  ,
                                                                   'node_count'         : 2                                                       ,
                                                                   'hash_mapping'       : { '8b1a9953c4': 'Hello' }                               ,
                                                                   'total_text_hashes'  : 1                                                       }


        assert response.obj()                                == __( html_dict           = __( tag   = 'p'                               ,
                                                                                              attrs = __()                              ,
                                                                                              nodes = [__( type = 'TEXT',
                                                                                                           data = '8b1a9953c4' )]       ) ,
                                                                    hash_mapping        = __(_8b1a9953c4 = 'Hello')                      ,
                                                                    node_count          = 2                                              ,
                                                                    max_depth           = 1                                              ,
                                                                    total_text_hashes   = 1                                              ,
                                                                    max_depth_reached   = False                                          )


    def test__html__to__dict__hashes__multiple_text_nodes(self): # Test multiple text nodes
        html        = Safe_Str__Html("<div><p>First</p><span>Second</span><p>Third</p></div>")
        response    = self.transformations.html__to__dict__hashes(html)
        text_values = list(response.hash_mapping.values())

        assert response.total_text_hashes    == 3
        assert len(response.hash_mapping)    == 3
        assert type(response.hash_mapping)   is Type_Safe__Dict
        assert "First"                       in text_values
        assert "Second"                      in text_values
        assert "Third"                       in text_values

        assert obj(response.hash_mapping) == __(_7fb55ed0b7='First' ,
                                                        c22cf8376b='Second',
                                                       _168909c0b6='Third' )


    def test__html__to__dict__hashes__nested_structure(self):    # Test deeply nested HTML
        html = Safe_Str__Html("<div><div><div><p>Nested</p></div></div></div>")

        response = self.transformations.html__to__dict__hashes(html)

        assert response.total_text_hashes   == 1
        assert response.max_depth           >  0
        assert "Nested"                     in response.hash_mapping.values()
        assert obj(response.hash_mapping)   == __(_13c479c348='Nested')

    def test__html__to__dict__hashes__empty_tags(self):          # Test empty tags produce no text
        html = Safe_Str__Html("<div><p></p><span></span></div>")

        response = self.transformations.html__to__dict__hashes(html)

        assert response.total_text_hashes   == 0
        assert len(response.hash_mapping)   == 0
        assert obj(response.hash_mapping)   == __()

    def test__html__to__dict__hashes__with_max_depth(self):      # Test max_depth parameter
        html         = Safe_Str__Html("<div><div><div><div><p>Deep</p></div></div></div></div>")
        max_depth    = Safe_UInt(2)

        response = self.transformations.html__to__dict__hashes(html, max_depth=max_depth)

        assert response.max_depth_reached                    == True
        assert response.total_text_hashes                    == 0    # Too deep to extract
        assert obj(response.hash_mapping)             == __()

    def test__html__to__dict__hashes__default_max_depth(self):   # Test default max_depth value
        html = Safe_Str__Html("<p>Test</p>")

        response = self.transformations.html__to__dict__hashes(html)

        assert response.max_depth_reached                    == False
        assert response.total_text_hashes                    == 1
        assert obj(response.hash_mapping)             == __(_0cbc6611f5='Test')

    def test__html__to__dict__hashes__complex_structure(self):   # Test complex HTML structure
        html = Safe_Str__Html("""<div>
                                    <h1>Title</h1>
                                    <p>Paragraph with <strong>bold</strong> text</p>
                                    <ul>
                                        <li>Item 1</li>
                                        <li>Item 2</li>
                                    </ul>
                                </div>
                            """)

        response = self.transformations.html__to__dict__hashes(html)

        assert response.total_text_hashes   >= 4    # Title, Paragraph, Item 1, Item 2
        assert response.node_count          >  5
        assert response.obj() ==             __( html_dict           = __( tag   = 'div' ,
                                                 attrs = __()    ,
                                                 nodes = [ __( tag   = 'h1' ,
                                                               attrs = __()  ,
                                                               nodes = [ __( type = 'TEXT'           ,
                                                                            data = 'b78a322350' ) ] ) ,
                                                          __( tag   = 'p'     ,
                                                             attrs = __()     ,
                                                             nodes = [ __( type = 'TEXT'           ,
                                                                          data = '47b74c884c' )   ,
                                                                       __( tag   = 'strong'       ,
                                                                          attrs = __()            ,
                                                                          nodes = [ __( type = 'TEXT'          ,
                                                                                       data = '69dcab4a73' ) ] ) ,
                                                                       __( type = 'TEXT'          ,
                                                                          data = 'ea1f576750' ) ] ) ,
                                                          __( tag   = 'ul'    ,
                                                             attrs = __()     ,
                                                             nodes = [ __( tag   = 'li'           ,
                                                                          attrs = __()            ,
                                                                          nodes = [ __( type = 'TEXT'          ,
                                                                                       data = 'f59e6f3afd' ) ] ) ,
                                                                       __( tag   = 'li'           ,
                                                                          attrs = __()            ,
                                                                          nodes = [ __( type = 'TEXT'          ,
                                                                   data = '9eda28f018' ) ] ) ] ) ] ) ,
                                                 hash_mapping = __( b78a322350  = 'Title'          ,
                                                                           _47b74c884c = 'Paragraph with ',
                                                                           _69dcab4a73 = 'bold'           ,
                                                                           ea1f576750  = ' text'          ,
                                                                           f59e6f3afd  = 'Item 1'         ,
                                                                           _9eda28f018 = 'Item 2'         ) ,
                                                 node_count          = 13                                ,
                                                 max_depth           = 3                                 ,
                                                 total_text_hashes   = 6                                 ,
                                                 max_depth_reached   = False                             )

        assert response.json() == { 'html_dict': {'attrs': {},
                                                  'nodes': [{'attrs': {},
                                                             'nodes': [{'data': 'b78a322350', 'type': 'TEXT'}],
                                                             'tag': 'h1'},
                                                            {'attrs': {},
                                                             'nodes': [{'data': '47b74c884c', 'type': 'TEXT'},
                                                                       {'attrs': {},
                                                                        'nodes': [{'data': '69dcab4a73',
                                                                                   'type': 'TEXT'}],
                                                                        'tag': 'strong'},
                                                                       {'data': 'ea1f576750', 'type': 'TEXT'}],
                                                             'tag': 'p'},
                                                            {'attrs': {},
                                                             'nodes': [{'attrs': {},
                                                                        'nodes': [{'data': 'f59e6f3afd',
                                                                                   'type': 'TEXT'}],
                                                                        'tag': 'li'},
                                                                       {'attrs': {},
                                                                        'nodes': [{'data': '9eda28f018',
                                                                                   'type': 'TEXT'}],
                                                                        'tag': 'li'}],
                                                             'tag': 'ul'}],
                                                  'tag': 'div'},
                                    'max_depth': 3,
                                    'max_depth_reached': False,
                                    'node_count': 13,
                                    'hash_mapping': {'47b74c884c': 'Paragraph with ',
                                                            '69dcab4a73': 'bold',
                                                            '9eda28f018': 'Item 2',
                                                            'b78a322350': 'Title',
                                                            'ea1f576750': ' text',
                                                            'f59e6f3afd': 'Item 1'},
                                    'total_text_hashes': 6}


    def test__html__to__dict__hashes__special_characters(self):  # Test special characters preserved
        html        = Safe_Str__Html('<p>Hello & "World"</p>')
        response    = self.transformations.html__to__dict__hashes(html)
        text_values = list(response.hash_mapping.values())

        assert response.total_text_hashes    >  0
        assert any('&' in val or '"'        in val for val in text_values)
        assert text_values                  == ['Hello & "World"']

    def test__html__to__dict__hashes__unicode_text(self):        # Test Unicode support
        html       = Safe_Str__Html("<p>Hello 世界 🌍</p>")
        response   = self.transformations.html__to__dict__hashes(html)
        text_value = list(response.hash_mapping.values())[0]

        assert response.total_text_hashes                   == 1
        assert "世界"                                        in text_value
        assert "🌍"                                         in text_value
        assert response.hash_mapping.values()        == ['Hello 世界 🌍']
        assert response.hash_mapping.values().obj () == ['Hello 世界 🌍']
        assert response.hash_mapping.values().json() == ['Hello 世界 🌍']

    def test__html__to__dict__hashes__hash_format(self):         # Test hash format is correct
        html = Safe_Str__Html("<p>Test</p>")

        response = self.transformations.html__to__dict__hashes(html)

        for hash_value in response.hash_mapping.keys():
            assert len(hash_value)                           == 10
            assert all(c in '0123456789abcdef' for c in hash_value.lower())

        assert response.hash_mapping.keys().obj () == ['0cbc6611f5']
        assert response.hash_mapping.keys().json() == ['0cbc6611f5']

    def test__html__to__text__hashes__simple_html(self):         # Test lightweight endpoint
        html = Safe_Str__Html("<p>Hello</p>")

        response = self.transformations.html__to__text__hashes(html)

        assert type(response)                                is Schema__Html__To__Text__Hashes__Response
        assert type(response.hash_mapping)            is Type_Safe__Dict
        assert response.total_text_hashes                    == 1
        assert type(response.max_depth_reached)              is bool
        assert hasattr(response, 'html_dict')                is False                                               # No html_dict in lightweight
        assert hasattr(response, 'node_count')               is False                                               # No node_count either
        assert response.obj()                                == __(hash_mapping = __(_8b1a9953c4='Hello'),
                                                                   total_text_hashes   = 1                      ,
                                                                   max_depth_reached   = False                  )

    def test__html__to__text__hashes__multiple_nodes(self):      # Test multiple nodes lightweight
        html        = Safe_Str__Html("<div><p>First</p><span>Second</span></div>")
        response    = self.transformations.html__to__text__hashes(html)
        text_values = list(response.hash_mapping.values())
        assert response.total_text_hashes   == 2
        assert "First"                      in text_values
        assert "Second"                     in text_values
        assert text_values                  == ['First', 'Second']

    def test__html__to__text__hashes__with_max_depth(self):      # Test max_depth in lightweight
        html      = Safe_Str__Html("<div><div><div><p>Deep</p></div></div></div>")
        max_depth = Safe_UInt(2)
        response  = self.transformations.html__to__text__hashes(html, max_depth=max_depth)

        assert response.max_depth_reached   == True
        assert response.total_text_hashes   == 0
        assert response.obj()               == __(hash_mapping =__() ,
                                                 total_text_hashes    = 0   ,
                                                 max_depth_reached    = True)

    def test__html__to__text__hashes__empty_html(self):          # Test empty HTML
        html = Safe_Str__Html("")

        response = self.transformations.html__to__text__hashes(html)

        assert response.total_text_hashes        == 0
        assert len(response.hash_mapping) == 0
        assert response.obj()                    == __(hash_mapping =__()  ,
                                                       total_text_hashes   = 0    ,
                                                       max_depth_reached   = False)


    def test__html__to__text__hashes__matches_dict__hashes(self): # Test both endpoints same mapping
        html          = Safe_Str__Html("<p>Test</p><span>Content</span>")
        response_dict = self.transformations.html__to__dict__hashes(html)
        response_text = self.transformations.html__to__text__hashes(html)

        assert response_dict.hash_mapping             == response_text.hash_mapping
        assert response_dict.total_text_hashes               == response_text.total_text_hashes

        assert response_dict.obj() == __( html_dict=__(tag='p',
                                                       attrs=__(),
                                                       nodes=[__(type='TEXT', data='0cbc6611f5'),
                                                              __(tag='span',
                                                                 attrs=__(),
                                                                 nodes=[__(type='TEXT', data='f15c1cae78')])]),
                                          hash_mapping=__(_0cbc6611f5='Test', f15c1cae78='Content'),
                                          node_count=4,
                                          max_depth=2,
                                          total_text_hashes=2,
                                          max_depth_reached=False)
        assert response_text.obj() == __( hash_mapping = __(_0cbc6611f5 ='Test'   ,
                                                                    f15c1cae78 ='Content'),
                                          total_text_hashes   = 2   ,
                                          max_depth_reached   = False)

    def test__html_dict__with__hashes(self):                     # Test hash replacement in dict
        html_dict = { 'tag': 'p',
                      'attrs': {},
                      'nodes': [{'type': 'TEXT', 'data': 'test_hash'}] }
        text_nodes = {'test_hash': {'text': 'Original', 'tag': 'p'}}

        result = self.transformations.html_dict__with__hashes(html_dict, text_nodes)

        assert result == html_dict                          # Returns same dict

    def test__html_dict__with__xxx__simple(self):                # Test xxx masking simple case
        html_dict = { 'tag': 'p',
                      'attrs': {},
                      'nodes': [{'type': 'TEXT', 'data': '47bce5c74f'}] }
        text_nodes = {'47bce5c74f': {'text': 'Hello', 'tag': 'p'}}

        result = self.transformations.html_dict__with__xxx(html_dict, text_nodes)

        assert type(result)    is dict
        assert result['tag']   == 'p'
        assert result          == {'attrs': {}, 'nodes': [{'data': 'xxxxx', 'type': 'TEXT'}], 'tag': 'p'}
        assert obj(result)     == __( tag   = 'p' ,
                                      attrs = __(),
                                      nodes = [__(type = 'TEXT'  ,
                                                  data = 'xxxxx')])

    def test__html_dict__with__xxx__preserves_spaces(self):      # Test space preservation in xxx
        html_dict = { 'tag': 'p',
                      'attrs': {},
                      'nodes': [{'type': 'TEXT', 'data': '47bce5c74f'}]}
        text_nodes = {'47bce5c74f': {'text': 'Text With Spaces', 'tag': 'p'}}

        result = self.transformations.html_dict__with__xxx(html_dict, text_nodes)

        assert type(result) is dict
        assert result == {'attrs': {},
                          'nodes': [{'data': 'xxxx xxxx xxxxxx', 'type': 'TEXT'}],
                          'tag': 'p'}

    def test__html_dict__with__xxx__multiple_nodes(self):        # Test xxx with multiple text nodes
        html_dict = { 'tag': 'div',
                      'attrs': {},
                      'nodes': [ {'tag': 'p'   , 'attrs': {}, 'nodes': [{'type': 'TEXT', 'data': 'hash1'}]},
                                 {'tag': 'span', 'attrs': {}, 'nodes': [{'type': 'TEXT', 'data': 'hash2'}]} ] }
        text_nodes = { 'hash1': {'text': 'First', 'tag': 'p'},
                       'hash2': {'text': 'Second', 'tag': 'span'} }

        result = self.transformations.html_dict__with__xxx(html_dict, text_nodes)

        assert type(result)                                  is dict
        assert result['tag']                                 == 'div'
        assert result == {'attrs': {},
                          'nodes': [{'attrs': {},
                                     'nodes': [{'data': 'xxxxx', 'type': 'TEXT'}],
                                     'tag': 'p'},
                                    {'attrs': {},
                                     'nodes': [{'data': 'xxxxxx', 'type': 'TEXT'}],
                                     'tag': 'span'}],
                          'tag': 'div'}
        assert obj(result) == __( tag   = 'div',
                                  attrs = __() ,
                                  nodes = [ __(tag='p'   , attrs=__(), nodes=[__(type='TEXT', data='xxxxx' )]),
                                            __(tag='span', attrs=__(), nodes=[__(type='TEXT', data='xxxxxx')])])

    def test__count_nodes__simple_structure(self):               # Test node counting simple
        html_dict = { 'tag': 'p',
                      'attrs': {},
                      'nodes': [{'type': 'TEXT', 'data': 'Hello'}]}

        count = self.transformations.count_nodes(html_dict)

        assert type(count)  is Safe_UInt
        assert count        == 2

    def test__count_nodes__nested_structure(self):               # Test node counting nested
        html_dict = { 'tag': 'div',
                      'attrs': {},
                      'nodes': [ {'tag': 'p', 'attrs': {}, 'nodes': [{'type': 'TEXT', 'data': 'Hello'}]},
                                 {'tag': 'span', 'attrs': {}, 'nodes': [{'type': 'TEXT', 'data': 'World'}]} ]}

        count = self.transformations.count_nodes(html_dict)

        assert type(count)  is Safe_UInt
        assert count        == 5

    def test__count_nodes__empty_dict(self):                     # Test node counting empty
        html_dict = {}

        count = self.transformations.count_nodes(html_dict)

        assert type(count)  is Safe_UInt
        assert count        == 1                                # todo: double check this value, since shouldn't this be zero if html_dict is {}

    def test__count_nodes__null_dict(self):                     # Test node counting empty
        html_dict = None

        count = self.transformations.count_nodes(html_dict)

        assert type(count)  is Safe_UInt
        assert count        == 0

    def test__calculate_max_depth__simple(self):                 # Test depth calculation simple
        html_dict = { 'tag': 'p',
                      'attrs': {},
                      'nodes': [{'type': 'TEXT', 'data': 'Hello'}]}

        depth = self.transformations.calculate_max_depth(html_dict)

        assert type(depth)    is Safe_UInt
        assert depth          == 1

    def test__calculate_max_depth__nested(self):                 # Test depth calculation nested
        html_dict = {'tag'  : 'div' ,
                     'attrs': {}    ,
                     'nodes': [{'tag'  : 'div'  ,
                                'attrs': {}     ,
                                'nodes': [{ 'tag'  : 'p'    ,
                                            'attrs': {}     ,
                                            'nodes': [ { 'type': 'TEXT',
                                                         'data': 'Deep' } ]} ]} ] }

        depth = self.transformations.calculate_max_depth(html_dict)

        assert type(depth)    is Safe_UInt
        assert depth          ==  3                              # Multiple levels

    def test__calculate_max_depth__empty(self):                  # Test depth calculation empty
        html_dict = {}

        depth = self.transformations.calculate_max_depth(html_dict)

        assert type(depth)   is Safe_UInt
        assert depth         == 0                                # todo: review this value with the result from test__count_nodes__empty_dict (here we get 0, but in test__count_nodes__empty_dict we get 1)

    def test__check_depth_exceeded__not_exceeded(self):          # Test depth not exceeded
        html_dict = { 'tag'  : 'p',
                      'attrs': {},
                      'nodes': [{'type': 'TEXT',
                                 'data': 'Hello'}]}
        max_depth = Safe_UInt(10)

        exceeded = self.transformations.check_depth_exceeded(html_dict, max_depth)

        assert type(exceeded)                                is bool
        assert exceeded                                      == False

    def test__check_depth_exceeded__exceeded(self):              # Test depth exceeded
        html_dict  = { 'tag': 'div',
                       'attrs': {},
                       'nodes': [
                           {'tag': 'div', 'attrs': {}, 'nodes': [
                               {'tag': 'div', 'attrs': {}, 'nodes': [
                                   {'tag': 'p', 'attrs': {}, 'nodes': [
                                       {'type': 'TEXT', 'data': 'Deep'}]}]}]}]}
        max_depth = Safe_UInt(2)
        exceeded  = self.transformations.check_depth_exceeded(html_dict, max_depth)

        assert type(exceeded)  is bool
        assert exceeded        == True

    def test__check_depth_exceeded__boundary(self):              # Test depth at boundary
        html_dict = { 'tag': 'div',
                      'attrs': {},
                      'nodes': [ {'tag': 'p',
                                  'attrs': {},
                                  'nodes': [ {'type': 'TEXT', 'data': 'Text'}]} ] }
        max_depth = Safe_UInt(2)

        exceeded = self.transformations.check_depth_exceeded(html_dict, max_depth)

        assert type(exceeded)                                is bool
        assert exceeded == True

    def test__integration__complete_workflow(self):              # Test complete hash workflow
        html             = Safe_Str__Html("<p>Original text</p>")
        extract_response = self.transformations.html__to__dict__hashes(html)
        original_hash    = list(extract_response.hash_mapping.keys())[0]

        assert extract_response.total_text_hashes                  == 1
        assert extract_response.hash_mapping[original_hash] == "Original text"
        assert len(original_hash)                                  == 10

    def test__integration__multiple_text_nodes_workflow(self):   # Test workflow with multiple nodes
        html             = Safe_Str__Html("<div><p>First</p><span>Second</span><p>Third</p></div>")
        extract_response = self.transformations.html__to__dict__hashes(html)
        text_values      = list(extract_response.hash_mapping.values())

        assert extract_response.total_text_hashes         == 3
        assert len(extract_response.hash_mapping)  == 3
        assert "First"                                    in text_values
        assert "Second"                                   in text_values
        assert "Third"                                    in text_values

    def test__edge_case__whitespace_only(self):                  # Test whitespace-only text
        html = Safe_Str__Html("<p>   </p>")

        response = self.transformations.html__to__dict__hashes(html)

        assert response.total_text_hashes == 0    # Whitespace stripped

    def test__edge_case__malformed_html(self):                   # Test malformed HTML
        html = Safe_Str__Html("<p>Unclosed paragraph<div>Nested</div>")

        response = self.transformations.html__to__dict__hashes(html)

        assert response.total_text_hashes == 2    # Should parse
        assert response.obj()             == __(html_dict=__(tag='p',
                                                             attrs=__(),
                                                             nodes=[__(type='TEXT', data='3bc7818faf'),
                                                                    __(tag='div',
                                                                       attrs=__(),
                                                                       nodes=[__(type='TEXT', data='13c479c348')])]),
                                                hash_mapping=__(_3bc7818faf='Unclosed paragraph',
                                                                       _13c479c348='Nested'),
                                                node_count=4,
                                                max_depth=2,
                                                total_text_hashes=2,
                                                max_depth_reached=False)

    def test__edge_case__very_large_html(self):                  # Test performance with large HTML
        items = "".join([f"<li>Item {i}</li>" for i in range(100)])
        html  = Safe_Str__Html(f"<ul>{items}</ul>")

        import time
        start    = time.time()
        response = self.transformations.html__to__dict__hashes(html)
        elapsed  = time.time() - start

        assert response.total_text_hashes                    == 100
        assert elapsed                                       <  0.01  # Reasonable time (max 10ms)

    def test__type_safety__invalid_html_type(self):              # Test type safety for html param
        error_messsage = "Parameter 'html' expected type <class 'osbot_utils.type_safe.primitives.domains.web.safe_str.Safe_Str__Html.Safe_Str__Html'>, but got <class 'int'>"
        with pytest.raises(ValueError, match=error_messsage):
            self.transformations.html__to__dict__hashes(12345)   # Should fail type check


    def test__type_safety__invalid_max_depth_type(self):         # Test type safety for max_depth
        html          = Safe_Str__Html("<p>Test</p>")
        error_message = "Parameter 'max_depth' expected type <class 'osbot_utils.type_safe.primitives.core.Safe_UInt.Safe_UInt'>, but got <class 'str'>"

        with pytest.raises(ValueError, match=error_message):
            self.transformations.html__to__dict__hashes(html, max_depth="invalid")

    def test__response_schema__dict__hashes_complete(self):      # Test response has all fields
        html     = Safe_Str__Html("<p>Test</p>")
        response = self.transformations.html__to__dict__hashes(html)


        assert hasattr(response, 'html_dict'          )
        assert hasattr(response, 'hash_mapping')
        assert hasattr(response, 'node_count'         )
        assert hasattr(response, 'max_depth'          )
        assert hasattr(response, 'total_text_hashes'  )
        assert hasattr(response, 'max_depth_reached'  )
        assert type(response) == Schema__Html__To__Dict__Hashes__Response
        assert response.obj() == __(html_dict=__(tag='p',
                                                 attrs=__(),
                                                 nodes=[__(type='TEXT', data='0cbc6611f5')]),
                                   hash_mapping=__(_0cbc6611f5='Test'),
                                   node_count=2,
                                   max_depth=1,
                                   total_text_hashes=1,
                                   max_depth_reached=False)



    def test__response_schema__text__hashes_lightweight(self):   # Test lightweight response fields
        html = Safe_Str__Html("<p>Test</p>")

        response = self.transformations.html__to__text__hashes(html)

        assert hasattr(response, 'hash_mapping')
        assert hasattr(response, 'total_text_hashes')
        assert hasattr(response, 'max_depth_reached')
        assert not hasattr(response, 'html_dict')                    # Should NOT have these
        assert not hasattr(response, 'node_count')

        assert type(response) == Schema__Html__To__Text__Hashes__Response
        assert response.obj() == __( hash_mapping = __(_0cbc6611f5='Test'),
                                     total_text_hashes   = 1    ,
                                     max_depth_reached   = False)

    def test__consistency__same_input_same_output(self):         # Test deterministic behavior
        html = Safe_Str__Html("<p>Test</p>")

        response1 = self.transformations.html__to__dict__hashes(html)
        response2 = self.transformations.html__to__dict__hashes(html)

        assert response1.hash_mapping                 == response2.hash_mapping
        assert response1.total_text_hashes                   == response2.total_text_hashes

        assert response1.obj() == __( html_dict=__( tag='p',
                                                    attrs=__(),
                                                    nodes=[__(type='TEXT', data='0cbc6611f5')]),
                                       hash_mapping=__(_0cbc6611f5='Test'),
                                       node_count=2,
                                       max_depth=1,
                                       total_text_hashes=1,
                                       max_depth_reached=False)

        assert response1.obj() == response2.obj()