# Import the modules that are required for execution

import pytest
import colorama
import urllib.request
from urllib.error import HTTPError, URLError
from time import sleep
import socket
import http.client
import json

from app import app

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

class Test_Routes:
        verbose = False

        def test_get_routes(self, base_url, request):
            self.check_verbose_level(request)
            urls = self.get_urls("GET")
            self.url_runner(base_url, urls)

        def test_get_routes_with_params(self, base_url, request):
            self.check_verbose_level(request)

            # Commented out URLs currently have an error
            urls = [
                ("/laborHistory/modal/printPdf/2", None),
                #("/admin/emailTemplates/getPurpose/student", None), # getPurpose has changed
                ("/admin/emailTemplates/getEmail/Labor%20Status%20Form%20Submitted%20For%20Student", None),
                ("/laborstatusform/getcompliance/2114", None),
                ("/laborstatusform/getPositions/2114", None),
                ("/laborstatusform/getstudents/202000/B00841417/1", None),
                ("/laborstatusform/getstudents/202000/B00841417/0", None),
                ("/laborstatusform/getDate/202000", None),
                ("/laborHistory/modal/2", None),
                ("/admin/pendingForms/pendingLabor", None),
                ("/admin/getNotes/2", None),
                ("/main/department/1", None),
                #("/studentOverloadApp/2", None), # We can't test a student yet
                ("/laborReleaseForm/2", None),
                ("/laborstatusform/2", None),
                # ("/laborHistory/2", None) # TODO: Not sure if this should stay here or the next laborHistory test
                ("/alterLSF/2", None),
                ("/laborHistory/B00730361", None),
            ]
            self.url_runner(base_url, urls)

        @pytest.mark.skip(reason="Not complete")
        def test_post_routes(self, base_url, request):
            self.check_verbose_level(request)
            urls = [
                ("/laborHistory/modal/withdrawform", b"FormID=2"),
                ("/admin/emailTemplates/postEmail", b"body=test&purpose=Labor%20Status%20Form%20Submitted%20For%20Student"),
                ("/studentOverloadApp/update", {2: {"formID": 2, "Notes": "test"}}),
                #("/laborstatusform/getstudents/202000/B00841417", None),
                # ("/laborstatusform/userInsert", []),
                # ("/adminManagement/userInsert", []),
                # ("/termManagement/manageStatus", []),
                # ("/termManagement/setDate", []),
                # ("/laborHistory/download", []),
                # ("/admin/complianceStatus", []),
                # ("/admin/termManagement", []),
                # ("/admin/checkedForms", []),
                # ("/adjustLSF/submitModifiedForm/<laborStatusKey>", []),
                # ("/modifyLSF/updateLSF/<laborStatusKey>", []),
                # ("/admin/updateStatus/<raw_status>", []),
                # ("/admin/notesInsert/<formId>", []),
                # ("/laborReleaseForm/<laborStatusKey>", []),
            ]
            self.url_runner(base_url, urls)

        def get_urls(self, method):
            """Retrieve the application routes for the given method"""

            links = []
            for rule in app.url_map.iter_rules():
                if method in rule.methods and has_no_empty_params(rule):
                    #url = url_for(rule.endpoint, **(rule.defaults or {}))
                    url = rule.rule
                    links.append((url,None))

            return links

        def url_runner(self, base_url, urls):
            """Test a list of URLs"""

            if(self.verbose):
                print()
            for url,params in urls:
                sleep(.05) # Without this sleep we end up with Remote Disconnect exceptions
                if(self.verbose):
                    print("  {}:".format(url), end=" ")

                try:
                    req = urllib.request.Request('{}{}'.format(base_url, url))
                    data = params

                    # if parameters come in as an object, handle data as json
                    if isinstance(params, dict):
                        req.add_header('Content-Type', 'application/json; charset=utf-8')
                        jsondata = json.dumps(params)
                        jsondataasbytes = jsondata.encode('utf-8')
                        req.add_header('Content-Length', len(jsondataasbytes))
                        data = jsondataasbytes

                    assert 200 == urllib.request.urlopen(req, data).getcode()

                except HTTPError as e:
                    pytest.fail("HTTPError! HTML Status Code {}".format(e.code))
                except URLError as e:
                    pytest.fail("URLError! {}".format(e.reason))
                except socket.timeout as e:
                    pytest.fail("Timeout!")
                except http.client.HTTPException as e:
                    pytest.fail("Remote Disconnected!")
                else:
                    if(self.verbose):
                        print(colorama.Fore.GREEN + "✓" + colorama.Style.RESET_ALL)
                    pass

        def check_verbose_level(self, request):
            """Record the output level requested"""
            self.verbose = (request.config.getoption('verbose') >= 1)
