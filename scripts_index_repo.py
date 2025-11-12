import os, requests, sys, json

BASE = os.getenv('ASSISTANT_BASE', 'http://127.0.0.1:5000')

def collect(folder):
    data = {}
    for root,_,files in os.walk(folder):
        for f in files:
            if f.endswith(('.py', '.md', '.txt')):
                path = os.path.join(root,f)
                with open(path,'r',encoding='utf-8') as fh:
                    data[path] = fh.read()
    return data

if __name__ == '__main__':
    folder = sys.argv[1] if len(sys.argv)>1 else '../examples'
    files = collect(folder)
    r = requests.post(f"{BASE}/index", json={"files": files})
    print(r.json())
