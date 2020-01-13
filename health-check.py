import sys
import os
import requests
import json

def main():
    check_image()


def check_image():
    try:
        tmp = requests.get("http://" + sys.argv[1] + "/")
        req = tmp.status_code
        print(req)
    except:
        req = 0
        print(req)


if __name__=='__main__':
    main()