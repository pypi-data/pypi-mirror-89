import codecs
import json
import os
from datetime import datetime
from typing import List
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from ruamel.yaml import YAML

from teko.helpers.clog import CLog
from teko.helpers.exceptions import TekoJiraException
from teko.models.jira_testcase import JiraTestcase, JiraTestScript, JiraTestScriptStep


class JiraService:
    """
    Jira API docs: https://support.smartbear.com/zephyr-scale-server/api-docs/v1/
    """
    def __init__(self, config={}):
        """

        :param config: a dict like this, if something is missing, it will get from env variable
                {
                    "server": "https://jira.teko.vn",
                    "username": "username",
                    "password": "password",
                    "project_key": "PRJ",
                }
        """
        load_dotenv()
        self.project_key = config.get('project_key') or os.getenv('JIRA_PROJECT_KEY')
        server = config.get('server') or os.getenv('JIRA_SERVER')
        username = config.get('username') or os.getenv('JIRA_USERNAME')
        password = config.get('password') or os.getenv('JIRA_PASSWORD')

        if not self.project_key or not server or not username or not password:
            msg = "No valide JIRA configuration found, please set JIRA_SERVER, JIRA_PROJECT_KEY, " \
                  "JIRA_USERNAME and JIRA_PASSWORD environment variables first"
            CLog.error(msg)
            raise TekoJiraException(msg)

        if not server.startswith("http://") and not server.startswith("https://"):
            server = "https://" + server
        self.base_api_url = urljoin(server, '/rest/atm/1.0')
        self.base_api_tests_url = urljoin(server, '/rest/tests/1.0')
        # self.issue_url = jira_settings['url'] + '/rest/api/latest/issue'

        self.s = requests.session()
        self.s.auth = (username, password)

    def search_testcases(self, issues=[], name=None):
        """

        :param issues: list of issue keys to filter
        :return:
        """
        query = f'projectKey = "{self.project_key}"'
        if issues:
            query += f' AND issueKeys IN ({",".join(issues)})'
        if name:
            query += f' AND name = "{name}"'

        params = {
            "query": query
        }

        url = self.base_api_url + "/testcase/search"

        res = self.s.get(url=url, params=params)

        if res.status_code != 200:
            CLog.error(f"HTTP Error {res.status_code}: {res.text}")
            return []
        raw = res.text

        testcases_json = json.loads(raw)
        # print(*testcases_json, sep="\n")

        print(json.dumps(testcases_json))

        testcases = []
        for t in testcases_json:
            testcases.append(JiraTestcase().from_dict(t))
        return testcases

    def delete_trace_link(self, link_id):
        url = self.base_api_url + "/tracelink/{link_id}"

        res = self.s.delete(url=url)

        if res.status_code != 200:
            CLog.error(f"HTTP Error {res.status_code}: {res.text}")
            return []
        raw = res.text

        testcases_json = json.loads(raw)

        print(json.dumps(testcases_json))

    def empty_trace_links(self, test_id):
        url_confluence = self.base_api_tests_url + f"/testcase/{test_id}/tracelinks/confluencepage"

        res = self.s.get(url=url_confluence)

        if res.status_code != 200:
            CLog.error(f"HTTP Error {res.status_code}: {res.text}")
        else:
            raw = res.text
            links = json.loads(raw)
            for link in links:
                self.delete_trace_link(link["id"])

        url_web = self.base_api_tests_url + f"/testcase/{test_id}/tracelinks/weblink"

        res = self.s.get(url=url_web)

        if res.status_code != 200:
            CLog.error(f"HTTP Error {res.status_code}: {res.text}")
        else:
            raw = res.text
            links = json.loads(raw)
            for link in links:
                self.delete_trace_link(link["id"])

    def add_links(self, test_id, confluences: List[str], webs: List[dict]):
        self.empty_trace_links(test_id)

        url = self.base_api_tests_url + "/tracelink/bulk/create"

        confluences_data = []

        for confluence_url in confluences:
            html = self.s.get(url=confluence_url)
            soup = BeautifulSoup(html.text, "html.parser")
            page_id = soup.find("meta", {"name": "ajs-page-id"})["content"]

            confluences_data.append({
                "testCaseId": test_id,
                "confluencePageId": page_id,
                "typeId": 1
            })

        webs_data = []

        for web in webs:
            if isinstance(web, str):
                webs_data.append({
                    "url": web,
                    "urlDescription": web,
                    "testCaseId": test_id,
                    "typeId": 1
                })
            else:
                webs_data.append({
                    "url": web.get('url'),
                    "urlDescription": web.get('description'),
                    "testCaseId": test_id,
                    "typeId": 1
                })

        if confluences_data:
            res = self.s.post(url=url, json=confluences_data)

            if res.status_code != 200:
                CLog.error(f"HTTP Error {res.status_code}: {res.text}")

        if webs_data:
            res = self.s.post(url=url, json=webs_data)

            if res.status_code != 200:
                CLog.error(f"HTTP Error {res.status_code}: {res.text}")

    def create_folder(self, name: str, type: str):
        data = {
            "projectKey": self.project_key,
            "name": name,
            "type": type
        }

        url = self.base_api_url + "/folder"

        """
        Ignore failure
        """
        res = self.s.post(url=url, json=data)
        if res.status_code != 201:
            CLog.info(f"Folder {name} has already exists")

    def get_test_id(self, test_key):
        url = self.base_api_tests_url + f"/testcase/{test_key}"

        res = self.s.get(url=url, params={"fields": "id"})
        if res.status_code != 200:
            CLog.error(f"HTTP Error {res.status_code}: {res.text}")
            return
        raw = res.text
        return json.loads(raw).get('id')

    def create_or_update_testcases_by_name(self, testcases: List[JiraTestcase], issues=[]):
        for testcase in testcases:
            existing_testcases = self.search_testcases(issues=issues, name=testcase.name)
            if not existing_testcases:
                key = self.create_testcase(testcase)
                CLog.info(f"New testcase created: {key}")
                testcase.key = key
            else:
                key = self.update_testcase(existing_testcases[0].key, testcase)
                CLog.info(f"Existing testcase updated: {key}")
                testcase.key = key
            if key:
                self.add_links(
                    test_id=self.get_test_id(key),
                    confluences=testcase.confluenceLinks,
                    webs=testcase.webLinks
                )
        return testcases

    def prepare_testcase_data(self, testcase: JiraTestcase):
        if not testcase.projectKey:
            testcase.projectKey = self.project_key

        data = {
            'name': testcase.name,
            'projectKey': testcase.projectKey,
            'folder': testcase.folder,
            'objective': testcase.objective,
            'precondition': testcase.precondition,
            'status': testcase.status
        }

        if testcase.testScript:
            testscript = testcase.testScript.to_dict()
            testscript.pop("id")
            if testscript["type"] == "PLAIN_TEXT":
                testscript.pop("steps")
            elif testscript["type"] == "STEP_BY_STEP":
                testscript.pop("text")
            data.update({'testScript': testscript})

        if testcase.folder == "":
            data.pop("folder")
        else:
            self.create_folder(testcase.folder, "TEST_CASE")

        if testcase.issueLinks:
            data['issueLinks'] = testcase.issueLinks

        return data

    def update_testcase(self, key:str, testcase: JiraTestcase):
        url = self.base_api_url + f"/testcase/{key}"
        data = self.prepare_testcase_data(testcase)
        data.pop('projectKey')
        res = self.s.put(url=url, json=data)

        if res.status_code != 200:
            CLog.error(f"HTTP Error {res.status_code}: {res.text}")
            return None

        return key

    def create_testcase(self, testcase: JiraTestcase):
        data = self.prepare_testcase_data(testcase)
        url = self.base_api_url + "/testcase"
        res = self.s.post(url=url, json=data)

        # print("data dict:", data)
        # print("url:", url)

        if res.status_code != 201:
            CLog.error(f"HTTP Error {res.status_code}: {res.text}")
            return None
        raw = res.text

        testcase_json = json.loads(raw)
        print(json.dumps(testcase_json))

        return testcase_json['key']

    def prepare_testrun_data(self, testcase: JiraTestcase):
        if not testcase.projectKey:
            testcase.projectKey = self.project_key

        data = {
            'testCaseKey': testcase.key,
            'status': testcase.testrun_status,
            'environment': testcase.testrun_environment,
            'executionTime': testcase.testrun_duration,
            'executionDate': testcase.testrun_date,
        }

        return data

    def create_test_cycle(self, testcases: List[JiraTestcase]):
        items_by_folder = dict()
        for testcase in testcases:
            existing_testcases = self.search_testcases(name=testcase.name)
            if not existing_testcases:
                CLog.warn(f"Testcase with name `{testcase.name}` not existed!")
            else:
                testcase.key = existing_testcases[0].key
                CLog.info(f"Testcase with name `{testcase.name}` existed: #{testcase.key}")
                if items_by_folder.get(testcase.testrun_folder) is None:
                    items_by_folder[testcase.testrun_folder] = []
                items_by_folder[testcase.testrun_folder].append(self.prepare_testrun_data(testcase))
        # print("items:", items)

        url = self.base_api_url + "/testrun"

        for folder, items in items_by_folder.items():
            data = {
                "projectKey": self.project_key,
                "name": f"[{self.project_key}] Cycle {datetime.now()}",
                "folder": folder,
                "items": items
            }

            if not folder:
                data.pop("folder")
            else:
                self.create_folder(folder, "TEST_RUN")

            print("data dict: ", data)

            res = self.s.post(url=url, json=data)

            if res.status_code != 201:
                CLog.error(f"HTTP Error {res.status_code}: {res.text}")
                return
            raw = res.text

            testcase_json = json.loads(raw)
            print(json.dumps(testcase_json))

            key = testcase_json['key']
            CLog.info(f"Test cycle `{key}` created!")

    @staticmethod
    def read_testcases_from_file(testcase_file):
        """

        :param testcase_file: yaml or json file
        :return:
        """
        filename, ext = os.path.splitext(testcase_file)
        print(os.path.abspath(testcase_file))
        if ext == ".json":
            with codecs.open(testcase_file, "r", encoding="utf-8") as f:
                testcase_data = json.load(f)
        elif ext == ".yaml":
            with codecs.open(testcase_file, "r", encoding="utf-8") as f:
                yaml = YAML(typ="safe")
                testcase_data = yaml.load(f)
        else:
            msg = f"File format not supported: {ext}"
            CLog.error(msg)
            raise TekoJiraException(msg)

        # print("data:", json.dumps(testcase_data))
        testcases = []
        for t in testcase_data:
            if t.get('folder') and t['folder'][0] != '/':
                t['folder'] = '/' + t['folder']
            if t.get('testrun_folder') and t['testrun_folder'][0] != '/':
                t['testrun_folder'] = '/' + t['testrun_folder']
            testcases.append(JiraTestcase().from_dict(t))

        return testcases

    @staticmethod
    def write_testcases_to_file(testcase_file, testcases):
        """

        :param testcase_file: yaml or json file
        :return:
        """
        testcases_json = []
        for t in testcases:
            print(t)
            data = t.to_dict()
            testcases_json.append(data)

        filename, ext = os.path.splitext(testcase_file)
        print(filename, ext)
        if ext == ".json":
            with codecs.open(testcase_file, "w", encoding="utf-8") as f:
                json.dump(testcases_json, f, indent=2)
        elif ext == ".yaml":
            with codecs.open(testcase_file, "w", encoding="utf-8") as f:
                yaml = YAML(typ="safe")
                yaml.indent(offset=2)
                yaml.dump(testcases_json, f)
        else:
            msg = f"File format not supported: {ext}"
            CLog.error(msg)
            raise TekoJiraException(msg)

        return None


