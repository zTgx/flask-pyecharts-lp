from flask import Flask
from jinja2 import Markup, Environment, FileSystemLoader
from pyecharts.globals import CurrentConfig

import pandas as pd

from pyecharts import options as opts
from pyecharts.charts import Pie
from pyecharts.charts import Bar

# 关于 CurrentConfig，可参考 [基本使用-全局变量]
CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("templates"))

app = Flask(__name__, static_folder="templates")

# 主数据结构
class LPData(object):
    """docstring for LPData"""
    def __init__(self, arg):
        super(LPData, self).__init__()
        self.arg = arg
        self.dataframe = pd.read_excel('data/data.xlsx', sheet_name=0, skiprows=1)

        self.dataframe.columns = ['id', 'sid', 'employer', 'job_catelog', 'job_name', 'job_desc', 
        'hdc', 'ratio', 'source', 'academic','degree', 'major', 'subjects', 'others', 'city', 'tel']

    # 招聘的城市
    def citys(self):
        if self.citys == None:
            self.citys = self.dataframe['city'].unique()
        
        return self.citys

    # 所有的用人单位
    def employers(self):
        return self.dataframe['employer'].unique()

    # 岗位类别
    def job_catelog(self):
        return self.dataframe['job_catelog'].unique()

    # 所有的岗位名称
    def job_name(self):
        return self.dataframe['job_name'].unique()

dt = LPData(0)

# 所有城市的招聘人数饼图
city_and_hds = {}
for city in list(dt.dataframe['city'].unique()):
    if False == isinstance(city, str):
        continue

    # print(city)
    city_and_hds[city] = int(dt.dataframe.loc[dt.dataframe['city'] == city].loc[:, 'hdc'].sum())
    
def pie() -> Pie:
    c = (
        Pie()
        .add("城市统计图", [list(z) for z in zip(city_and_hds.keys(), city_and_hds.values())])
        # .set_colors(["blue", "green", "yellow", "red", "pink", "orange", "purple"])
        # .set_global_opts(title_opts=opts.TitleOpts(title="Pie图"))
        # .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )

    return c

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
    # c = bar_base()
    c = pie()
    return Markup(c.render_embed())


if __name__ == "__main__":
    app.run()