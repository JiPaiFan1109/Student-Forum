from pyecharts import options as opts
from pyecharts.charts import WordCloud, Liquid
from pyecharts.globals import SymbolType
from flask.json import jsonify

from . import main
from ..models import Category, User

import random

#词云图部分
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
def liquid_base(proportion) -> Liquid:
    liquidBall = (
        Liquid()
        .add("Online Population", [proportion-0.1, proportion])
        .set_global_opts(title_opts=opts.TitleOpts(title="Online Population"))
    )
    return liquidBall

@main.route("/LiquidBall")
def getLiquidBall():
    liquidball = liquid_base(getProportion())
    return liquidball.dump_options_with_quotes()

def getProportion():
    online = User.query.filter_by(statue = 'True').count()
    userPopulation = User.query.count()
    proportion = online/userPopulation
    return proportion


