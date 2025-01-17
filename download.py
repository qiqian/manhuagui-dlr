# Development by HSSLCreative
# Date: 2020/5/6

import os, time, re
from get import get
from PIL import Image
from proxy import requests_get

def downloadCh(url, config_json=None):    
    root = os.getcwd();
    j = get(url)
    if not j:
        return False
    bname = re.sub(r'[\\/:*?"<>|]', '_', j['bname']);
    cname = j['cname'];
    bdir = os.path.join(os.getcwd(), bname);

    def downloadPg(url, e, m, counter):
        h = {'accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'referer': 'https://www.manhuagui.com/',
        'sec-fetch-dest': 'image',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'}
        #單頁最大重試次數
        for i in range(10):
            try:
                res = None
                res = requests_get(url, params={'e':e, 'm':m}, headers = h, timeout=10)
                res.raise_for_status()
            except:
                print('頁面 %s 下載失敗: %s 重試中...' % (url, res.status_code if res else 'OTHER'), end='')
                print('等待2秒...')
                #每次重試間隔
                time.sleep(2)
                continue
            filename = str(counter) + '_' + os.path.basename(url)
            file = open(filename,'wb')
            for chunk in res.iter_content(100000):
                file.write(chunk)
            file.close()
            #轉檔 調整為False將不會轉檔
            if True:
                output_filename = filename + '.jpg'
                src_filename = os.path.join(bdir, 'jpg', cname, output_filename)
                im = Image.open(filename)
                im.save(src_filename, 'jpeg')
            #轉檔結束
            return
        print('超過重試次數 跳過此檔案')
    
    #print('0 ', bname, bdir);
    #print('1 ', os.getcwd());
    chdir(os.path.join(bdir, 'jpg', cname))
    #print('2 ', os.getcwd());
    os.chdir(bdir)
    #print('3 ', os.getcwd());
    if config_json:
        with open('config.json', 'w') as config:
            config.write(config_json)
    chdir(os.path.join(bdir, 'raw', cname))
    #print('4 ', os.getcwd());
    length = j['len']
    print('下載 %s %s 中 共%s頁' % (bname, cname, length))
    e = j['sl']['e']
    m = j['sl']['m']
    path = j['path']
    i = 1
    for filename in j['files']:
        pgUrl = 'https://i.hamreus.com' + path + filename
        print(os.path.basename(pgUrl))
        print('%s / %s' % (i, length), end='\r')
        downloadPg(pgUrl, e, m, i)
        #每頁間隔0.5秒
        time.sleep(0.5)
        i += 1
    os.chdir(root);
    #print('5 ', os.getcwd());
    return True

def chdir(ds):
    os.makedirs(ds, exist_ok=True)
    os.chdir(ds)
