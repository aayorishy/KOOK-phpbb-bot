from khl import Message
from khl.card import CardMessage
import mysql.connector

bot = Bot(token="token")

def validate_user_in_db(username: str):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="root"
        )
        cursor = db.cursor()
        query = "SELECT user_id, pf_kook FROM phpbb_profile_fields_data WHERE pf_kook = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        cursor.close()
        db.close()
        if result:
            return result[0], result[1]
        else:
            return None, None
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None, None

def get_username_by_user_id(user_id: int):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="root"
        )
        cursor = db.cursor()
        query = "SELECT username FROM phpbb_users WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        cursor.close()
        db.close()
        if result:
            return result[0]
        else:
            return None
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

@bot.command(name="verify", case_sensitive=False)
async def phpbb_verify(msg: Message, username: str):
    if username is None:
        await msg.reply(CardMessage(Card(Module.Section('用法: /verify KOOK昵称#编号'))))
        return

    user_id, kook_value = validate_user_in_db(username)

    cm = CardMessage()
    c1 = Card(color='#172d45')
    c1.append(Module.Divider())
    c1.append(Module.Header('KOOK身份验证系统'))
    if kook_value:
        c1.append(Module.Section(f'> {username} 身份验证成功，pf_kook: {kook_value}，user_id: {user_id}'))
        user_username = get_username_by_user_id(user_id)
        if user_username:
            c1.append(Module.Section(f'> 论坛用户名:{user_username}'))
    else:
        c1.append(Module.Section(f'> {username} 身份验证失败'))
    cm.append(c1)
    await msg.reply(cm, is_temp=True)

bot.run()
