import reflex as rx
from openai import OpenAI
from concurrent.futures import TimeoutError

client = OpenAI(
    api_key = "",
    base_url ="",
)

class State(rx.State):
    """The app State"""
    prompt : str = ""
    answer : str = ""
    current : str = ""
    processing : bool = False
    complete : bool = False
    error_message : str = ""

    async def get_answer(self):
        """Get the answer from the prompt."""
        if self.prompt.strip() == "":
            yield rx.window_alert("请输出你的问题")
            return
        
        self.processing, self.complete = True, False
        self.answer = ""
        self.error_message = ""
        yield

        try:
            stream = client.chat.completions.create(
                model = 'deepseek-r1-250528',
                messages=[
                    {"role": "system", "content": "你是人工智能助手"},
                    {"role": "user", "content": self.prompt}
                ],
                stream = True
            )
            # 逐块处理
            for chunk in stream:
                if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                    self.current += chunk.choices[0].delta.content
                    yield
            
            self.processing = False
            self.complete = True

        
        except TimeoutError:
            self.processing = False
            self.error_message = "请求超时，请检查网络连接或稍后重试"
            yield rx.window_alert("请求超时!")
            return 
        except Exception as e:
            self.processing = False
            self.error_message = f"发生错误:{str(e)}"
            yield rx.window_alert(f"错误:{str(e)}")
            return 
        

    def set_prompt(self, value):
        """当输入框失去焦点时，更新prompt变量"""
        self.prompt = value
    
    def clear_conversation(self):
        """
        清空当前对话，重置所有状态
        """
        self.prompt = ""
        self.answer = ""
        self.current = ""
        self.complete = False
        self.processing = False
        self.error_message = ""



def chat():
    return rx.center( # 绝对居中
        rx.el.link(rel="stylesheet", href="/form.css"),
        rx.el.link(rel="stylesheet", href="/input_style.css"),
        rx.vstack(
            rx.heading("DeepSeek", size = "9", color="blue.700"),
            # 输入框
            rx.box(
                rx.text("请输入你的问题：", weight='bold', margin_bottom='0.5em'),
                rx.input( 
                    placeholder="例如：常见的十字花科植物有哪些？",
                    on_blur = State.set_prompt,
                    width="25em",
                    variant = "soft",
                    class_name= "no-border-input",
                    radius = "none",
                ),
                class_name = "form-control",
                style = {
                        # "margin_top": "-15px",      # 调整定位
                        "margin_x": "auto",         # 水平居中
                },
            ),
            rx.button( # 按钮组件
                "生成回答",
                size = "3",
                width = "12em",
                loading = State.processing,
                on_click = State.get_answer,
                # color_scheme='blue',
                variant="ghost",
            ),
            rx.cond(
                State.complete,
                rx.box(
                    rx.heading("AI回答:", size="6", color="blue.700"),
                    rx.box(
                        rx.text(State.current, white_space="pre-wrap"),  # 保留换行格式
                        padding="1em",
                        border="1px solid #e2e8f0",
                        border_radius="8px",
                        background="white",
                        max_height="300px",
                        overflow_y="auto"
                    ),
                    width="25em"
                ),
        ),
        ),
        align='center',
        spacing='6',
        padding='2em',
        width = "100%",
        height = "100vh",
    )