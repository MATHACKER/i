#a4051407e07d7699ae90a75b81bcdf0b1549d8e1929d07ed5f383389331500206e756916aa3c18b96d9ba
from typing import Tuple

from vkbottle import VKAPIError, API, PhotoMessageUploader
from vkbottle.user import User, Message
from vkbottle.dispatch.rules.base import CommandRule

import time
import requests
import re
from PIL import Image, ImageDraw, ImageFont, ImageOps

sessia='a4051407e07d7699ae90a75b81bcdf0b1549d8e1929d07ed5f383389331500206e756916aa3c18b96d9ba'
user = User(sessia)
api=API(sessia)


# Если поставить эту функцию ниже sticker_handler - она не будет работать.

'''
@user.on.message(attachment="sticker")
async def sticker_handler(message: Message):
	await message.answer(f"Sticker ID: {message.attachments[0].sticker.sticker_id}")
'''
'''
@user.on.message(func=lambda message: len(message.text) < 5)
async def text_handler(message: Message):
	await message.answer("Message less 5 symbols")
'''
@user.on.chat_message(text=['кик', 'бан', 'ban', 'kick'])
async def kick(message: Message):
  try:
    members = await api.messages.get_conversation_members(
          peer_id=message.peer_id,
          user_id=message.reply_message.from_id
        )
    admins = [member.member_id for member in members.items if member.is_admin]
  except:
    print('error')
  #if message.from_id not in admins:
  #  await message.answer('ты не одмен беседы.')
  else:
    txt = message.reply_message.text
    await api.messages.remove_chat_user(message.peer_id - 2000000000, message.reply_message.from_id)
    return "Пользователь успешно исключён"

@user.on.message(text=['цитата', 'цит', 'цитатни', 'цита'])
async def kick(message: Message):

  await message.answer('Ожидайте...')

  people = await user.api.users.get(user_ids=message.reply_message.from_id, fields='photo_max')


  text = message.reply_message.text

  background = Image.open('фон_3_новый.QFSqF.jpg')
  idraw = ImageDraw.Draw(background)

  headline = ImageFont.truetype('arial.ttf', size=52)
  text_font = ImageFont.truetype('arial.ttf', size=35)
  name_font = ImageFont.truetype('arial.ttf', size=38)

  text = text + '»'
  head = "Цитаты великих людей"
  text = '«' + text[:37] + '\n' + text[37:]
  try:
    text = text[:74] + '\n' + text[74:]
  except:
    pass

  first_name_users = people[0].first_name
  last_name_users = people[0].last_name

  idraw.text((130, 55), head, font=headline)
  idraw.text((130, 132), text, font=text_font)
  idraw.text((245, 255), " – " + first_name_users + " " + last_name_users, font=name_font)
  
  #photo = user.api.users.get(user_ids=message.reply_message.from_id, fields='photo_400')
  
  photo = people[0].photo_max
  #await message.answer(str(photo))

  ava = requests.get(photo, allow_redirects=True)
  open('ava.png', 'wb').write(ava.content)

  size = (110, 110)

  ava = Image.open('ava.png').convert('RGB')

  mask = Image.new('L', size, 0)
  draw = ImageDraw.Draw(mask)
  draw.ellipse((0, 0) + size, fill=255)

  ava = ava.resize(size).convert('RGB')

  output = ImageOps.fit(ava, mask.size, centering=(0.5, 0.5))
  output.putalpha(mask)
  output.thumbnail(size, Image.ANTIALIAS)
  output.save('ava.png')

  ava = Image.open('ava.png')

  background.paste(ava, (130, 225), ava)

  background.save('citata.png')

  vk_cita = PhotoMessageUploader(user.api)
  photo_cita_vk = await vk_cita.upload("citata.png")
  await message.answer("💬 Ваша цитата готова!", attachment=photo_cita_vk)



@user.on.message()
async def frend(message:Message):
  if message.text.lower().startswith('инфа'):
    try:
      try:
        ids = message.reply_message.from_id
      except:
        chel= re.findall(r"[0-9]+", message.text)[0]
        chel = ''.join(chel).lower()
        ids = await api.users.get(chel)
        ids = ids[0].id


      zapros = requests.post(f'http://v1209481.hosted-by-vdsina.ru/method/users.get?token={sessia}&user_ids={int(ids)}&fields=status')
      zapros = zapros.json()
      await message.answer(f'Имя: {zapros[0]["first_name"]}\nФамилия: {zapros[0]["last_name"]}\nID: {zapros[0]["id"]}\nЗакрыт: {zapros[0]["is_closed"]} \nCтатус: {zapros[0]["status"]}')
    except:
      await message.answer('Произошла ошибка, возможно пользователь заблокирован или не существует!')
      #################################################################
  elif message.text.lower().startswith('стикеры'):
    await message.answer('Ожидайте, идёт получение информации о стикерпаках!')
    try:
      chel= re.findall(r"[0-9]+", message.text)[0]
      chel = ''.join(chel).lower()
    except:
      chel = message.from_id
    ids = await api.users.get(chel)
    ids = ids[0].id
    q = requests.post(f'http://v1209481.hosted-by-vdsina.ru/method/users.stickers?token={sessia}&user_id={int(ids)}')
    w = requests.post(f'http://v1209481.hosted-by-vdsina.ru/method/users.stickers?token={sessia}&user_id={int(ids)}&free=true')
    ####await message.answer(str(q.json()))
    countFree = str(w.json()['count'])
    countSell = int(q.json()['count'])
    names=[]
    votes = str(q.json()['stickers_vote'])
    i=0
    try:
      while i<=countSell-1:
        names.append(q.json()['sticker'][i]['name'])
        i+=1
      names = ', '.join(names)
      await message.answer(f'У [id{ids}|этого пользователя] {countFree} стикерпаков, из них {str(countSell)} платных стикер-паков:\n\n{names}\n\nПримерная стоимость:\n— {votes} голосов\n— {int(votes)*7} рублей')
    except:
      await message.answer(f'У [id{ids}|этого пользователя] отстутсвуют платные стикерпаки!')

    ##########################################################



user.run_forever()