from airtest.cli.runner import AirtestCase, run_script
import airtest.report.report as report
from airtest.report.report import simple_report

#from conf.send_email import send_email
from argparse import *
import shutil,os,io,jinja2,datetime
from airtest.core.helper import device_platform
from airtest.core.api import auto_setup, log, connect_device

log_path = "/Users/luodan/program/airtest/log"
air_path = "/Users/luodan/program/airtest/case"
root_path = "/Users/luodan/program/airtest/"
start_time = datetime.datetime.now()
start_time_fmt = start_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
results = []
root_log = log_path

for file in os.listdir(air_path):
    # 如果file中结尾带了“.air”
    if file.endswith(".air"):
        airName = file
        print("airName-->",airName)
        # 把“.air”换成空格,因为airtest自动生成的文件名带.air
        airDirName = file.replace(".air", "")
        # root\air\xxx.air，每个用例的脚本路径
        air_dir = air_path +'/'+ airDirName
        script = os.path.join(air_path, file)
        # root\log\\xxx,每个用例的测试报告
        air_log = os.path.join(root_path, "log/" + airDirName)  # 如果air_log是目录，删除其目录下的子目录及文件夹
        if os.path.isdir(air_log):
            print(air_log)
            # shutil.rmtree(air_log)
            pass

        else:
            os.makedirs(air_log)
            # html每个用例测试报告（html文件）存放的路径，root\log\\xxx\log.html
        html = os.path.join(air_log, "log.html")
        recording_mp4 = os.path.join(air_log, airDirName + ".mp4")
        # if deviceType.upper() == "WEB":
        #     args = Namespace(device=[], log=air_log, recording=None, script=script, language="zh", compress=0,
        #                      no_image=False)
        # elif deviceType.upper() == "APP":
        #     args = Namespace(device=device, log=air_log, recording=recording_mp4, script=script, language="zh",
        #                      compress=0, no_image=False)
        # else:
        device = "android://127.0.0.1:5037/NDF0217B10002156?cap_method=JAVACAP&&ori_method=MINICAPORI&&touch_method=MINITOUCH"
        args = Namespace(device=device, log=air_log, recording=None, script=script, language="zh",
                             compress=0, no_image=False)
        try:
            run_script(args, AirtestCase)  # airtest的run方法
        except:
            pass
        finally:
            # 将脚本路径和测试报告（截图）路径用report.py的LogToHtml生成html文件
            print("script-->",script)
            print("air_log-->",air_log)
            rpt = report.LogToHtml(script, air_log, lang="zh")
            # "log_template.html"报告名称，输出文件是HTML文件
            rpt.report("log_template.html", output_file=html)
            # simple_report(script, air_log,output=html,p)
            result = {}
            result["name"] = airName.replace('.air', '')
            result["result"] = rpt.test_result
            results.append(result)
end_time = datetime.datetime.now()
end_time_fmt = end_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
duration = (end_time - start_time).seconds
# jinja2是python的模板引擎（语法），loader模板加载器，FileSystemLoader从文件目录中获取模板
env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(root_path),
    extensions=(),
    autoescape=True
)
# template = env.get_template(template_name, template_path)
template = env.get_template('log_template.html', root_path)

project_name = root_path.split("\\")[-1]
success = 0
fail = 0
for res in results:
    if res['result']:
        success += 1
    else:
        fail += 1
report_name = end_time.strftime("%Y-%m-%d %H-%M-%S") + "SummayrReport" + ".html"
html = template.render(
    {"results": results, "device": "", "stime": start_time_fmt, 'etime': end_time_fmt,
     'duration': duration, "project": project_name, "success": success, "fail": fail})
output_file = os.path.join(root_path, "report", report_name)
print("report_name-->",report_name)
with io.open(output_file, 'w', encoding="utf-8") as f:
    f.write(html)

