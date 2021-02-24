# 可视化评论数据的函数


from wordcloud import WordCloud
import jieba
import numpy as np
import PIL.Image as Image
from get_reviews import get_reviews, grab_data


def chinese_jieba(text_str):
    # 功能：利用jieba划分中文
    # 形参：text_str[str]:需要处理的文本
    # 返回：space_word_str[str]：划分好的中文
    wordlist_jieba=jieba.cut(text_str)
    r_space_wordlist_str="".join(wordlist_jieba)
    return r_space_wordlist_str


def word_cloud(text_str, path_png_str, path_font_str, png_name_str):
    text_str=chinese_jieba(text_str)
    # 调用包PIL中的open方法，读取图片文件，通过numpy中的array方法生成数组
    mask_pic=np.array(Image.open(path_png_str))
    wordcloud = WordCloud(font_path=path_font_str,#设置字体
                        mask=mask_pic,#设置背景图片
                        background_color="white",#设置背景颜色
                        max_font_size=150,# 设置字体最大值
                        max_words=2000, # 设置最大显示的字数
                        stopwords={'流浪地球', '星际穿越'}, #设置停用词，停用词则不再词云图中表示
                        ).generate(text_str)
    image=wordcloud.to_image()
    wordcloud.to_file(png_name_str)
    image.show()


if __name__ == '__main__':
    m_reviews_str = grab_data('流浪地球_reviews.txt')
    word_cloud(m_reviews_str, 'china.png', 'A:\字体\明月九连天\AaMingYueJiuLinTian-2.ttf', 'visual_text02.png')
