from flask import Blueprint
from flask import request
from flask import jsonify, render_template
from be.model2 import user
from be.model2.user import User
from be.model2 import error
from be.model2.hash.hashTool import HashTool
def search_author(author, page):
    u = user.User()
    code, message = u.search_author(author=author, page=int(page))
    body, word = '', '书'
    for i in message:
        title=i['title']
        print("title:----------------", title)
        author = i['author']
        publisher  = i['publisher']
        book_intro = i['book_intro']
        tags = i['tags']
        print("type(i['picture'])",type(i['picture']))#Memoryview
        # picture = HashTool.buffer_pil(i['picture'])
        picture = i['picture']
        if picture:
            print("XXXXXXXXXXX", type(picture))
            piexl = picture.load()  # 获取像素信息
            width, height = picture.size  # 获取图像尺寸
            font_pic = '<p style="color: {color}" class="small-font">{word}</p>'
            font_word= '<div class="intro">title:<a href="/auth/search_title_store_id/{title}" >{title}</a><br />author:{author}<br />publisher:{publisher}<br />book_intro:{book_intro}<br />tags:{tags}<br /></div>'
            body+="<div class='all'>"
            for y in range(height):
                body+="<div class='br'>"
                for x in range(width):
                    r, g, b = piexl[x, y]  # 获取像素RGB值
                    body += font_pic.format(
                        color='#{:02x}{:02x}{:02x}'.format(r, g, b),
                        # word=word[((y * width + x) % len(word))]
                        word=word
                    )
                body += '\n</div>\n'
            body+=font_word.format(title=title,author=author,publisher=publisher,book_intro=book_intro,tags=tags)
            body += "</div>\n<br />\n"
        else:
            # print("XXXXXXXXXXX", type(picture))
            font_word= '<div class="intro">title:<a href="/auth/search_title_store_id/{title}">{title}</a><br />author:{author}<br />publisher:{publisher}<br />book_intro:{book_intro}<br />tags:{tags}<br /></div>'
            body+="<div>"
            body+=font_word.format(title=title,author=author,publisher=publisher,book_intro=book_intro,tags=tags)
            body += "</div>\n<br />\n"
    from flask import Markup
    return render_template('search2.html', body=Markup(body))#, result={"message": message, "code": code}


def search_book_intro(book_intro, page):
    u = user.User()
    code, message = u.search_book_intro(book_intro=book_intro, page=int(page))
    body, word = '', '书'
    for i in message:
        title=i['title']
        print("title:----------------", title)
        author = i['author']
        publisher  = i['publisher']
        book_intro = i['book_intro']
        tags = i['tags']
        print("type(i['picture'])",type(i['picture']))#Memoryview
        # picture = HashTool.buffer_pil(i['picture'])
        picture = i['picture']
        if picture:
            print("XXXXXXXXXXX", type(picture))
            piexl = picture.load()  # 获取像素信息
            width, height = picture.size  # 获取图像尺寸
            font_pic = '<p style="color: {color}" class="small-font">{word}</p>'
            font_word= '<div class="intro">title:<a href="/auth/search_title_store_id/{title}" >{title}</a><br />author:{author}<br />publisher:{publisher}<br />book_intro:{book_intro}<br />tags:{tags}<br /></div>'
            body+="<div class='all'>"
            for y in range(height):
                body+="<div class='br'>"
                for x in range(width):
                    r, g, b = piexl[x, y]  # 获取像素RGB值
                    body += font_pic.format(
                        color='#{:02x}{:02x}{:02x}'.format(r, g, b),
                        # word=word[((y * width + x) % len(word))]
                        word=word
                    )
                body += '\n</div>\n'
            body+=font_word.format(title=title,author=author,publisher=publisher,book_intro=book_intro,tags=tags)
            body += "</div>\n<br />\n"
        else:
            # print("XXXXXXXXXXX", type(picture))
            font_word= '<div class="intro">title:<a href="/auth/search_title_store_id/{title}">{title}</a><br />author:{author}<br />publisher:{publisher}<br />book_intro:{book_intro}<br />tags:{tags}<br /></div>'
            body+="<div>"
            body+=font_word.format(title=title,author=author,publisher=publisher,book_intro=book_intro,tags=tags)
            body += "</div>\n<br />\n"
    from flask import Markup
    return render_template('search2.html', body=Markup(body))


