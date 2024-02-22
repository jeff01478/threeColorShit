from pypinyin import pinyin, Style

def get_zhuyin(text):
    """
    將文字轉換為注音
    """
    zhuyin_list = pinyin(text, style=Style.BOPOMOFO)
    zhuyin = ''.join([p[0] for p in zhuyin_list])
    return zhuyin

# 測試
text = "抓錯人啦 警官"
zhuyin = get_zhuyin(text)
msg = zhuyin.replace(" ","").replace("ㄕ","ㄙ").replace("ㄔ","ㄙ").replace("ㄘ","ㄙ")
print(msg)  # Output: 'ㄋㄧˇㄏㄠˇ'