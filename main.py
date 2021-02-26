# 功能：运行程序的切入点（项目的主程序）


from get_reviews import *
from visual import *
import time


def main():
    # 通过用户输入获取信息
    grab_data_str = input('【重要】\n\t是否已提前生成二进制数据，直接加载即可（y/n）：')
    if grab_data_str == 'y':
        grab_data_bool = True
        grab_fn_str = input('【基本】\n\t请输入二进制数据的文件名：')
    else:
        grab_data_bool = False
        film_url_str = input('【基本】\n\t请输入豆瓣电影的网址：')
    print('【绘制统计图】\n\t词云图')
    path_png_str = input('\t\tPNG：')
    scale_int = int(input('\t\t词云图分辨率（最大为64）：'))
    if grab_data_bool:
        grab_fn_str  = '评论二进制文件\\' + grab_fn_str
        reviews_str = grab_data(grab_fn_str)
        film_name_str = (grab_fn_str.split('\\')[-1]).split('_')[0]
        film_name_str = remove_punctuation(film_name_str)
    else:
        film_name_str = get_film_name(film_url_str)
        film_name_str = remove_punctuation(film_name_str)
        all_reviews_url_str = film_url_str + 'comments?sort=new_score&status=P'
        reviews_str = get_reviews(all_reviews_url_str)
        store_data(reviews_str, '评论二进制文件\\' + film_name_str + '_reviews.bin')
    stop_words = {film_name_str}
    png_name_str = 'PNG\\' + 'word_cloud_' + film_name_str + '.png'
    path_font_str = '字体\\AaMingYueJiuLinTian-2.ttf'
    path_png_str = 'PNG\\' + path_png_str
    try:
        word_cloud(
            reviews_str, path_png_str, path_font_str,
            png_name_str, stop_words=stop_words, scale_int=scale_int,
        )
    except MemoryError:
        print('Visual_Douban_Review/main:\n\tMemoryError\t可能是因为您所选的PNG图片文件较大，造成内存溢出，程序将重新运行。评论二进制文件已经生成，文件名为', grab_fn_str.split('\\')[-1], '，请直接选择加载评论二进制文件，并选择一个较小的PNG文件')
        main()
    else:
        print('Visual_Douban_Review/main:DONE')


if __name__ == '__main__':
    main()
