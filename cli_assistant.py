#!/usr/bin/env python3
import sys, os, requests
BASE = os.getenv('ASSISTANT_BASE', 'http://127.0.0.1:5000')

def main():
    if len(sys.argv) < 2:
        print('Usage: python assistant.py "your question"')
        return
    prompt = ' '.join(sys.argv[1:])
    try:
        r = requests.post(f"{BASE}/chat", json={"prompt": prompt})
        print(r.json().get('reply'))
    except Exception as e:
        print('Error contacting assistant:', e)

if __name__ == '__main__':
    main()
