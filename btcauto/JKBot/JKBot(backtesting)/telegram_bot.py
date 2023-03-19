import telegram

token = '5063162728:AAEq09U5i6tPlGui6rgTFs0wrWzTnUEU0Lg'
mc = '5094935427'
text = "안녕하세요"

def talk(text):
    bot = telegram.Bot(token)
    bot.sendMessage(mc, text)

talk(text)

# def btn_show(msg):
#     btn1 = BT(text = "1. Hello", callback_data = "1")
#     btn2 = BT(text="2. Bye", callback_data="1")
#     mu = MU(inline_keyboard = [[btn1, btn2]])
#     bot.sendMessage(mc, "선택하세요", reply_markup=mu)

# def querry_ans(msg):
#     querry_id = msg["id"]
#     querry_data = msg['data']
#     if querry_data == "1":
#         bot.answerCallbackQuery(querry_id, text="안녕하세요")
#     elif querry_data == "2":
#         bot.answerCallbackQuery(querry_id, text="안녕히계세요")
#
# MessageLoop(bot, {'chat': btn_show, 'callback_querry': querry_ans}).run_as_thread()

#
#
#
# # print(bot.getUpdates())
#
# # for i in bot.getUpdates():
# #     print(i.message.chat.id)
# #     print()
#
# bot.sendMessage(mc, text='완전간단')