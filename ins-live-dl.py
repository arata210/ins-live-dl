import requests
import xml.etree.ElementTree as ET
import time
import os

t = dict()
url = input()
f_name = url.split('dash-abr/')[1].split('.mpd')[0]
os.makedirs(f_name)
t['mpd'] = url
"""
下载init文件
优化结构
实现多线程
加代理
下载文件存入video/audio文件夹
自动获取mpd
尝试逆推片头文件 live-from-start
"""
while 1:
    time.sleep(1.5)
    r0 = requests.get(url)

    if r0.status_code == 200:
        xml_data = r0.text
        # print(xml_data)

        # 现在您可以使用前面提供的代码解析XML数据
        # 请将xml_data替换为下载的XML内容
        root = ET.fromstring(xml_data)
        ns = {'mpd': 'urn:mpeg:dash:schema:mpd:2011'}

        # 使用单个循环
        for s_element in root.findall(
                './/mpd:AdaptationSet/mpd:Representation/mpd:SegmentTemplate/mpd:SegmentTimeline/mpd:S', ns):
            t_value = s_element.get('t')
            v = url.replace('dash-abr', 'live-pst-v').split('.mpd')[0] + '_0-' + t_value + '.m4v'
            a = url.replace('dash-abr', 'live-hd-a').split('.mpd')[0] + '_0-' + t_value + '.m4a'
            f1 = 'v_' + t_value.zfill(10) + ".mp4"
            f2 = 'a_' + t_value.zfill(10) + ".mp4"

            res1 = requests.get(v, stream=True)
            res2 = requests.get(a, stream=True)

            with open(f1, 'wb') as file:
                for chunk in res1.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
            with open(f2, 'wb') as file:
                for chunk in res2.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)

            t[t_value] = s_element.get('d')
            t[t_value] = s_element.get('d')

            # 只处理第一个 SegmentTimeline，可以通过 break 中断循环
            break

        print(f"\r{t}", end='', flush=True)
        f0 = open('backup_' + f_name + '.txt', 'w', encoding='utf-8')
        f0.write(str(t))
    else:
        print(f"Failed to download the file. Status code: {r0.status_code}")
