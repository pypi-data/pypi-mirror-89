# -*- coding: utf-8 -*-
'''
Created on 2020年11月05日
'''
import re
import html


class HtmlProcess:
    @staticmethod
    def replace_html(html_source):
        cleaned = html.unescape(html_source.strip())

        cleaned = re.sub(r"&amp;", "&", cleaned)
        cleaned = re.sub(r"&lt;", "<", cleaned)
        cleaned = re.sub(r"&gt;", ">", cleaned)
        cleaned = re.sub(r"&middot;", "·", cleaned)
        cleaned = re.sub(r"&shy;", "", cleaned)
        cleaned = re.sub(r"&#160;", " ", cleaned)
        cleaned = re.sub(r"", "", cleaned)
        cleaned = re.sub(r"[ ]", " ", cleaned)
        # 替换html中的<p>
        cleaned = re.sub(r"\s*<p[^>]*?>", "\r\n", cleaned)
        cleaned = re.sub(r"</p>\s*", "\r\n", cleaned)
        cleaned = re.sub(r"\（(相关资料:)\w*\）", "\r\n", cleaned)
        cleaned = re.sub(r"<[/]?center>", "\r\n", cleaned)
        cleaned = re.sub(r"<br\s*?[/]?>", "\r\n", cleaned)
        cleaned = re.sub(r"\[接上页\]", "", cleaned)

        cleaned = HtmlProcess.clean_html(cleaned)
        return cleaned.strip()

    @staticmethod
    def clean_html(html_source):  # 利用nltk的clean_html()函数将html文件解析为text文件
        # First we remove inline JavaScript/CSS:
        cleaned = re.sub(r"(?is)<(script|style).*?>.*?(</\1>)", "", html_source.strip())
        # Then we remove html comments. This has to be done before removing regular
        # tags since comments can contain '>' characters.
        cleaned = re.sub(r"(?s)<!--(.*?)-->[\n]?", "", cleaned)
        # Next we can remove the remaining tags:
        cleaned = re.sub(r"(?s)<.*?>", " ", cleaned)
        # Finally, we deal with whitespace
        cleaned = re.sub(r"&nbsp;", " ", cleaned)
        cleaned = re.sub(r"  ", " ", cleaned)
        cleaned = re.sub(r" ", "", cleaned)
        return cleaned.strip()