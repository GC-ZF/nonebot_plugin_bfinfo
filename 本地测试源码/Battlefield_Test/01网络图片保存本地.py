import requests

def getjpg(url):
    try:
        path='./code.jpg'
        r=requests.get(url)
        print(r)
        print(r.status_code)
        with open(path,'wb') as f:
            f.write(r.content)
            f.close()
            print('图片保存成功')
    except:
        print('异常')

getjpg('https://secure.download.dm.origin.com/production/avatar/prod/1/599/208x208.JPEG')
