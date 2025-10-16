from unittest import TestCase


class test__bugs__OSBot_Utils(TestCase):

    def test__bug__osbot_utils__obj__doesnt_handle_reserved_keywords(self):
        an_json = {"tag"   : "p",
                   "class" : "title"}

        #assert obj(an_json) == __(tag='p', class='title')  # todo: BUG this doesn't compile
