#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""https://www.zhihu.com/question/300985609"""
from tkinter import *
from tkinter.ttk import *
from threading import Thread
import time
class Application_ui(Frame):
    #这个类仅实现界面生成功能，具体事件处理代码在子类Application中。
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title('知乎话题收集装置 by 吾爱破解：xccxvb')
        self.master.geometry('537x290')
        self.createWidgets()

    def createWidgets(self):
        self.top = self.winfo_toplevel()

        self.style = Style()

        self.TreeView1Cols = ["ID","作者","编辑时间","点赞数","评论数","内容","网址"]    #TODO在这里添加标题列表，第一列固定为树形显示
        self.style.configure('TTreeView1.Treeview', font=('微软雅黑',9))
        self.TreeView1 = Treeview(self.top, show='headings', columns=self.TreeView1Cols, displaycolumns='#all', style='TTreeView1.Treeview')
        self.TreeView1.place(relx=0.03, rely=0.221, relwidth=0.896, relheight=0.700)
        for i in range(len(self.TreeView1Cols)):
            self.TreeView1.column(self.TreeView1Cols[i-1], width=100, anchor='center')
            self.TreeView1.heading(self.TreeView1Cols[i-1], text=self.TreeView1Cols[i-1])
        # ----水平滚动条------------
        vbar1 = Scrollbar(self.TreeView1, orient=VERTICAL, command=self.TreeView1.yview)
        self.TreeView1.configure(yscrollcommand=vbar1.set)
        vbar1.pack(side=RIGHT, fill=Y)
        # ----竖直滚动条----------
        hbar1 = Scrollbar(self.TreeView1, orient=HORIZONTAL, command=self.TreeView1.xview)
        self.TreeView1.configure(xscrollcommand=hbar1.set)
        hbar1.pack(side=BOTTOM, fill=X)

        self.Text1Var = StringVar(value='')
        self.Text1 = Entry(self.top, textvariable=self.Text1Var, font=('宋体',9))
        self.Text1.setText = lambda x: self.Text1Var.set(x)
        self.Text1.text = lambda : self.Text1Var.get()
        self.Text1.place(relx=0.104, rely=0.055, relwidth=0.687, relheight=0.086)

        self.Label1Var = StringVar(value='网址:')
        self.style.configure('TLabel1.TLabel', anchor='w', font=('微软雅黑',12))
        self.Label1 = Label(self.top, text='网址:', textvariable=self.Label1Var, style='TLabel1.TLabel')
        self.Label1.setText = lambda x: self.Label1Var.set(x)
        self.Label1.text = lambda : self.Label1Var.get()
        self.Label1.place(relx=0.015, rely=0.055, relwidth=0.076, relheight=0.086)

        self.Command1Var = StringVar(value='开始收集')
        self.style.configure('TCommand1.TButton', font=('微软雅黑',12))
        self.Command1 = Button(self.top, text='开始收集', textvariable=self.Command1Var, command=self.Command1_Cmd, style='TCommand1.TButton')
        self.Command1.setText = lambda x: self.Command1Var.set(x)
        self.Command1.text = lambda : self.Command1Var.get()
        self.Command1.place(relx=0.804, rely=0.028, relwidth=0.151, relheight=0.141)


class Application(Application_ui):
    #这个类实现具体的事件处理回调函数。界面生成代码在Application_ui中。
    def __init__(self, master=None):
        Application_ui.__init__(self, master)

    def Command1_Cmd(self, event=None):
        from SSpider import ContentSpider
        url = self.Text1Var.get()
        class BtnSpider(ContentSpider):
            def __init__(self, fulei, url, offset):
                self.fulei = fulei
                self.url = url
                super().__init__(offset)
            def sort_data(self):  # 给数据分类，内容content，作者author[name],评论数comment_count，赞成voteup_count，编辑时间戳updated_time
                for i, index in zip(self.data, range(len(self.data))):
                    id = i['id']
                    author = i['author']['name']
                    updated_time = time.localtime(i['updated_time'])
                    updated_time = time.strftime("%Y-%m-%d %H:%M:%S", updated_time)
                    voteup_count = i['voteup_count']
                    comment_count = i['comment_count']
                    content = i['content']
                    content = re.sub('<(.*?)>', '', content)
                    link = self.url + '/answer/' + str(id)
                    self.items.append([id, author, updated_time, voteup_count, comment_count, content, link])
                    self.console_items.append([id, author, updated_time, voteup_count, comment_count, content, link])
                    try:
                        self.fulei.TreeView1.insert('', index-1, values=(self.console_items[index-1][0], self.console_items[index-1][1], self.console_items[index-1][2], self.console_items[index-1][3], self.console_items[index-1][4], self.console_items[index-1][5], self.console_items[index-1][6]))
                    except:
                        pass
        def thread_1():
            offset = 0
            while True:
                spider = BtnSpider(self, url, offset)
                if not len(spider.data):
                    print('爬取完毕!')
                    break
                offset += 10
        thread_it(thread_1)
def thread_it(func, *args):
    '''将函数打包进线程'''
    # 创建
    t = Thread(target=func, args=args)
    # 守护 !!! 主线程关闭时，同时kill掉该线程
    t.setDaemon(True)
    # 启动
    t.start()
    # 阻塞--卡死界面！
    # t.join()


if __name__ == "__main__":
    top = Tk()
    Application(top).mainloop()



