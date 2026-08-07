
import flet as ft

from ui.Image_Process  import ImageComparator

def main(page: ft.Page):
    page.title = "图片效果滑动对比"
    page.bgcolor = "white"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    imglist = ['1.jpg', '2.jpg']

    page.add(
        ImageComparator(imglist, image_width=1166, image_height=684)
    )


if __name__ == '__main__':
    ft.run(main)