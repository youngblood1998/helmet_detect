import sqlite3
import cv2
import datetime

conn = sqlite3.connect('helmetDB.db3')
cursor = conn.cursor()

img_arr = ["w", "b"]
pwd = "./data_test/20220805/L/"

# 执行插入
for img in img_arr:
     image = cv2.imread(pwd + img + ".bmp")
     image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
     sql = 'INSERT into helmet values (?,?,?,?,?,?,?,?,?)'
     x = [img, "M", "color", 0, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), image.shape[1], image.shape[0],0,
          image.tobytes()]
     cursor.execute(sql, x)
     conn.commit()

# 关闭数据库
cursor.close()
conn.close()