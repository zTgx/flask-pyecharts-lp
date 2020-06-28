from flask import Flask
from jinja2 import Markup, Environment, FileSystemLoader
from pyecharts.globals import CurrentConfig

import pandas as pd

# 关于 CurrentConfig，可参考 [基本使用-全局变量]
CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("templates"))

from pyecharts import options as opts
from pyecharts.charts import Bar


app = Flask(__name__, static_folder="templates")

data = pd.read_excel('data/data.xlsx', sheet_name=0, skiprows=1)

# 岗位类别
leibies = {}
for x in data.index:
    item = data.loc[x]
    if item['地点'] == '山西太原':
        leibie = item['岗位类别']
        count = item['招考数量']
        if leibies.get(leibie) == None:
            leibies[leibie] = count

        t = leibies[leibie]
        tt = int(t + count)
        leibies[leibie] = tt

x = list(leibies.keys())
y = list(leibies.values())

if type(y) is list:
    print("YES y")
else:
    print("NO y")


def bar_base() -> Bar:
    c = (
        Bar()
        .add_xaxis(x)
        .add_yaxis("山西太原", y)
        .set_global_opts(title_opts=opts.TitleOpts(title="示例", subtitle="副标题"))
    )
    return c


@app.route("/")
def index():
    c = bar_base()
    return Markup(c.render_embed())


if __name__ == "__main__":
    app.run()