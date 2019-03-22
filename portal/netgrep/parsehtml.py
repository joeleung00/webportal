import re
import urllib3
from bs4 import BeautifulSoup

''' Checklist:
1. [X] Exception handling for invalid input arguments
2. [X] Injection prevention
3. [X] Unit test
4. [V] Documentation for all exporting interfaces
'''


class ParseHtml:

    def __init__(self):
        pass

    @staticmethod
    def convert_tag_to_string(target_tag):
        '''
        Input:
            bs4.element.Tag target_tag
                the tag to be converted
        Output:
            string
                a string concatenating all strings in target_tag
        '''

        result = ''
        for string in target_tag.stripped_strings:
            result += ' ' + string
        result = re.sub('\s+', ' ', result).strip()
        return result

    @classmethod
    def grep_tags(cls, rexpr, url):
        '''
        Retrieve the tags with contents matching the regular expression rexpr

        Input:
            list<string> rexpr
            string url
                The url of the target webpage
        Output:
            list<bs4.element.Tag>
                list of tags matching the regular expression rexpr
        '''

        soup = ParseHtml._url_to_soup(url, 'html.parser')
        matches = soup.find_all(text=re.compile(rexpr))
        matching_tags = [tag.parent for tag in matches]
        return matching_tags

    @classmethod
    def retrieve_first_tags_matches(cls, full_tags, url):
        '''
        For every full_tag in full_tags,
            retrieve the first tag having exact match with the full_tag

        Input:
            list<string> full_tags
                Every element is the whole starting tag of the target section, but excludes the ending tag
                e.g. full_tags[0] = '<div class="login">', does not need '</div>'
            string url
                The url of the target webpage
        Output:
            list<bs4.element.Tag>
                list of tag having the first exact match for each full_tag in full_tags
        '''

        soup = ParseHtml._url_to_soup(url, 'html.parser')
        return [ParseHtml._retrieve_first_tag_match(full_tag, soup) for full_tag in full_tags]

    @classmethod
    def retrieve_hierarchical_tags_matches(cls, hierarchy_tags, url):
        '''
        UNDER CONSTRUCTION: standards are subject to change

        For every hierarchy_tag in hierarchy_tags,
            retrieve the tag with the same hierarchical position as hierarchy_tag

        Input:
            list<string> hierarchy_tags
                Every element is a string containing the ancestors/ancestors' siblings/siblings of the target tag
                Siblings are separated by comma
                No ending tag is needed
                e.g.
                    <html>
                        <head></head>
                        <body><h1> A </h1><h1> <b>B</b> <i>Target</i> </h1></body>
                    </html>
                hierarchy_tags[0] = '<html><body><h1>,<h1><b>,<i>'
            string url
                The url of the target webpage
        Output:
            list<bs4.element.Tag>
                list of tag with the same hierarchical position as hierarchy_tag for each hierarchy_tag in hierarchy_tags
        '''

        raise NotImplemented('netgrep: retrieve_hierarchical_tags_matches is still under construction')



    ''' ********** Below are private methods ********** '''

    @classmethod
    def _url_to_soup(cls, url, parser = 'html.parser'):
        '''
        Return the BeautifulSoup object corresponding to the supplied url
        Does not guarantee to return a real time updated version

        Input:
            string url
        Output:
            BeautifulSoup soup
                The BeautifulSoup object containing the contents of target website
        '''

        if parser != 'html.parser':
            raise NotImplemented('netgrep: only html.parser is currently supported')
        http = urllib3.PoolManager() # TODO: Should be moved as class variable later to avoid multiple allocation
        page = http.request('GET', url) # TODO: Cache retrieved webpages and only refresh every some intervals
        soup = BeautifulSoup(page.data, parser)
        return soup

    @classmethod
    def _retrieve_first_tag_match(cls, full_tag, soup):
        '''
        Retrieve the first tag having exact match with the full_tag
        This function can only handle one tag at once

        Input:
            string full_tag
                The whole starting tag of the target section, but excludes the ending tag
                e.g. full_tag = '<div class="login">', does not need '</div>'
            BeautifulSoup soup
                The BeautifulSoup object containing the contents of target website
        Output:
            bs4.element.Tag
                containing whole section of the target part
        '''

        # Evaluate the format of target tag
        tag_soup = BeautifulSoup(full_tag, 'html.parser')
        target_tag = tag_soup.contents[0]

        # Search for first match
        sections = soup.find_all(target_tag.name)
        result = ''
        for section in sections:
            if section.attrs == target_tag.attrs:
                return section
        else:
            return None

if __name__ == "__main__":
    # For testings
    testcase = 2
    siuon_url = 'http://www.cse.cuhk.edu.hk/~siuon/csci4230/'
    if testcase == 1:
        target_tags = ['<section id="topics">', '<div class="login">', '<ul class="news">', '<thead>']
        multiple = ParseHtml.retrieve_first_tags_matches(target_tags, siuon_url)
        for tag in multiple:
            if tag is not None:
                print(ParseHtml.convert_tag_to_string(tag), end='\n\n')
            else:
                print("Not found D:", end='\n\n')
    if testcase == 2:
        multiple = ParseHtml.grep_tags("learning", siuon_url)
        for tag in multiple:
            if tag is not None:
                print(ParseHtml.convert_tag_to_string(tag), end='\n\n')
            else:
                print("Not found D:", end='\n\n')