def search_tags(tags, page):
    u = user.User()
    code, message = u.search_tags(tags=tags, page=int(page))
    body, word = '', '书'
    for i in message:
        title=i['title']
        print("title:----------------", title)
        author = i['author']
        publisher  = i['publisher']
        book_intro = i['book_intro']
        tags = i['tags']
        print("type(i['picture'])",type(i['picture']))#Memoryview
        # picture = HashTool.buffer_pil(i['picture'])
        picture = i['picture']
        if picture:
            print("XXXXXXXXXXX", type(picture))
            piexl = picture.load()  # 获取像素信息
            width, height = picture.size  # 获取图像尺寸
            font_pic = '<p style="color: {color}" class="small-font">{word}</p>'
            font_word= '<div class="intro">title:<a href="/auth/search_title_store_id/{title}" >{title}</a><br />author:{author}<br />publisher:{publisher}<br />book_intro:{book_intro}<br />tags:{tags}<br /></div>'
            body+="<div class='all'>"
            for y in range(height):
                body+="<div class='br'>"
                for x in range(width):
                    r, g, b = piexl[x, y]  # 获取像素RGB值
                    body += font_pic.format(
                        color='#{:02x}{:02x}{:02x}'.format(r, g, b),
                        # word=word[((y * width + x) % len(word))]
                        word=word
                    )
                body += '\n</div>\n'
            body+=font_word.format(title=title,author=author,publisher=publisher,book_intro=book_intro,tags=tags)
            body += "</div>\n<br />\n"
        else:
            # print("XXXXXXXXXXX", type(picture))
            font_word= '<div class="intro">title:<a href="/auth/search_title_store_id/{title}">{title}</a><br />author:{author}<br />publisher:{publisher}<br />book_intro:{book_intro}<br />tags:{tags}<br /></div>'
            body+="<div>"
            body+=font_word.format(title=title,author=author,publisher=publisher,book_intro=book_intro,tags=tags)
            body += "</div>\n<br />\n"
    from flask import Markup
    return render_template('search2.html', body=Markup(body))


def search_title(title, page):
    u = user.User()
    code, message = u.search_title(title=title, page=int(page))
    body, word = '', '书'
    for i in message:
        title=i['title']
        print("title:----------------", title)
        author = i['author']
        publisher  = i['publisher']
        book_intro = i['book_intro']
        tags = i['tags']
        print("type(i['picture'])",type(i['picture']))#Memoryview
        # picture = HashTool.buffer_pil(i['picture'])
        picture = i['picture']
        if picture:
            print("XXXXXXXXXXX", type(picture))
            piexl = picture.load()  # 获取像素信息
            width, height = picture.size  # 获取图像尺寸
            font_pic = '<p style="color: {color}" class="small-font">{word}</p>'
            font_word= '<div class="intro">title:<a href="/auth/search_title_store_id/{title}" >{title}</a><br />author:{author}<br />publisher:{publisher}<br />book_intro:{book_intro}<br />tags:{tags}<br /></div>'
            body+="<div class='all'>"
            for y in range(height):
                body+="<div class='br'>"
                for x in range(width):
                    r, g, b = piexl[x, y]  # 获取像素RGB值
                    body += font_pic.format(
                        color='#{:02x}{:02x}{:02x}'.format(r, g, b),
                        # word=word[((y * width + x) % len(word))]
                        word=word
                    )
                body += '\n</div>\n'
            body+=font_word.format(title=title,author=author,publisher=publisher,book_intro=book_intro,tags=tags)
            body += "</div>\n<br />\n"
        else:
            # print("XXXXXXXXXXX", type(picture))
            font_word= '<div class="intro">title:<a href="/auth/search_title_store_id/{title}">{title}</a><br />author:{author}<br />publisher:{publisher}<br />book_intro:{book_intro}<br />tags:{tags}<br /></div>'
            body+="<div>"
            body+=font_word.format(title=title,author=author,publisher=publisher,book_intro=book_intro,tags=tags)
            body += "</div>\n<br />\n"
    from flask import Markup
    return render_template('search2.html', body=Markup(body))


