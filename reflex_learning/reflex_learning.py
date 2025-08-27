"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config
from reflex_learning import about, chat
from reflex_learning import loading

class State(rx.State):
    """The app state."""


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container( # 创建响应式布局，确保内容在桌面和移动设备上都看起来不错。
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("欢迎来的我的Reflex界面", size="9"),
            rx.text(
                "Get started by editing ",
                rx.code(f"{config.app_name}/{config.app_name}.py"),
                size="5",
            ),
            rx.link(
                rx.button("我的主页"),
                href="/about",
                is_external=True,
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
    )



app = rx.App()
app.add_page(index, route='/')
app.add_page(about, route='/about')
app.add_page(chat, route='/chat', title='Draw')
app.add_page(loading, route='/loading', title='Loading picture')
app._compile()

