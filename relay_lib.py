import ctypes
import time


def init_relay():
   objdll = ctypes.windll.LoadLibrary('./usbrelay.dll')
   objdll.USBRELAY_Open.restype = ctypes.c_uint64

   relay_dic = {}

   i = 1
   while True:
      hdl = objdll.USBRELAY_Open(i)
      i += 1
      if len(str(hdl)) != 20:
         j = 1
         while True:
            res = objdll.USBRELAY_SetRelay(ctypes.c_uint64(hdl), j, 0)  # 打开
            if res == 0:
               j += 1
            else:
               break
         relay_dic[str(hdl)] = j
      else:
         break

   return relay_dic


def close_relay(relay_dic):
   objdll = ctypes.windll.LoadLibrary('./usbrelay.dll')
   objdll.USBRELAY_Open.restype = ctypes.c_uint64

   for key, value in relay_dic.items():
      for i in range(1, value):
         objdll.USBRELAY_SetRelay(ctypes.c_uint64(int(key)), i, 0)  # 关闭
      objdll.USBRELAY_Close(ctypes.c_uint64(int(key)))


def test_delay(relay_dic):
   objdll = ctypes.windll.LoadLibrary('./usbrelay.dll')
   objdll.USBRELAY_Open.restype = ctypes.c_uint64

   for key, value in relay_dic.items():
      for i in range(1, value):
         objdll.USBRELAY_SetRelay(ctypes.c_uint64(int(key)), i, 1)
         time.sleep(0.5)
         objdll.USBRELAY_SetRelay(ctypes.c_uint64(int(key)), i, 0)


def export_relay(relay_dic, port):
   objdll = ctypes.windll.LoadLibrary('./usbrelay.dll')
   objdll.USBRELAY_Open.restype = ctypes.c_uint64

   num = 1
   # 全部关闭
   for key, value in relay_dic.items():
      for i in range(1, value):
         objdll.USBRELAY_SetRelay(ctypes.c_uint64(int(key)), i, 0)
         if num == port:
            objdll.USBRELAY_SetRelay(ctypes.c_uint64(int(key)), i, 1)
         num += 1