def search_author_in_store(author, page, store_id):
    u = user.User()
    code, message = u.search_author_in_store(author=author, store_id=store_id, page=page)
    body, word = '', '书'
    for i in message:
        title=i['title']
        print("title:----------------", title)
        author = i['author']
        publisher  = i['publisher']
        book_intro = i['book_intro']
        tags = i['tags']
        print("type(i['picture'])",type(i['picture']))#Memoryview
        # picture = HashTool.buffer_pil(i['picture'])
        picture = i['picture']
        if picture:
            print("XXXXXXXXXXX", type(picture))
            piexl = picture.load()  # 获取像素信息
            width, height = picture.size  # 获取图像尺寸
            font_pic = '<p style="color: {color}" class="small-font">{word}</p>'
            font_word= '<div class="intro">title:<a href="/auth/search_title_store_id/{title}" >{title}</a><br />author:{author}<br />publisher:{publisher}<br />book_intro:{book_intro}<br />tags:{tags}<br /></div>'
            body+="<div class='all'>"
            for y in range(height):
                body+="<div class='br'>"
                for x in range(width):
                    r, g, b = piexl[x, y]  # 获取像素RGB值
                    body += font_pic.format(
                        color='#{:02x}{:02x}{:02x}'.format(r, g, b),
                        # word=word[((y * width + x) % len(word))]
                        word=word
                    )
                body += '\n</div>\n'
            body+=font_word.format(title=title,author=author,publisher=publisher,book_intro=book_intro,tags=tags)
            body += "</div>\n<br />\n"
        else:
            # print("XXXXXXXXXXX", type(picture))
            font_word= '<div class="intro">title:<a href="/auth/search_title_store_id/{title}">{title}</a><br />author:{author}<br />publisher:{publisher}<br />book_intro:{book_intro}<br />tags:{tags}<br /></div>'
            body+="<div>"
            body+=font_word.format(title=title,author=author,publisher=publisher,book_intro=book_intro,tags=tags)
            body += "</div>\n<br />\n"
    from flask import Markup
    return render_template('search2.html', body=Markup(body))


def search_book_intro_in_store(book_intro, page, store_id):
    u = user.User()
    code, message = u.search_book_intro_in_store(book_intro=book_intro, store_id=store_id, page=page)
    body, word = '', '书'
    for i in message:
        title=i['title']
        print("title:----------------", title)
        author = i['author']
        publisher  = i['publisher']
        book_intro = i['book_intro']
        tags = i['tags']
        print("type(i['picture'])",type(i['picture']))#Memoryview
        # picture = HashTool.buffer_pil(i['picture'])
        picture = i['picture']
        if picture:
            print("XXXXXXXXXXX", type(picture))
            piexl = picture.load()  # 获取像素信息
            width, height = picture.size  # 获取图像尺寸
            font_pic = '<p style="color: {color}" class="small-font">{word}</p>'
            font_word= '<div class="intro">title:<a href="/auth/search_title_store_id/{title}" >{title}</a><br />author:{author}<br />publisher:{publisher}<br />book_intro:{book_intro}<br />tags:{tags}<br /></div>'
            body+="<div class='all'>"
            for y in range(height):
                body+="<div class='br'>"
                for x in range(width):
                    r, g, b = piexl[x, y]  # 获取像素RGB值
                    body += font_pic.format(
                        color='#{:02x}{:02x}{:02x}'.format(r, g, b),
                        # word=word[((y * width + x) % len(word))]
                        word=word
                    )
                body += '\n</div>\n'
            body+=font_word.format(title=title,author=author,publisher=publisher,book_intro=book_intro,tags=tags)
            body += "</div>\n<br />\n"
        else:
            # print("XXXXXXXXXXX", type(picture))
            font_word= '<div class="intro">title:<a href="/auth/search_title_store_id/{title}">{title}</a><br />author:{author}<br />publisher:{publisher}<br />book_intro:{book_intro}<br />tags:{tags}<br /></div>'
            body+="<div>"
            body+=font_word.format(title=title,author=author,publisher=publisher,book_intro=book_intro,tags=tags)
            body += "</div>\n<br />\n"
    from flask import Markup
    return render_template('search2.html', body=Markup(body))


def search_tags_in_store(tags, page, store_id):
    u = user.User()
    code, message = u.search_tags_in_store(tags=tags, store_id=store_id, page=page)
    body, word = '', '书'
    for i in message:
        title=i['title']
        print("title:----------------", title)
        author = i['author']
        publisher  = i['publisher']
        book_intro = i['book_intro']
        tags = i['tags']
        print("type(i['picture'])",type(i['picture']))#Memoryview
        # picture = HashTool.buffer_pil(i['picture'])
        picture = i['picture']
        if picture:
            print("XXXXXXXXXXX", type(picture))
            piexl = picture.load()  # 获取像素信息
            width, height = picture.size  # 获取图像尺寸
            font_pic = '<p style="color: {color}" class="small-font">{word}</p>'
            font_word= '<div class="intro">title:<a href="/auth/search_title_store_id/{title}" >{title}</a><br />author:{author}<br />publisher:{publisher}<br />book_intro:{book_intro}<br />tags:{tags}<br /></div>'
            body+="<div class='all'>"
            for y in range(height):
                body+="<div class='br'>"
                for x in range(width):
                    r, g, b = piexl[x, y]  # 获取像素RGB值
                    body += font_pic.format(
                        color='#{:02x}{:02x}{:02x}'.format(r, g, b),
                        # word=word[((y * width + x) % len(word))]
                        word=word
                    )
                body += '\n</div>\n'
            body+=font_word.format(title=title,author=author,publisher=publisher,book_intro=book_intro,tags=tags)
            body += "</div>\n<br />\n"
        else:
            # print("XXXXXXXXXXX", type(picture))
            font_word= '<div class="intro">title:<a href="/auth/search_title_store_id/{title}">{title}</a><br />author:{author}<br />publisher:{publisher}<br />book_intro:{book_intro}<br />tags:{tags}<br /></div>'
            body+="<div>"
            body+=font_word.format(title=title,author=author,publisher=publisher,book_intro=book_intro,tags=tags)
            body += "</div>\n<br />\n"
    from flask import Markup
    return render_template('search2.html', body=Markup(body))


