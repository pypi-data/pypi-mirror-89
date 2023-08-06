# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import absolute_import

from base64 import b64encode, b64decode
from collections import OrderedDict
from os.path import isfile
import datetime
import json
import os
import pkg_resources
import sys
import time
import bisect
import hashlib
import warnings
import re

try:
    from ansi2html import Ansi2HTMLConverter, style

    ANSI = True
except ImportError:
    # ansi2html is not installed
    ANSI = False

from py.xml import html, raw

from . import extras
from . import __version__, __pypi_url__

PY3 = sys.version_info[0] == 3

# Python 2.X and 3.X compatibility
if PY3:
    basestring = str
    from html import escape
else:
    from codecs import open
    from cgi import escape


def pytest_addhooks(pluginmanager):
    from . import hooks
    pluginmanager.add_hookspecs(hooks)


def pytest_addoption(parser):
    group = parser.getgroup('terminal reporting')
    group.addoption('--html', action='store', dest='htmlpath',
                    metavar='path', default=None,
                    help='create html report file at given path.')
    group.addoption('--self-contained-html', action='store_true',
                    help='create a self-contained html file containing all '
                         'necessary styles, scripts, and images - this means '
                         'that the report may not render or function where CSP '
                         'restrictions are in place (see '
                         'https://developer.mozilla.org/docs/Web/Security/CSP)')
    group.addoption('--css', action='append', metavar='path', default=[],
                    help='append given css file content to report style file.')


def pytest_configure(config):
    htmlpath = config.getoption('htmlpath')
    if htmlpath:
        for csspath in config.getoption('css'):
            open(csspath)
        if not hasattr(config, 'slaveinput'):
            # prevent opening htmlpath on slave nodes (xdist)
            config._html = HTMLReport(htmlpath, config)
            config.pluginmanager.register(config._html)


def pytest_unconfigure(config):
    html = getattr(config, '_html', None)
    if html:
        del config._html
        config.pluginmanager.unregister(html)


def data_uri(content, mime_type='text/plain', charset='utf-8'):
    data = b64encode(content.encode(charset)).decode('ascii')
    return 'data:{0};charset={1};base64,{2}'.format(mime_type, charset, data)


