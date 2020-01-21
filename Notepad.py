# -*- coding: Shift_JIS -*-

import datetime
import tkinter
import tkinter.font as font
import json, config #標準のjsonモジュールとconfig.pyの読み込み
from requests_oauthlib import OAuth1Session #OAuthのライブラリの読み込み



def tweet():
	tweet = text_widget.get('1.0','end -1c')
	params = {"status": tweet}
	twitter.post("https://api.twitter.com/1.1/statuses/update.json",params = params)

def getTimeLine():
	# テキストボックスをクリア
	text_widget.delete(1.0,tkinter.END)
	
	url = "https://api.twitter.com/1.1/statuses/home_timeline.json"

	params ={'count' : 200}
	req = twitter.get(url, params = params)
	

	if req.status_code == 200:
	    timeline = json.loads(req.text)
	    for tweet in timeline:
	        #tweetの対応外文字削除
	        char_list = [tweet['text'][i] for i in range(len(tweet['text'])) if ord(tweet['text'][i]) in range(65535)]
	        tweetstr = ''
	        for i in char_list:
	        	tweetstr=tweetstr+i
	        #usernameの対応外文字削除
	        char_list = [tweet['user']['name'][j] for j in range(len(tweet['user']['name'])) if ord(tweet['user']['name'][j]) in range(65535)]
	        name = ''
	        for j in char_list:
	        	name=name+j
	        
	        print(tweet['user']['name']+'::'+tweet['text'])
	        print(tweet['created_at'])
	        print('----------------------------------------------------')
	        text_widget.insert('end',name + '\n' + tweetstr+'\n')
	        text_widget.insert('end',tweet['created_at']+'\n')
	        text_widget.insert('end','----------------------------------------------------\n')
	else:
	    print("ERROR: %d" % req.status_code)

def clearEdit():
    # テキストボックスをクリア
    text_widget.delete(1.0,tkinter.END)

CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET
twitter = OAuth1Session(CK, CS, AT, ATS)


root = tkinter.Tk()

my_font = font.Font(root,family="MS Gothic")

menubar = tkinter.Menu(root,font = my_font)
filemenu = tkinter.Menu(menubar, tearoff=0)
filemenu.add_command(label="新規(N)", command=tweet)
filemenu.add_command(label="開く(O)...", command=getTimeLine)
filemenu.add_command(label="上書き保存(S)",command=clearEdit)
filemenu.add_command(label="名前を付けて保存(A)...")
filemenu.add_separator()
filemenu.add_command(label="ページ設定(U)...")
filemenu.add_command(label="印刷(P)...")
filemenu.add_separator()
filemenu.add_command(label="メモ帳の終了(X)", command=root.quit)
menubar.add_cascade(label="ファイル(F)", menu=filemenu)

editmenu = tkinter.Menu(menubar, tearoff=0)
editmenu.add_command(label="Undo")
editmenu.add_separator()
editmenu.add_command(label="Cut")
editmenu.add_command(label="Copy")
editmenu.add_command(label="Paste")
editmenu.add_command(label="Delete")
editmenu.add_command(label="Select All")
menubar.add_cascade(label="編集(E)", menu=editmenu)

formatmenu = tkinter.Menu(menubar, tearoff=0)
formatmenu.add_command(label="Help Index")
formatmenu.add_command(label="About...")
menubar.add_cascade(label="書式(O)", menu=formatmenu)

viewmenu = tkinter.Menu(menubar, tearoff=0)
viewmenu.add_command(label="About...")
menubar.add_cascade(label="表示(V)", menu=viewmenu)

helpmenu = tkinter.Menu(menubar, tearoff=0)
helpmenu.add_command(label="About...")
menubar.add_cascade(label="ヘルプ(H)", menu=helpmenu)



#EDIT
text_widget = tkinter.Text(root,wrap=tkinter.NONE,font=my_font)
text_widget.grid(column=0, row=0, sticky=(tkinter.N, tkinter.S, tkinter.E, tkinter.W))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# スクロールバー
yscroll = tkinter.Scrollbar(text_widget,command=text_widget.yview)
xscroll = tkinter.Scrollbar(text_widget,command=text_widget.xview,orient=tkinter.HORIZONTAL)
yscroll.pack(side=tkinter.RIGHT,fill="y")
xscroll.pack(side=tkinter.BOTTOM,fill="x")
text_widget['yscrollcommand'] = yscroll.set
text_widget['xscrollcommand'] = xscroll.set


#scrollbar = tkinter.Scrollbar(text_widget)
#scrollbar.pack(side=tkinter.RIGHT, fill="y")
#text_widget["yscrollcommand"] = scrollbar.set


root.config(menu=menubar)
root.title("無題 - メモ帳")
root.geometry("500x500")
root.iconbitmap('notepad32x32.ico')
root.mainloop()