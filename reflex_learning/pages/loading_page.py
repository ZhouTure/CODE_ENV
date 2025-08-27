import reflex as rx
import time
import asyncio

# 1.定义应用状态
class MyState(rx.State):
    """应用的状态管理"""
    is_loading: bool = False

    async def handle_click(self):
        """按钮点击事件处理器"""
        # 开始加载
        self.is_loading = True
        yield  # 更新 UI

        # 模拟异步任务
        await asyncio.sleep(30)

        # 结束加载
        self.is_loading = False
        yield  # 更新 UI

def loading():
    return rx.fragment(
        # 导入css, href源于.web/public
        rx.el.link(rel="stylesheet", href="/styles.css"),
        rx.center(
            rx.vstack(
                rx.text("这是一个加载测试界面", size = '9'),
                rx.button(
                    rx.cond(
                        MyState.is_loading,
                        rx.box(
                            class_name="loader",
                            style={
                                "margin_top": "-15px",      # 调整定位
                                "margin_x": "auto",         # 水平居中
                                },
                        ),
                        "开始加载",
                    ),
                    on_click=MyState.handle_click,
                    disabled=MyState.is_loading,
                    min_height="180px",
                    min_width="240px",
                ),
                    
            ),
            height="100vh",
        ),
    )


    