class HTMLReport(object):

    def __init__(self, logfile, config):
        logfile = os.path.expanduser(os.path.expandvars(logfile))
        self.logfile = os.path.abspath(logfile)#报告地址
        self.errors = self.failed = 0
        self.passed = self.skipped = 0
        self.xfailed = self.xpassed = 0
        has_rerun = config.pluginmanager.hasplugin('rerunfailures')#重试
        self.rerun = 0 if has_rerun else None
        #self.self_contained = config.getoption('self_contained_html')
        self.config = config
        self.results = {
        "testPass": 0,
        "testName": "测试报告",
        "testAll": 0,
        "testFail": 0,
        "beginTime": "",
        "totalTime": "",
        "testSkip": 0,
        "testError": 0,
        "testResult":[]}

    class TestResult:

        def __init__(self, report, config):
            self.test_id = report.nodeid
            if getattr(report, 'when', 'call') != 'call':
                self.test_id = '::'.join([report.nodeid, report.when])
            self.time = getattr(report, 'duration', 0.0)
            #self.self_contained = config.getoption('self_contained_html')
            self.config = config
            self.all={ "className": "",
                        "methodName": "",
                        "description": "",
                        "spendTime": '%.2f' % self.time+' s',
                        "status": report.outcome,
                        "img":"",
                        "log": [],
                        "log_err":[]}

            if hasattr(report,'className'):
                self.all['className'] = report.className

            if hasattr(report, 'methodName'):
                self.all['methodName']=  report.methodName

            self.all['description']=self.get_parameter(report)
            if hasattr(report,'extra'):
                self.all['img']=report.extra


            self.append_log(report)#加日志

            # self.config.hook.pytest_html_results_table_row(#hook
            #     report=report, cells=cells)
            #
            # self.config.hook.pytest_html_results_table_html(#hook
            #     report=report, data=self.additional_html)


        def get_parameter(self,report):
            file=test_class= test_method=""
            if report.nodeid.split('::').__len__()==3:
                file,test_class,test_method=report.nodeid.split('::')
            else:
                file, test_method=report.nodeid.split('::')

            return ''.join(re.findall('\[(.*?)\]', test_method))


        def append_log(self, report):
            if report.longrepr:
                for line in report.longreprtext.splitlines():
                    self.all['log_err'].append(escape(line))
                    # separator = line.startswith('_ ' * 10)
                    # if separator:
                    #     self.all['log_err'].append(line[:80])
                    # else:
                    #     exception = line.startswith("E   ")
                    #     if exception:
                    #         self.all['log_err'].append(escape(line))
                    #
                    #     else:
                    #         self.all['log_err'].append(escape(line))


            for section in report.sections:
                header, content = map(escape, section)

                import threading
                list_c = content.split('\n')

                for x in list_c:
                    if threading.current_thread().name in x:
                        self.all['log'].append(x)







    def _appendrow(self, outcome, report):
        result = self.TestResult(report, self.config)
        self.results['testResult'].append(result.all)
        #print(result)

    def append_passed(self, report):
        if report.when == 'call':
            if hasattr(report, "wasxfail"):
                self.xpassed += 1
                self._appendrow('XPassed', report)
            else:
                self.passed += 1
                self._appendrow('Passed', report)

    def append_failed(self, report):
        if getattr(report, 'when', None) == "call":
            if hasattr(report, "wasxfail"):
                # pytest < 3.0 marked xpasses as failures
                self.xpassed += 1
                self._appendrow('XPassed', report)
            else:
                self.failed += 1
                self._appendrow('Failed', report)
        else:
            self.errors += 1
            self._appendrow('Error', report)

    def append_skipped(self, report):
        if hasattr(report, "wasxfail"):
            self.xfailed += 1
            self._appendrow('XFailed', report)
        else:
            self.skipped += 1
            self._appendrow('Skipped', report)

    def append_other(self, report):
        # For now, the only "other" the plugin give support is rerun
        self.rerun += 1
        self._appendrow('Rerun', report)

    def _generate_report(self, session):
        # session.config.hook.pytest_html_results_summary(
        #     prefix=summary_prefix, summary=summary, postfix=summary_postfix)
        # session.config.hook.pytest_html_results_table_header(cells=cells)
        suite_stop_time = int(time.time())
        self.results['totalTime'] = str(suite_stop_time - self.suite_start_time)+'s'#执行时间
        self.results['testAll'] = self.passed + self.failed + self.xpassed + self.xfailed
        self.results['testPass']=self.passed  + self.xpassed
        self.results['testFail']=self.failed  + self.xfailed
        self.results['testSkip']=self.skipped
        self.results['testError']=self.errors


    def _generate_environment(self, config):
        if not hasattr(config, '_metadata') or config._metadata is None:
            return []

        metadata = config._metadata
        environment = [html.h2('测试环境')] 
        rows = []

        keys = [k for k in metadata.keys()]
        if not isinstance(metadata, OrderedDict):
            keys.sort()

        for key in keys:
            value = metadata[key]
            if isinstance(value, basestring) and value.startswith('http'):
                value = html.a(value, href=value, target='_blank')
            elif isinstance(value, (list, tuple, set)):
                value = ', '.join((str(i) for i in value))
            rows.append(html.tr(html.td(key), html.td(value)))

        environment.append(html.table(rows, id='environment'))
        return environment


    def _save_report(self, report_content):
        dir_name = os.path.dirname(self.logfile)
        assets_dir = os.path.join(dir_name, 'assets')

        from distutils.sysconfig import get_python_lib
        SITE_PAKAGE_PATH = get_python_lib()
        #config_tmp_path = SITE_PAKAGE_PATH + '/pytest_html/report.html'
        #config_tmp_path = os.path.abspath('.')+'/report.html'
        DIR = os.path.dirname(os.path.abspath(__file__))
        config_tmp_path = os.path.join(DIR, 'report.html')
        with open(config_tmp_path, 'rb') as file:
            body = file.readlines()
        with open(self.logfile, 'wb') as write_file:
            for item in body:
                if item.strip().startswith(b'var resultData'):
                    head = '    var resultData = '
                    item = item.decode().split(head)
                    item[1] = head + json.dumps(self.results, ensure_ascii=False, indent=4)
                    item = ''.join(item).encode()
                    item = bytes(item) + b';\n'
                write_file.write(item)



    def pytest_runtest_logreport(self, report):#入口
        if report.passed:
            self.append_passed(report)
        elif report.failed:
            self.append_failed(report)
        elif report.skipped:
            self.append_skipped(report)
        else:
            self.append_other(report)


    def pytest_collectreport(self, report):
        if report.failed:
            self.append_failed(report)


    def pytest_sessionstart(self, session):
        self.results['beginTime'] =time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.suite_start_time=int(time.mktime(time.strptime(self.results['beginTime'], '%Y-%m-%d %H:%M:%S')))



    def pytest_sessionfinish(self, session):
        report_content = self._generate_report(session)
        self._save_report(report_content)


    def pytest_terminal_summary(self, terminalreporter):
        terminalreporter.write_sep('-', 'generated html file: {0}'.format(
            self.logfile))
