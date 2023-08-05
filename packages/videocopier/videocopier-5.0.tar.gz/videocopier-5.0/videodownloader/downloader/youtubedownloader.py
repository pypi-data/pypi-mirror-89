# -*- coding: utf-8 -*-
import requests
import re
import os
import sys
import json
'''
youtube视频下载模块

@author: LJJ
'''

export_folder = r'./'
user_agent = r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
dl_headers = {
    'User-Agent': user_agent

}


def getVideoCode(url):
    '''
            解析url获取视频编号，作为文件夹名
    '''
    return url.split('?')[-1][2:]



def youtubeDownload(url):
    '''
                下载视频
    '''
    if url.startswith(r"www"):
        url = r'https://' + url
    video_code = getVideoCode(url)
    
    html = requests.get(url,headers=dl_headers).text
    video_url = re.findall(r'\\"url\\":\\"https:\\/\\/r(.+?)\\"', html)[0]
    video_url = re.sub(r'\\/',r'/',video_url)   
    video_url = 'https://r' + re.sub(r'\\\\u0026',r'&',video_url)
    
    print(r'开始下载')
    video = open(os.path.join(export_folder,video_code + r'.mp4'),'wb')
    res = requests.get(video_url,stream=True, headers=dl_headers)
    totallength = int(res.headers.get('content-length'))
    datalength = 0
    for block in res.iter_content(chunk_size=10240):
        datalength += len(block)
        video.write(block)
        done = int(50 * datalength / totallength)
        sys.stdout.write("\r[%s%s] %s%%" % ('=' * done, ' ' * (50 - done), done / 50 * 100))
        sys.stdout.flush()
    video.close()
    print(r'下载完成')

if __name__ == '__main__':
    url=r'https://www.youtube.com/watch?v=GlmE8cqWqaU&list=RDGlmE8cqWqaU&start_radio=1'
    print(getVideoCode(url))
    youtubeDownload(url)
    


