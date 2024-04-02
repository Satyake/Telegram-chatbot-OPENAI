from aiogram import Bot, Dispatcher, executor, types
import os 
from dotenv import load_dotenv
import logging
import openai

load_dotenv()
TOKEN=os.getenv('TOKEN')
OPENAI_API_KEY=os.getenv('OPENAI_API_KEY')

openai.api_key = OPENAI_API_KEY

MODEL_NAME='gpt-3.5-turbo'

bot=Bot(token=TOKEN)
dispatcher=Dispatcher(bot)

class Reference:
    def __init__(self):
        self.response=""


reference=Reference()
def clear_past():
    reference.response=""

@dispatcher.message_handler(commands=['start'])
async def command_start_handler(message:types.Message):
    await message.reply("I am a Chatbot created by Satyake. How may i assist?")


@dispatcher.message_handler(commands=['help'])
async def helper(message:types.Message):
    help_command="""
    Hi there, i am a bot created by Satyake. Please follow the commands-
    /start- to start the conversation
    /clear- to clear the previous response
    /help- to see the help menu
    I hope this helps
    """
    await message.reply(help_command)

@dispatcher.message_handler(commands=['clear'])
async def clear(message:types.Message):
    clear_past()
    await message.reply('Previous response cleared!')

@dispatcher.message_handler()
async def main_bot(message:types.Message):
    """ handler for integration of Open ai"""
    print(f">>> USER: \n\t {message.text}")
    response=openai.ChatCompletion.create(
        model=MODEL_NAME,
        messages=[
            {'role': "system",'content': "you are a transformers robot like from the movie Transformers, You have to speak like that"},
            {"role": "assistant","content": reference.response},
            {"role": "user","content": message.text}
        ]
    )
    reference.response=response['choices'][0]['message']['content']
    print(f"<<< chatGPT: \n\t{reference.response}")
    await bot.send_message(chat_id=message.chat.id, text=reference.response)


if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True)
