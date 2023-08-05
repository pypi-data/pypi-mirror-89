# -*- coding: utf-8 -*-
import requests
import re
import os
import json
import sys

'''
B站视频下载模块

@author: LJJ&MT
'''

export_folder = r'./'
user_agent = r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
cookie = r"LIVE_BUVID=AUTO3115713170022340; stardustvideo=1; rpdid=|(u|kk)J|m))0J'ul~uJu~|Yk; sid=89160sq9; im_notify_type_13878796=0; LIVE_PLAYER_TYPE=1; buvid3=F064F543-B276-4DF9-8E06-17DE02A3CEDD155832infoc; blackside_state=1; dy_spec_agreed=1; CURRENT_FNVAL=80; _uuid=612E4207-FE02-8D41-220B-20911597179B18512infoc; bp_video_offset_13878796=449935491123664012; PVID=8; finger=158939783; DedeUserID=4661578; DedeUserID__ckMd5=ec615f9d7d365898; SESSDATA=37e75701%2C1619331024%2C2196a*a1; bili_jct=e998f74ae827f1bda15dd43b0ebc5efd; CURRENT_QUALITY=120"
dl_headers = {
    'Referer': r'https://www.bilibili.com/video/BV1aV41127Ay',
    'User-Agent': user_agent,
    'cookie': cookie
}


def getVideoCode(url):
    '''
            解析url获取视频编号，作为文件夹名
    '''
    if url.startswith(r"BV") or url.startswith(r"ss") or url.startswith(r"ep") :
        return url.split('?')[0]
    else:
        return url.split('?')[0].split(r'/')[-1]


def __epdl(url, single_video=False):
    '''
            下载ep类型的视频或ss剧集
    '''
    folder_name = getVideoCode(url)
    os.mkdir(os.path.join(export_folder, folder_name))
    if url.startswith(r"ss") or url.startswith(r'ep'):
        url = r'https://www.bilibili.com/bangumi/play/' + url
    if url.startswith(r"www"):
        url = r'https://' + url
    
    epList = []
    if folder_name.startswith(r'ep') and single_video:
        epList.append(folder_name)
    else:
        pageHTML = requests.get(url, headers=dl_headers).text
        epListStr = re.findall(r'"epList":(.+?)]', pageHTML)[0] + r']'
        epInfo = json.loads(epListStr)
        for singleInfo in epInfo:
            epList.append(r'ep' + str(singleInfo[r'id']))
    
    print("共有", len(epList), "个视频需要下载")
    for i, ep in enumerate(epList):
        index = i + 1
        epUrl = r'https://www.bilibili.com/bangumi/play/' + ep
        pageHTML = requests.get(epUrl, headers=dl_headers).text
        videoScriptStr = re.findall(r'<script>window.__playinfo__=(.+?)</script>', pageHTML)[0]
        videoScriptStr = videoScriptStr + r'</script>'
        audioScriptStr = re.findall(r'"audio":(.+?)</script>', videoScriptStr)[0]
        videoStr = re.findall(r'"baseUrl":"(.+?)"', videoScriptStr)[0]
        audioStr = re.findall(r'"baseUrl":"(.+?)"', audioScriptStr)[0]
        print('正在下载第', index, '个视频:', ep)
        save_video_name = ep + r'.mp4'
        video = open(os.path.join(export_folder, folder_name, save_video_name), 'wb')
        res = requests.get(videoStr,stream=True, headers=dl_headers)
        totallength = int(res.headers.get('content-length'))
        datalength = 0
        for block in res.iter_content(chunk_size=10240):
            datalength += len(block)
            video.write(block)
            done = int(50 * datalength / totallength)
            sys.stdout.write("\r[%s%s] %s%%" % ('=' * done, ' ' * (50 - done), done / 50 * 100))
            sys.stdout.flush()
        video.close()
        print(ep, '视频部分已下载完成')

        print('正在下载第', index, '个音频:', ep)
        save_audio_name = ep + r'.mp3'
        audio = open(os.path.join(export_folder, folder_name, save_audio_name), 'wb')
        res = requests.get(audioStr,stream=True, headers=dl_headers)
        totallength = int(res.headers.get('content-length'))
        datalength = 0
        for block in res.iter_content(chunk_size=10240):
            datalength += len(block)
            audio.write(block)
            done = int(50 * datalength / totallength)
            sys.stdout.write("\r[%s%s] %s%%" % ('=' * done, ' ' * (50 - done), done / 50 * 100))
            sys.stdout.flush()
        audio.close()
        print(ep, '音频部分已下载完成')
    print("全部下载完成")

    
