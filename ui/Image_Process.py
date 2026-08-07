

import  flet as ft


class ImageComparator(ft.Container):

    """
     图片滑动对比器
    """
    def __init__(self, images: list[str], image_width: int, image_height: int):
        super().__init__()          # 调用父类 flet.Container 的初始化方法

        self.image_width = image_width
        self.image_height = image_height

        self.slider_width = 90  # 滑动线和 图标 的总宽度

        # 滑动线的初始位置   在中间
        self.slider_x = (image_width - self.slider_width) / 2
        # 透明色的分界位置 在中间
        self.split_position = 0.5  # 控制透明分界的位置 (0.0 ~ 1.0)

        self.slider_line = self.creat_slider()

        self.content = ft.Stack(
            width=image_width,
            height=image_height,
            controls=[
                # 底层图片
                ft.Container(
                    content=ft.Image(
                        src=images[0],
                        fit=ft.BoxFit.FILL,
                        width=image_width,
                        height=image_height,
                    ),
                    width=image_width,
                    height=image_height,
                ),
                # 上层图片
                ft.Container(
                    content=ft.ShaderMask(
                        content=ft.Image(
                            src=images[1],
                            fit=ft.BoxFit.FILL,
                            width=image_width,
                            height=image_height,
                        ),
                        shader=ft.LinearGradient(
                            begin=ft.Alignment(-1, 0),
                            end=ft.Alignment(1, 0),
                            colors=[
                                ft.Colors.TRANSPARENT,
                                ft.Colors.TRANSPARENT,
                                ft.Colors.WHITE,
                                ft.Colors.WHITE,
                            ],
                            stops=[0.0, self.split_position, self.split_position, 1.0]
                        ),
                    ),
                    width=image_width,
                    height=image_height,
                ),
                self.slider_line
            ]
        )

    def creat_slider(self):
        # 滑动条
        left_icon = ft.Icon(
            ft.Icons.CHEVRON_LEFT,
            color=ft.Colors.BLUE,
            size=40,
        )

        right_icon = ft.Icon(
            ft.Icons.CHEVRON_RIGHT,
            color=ft.Colors.BLUE,
            size=40,
        )

        gesture_detector = ft.GestureDetector(
            mouse_cursor=ft.MouseCursor.RESIZE_COLUMN,
            drag_interval=2,
            on_pan_update=self.update_state,
        )

        divider_line = ft.Container(
            bgcolor=ft.Colors.WHITE,
            width=3,
            shadow=None,
            content=gesture_detector,
        )

        container = ft.Container(
            content=ft.Row(
                controls=[
                    left_icon,
                    divider_line,
                    right_icon,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=1,      # 设置间距，图标紧挨着分割线
            ),
            width=self.slider_width,
            height=self.image_height,
            bgcolor=ft.Colors.TRANSPARENT,
            left=self.slider_x,      #  滑动条初始位于 中间
            top=0,
        )

        return container

    def did_mount(self):
        # 在组件被添加到页面并且完成挂载后自动调用
        # 将滑动条位置设置为 中间
        self.slider_line.left = (self.image_width - self.slider_width) / 2
        self.slider_line.update()

    def update_state(self, event: ft.DragUpdateEvent[ft.GestureDetector]):
        # 计算新的 X 位置
        new_x = self.slider_line.left + event.local_delta.x

        # 限制移动范围
        min_x = 0 - self.slider_width / 2                     # 改为负数，允许滑动直线在最左边
        max_x = self.image_width - self.slider_width / 2      # 允许滑动直线在最右边
        new_x = max(min_x, min(max_x, new_x))

        # 更新容器位置
        self.slider_line.left = new_x

        # 更新分界位置（根据滑块位置计算）
        split_position = (new_x + self.slider_width / 2 ) / self.image_width  # 0 ~ 1 之间

        # 更新蒙版的分界位置
        shader_mask = self.content.controls[1].content  # 获取 ShaderMask
        shader_mask.shader.stops = [0.0, split_position, split_position, 1.0]

        # 更新所有控件
        self.slider_line.update()
        shader_mask.update()