def test():
    jira_srv = JiraService()

    # testscript = JiraTestScript(text="From ABC to XYZ")
    testscript = JiraTestScript(type="STEP_BY_STEP",
                                steps=[JiraTestScriptStep(description="<b>Step 1</b>",
                                                          testData="<strong>XYZ</strong>",
                                                          expectedResult="res1"),
                                       JiraTestScriptStep(description="Step2", expectedResult="res2"),
                                       JiraTestScriptStep(description="Step3", expectedResult="res3"),
                                       ])
    testcase = JiraTestcase(name="THUC TEST UNIQUE 3",
                            objective="Test submit testcase from Teko cli tools 2",
                            testScript=testscript)

    # key = jira_srv.create_or_update_testcase_by_name(testcase, issues=['TESTING-1'])

    testcases = jira_srv.search_testcases()
    # testcases = jira_srv.search_testcases(issues=['TESTING-1'], name="THUC TEST UNIQUE 3")

    for t in testcases:
        print(t)


if __name__ == "__main__":
    # test()

    jira_srv = JiraService()

    testcase_file = "../../../sample/testcases.json"
    testcases = JiraService.read_testcases_from_file(testcase_file)

    for t in testcases:
        print(t)

    jira_srv.create_or_update_testcases_by_name(testcases)

    print("\nAfter:\n")
    for t in testcases:
        print(t)

    testcycle_file = "../../../sample/testcycles.json"
    testcases = JiraService.read_testcases_from_file(testcycle_file)
    jira_srv.create_test_cycle(testcases)