def search_title_in_store(title, page, store_id):
    u = user.User()
    code, message = u.search_title_in_store(title=title, store_id=store_id, page=page)
    body, word = '', '书'
    for i in message:
        title=i['title']
        print("title:----------------", title)
        author = i['author']
        publisher  = i['publisher']
        book_intro = i['book_intro']
        tags = i['tags']
        print("type(i['picture'])",type(i['picture']))#Memoryview
        # picture = HashTool.buffer_pil(i['picture'])
        picture = i['picture']
        if picture:
            print("XXXXXXXXXXX", type(picture))
            piexl = picture.load()  # 获取像素信息
            width, height = picture.size  # 获取图像尺寸
            font_pic = '<p style="color: {color}" class="small-font">{word}</p>'
            font_word= '<div class="intro">title:<a href="/auth/search_title_store_id/{title}" >{title}</a><br />author:{author}<br />publisher:{publisher}<br />book_intro:{book_intro}<br />tags:{tags}<br /></div>'
            body+="<div class='all'>"
            for y in range(height):
                body+="<div class='br'>"
                for x in range(width):
                    r, g, b = piexl[x, y]  # 获取像素RGB值
                    body += font_pic.format(
                        color='#{:02x}{:02x}{:02x}'.format(r, g, b),
                        # word=word[((y * width + x) % len(word))]
                        word=word
                    )
                body += '\n</div>\n'
            body+=font_word.format(title=title,author=author,publisher=publisher,book_intro=book_intro,tags=tags)
            body += "</div>\n<br />\n"
        else:
            # print("XXXXXXXXXXX", type(picture))
            font_word= '<div class="intro">title:<a href="/auth/search_title_store_id/{title}">{title}</a><br />author:{author}<br />publisher:{publisher}<br />book_intro:{book_intro}<br />tags:{tags}<br /></div>'
            body+="<div>"
            body+=font_word.format(title=title,author=author,publisher=publisher,book_intro=book_intro,tags=tags)
            body += "</div>\n<br />\n"
    from flask import Markup
    return render_template('search2.html', body=Markup(body))

def search_title_store_id(title):
    u = user.User()
    code, message = u.search_title_store_id(title=title)
    body, word = '', '书'
    for i in message:
        title=i['title']
        print("title:----------------", title)
        author = i['author']
        publisher  = i['publisher']
        book_intro = i['book_intro']
        tags = i['tags']
        print("type(i['picture'])",type(i['picture']))#Memoryview
        # picture = HashTool.buffer_pil(i['picture'])
        picture = i['picture']
        if picture:
            print("XXXXXXXXXXX", type(picture))
            piexl = picture.load()  # 获取像素信息
            width, height = picture.size  # 获取图像尺寸
            font_pic = '<p style="color: {color}" class="small-font">{word}</p>'
            font_word= '<div class="intro">title:<a href="/auth/search_title_store_id/{title}" >{title}</a><br />author:{author}<br />publisher:{publisher}<br />book_intro:{book_intro}<br />tags:{tags}<br /></div>'
            body+="<div class='all'>"
            for y in range(height):
                body+="<div class='br'>"
                for x in range(width):
                    r, g, b = piexl[x, y]  # 获取像素RGB值
                    body += font_pic.format(
                        color='#{:02x}{:02x}{:02x}'.format(r, g, b),
                        # word=word[((y * width + x) % len(word))]
                        word=word
                    )
                body += '\n</div>\n'
            body+=font_word.format(title=title,author=author,publisher=publisher,book_intro=book_intro,tags=tags)
            body += "</div>\n<br />\n"
        else:
            # print("XXXXXXXXXXX", type(picture))
            font_word= '<div class="intro">title:<a href="/auth/search_title_store_id/{title}">{title}</a><br />author:{author}<br />publisher:{publisher}<br />book_intro:{book_intro}<br />tags:{tags}<br /></div>'
            body+="<div>"
            body+=font_word.format(title=title,author=author,publisher=publisher,book_intro=book_intro,tags=tags)
            body += "</div>\n<br />\n"
    from flask import Markup
    return render_template('search2.html', body=Markup(body))