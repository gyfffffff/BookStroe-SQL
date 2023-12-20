import jieba


def cut(book_info):    
    _ts_insert = []
    attrs = ['title', 'author', 'tags', 'author_intro', 'book_intro', 'content']
    for attr in attrs:
        text = book_info[attr]
        if text != None:
            _ts_insert.extend(jieba.cut(str(text)))
    cutted = ' '.join(_ts_insert)
    return cutted

