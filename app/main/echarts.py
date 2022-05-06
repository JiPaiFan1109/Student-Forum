from pyecharts import options as opts
from pyecharts.charts import WordCloud, Liquid
from pyecharts.globals import SymbolType
from pyecharts.commons.utils import JsCode
from flask.json import jsonify

from . import main
from ..models import Category, User

import random

#词云图部分
def getWordPair(font):
    all_categories = []
    all_heat = []
    word_pair = []
    for i in Category.query.with_entities(Category.name).all():
        all_categories.append(i[0])
    for i in Category.query.with_entities(Category.heat).all():
        all_heat.append(i[0])
    for i in range(len(all_categories)):
        word_pair.append([all_categories[all_heat.index(max(all_heat))], font[i]])
        all_heat[all_heat.index(max(all_heat))] = -1
    return word_pair

def wordCloud_base(wordPair) -> WordCloud:
    cloud = (
         WordCloud()
        .add(series_name = "Category", data_pair = wordPair, shape = SymbolType.DIAMOND)
        .set_global_opts(
        title_opts=opts.TitleOpts(title="Category Heat", pos_left="center", pos_right="center", title_textstyle_opts=opts.TextStyleOpts(font_size=30)),
        tooltip_opts=opts.TooltipOpts(is_show=True)
                        )
            )
    return cloud

@main.route('/WordCloud')
def getWordCloud():
    font = [10000, 6181, 4386, 4055, 2467, 2244, 1868, 1484, 1112, 865,
            847, 582, 555, 550, 462, 366, 360, 282, 273, 265]
    wordCloud = wordCloud_base(getWordPair(font))
    return wordCloud.dump_options_with_quotes()

@main.route("/getDynamicWordCloud")
def update_word_cloud():
    font1 = [10000, 6181, 4386, 4055, 2467, 2244, 1868, 1484, 1112, 865,
            847, 582, 555, 550, 462, 366, 360, 282, 273, 265]
    wordpair1 = getWordPair(font1)

    font2 = [6181, 10000, 4055, 4386, 2244, 2467, 1484, 1868, 865, 1112,
            582, 847, 550, 555, 366, 462, 282, 360, 265, 273]
    wordpair2 = getWordPair(font2)

    luckyWordPair = random.choice(wordpair1, wordpair2)
    return jsonify(luckyWordPair)



#在线人数部分
def getOnlinePopulation():
    onlinePopulation =User.query.filter_by(statue = 1).count()
    return onlinePopulation

def getProportion():
    online = User.query.filter_by(statue = 1).count()
    userPopulation = User.query.count()
    proportion = online/userPopulation
    return proportion

def liquid_base(proportion) -> Liquid:
    liquidBall = (
        Liquid()
        .add("Online Population", data=[proportion, proportion-0.1], color=["#1598ED","#45BDFF"]
             ,is_outline_show=False
             ,shape="path://M367.855,428.202c-3.674-1.385-7.452-1.966-11.146-1.794c0.659-2.922,0.844-5.85,0.58-8.719 c-0.937-10.407-7.663-19.864-18.063-23.834c-10.697-4.043-22.298-1.168-29.902,6.403c3.015,0.026,6.074,0.594,9.035,1.728 c13.626,5.151,20.465,20.379,15.32,34.004c-1.905,5.02-5.177,9.115-9.22,12.05c-6.951,4.992-16.19,6.536-24.777,3.271 c-13.625-5.137-20.471-20.371-15.32-34.004c0.673-1.768,1.523-3.423,2.526-4.992h-0.014c0,0,0,0,0,0.014 c4.386-6.853,8.145-14.279,11.146-22.187c23.294-61.505-7.689-130.278-69.215-153.579c-61.532-23.293-130.279,7.69-153.579,69.202 c-6.371,16.785-8.679,34.097-7.426,50.901c0.026,0.554,0.079,1.121,0.132,1.688c4.973,57.107,41.767,109.148,98.945,130.793 c58.162,22.008,121.303,6.529,162.839-34.465c7.103-6.893,17.826-9.444,27.679-5.719c11.858,4.491,18.565,16.6,16.719,28.643 c4.438-3.126,8.033-7.564,10.117-13.045C389.751,449.992,382.411,433.709,367.855,428.202z"
             ,label_opts=opts.LabelOpts(formatter="{} Online".format(getOnlinePopulation()), font_size = 30, position = [80,100])
             )
        .set_global_opts(title_opts=opts.TitleOpts(title="Online Population", pos_left="center", pos_right="center", pos_top="40px"))
    )
    return liquidBall

@main.route("/LiquidBall")
def getLiquidBall():
    liquidball = liquid_base(getProportion())
    return liquidball.dump_options_with_quotes()



