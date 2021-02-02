# Import the modules that are required for execution

import pytest
from conftest import MultipleBrowserTest 
import colorama
import urllib.request

from app import app

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

@pytest.mark.skip(reason="Not being used yet")
class Test_Routes(MultipleBrowserTest):
        drivers = []
        def get_urls(self, method):
            links = []
            for rule in app.url_map.iter_rules():
                if method in rule.methods and has_no_empty_params(rule):
                    #url = url_for(rule.endpoint, **(rule.defaults or {}))
                    url = rule.rule
                    #links.append((url, rule.endpoint))
                    links.append(url)

            return links
        
        def test_get_routes(self, base_url):
            pass
            urls = self.get_urls("GET")
            for browser in self.drivers:
                print("\nTesting {}".format(browser.name))

                for url in urls:
                    print("  {}:".format(url), end=" ")
                    browser.get(base_url + url)
                    #assert 200 == urllib.request.urlopen('{}/{}'.format(base_url, url)).getcode()
                    print(colorama.Fore.GREEN + "✓" + colorama.Style.RESET_ALL)
