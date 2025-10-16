import difflib
from unittest                                                     import TestCase
from fastapi.testclient                                           import TestClient
from mgraph_ai_service_html.html__fast_api.Html_Service__Fast_API import Html_Service__Fast_API


class test_Round_Trip_Validation(TestCase):

    @classmethod
    def setUpClass(cls):                                         # ONE-TIME expensive setup
        with Html_Service__Fast_API() as api:
            api.setup()
            cls.app    = api.app()
            cls.client = TestClient(cls.app)

    def _calculate_similarity(self, str1: str, str2: str) -> float:  # Helper: calculate text similarity
        """Calculate similarity ratio between two strings (0.0 to 1.0)"""
        return difflib.SequenceMatcher(None, str1, str2).ratio()

    def test__simple_html(self):                                 # Basic round-trip validation
        original = "<html><body>Test</body></html>"

        response = self.client.post('/html/to/html',
                                   json={'html': original})

        assert response.status_code == 200
        roundtrip = response.text

        assert 'html' in roundtrip.lower()                       # Key elements preserved
        assert 'body' in roundtrip.lower()
        assert 'Test' in roundtrip

    def test__simple_html__exact_match(self):                    # Test for exact preservation
        original = "<html><body><p>Exact Test</p></body></html>"

        response = self.client.post('/html/to/html',
                                   json={'html': original})

        assert response.status_code == 200
        roundtrip = response.text

        assert '<p>Exact Test</p>' in roundtrip                  # Exact content match

    def test__nested_structure(self):                            # Nested elements preservation
        original = "<html><body><div><p>Hello</p><span>World</span></div></body></html>"

        response = self.client.post('/html/to/html',
                                   json={'html': original})

        assert response.status_code == 200
        roundtrip = response.text

        assert 'Hello' in roundtrip                              # Content preserved
        assert 'World' in roundtrip
        assert '<p>'   in roundtrip or 'p>' in roundtrip         # Structure preserved
        assert '<span>' in roundtrip or 'span>' in roundtrip

    def test__with_attributes(self):                             # Attribute preservation
        original = '<html><body><div class="container" id="main"><p class="text">Content</p></div></body></html>'

        response = self.client.post('/html/to/html',
                                   json={'html': original})

        assert response.status_code == 200
        roundtrip = response.text

        assert 'Content' in roundtrip                            # Content preserved
        assert 'class'   in roundtrip or 'id' in roundtrip       # At least some attributes

    def test__with_text_extraction(self):                        # Full pipeline test
        original = "<html><body><p>Test Content</p></body></html>"

        response1 = self.client.post('/html/to/text/nodes',      # Step 1: Extract text nodes
                                    json={'html': original})
        assert response1.status_code == 200
        text_nodes = response1.json()['text_nodes']

        response2 = self.client.post('/html/to/dict',            # Step 2: Get html_dict
                                    json={'html': original})
        assert response2.status_code == 200
        html_dict = response2.json()['html_dict']

        response3 = self.client.post('/hashes/to/html',          # Step 3: Reconstruct (no changes)
                                    json={'html_dict'   : html_dict,
                                          'hash_mapping': {}     })

        assert response3.status_code == 200
        reconstructed = response3.text

        assert 'Test Content' in reconstructed or 'Test' in reconstructed  # Content preserved

    def test__complex_wikipedia_style(self):                     # Real-world complex HTML
        original = """
        <html>
            <head>
                <meta charset="UTF-8">
                <title>Test Article</title>
            </head>
            <body>
                <div id="content">
                    <h1>Main Article Title</h1>
                    <div class="intro">
                        <p>This is the introduction paragraph with <b>bold text</b> and <i>italic text</i>.</p>
                    </div>
                    <div class="section">
                        <h2>First Section</h2>
                        <p>Section content here with <a href="#">a link</a>.</p>
                        <ul>
                            <li>First item</li>
                            <li>Second item with <code>code</code></li>
                            <li>Third item</li>
                        </ul>
                    </div>
                    <div class="section">
                        <h2>Second Section</h2>
                        <p>More content with <span class="highlight">highlighted text</span>.</p>
                        <table>
                            <tr>
                                <th>Header 1</th>
                                <th>Header 2</th>
                            </tr>
                            <tr>
                                <td>Cell 1</td>
                                <td>Cell 2</td>
                            </tr>
                        </table>
                    </div>
                </div>
            </body>
        </html>
        """

        response = self.client.post('/html/to/html',
                                   json={'html': original})

        assert response.status_code == 200
        roundtrip = response.text

        similarity = self._calculate_similarity(original, roundtrip)
        assert similarity > 0.70                                 # At least 70% similarity

        assert 'Main Article Title' in roundtrip                 # Key content preserved
        assert 'introduction paragraph' in roundtrip
        assert 'First Section' in roundtrip
        assert 'Second Section' in roundtrip

    def test__bbc_article_style(self):                           # BBC-style article structure
        original = """
        <html>
            <body>
                <article>
                    <header>
                        <h1>Breaking News: Important Event</h1>
                        <time datetime="2024-01-15">January 15, 2024</time>
                    </header>
                    <section class="summary">
                        <p>This is a summary of the breaking news story.</p>
                    </section>
                    <section class="content">
                        <p>First paragraph of detailed content.</p>
                        <p>Second paragraph with more information.</p>
                        <blockquote>
                            <p>A quote from a relevant source.</p>
                        </blockquote>
                        <p>Final paragraph with conclusion.</p>
                    </section>
                    <footer>
                        <p>Related articles: <a href="#">Link 1</a>, <a href="#">Link 2</a></p>
                    </footer>
                </article>
            </body>
        </html>
        """

        response = self.client.post('/html/to/html',
                                   json={'html': original})

        assert response.status_code == 200
        roundtrip = response.text

        similarity = self._calculate_similarity(original, roundtrip)
        assert similarity > 0.70                                 # At least 70% similarity

        assert 'Breaking News' in roundtrip                      # Content verification
        assert 'summary' in roundtrip
        assert 'detailed content' in roundtrip

    def test__table_structure(self):                             # Table preservation
        original = """
        <html>
            <body>
                <table border="1">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Age</th>
                            <th>City</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Alice</td>
                            <td>30</td>
                            <td>New York</td>
                        </tr>
                        <tr>
                            <td>Bob</td>
                            <td>25</td>
                            <td>London</td>
                        </tr>
                    </tbody>
                </table>
            </body>
        </html>
        """

        response = self.client.post('/html/to/html',
                                   json={'html': original})

        assert response.status_code == 200
        roundtrip = response.text

        assert 'Alice' in roundtrip                              # Table data preserved
        assert 'Bob'   in roundtrip
        assert '30'    in roundtrip
        assert '25'    in roundtrip

    def test__list_structures(self):                             # List preservation
        original = """
        <html>
            <body>
                <h2>Ordered List</h2>
                <ol>
                    <li>First item</li>
                    <li>Second item</li>
                    <li>Third item</li>
                </ol>
                <h2>Unordered List</h2>
                <ul>
                    <li>Bullet point 1</li>
                    <li>Bullet point 2</li>
                    <li>Bullet point 3</li>
                </ul>
            </body>
        </html>
        """

        response = self.client.post('/html/to/html',
                                   json={'html': original})

        assert response.status_code == 200
        roundtrip = response.text

        assert 'First item'      in roundtrip                    # List content preserved
        assert 'Bullet point 1'  in roundtrip

    def test__deeply_nested_structure(self):                     # Deep nesting preservation
        original = """
        <html>
            <body>
                <div>
                    <div>
                        <div>
                            <div>
                                <div>
                                    <p>Very deep content</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </body>
        </html>
        """

        response = self.client.post('/html/to/html',
                                   json={'html': original})

        assert response.status_code == 200
        roundtrip = response.text

        assert 'Very deep content' in roundtrip                  # Content survives depth

    def test__whitespace_handling(self):                         # Whitespace policy test
        original = """
        <html>
            <body>
                <p>Text with    multiple   spaces</p>
                <p>Text with
                newlines</p>
            </body>
        </html>
        """

        response = self.client.post('/html/to/html',
                                   json={'html': original})

        assert response.status_code == 200
        roundtrip = response.text

        assert 'multiple' in roundtrip                           # Content preserved
        assert 'newlines' in roundtrip

    def test__empty_elements(self):                              # Empty element handling
        original = """
        <html>
            <body>
                <div></div>
                <p></p>
                <span>Content</span>
            </body>
        </html>
        """

        response = self.client.post('/html/to/html',
                                   json={'html': original})

        assert response.status_code == 200
        roundtrip = response.text

        assert 'Content' in roundtrip                            # Non-empty preserved

    def test__special_characters(self):                          # Special character preservation
        original = """
        <html>
            <body>
                <p>Text with &amp; ampersand</p>
                <p>Text with &lt; less than</p>
                <p>Text with &gt; greater than</p>
                <p>Text with &quot; quotes</p>
            </body>
        </html>
        """

        response = self.client.post('/html/to/html',
                                   json={'html': original})

        assert response.status_code == 200
        roundtrip = response.text

        assert 'ampersand'    in roundtrip                       # Text content preserved
        assert 'less than'    in roundtrip
        assert 'greater than' in roundtrip

    def test__unicode_characters(self):                          # Unicode preservation
        original = """
        <html>
            <body>
                <p>Unicode: â˜… â™¥ â˜º</p>
                <p>Japanese: æ—¥æœ¬èªž</p>
                <p>Emoji: ðŸ˜€ ðŸ'</p>
            </body>
        </html>
        """

        response = self.client.post('/html/to/html',
                                   json={'html': original})

        assert response.status_code == 200
        roundtrip = response.text

        assert 'Unicode:' in roundtrip                           # Unicode text present
        assert 'Japanese:' in roundtrip

    def test__form_elements(self):                               # Form element preservation
        original = """
        <html>
            <body>
                <form>
                    <label for="name">Name:</label>
                    <input type="text" id="name" name="name">
                    <label for="email">Email:</label>
                    <input type="email" id="email" name="email">
                    <button type="submit">Submit</button>
                </form>
            </body>
        </html>
        """

        response = self.client.post('/html/to/html',
                                   json={'html': original})

        assert response.status_code == 200
        roundtrip = response.text

        assert 'Name:' in roundtrip                              # Label text preserved
        assert 'Email:' in roundtrip
        assert 'Submit' in roundtrip

    def test__malformed_html(self):                              # Malformed HTML handling
        original = "<html><body><p>Unclosed paragraph<div>Nested</div>"

        response = self.client.post('/html/to/html',
                                   json={'html': original})

        assert response.status_code == 200
        roundtrip = response.text

        assert 'Unclosed paragraph' in roundtrip                 # Content preserved
        assert 'Nested' in roundtrip

    def test__script_style_preservation(self):                   # Script/style element handling
        original = """
        <html>
            <head>
                <style>body { color: blue; }</style>
                <script>console.log('test');</script>
            </head>
            <body>
                <p>Content</p>
            </body>
        </html>
        """

        response = self.client.post('/html/to/html',
                                   json={'html': original})

        assert response.status_code == 200
        roundtrip = response.text

        assert 'Content' in roundtrip                            # Body content preserved

    def test__performance__large_document(self):                 # Large document round-trip
        html_parts = ["<html><body>"]
        for i in range(200):
            html_parts.append(f"<p>Paragraph {i} with some content to make it realistic.</p>")
        html_parts.append("</body></html>")
        original = "".join(html_parts)

        response = self.client.post('/html/to/html',
                                   json={'html': original})

        assert response.status_code == 200
        roundtrip = response.text

        assert 'Paragraph 0'   in roundtrip                      # First preserved
        assert 'Paragraph 199' in roundtrip                      # Last preserved

        similarity = self._calculate_similarity(original, roundtrip)
        assert similarity > 0.80                                 # High similarity for large doc