# zhou/pages/about.py
import reflex as rx

def about() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.heading("关于我", size="9"),
            rx.text("这是关于页面内容"),
            rx.link("聊聊天", href="/chat"),
            padding="2rem",
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
    )