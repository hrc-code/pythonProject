import string

import execjs


def jsx(url: string):
    # 确保JavaScript文件以UTF-8编码保存
    with open(url, 'r', encoding='utf-8') as file:
        js_code = file.read()

    # 使用execjs编译JavaScript代码
    context = execjs.compile(js_code)

    try:
        result = context
        return result
    except Exception as e:
        print("Error calling JavaScript function:", e)
