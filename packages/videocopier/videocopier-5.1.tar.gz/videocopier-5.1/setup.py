from distutils.core import setup

setup(
    name = 'videocopier',
    version = '5.1',
    description = '视频下载工具',
    author = 'LJJ&MT',
    author_email = 'mu_zi_liu_ri@163.com',
    py_modules = ['videodownloader.downloader.bilibilidownloader',
                  'videodownloader.downloader.cntvdownloader',
                  'videodownloader.downloader.acfundownloader',
                  'videodownloader.downloader.youtubedownloader',
                  'videodownloader.downloader.fenghuangdownloader',
                  'videodownloader.util.moviepy_util',
                  'videodownloader.util.ffmpeg_util']
)