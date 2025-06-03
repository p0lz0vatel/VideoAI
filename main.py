import telebot
from telebot import types

from config import *
from additionals import VideoGenerator, MiniMaxAi, clear_topics



new_video_button = types.KeyboardButton("Создать Видео")
main_markup = types.ReplyKeyboardMarkup().add(
  new_video_button
)

new_topic_markup = types.InlineKeyboardMarkup().row(
  types.InlineKeyboardButton("Сгенерировать Описание по Теме", callback_data="generate_character")).row(
  types.InlineKeyboardButton("Написать свое Описание", callback_data="manual_character")
)

new_plot_markup = types.InlineKeyboardMarkup().row(
  types.InlineKeyboardButton("Сгенерировать Сюжет по Теме", callback_data="generate_plot")).row(
  types.InlineKeyboardButton("Написать свой Сюжет", callback_data="manual_plot")
)

character_validate_markup = types.InlineKeyboardMarkup().row(
  types.InlineKeyboardButton("Сгенерировать Описание Заново", callback_data="generate_character")).row(
  types.InlineKeyboardButton("Написать свое Описание", callback_data="manual_character")).row(
  types.InlineKeyboardButton("Перейти к Генерации Изображения", callback_data="apply_character")
)

character_image_validate_markup = types.InlineKeyboardMarkup().row(
  types.InlineKeyboardButton("Сгенерировать Заново", callback_data="generate_image")).row(
  types.InlineKeyboardButton("Перейти к Генерации Сюжета", callback_data="apply_image")
)

video_generate_markup = types.InlineKeyboardMarkup().row(
  types.InlineKeyboardButton("Сгенерировать Сюжет Заново", callback_data="generate_plot")).row(
  types.InlineKeyboardButton("Сгенерировать Видео", callback_data="apply_plot")
)


video_generation_classes = {}
minimaxai_class = MiniMaxAi(API_KEY, group_id, storage_path)


bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
  bot.send_message(message.chat.id, "*Привет, Здесь ты можешь создать свое уникальное Видео за пару минут\\!*", reply_markup=main_markup, parse_mode="MarkdownV2")


@bot.callback_query_handler(func=lambda call: call)
def calldata_handler(call):
  chat_id = call.message.chat.id
  message_id = call.message.message_id

  method, arg = call.data.split("_")

  if (method == "generate"):

    if (arg == "character"):
      bot.send_chat_action(chat_id, "typing")

      character_description_response = minimaxai_class.generate_description(video_generation_classes[chat_id].topic)

      bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"<b>Описание Изображения:</b>\n\n{character_description_response}\n\n<i>После Подтверждения будет Сгенерировано Изображение!</i>", reply_markup=character_validate_markup, parse_mode="HTML")

    elif (arg == "image"):
      bot.send_chat_action(chat_id, "upload_photo")

      generate_image(chat_id)

    elif (arg == "plot"):
      bot.send_chat_action(chat_id, "typing")

      plot_response = minimaxai_class.generate_plot(video_generation_classes[chat_id].topic, video_generation_classes[chat_id].character_description)

      bot.send_message(chat_id, f"<b>Сюжет для Видео:</b>\n\n{plot_response}\n\n<i>Генерируем Видео?</i>", reply_markup=video_generate_markup, parse_mode="HTML")


  elif (method == "manual"):

    if (arg == "character"):
      bot.send_chat_action(chat_id, "upload_photo")

      msg = bot.send_message(chat_id, "*Напиши Описание для Изображения:*\n\n_Предпочтительно Английский Язык_", parse_mode="MarkdownV2")

      bot.register_next_step_handler(msg, new_character_applier)

    elif (arg == "plot"):
      msg = bot.send_message(chat_id, "*Напиши Сюжет для Видео:*\n\n_Предпочтительно Английский Язык_", parse_mode="MarkdownV2")

      bot.register_next_step_handler(msg, new_video_plot_applier)

  elif (method == "apply"):

    if (arg == "character"):
      bot.send_chat_action(chat_id, "upload_photo")

      new_character_applier(call.message)

    elif (arg == "image"):
      bot.edit_message_caption(chat_id=chat_id, message_id=message_id, caption="*Переходим к Генерации Сюжета\\!*", reply_markup=new_plot_markup, parse_mode="MarkdownV2")

    elif (arg == "plot"):
      bot.send_chat_action(chat_id, "upload_video")

      new_video_plot_applier(call.message)


def generate_image(chat_id):
  character_image_path = minimaxai_class.generate_image(video_generation_classes[chat_id].character_description)

  video_generation_classes[chat_id].new_character_image(character_image_path)

  bot.send_photo(chat_id, open(character_image_path, "rb").read(), caption="*На основе этого Изображения будет сделано Видео\\!*\n\n_Готов Генерировать Сюжет\\?_", reply_markup=character_image_validate_markup, parse_mode="MarkdownV2")

def new_character_applier(message):
  video_generation_classes[message.chat.id].new_character_description(clear_topics(message.text))

  generate_image(message.chat.id)

def new_video_plot_applier(message):
  video_generator_class = video_generation_classes[message.chat.id]

  video_generator_class.new_video_plot(clear_topics(message.text))

  video_generation_classes[message.chat.id].debugger()

  video_filename = minimaxai_class.generate_video(video_generator_class.video_plot, video_generator_class.topic, video_generator_class.character_image)
  print(video_filename)

  if (video_filename):
    video_opened = open(storage_path + video_filename, 'rb')

    bot.send_video(message.chat.id, video=video_opened)
    bot.send_document(message.chat.id, video_opened, caption=f"<b>Тема Видео: {video_generator_class.topic}</b>", parse_mode="HTML")

  else:
    bot.send_message(message.chat.id, "Не удалось Загрузить Видео", parse_mode="MarkdownV2")

@bot.message_handler(content_types=['text'])
def text_handler(message):
  chat_id = message.chat.id

  if (message.text == new_video_button.text):
    bot.clear_step_handler_by_chat_id(chat_id)

    msg = bot.send_message(chat_id, new_topic_message, parse_mode="MarkdownV2")

    bot.register_next_step_handler(msg, new_topic, msg.message_id)


def new_topic(message, edit_message_id):
  bot.edit_message_text(chat_id=message.chat.id, message_id=edit_message_id, text=f"<b>Тема Видео: {message.text}</b>\n\n<i>Переходим к Описанию Изображения, на основе которого будет сделано Видео?</i>", reply_markup=new_topic_markup, parse_mode="HTML")

  bot.delete_message(message.chat.id, message.message_id)

  video_generation_classes[message.chat.id] = VideoGenerator(message.text, storage_path)




while True:
  try:
    bot.polling(none_stop=True)

  except Exception as error:
    if (error.args[0] == "stop"):
      print("% Bot Stopped")
      break

    # print(error)
    raise error