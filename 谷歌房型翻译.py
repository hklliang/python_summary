# -*- coding:utf-8 -*-  
__author__ = 'hklliang'
__date__ = '2017-09-08 9:39'
import requests
import urllib
import re, MySQLdb, MySQLdb.cursors
import time
import aiohttp
import asyncio
import async_timeout
import execjs


# pattern=re.compile('null|false|true')
# url='https://translate.google.cn/translate_a/single?client=t&sl=zh-CN&tl=en&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&source=btn&ssel=6&tsel=3&kc=0&tk=159538.266219&q={key_word}'
# key_word=urllib.parse.quote('一卧')
# print(key_word)
# format_url=url.format(key_word=key_word)
# print(format_url)
#
# r=requests.get(format_url)
# str=pattern.sub('999',r.text)
# print(eval(str)[0][0][0])

class Mysql_db(object):
    def __init__(self, dbparms):
        self.conn = MySQLdb.connect(**dbparms)
        self.cursor = self.conn.cursor()

    def do_sql_many(self, sql, param=None):
        self.cursor.executemany(sql, param)
        self.conn.commit()
        # print(self.cursor._last_executed)

    def do_fetch(self, sql):
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result


dbparms = dict(
    host='127.0.0.1',
    db='data',
    user='root',
    passwd='123456',
    charset='utf8',
    use_unicode=True,
    cursorclass=MySQLdb.cursors.DictCursor
)


class TranslateRoom():
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        self.response_list = []
        self.pattern = re.compile('null|false|true')
        self.ctx = execjs.compile("""
           function TL(a) {
           var k = "";
           var b = 406644;
           var b1 = 3293161072;

           var jd = ".";
           var $b = "+-a^+6";
           var Zb = "+-3^+b+-f";

           for (var e = [], f = 0, g = 0; g < a.length; g++) {
               var m = a.charCodeAt(g);
               128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023),
               e[f++] = m >> 18 | 240,
               e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224,
               e[f++] = m >> 6 & 63 | 128),
               e[f++] = m & 63 | 128)
           }
           a = b;
           for (f = 0; f < e.length; f++) a += e[f],
           a = RL(a, $b);
           a = RL(a, Zb);
           a ^= b1 || 0;
           0 > a && (a = (a & 2147483647) + 2147483648);
           a %= 1E6;
           return a.toString() + jd + (a ^ b)
       };

       function RL(a, b) {
           var t = "a";
           var Yb = "+";
           for (var c = 0; c < b.length - 2; c += 3) {
               var d = b.charAt(c + 2),
               d = d >= t ? d.charCodeAt(0) - 87 : Number(d),
               d = b.charAt(c + 1) == Yb ? a >>> d: a << d;
               a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d
           }
           return a
       }
       """)

    def getTk(self, text):
        return self.ctx.call("TL", text)

    async def fetch(self, session, url):
        with async_timeout.timeout(10):
            async with session.get(url) as response:
                return await response.text()

    async def main(self, room_name, format_url):
        async with aiohttp.ClientSession(headers=self.headers) as session:
            html = await self.fetch(session, format_url)
            str = self.pattern.sub('999', html)
            translate_name = eval(str)[0][0][0]
            self.response_list.append((room_name, translate_name))


    def run(self, rooms):
        self.response_list = []
        requets_list = []

        for room in rooms:
            room_name = room['room_name']
            tk = self.getTk(room_name)
            key_word = urllib.parse.quote(room_name)
            format_url = 'https://translate.google.cn/translate_a/single?client=t&sl=zh-CN&tl=en&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&source=btn&ssel=6&tsel=3&kc=0&tk={tk}&q={key_word}'. \
                format(key_word=key_word, tk=tk)
            requets_list.append(self.main(room_name,format_url))

        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(requets_list))
        return self.response_list


if __name__ == '__main__':
    t1 = time.time()
    #     rooms_sql = """
    #              select  a.hotel_id  from (SELECT old_hotel_id hotel_id from hotel_check union  select new_hotel_id from hotel_check) a
    # left join hotel_rate b on a.hotel_id=b.hotel_id where b.hotel_id is null group by a.hotel_id
    #             """
    rooms_sql = """
        SELECT left(roomName,locate('(',roomName)-1) room_name
FROM `ctrip_hotel_room_mapping` a
join hotel_map_ctrip b on a.ctripHotelId=b.supplier_hotel_id
and supplier='ctrip' left join translate_room c on left(roomName,locate('(',roomName)-1)=c.room_name
where c.room_name is null
group by left(roomName,locate('(',roomName)-1)

    """
    mysql_db = Mysql_db(dbparms)
    rooms = mysql_db.do_fetch(rooms_sql)
    rooms_count = len(rooms)
    print(rooms_count)
    group = 50
    translateRoom = TranslateRoom()
    groups_rooms = [rooms[i:i + group] for i in range(0, rooms_count, group)]

    for group_rooms in groups_rooms:
        response_list = translateRoom.run(group_rooms)
        insert_sql = """
        insert into translate_room(room_name,room_name_en)values(%s,%s)
        """
        mysql_db.do_sql_many(insert_sql,response_list)

    print(time.time() - t1)