def __bvdl(url):
    '''
            下载bv类型的视频
    '''
    if url.startswith(r"BV"):
        url = r'https://www.bilibili.com/video/' + url
    if url.startswith(r"www"):
        url = r'https://' + url
    bv = getVideoCode(url)
    certainPart = False
    if not 'p=' in url:
        url = url.split('?')[0]
    else:
        certainPart = True

    os.mkdir(os.path.join(export_folder, bv))

    part = 1
    while True:
        part_url = ''
        if certainPart and part == 1:
            part_url = url
        elif certainPart and part == 2:
            break
        else:
            part_url = url + r'?p=' + str(part)
        pageHTML = requests.get(part_url, headers=dl_headers).text

        videoScriptStr = ''
        try:
            videoScriptStr = re.findall(r'<script>window.__playinfo__=(.+?)</script>', pageHTML)[0]
        except:
            break
        videoScriptStr = videoScriptStr + r'</script>'
        audioScriptStr = re.findall(r'"audio":(.+?)</script>', videoScriptStr)[0]
        videoStr = re.findall(r'"baseUrl":"(.+?)"', videoScriptStr)[0]
        audioStr = re.findall(r'"baseUrl":"(.+?)"', audioScriptStr)[0]
        print('正在下载', bv, '的第', part, '个视频')
        save_video_name = bv + r'-Part' + str(part) + r'.mp4' if not certainPart else bv + r'.mp4'
        video = open(os.path.join(export_folder, bv, save_video_name), 'wb')
        res = requests.get(videoStr,stream=True, headers=dl_headers)
        totallength=int(res.headers.get('content-length'))
        datalength = 0
        for block in res.iter_content(chunk_size=10240):
            datalength += len(block)
            video.write(block)
            done = int(50 * datalength / totallength)
            sys.stdout.write("\r[%s%s] %s%%" % ('=' * done, ' ' * (50 - done), done / 50 * 100))
            sys.stdout.flush()

        video.close()
        print(bv, '的第', part, '个视频已下载完成')

        print('正在下载', bv, '的第', part, '个音频')
        save_audio_name = (bv + r'-Part' + str(part) + r'.mp3') if not certainPart else (bv + r'.mp3')
        audio = open(os.path.join(export_folder, bv, save_audio_name), 'wb')
        res = requests.get(audioStr,stream=True, headers=dl_headers)
        totallength = int(res.headers.get('content-length'))
        datalength = 0
        for block in res.iter_content(chunk_size=10240):
            datalength += len(block)
            audio.write(block)
            done = int(50 * datalength / totallength)
            sys.stdout.write("\r[%s%s] %s%%" % ('=' * done, ' ' * (50 - done), done / 50 * 100))
            sys.stdout.flush()

        audio.close()
        print(bv, '的第', part, '个音频已下载完成')

        part = part + 1


    
    if part == 2 and not certainPart:
        os.rename(os.path.join(export_folder, bv, bv + r'-Part1.mp4'), os.path.join(export_folder, bv, bv + r'.mp4'))
        os.rename(os.path.join(export_folder, bv, bv + r'-Part1.mp3'), os.path.join(export_folder, bv, bv + r'.mp3'))

        
def biliDownload(url, single_video=False):
    '''
                下载视频
    '''
    if r'BV' in url:
        __bvdl(url)
    elif r'ep' in url or r'ss' in url:
        __epdl(url, single_video=single_video)
    else:
        print('不明确的视频类型')

    
if __name__ == '__main__':
    url=r'https://www.bilibili.com/bangumi/play/ep341486'
    biliDownload(url,single_video=False)


