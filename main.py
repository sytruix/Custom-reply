from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api.config import Config

# 默认配置
DEFAULT_CONFIG = {
    "reply_message": "Hello, {user_name}, 你发了 {message_str}!"
}

@register("Custom-reply", "自定义回复插件", "一个简单的 自定义回复 插件", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        # 初始化配置
        self.config = Config(self.context.config, "CustomReplyPlugin", DEFAULT_CONFIG)
        # 配置中提供的默认值
        self.reply_message = self.config.get("reply_message")

    async def initialize(self):
        """插件初始化时读取配置"""
        logger.info("插件初始化完成，配置已加载。")

    @filter.command("Custom-reply")
    async def helloworld(self, event: AstrMessageEvent):
        """处理 /Custom-reply 指令"""
        user_name = event.get_sender_name()
        message_str = event.message_str
        logger.info(f"收到消息: {message_str}")

        # 使用配置中的自定义回复消息
        reply_text = self.reply_message.format(user_name=user_name, message_str=message_str)
        yield event.plain_result(reply_text)

    @filter.command("set-reply-message")
    async def set_reply_message(self, event: AstrMessageEvent):
        """允许用户设置自定义回复消息"""
        new_message = event.message_str.strip()
        if new_message:
            self.config.set("reply_message", new_message)
            self.reply_message = new_message
            yield event.plain_result(f"回复消息已更新为：{new_message}")
        else:
            yield event.plain_result("请输入有效的消息内容。")

    async def terminate(self):
        """插件销毁时可以进行清理"""
        logger.info("插件已卸载。")
