import re
import urllib3
from bs4 import BeautifulSoup
from lxml import etree

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

        if hasattr(target_tag, 'stripped_strings'):
            result = ''
            for string in target_tag.stripped_strings:
                result += ' ' + string
            result = re.sub('\s+', ' ', result).strip()
            return result
        else:
            return ''

    @staticmethod
    def convert_lxml_element_to_string(target_elem, truncate=-1):
        '''
        Input:
            lxml.etree._Element | string target_elem
                the element to be converted
                if it is error message, it is of string type
            int truncate
                maximum number of characters allowed
                if truncated, "..." will be appended such that total length is exactly truncate
        Output:
            string
                a string concatenating all strings in target_elem
        '''

        result = ''
        if hasattr(target_elem, 'itertext') and callable(target_elem.itertext):
            for string in target_elem.itertext():
                if isinstance(string, str):
                    result += ' ' + string
        elif isinstance(target_elem, str):
            result += ' ' + target_elem
        result = re.sub('\s+', ' ', result).strip()
        if truncate >= 3:
            if len(result) > truncate:
                result = result[0: truncate - 3] + "..."
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
            list<bs4.element.Tag | NoneType>
                bs4.element.Tag: tag matching the regular expression rexpr
                NoneType: URL not found / rexpr not found
        '''

        soup = ParseHtml._url_to_soup(url, 'html.parser')
        if soup is not None:
            matches = soup.find_all(text=re.compile(rexpr))
            matching_tags = [tag.parent for tag in matches]
            return matching_tags
        else:
            return [None for tag in matches]

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
            list<bs4.element.Tag | NoneType>
                bs4.element.Tag: tag having the first exact match for each full_tag in full_tags
                NoneType: URL not found / tag not found
        '''

        soup = ParseHtml._url_to_soup(url, 'html.parser')
        if soup is not None:
            return [ParseHtml._retrieve_first_tag_match(full_tag, soup) for full_tag in full_tags]
        else:
            return [None for full_tag in full_tags]

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
            list<bs4.element.Tag | NoneType>
                bs4.element.Tag: tag with the same hierarchical position as hierarchy_tag for each hierarchy_tag in hierarchy_tags
                NoneType: URL not found / tag not found
        '''

        raise NotImplemented('netgrep: retrieve_hierarchical_tags_matches is still under construction')

    @classmethod
    def retrieve_xpath_matches(cls, xpath_pattern, url):
        '''
        Retreieve the lxml elements matching the xpath_pattern
        TODO: Fix:
            XPath still has problem extracting certain html tags and causing obvious artifacts
            Especially for html comment blocks

        Input:
            string xpath_pattern
                String in XPath format, which specifies the elements
            string url
                The url of the target webpage
        Output:
            list<lxml.etree._Element>
                lxml.etree._Element: elements having the first exact match for xpath_pattern
                empty list is returned if target is not found
        '''

        # TODO: Use centralized webpage getter
        http_pool = urllib3.PoolManager(
            timeout=urllib3.Timeout(connect=1.0,  read=2.0),
            retries=urllib3.Retry(2, redirect=2)
        )
        try:
            page = http_pool.request('GET', url)
            html_str = page.data.decode("utf-8")

            html_elem = etree.HTML(html_str)
            try:
                matches = html_elem.xpath(xpath_pattern)
            except etree.XPathSyntaxError as e:
                return ["Error: invalid selector syntax: {}".format(e)]
            except etree.XPathEvalError as e:
                return ["Error: cannot evaluate selector format: {}".format(e)]

            return matches
        except urllib3.exceptions.BodyNotHttplibCompatible:
            return ["Error: target site cannot be parsed"]
        except urllib3.exceptions.ConnectionError:
            return ["Error: error occurs during connection"]
        except urllib3.exceptions.NewConnectionError:
            return ["Error: fails to connect"]
        except urllib3.exceptions.TimeoutError:
            return ["Error: connection timeout"]
        except urllib3.exceptions.MaxRetryError:
            return ["Error: too many retries"]
        except Exception as e:
            print("FATAL: unexpected error. ", e)
            raise
        return ["Error: unknown"]


    ''' ********** Below are private methods ********** '''

    @classmethod
    def _url_to_soup(cls, url, parser = 'html.parser'):
        '''
        Return the BeautifulSoup object corresponding to the supplied url
        Does not guarantee to return a real time updated version

        Input:
            string url
        Successful output:
            BeautifulSoup soup
                The BeautifulSoup object containing the contents of target website
        Special output:
            NoneType
                Not found
        '''

        if parser != 'html.parser':
            raise NotImplemented('netgrep: only html.parser is currently supported')

        # TODO: Should be moved as class variable later to avoid multiple allocation
        # TODO: Cache retrieved webpages and only refresh every some intervals
        http_pool = urllib3.PoolManager(
            timeout=urllib3.Timeout(connect=1.0,  read=2.0),
            retries=urllib3.Retry(2, redirect=2)
        )
        try:
            page = http_pool.request('GET', url)
            soup = BeautifulSoup(page.data, parser)
            return soup
        except urllib3.exceptions.BodyNotHttplibCompatible:
            return None
        except urllib3.exceptions.ConnectionError:
            return None
        except urllib3.exceptions.NewConnectionError:
            return None
        except urllib3.exceptions.TimeoutError:
            return None
        except urllib3.exceptions.MaxRetryError:
            # TODO: raise more meaningful message
            return None
        except Exception as e:
            print("FATAL: unexpected error. ", e)
            raise

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
        Successful output:
            bs4.element.Tag
                containing whole section of the target part
        Special output:
            NoneType
                Not found
        '''

        try:
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
        except:
            print("Error: Trying to search for:", target_tag)
            # TODO: return the reason causing error
            return None

if __name__ == "__main__":
    # For testings
    testcase = 3
    siuon_url = 'http://www.cse.cuhk.edu.hk/~siuon/csci4230/'
    if testcase == 1:
        #target_tags = ['<section id="topics">', '<div class="login">', '<ul class="news">', '<thead>']
        target_tags = ['<>']
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
    if testcase == 3:
        #siuon_url = 'fake'
        xpath_pattern = '//*[(@id = "news")]'
        xpath_pattern = 'randomwrongformat'
        matches = ParseHtml.retrieve_xpath_matches(xpath_pattern, siuon_url)
        for elem in matches:
            print(ParseHtml.convert_lxml_element_to_string(elem))
