import requests
import json
import time
import csv
import re
class ContentSpider():
    """url指话题目录，如：https://www.zhihu.com/question/19603240
    headers包括user-agent和你的cookie即可
    offset控制从第几条数据开始"""
    url = 'https://www.zhihu.com/question/300985609'
    items = []
    def __init__(self, offset):
        with open('cookie.txt', 'rb') as f:
            cookie = f.read()
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
            'cookie': cookie
        }
        self.console_items = []
        self.api = 'https://www.zhihu.com/api/v4/questions/'+self.url.split('/')[-1]+'/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=10&offset={}&platform=desktop&sort_by=default'.format(offset) #每次请求5条数据，从format处开始
        self.get_data()
        self.sort_data()
        self.write_csv()
        self.console_print()
    def get_data(self): #通过ajax请求得到json数据
        rsp = requests.get(self.api, headers=self.headers)
        print(rsp.status_code)
#        print(rsp.content.decode('utf-8'))
        self.data = json.loads(rsp.content)['data']
    def sort_data(self): #给数据分类，内容content，作者author[name],评论数comment_count，赞成voteup_count，编辑时间戳updated_time
        for i in self.data:
            id = i['id']
            author = i['author']['name']
            updated_time = time.localtime(i['updated_time'])
            updated_time = time.strftime("%Y-%m-%d %H:%M:%S", updated_time)
            voteup_count = i['voteup_count']
            comment_count = i['comment_count']
            content = i['content']
            content = re.sub('<(.*?)>', '', content)
            link = self.url+'/answer/'+str(id)
            self.items.append([id, author, updated_time, voteup_count, comment_count, content, link])
            self.console_items.append([id, author, updated_time, voteup_count, comment_count, content, link])
    def write_csv(self):
        with open('data.csv', 'w', encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['ID', '作者', '编辑时间', '点赞数', '评论数', '内容', '网址'])
            for item in self.items:
                writer.writerow(item)
    def console_print(self):
        for i in self.console_items:
            print(i)

if __name__ == '__main__':
    offset = 0
    while True:
        spider = ContentSpider(offset)
        if not len(spider.data):
            print('爬取完毕!')
            break
        offset += 10
