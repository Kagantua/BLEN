#coding:utf-8
from lib.core.log import loglogo

def Txt_output(filename,output_dict,target_list):
    with open(filename,"w") as f:
        for vuln_name in output_dict:
            loglogo("漏洞名：%s"%(vuln_name))
            f.write(vuln_name+"\n")
            loglogo("共测试url %d 条， %d 条存在漏洞"%(len(target_list),len(output_dict[vuln_name])))
            for vuln_url in output_dict[vuln_name]:
                f.write(vuln_url.split("||")[0].strip()+"\n")
            f.write("\n\n")
    loglogo("TXT格式报告输出至：%s"%(filename))

doc = ""
def Mkdn_output(filename,output_dict,target_list,actual_list,total_time):
    global doc
    doc += "<div align='center' ><font size='6'>检测报告</font></div>\n\n\n\
```\n\
oFx :: order by jijue\n\
```\n\n"
    doc += "|条目|数值|\n|-|-|\n|预计测试条数|{target_list_length}|\n|实际测试条数|{actual_list_length}|\n|共计耗时|{total_time}秒|\n\n".format(target_list_length = len(target_list),actual_list_length = len(actual_list),total_time = total_time)
    for poc_name in output_dict:
        doc += "### {}\n".format(poc_name)
        doc += "|url|title|\n"
        doc += "|-|-|\n"
        for vuln_url in output_dict[poc_name]:

            web_title = vuln_url.split("||")[1].strip()

            doc += "|{}|{}|\n".format(vuln_url.split("||")[0],web_title)
        
    with open(filename,"w") as f:
        f.write(doc)
    loglogo("Markdown格式报告输出至：%s"%(filename))

csv_doc = """
检测报告,,,,,
,,,,,
,,,,,
oFx :: order by jijue,,,,,
,,,,,
,,,,,
条目,数值,
预计测试条数,{target_list_length}条,
实际测试条数,{actual_list_length}条,
共计耗时,{total_time}秒,
,,,,,
,,,,,\n
"""
def Csv_output(filename,output_dict,target_list,actual_list,total_time):
    global csv_doc
    csv_doc = csv_doc.format(target_list_length = len(target_list),actual_list_length = len(actual_list),total_time = total_time)

    for poc_name in output_dict:
        csv_doc += "{},\nurl,title,,\n".format(poc_name)
        for vuln_url in output_dict[poc_name]:
            web_title = vuln_url.split("||")[1].strip()
            csv_doc += "{vuln_url},{web_title},\n".format(vuln_url=vuln_url.split("||")[0],web_title=web_title)
        csv_doc += ",,,,,\n,,,,,\n"
    with open(filename,"w") as f:
        f.write(csv_doc)
    loglogo("CSV格式报告输出至：%s" % (filename))