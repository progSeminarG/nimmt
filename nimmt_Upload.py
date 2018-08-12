#! /usr/bin/env python3

import argparse
import requests

class Uploader(object):
    def __init__(self,fig="stat.png",channel="CC71W2UQJ",filename=None,title=None):
        self.fig = fig
        self.channel = channel
        self.filename = filename
        self.title = title
        self.url = "https://slack.com/api/files.upload"

    def upload(self,token):
        self.token = token
        self.files_JSON = files = {"file":open(self.fig,'rb')}
        self.param_JSON = {
                "token":self.token,
                "channels":self.channel,
                "filename":self.filename,
                "title":self.title
                }
        requests.post(url=self.url, params=self.param_JSON, files=self.files_JSON)


if __name__ == '__main__':
    class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter,argparse.MetavarTypeHelpFormatter):
        pass
    parser = argparse.ArgumentParser(description="Upload figure", formatter_class=CustomFormatter)
    parser.add_argument('--token', type=str, nargs=1, required=True, help="token")
    parser.add_argument('--fig', '--file', type=str, dest='figfile', nargs='?', default='stat.png', help="figure")
    parser.add_argument('--channel', type=str, dest='channel', nargs='?', default='C0FJKDWR5', help="chnnel ID")
    parser.add_argument('--filename', type=str, dest='filename', nargs='?', default=None, help="upload file as <filename>")
    parser.add_argument('--title', type=str, dest='title', nargs='?', default=None, help="title of figure")
    parser.add_argument('--test', action="store_true", help="test mode: upload file to #random")

    args = parser.parse_args()

    if args.test:
        args.channel = "C0FB6UJ9J" # #random channel
    uploader_inst = Uploader(fig=args.figfile,channel=args.channel,filename=args.filename,title=args.title)
    uploader_inst.upload(args.token)

