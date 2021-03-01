import logging

import requests
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, CallbackQueryHandler
from telegram.parsemode import ParseMode

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Initial logger with level DEBUG
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

MAX_INLINE_BUTTON = 60


# Blog Api Parser

class BlogApi:

    def __init__(self):
        self.hostname = "http://127.0.0.1:8000/api"

    def get_url(self, path):
        return f"{self.hostname}{path}"

    def get(self, path, query_params=None):
        url = self.get_url(path)
        response = requests.get(url)
        return response.json()

    def get_post_list(self):
        path = "/article/posts/"
        response = self.get(path)
        return response["results"]

    def get_post_detail(self, post_id):
        path = f"/article/posts/{post_id}/"
        response = self.get(path)
        return response


def build_menu(buttons, cols=2):
    buttons = buttons[:MAX_INLINE_BUTTON]
    menu = [buttons[i:i + cols] for i in range(0, len(buttons), cols)]
    return menu


# Initial function for handler
# Command handlers
def start(update: Update, context: CallbackContext):
    update.effective_message.reply_text(
        text="I`m a bot, who parse your blog!",
        reply_markup=ReplyKeyboardMarkup([["Posts"]], resize_keyboard=True)
    )


def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


# Message handlers

def message_posts(update: Update, context: CallbackContext):
    api = BlogApi()
    posts_inlines = [
        InlineKeyboardButton(
            text=f"{post['title']}",
            callback_data=f"post-{post['id']}"
        ) for post in api.get_post_list()
    ]
    update.effective_message.reply_text(
        "Select to view post.",
        reply_markup=InlineKeyboardMarkup(build_menu(posts_inlines))
    )


def select_post(update, context):
    api = BlogApi()
    query: CallbackQuery = update.callback_query
    post_id = query.data.replace("post-", "")
    post = api.get_post_detail(post_id)

    author = post["author"]

    message = (
        f"*Title:* {post['title']}\n"
        f"*Body:* {post['body']}\n\n"
        f"*Author:* {author['first_name']} {author['last_name']}\n"
        f"*Created:* {post['created']}\n"
    )
    comments = "\n".join(
        [f"\n   *{comment['author']}*: {comment['body']}" for comment in post["comments"]]
    )
    if comments:
        message = message + f"*Comments:* {comments}"

    query.edit_message_text(text=message, parse_mode=ParseMode.MARKDOWN)


if __name__ == '__main__':
    # Initial Updater and Dispatcher
    updater = Updater(token="", use_context=True)
    dispatcher = updater.dispatcher

    # Initial Handlers

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.regex("Posts"), message_posts))
    dispatcher.add_handler(CallbackQueryHandler(select_post, pattern="^post+"))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    # Start to parse telegram updates
    updater.start_polling()
    updater.idle()
