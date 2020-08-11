import requests
import json
from lxml import etree


url = "http://www.weather.com.cn/weather1d/101210101.shtml"
shi_url = "https://v1.jinrishici.com/all.json"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
                  Chrome/81.0.4044.92 Safari/537.36 "
}

shici_response = requests.get(shi_url, headers=headers)
shici_all_content = json.loads(shici_response.content.decode())
shici_result = shici_all_content['content'][:-1] + "（" + shici_all_content["author"] + "）"

weather_response = requests.get(url=url, headers=headers)
weather_result = weather_response.content.decode('utf-8')
weather_html = etree.HTML(weather_result)

# 今天夜间
night_wea_xp = {
    'wea_status': '/html/body/div[5]/div[1]/div[1]/div[2]/div[2]/ul/li[1]/p[1]',
    'dc': '/html/body/div[5]/div[1]/div[1]/div[2]/div[2]/ul/li[1]/p[2]/span',
    'wind_fx': '/html/body/div[5]/div[1]/div[1]/div[2]/div[2]/ul/li[1]/p[3]/span/@title',  # 风向
    'wind': '/html/body/div[5]/div[1]/div[1]/div[2]/div[2]/ul/li[1]/p[3]/span'
}
# 明天白天
tom_wea_xp = {
    'wea_status': '/html/body/div[5]/div[1]/div[1]/div[2]/div[2]/ul/li[2]/p[1]',
    'dc': '/html/body/div[5]/div[1]/div[1]/div[2]/div[2]/ul/li[2]/p[2]/span',
    'wind_fx': '/html/body/div[5]/div[1]/div[1]/div[2]/div[2]/ul/li[2]/p[3]/span/@title',
    'wind': '/html/body/div[5]/div[1]/div[1]/div[2]/div[2]/ul/li[2]/p[3]/span'

}


# 解析xpath 获取数值
def parse_xpath(str_xpath, html):
    values = html.xpath(str_xpath)
    return values


def get_night():
    wea = parse_xpath(night_wea_xp['wea_status'], weather_html)
    dc = parse_xpath(night_wea_xp['dc'], weather_html)
    wind_fx = parse_xpath(night_wea_xp['wind_fx'], weather_html)
    wind = parse_xpath(night_wea_xp['wind'], weather_html)

    return wea[0].text, dc[0].text, wind_fx[0], wind[0].text


def get_tom():
    t_wea = parse_xpath(tom_wea_xp['wea_status'], weather_html)
    t_dc = parse_xpath(tom_wea_xp['dc'], weather_html)
    t_wind_fx = parse_xpath(tom_wea_xp['wind_fx'], weather_html)
    t_wind = parse_xpath(tom_wea_xp['wind'], weather_html)
    return t_wea[0].text, t_dc[0].text, t_wind_fx[0], t_wind[0].text


wea, dc, wind_fx, wind = get_night()
t_wea, t_dc, t_wind_fx, t_wind = get_tom()

text = "天气播报来了,\n今天夜里{}, 温度{}, 风向{}{},\n明天白天{}, 温度{}, 风向{}{}, " \
       "\n每日诗词 --- {}"\
    .format(wea, dc, wind_fx, wind, t_wea, t_dc, t_wind_fx, t_wind, shici_result)

print(text)