import requests,json,time,re,datetime,os
import pandas as pd
import http.client,warnings
import pywinauto
import pywinauto.clipboard
import win32gui,win32api,win32con
from io import StringIO

pd.set_option('display.max_rows',None)   #显示所有行
pd.set_option('display.unicode.east_asian_width', True)#设置列名对齐
warnings.simplefilter('ignore', category=UserWarning)
global app,hwnd,main_window,left_window,button_window_list,edit_windows_list,cang_df

#交易端初始化
def hx_init():
    global app,hwnd,main_window,left_window,button_window_list,edit_windows_list,cang_df
    button_window_list=[];edit_windows_list=[]
    app = pywinauto.application.Application()
    app.connect(title='网上股票交易系统5.0')
    hwnd = win32gui.FindWindow(None,'网上股票交易系统5.0') 
    main_window = app.window(handle=hwnd)
    lefthwnd = pywinauto.findwindows.find_windows(top_level_only=False, class_name='SysTreeView32', parent=hwnd)[0] 
    left_window = pywinauto.controls.common_controls.TreeViewWrapper(lefthwnd)
    left_window.get_item([4]).click()
    main_window.type_keys('{F6}')
    edit_hwnd = pywinauto.findwindows.find_windows(top_level_only=False, class_name='Edit', parent=hwnd)#[459868, 594614, 528692]  右侧整个窗口
    button_hwnd = pywinauto.findwindows.find_windows(top_level_only=False, class_name='Button', parent=hwnd)
    for i in [0,1,5]:
        button_window_list.append(pywinauto.controls.win32_controls.ButtonWrapper(button_hwnd[i]))
    for i in range(0,6):
        edit_windows_list.append(pywinauto.controls.win32_controls.EditWrapper(edit_hwnd[i]))
hx_init()
#获取持仓
def get_chicang():
    global hwnd
    button_hwnd = pywinauto.findwindows.find_windows(top_level_only=False, class_name='Button', parent=hwnd)
    suanxin_window = pywinauto.controls.common_controls.TreeViewWrapper(button_hwnd[4])
    suanxin_window.click();time.sleep(1)
    cang_hwnd = pywinauto.findwindows.find_windows(top_level_only=False, class_name='CVirtualGridCtrl', parent=hwnd)[0] 
    cang_window = pywinauto.controls.common_controls.TreeViewWrapper(cang_hwnd)
    cang_window.click()
    cang_window.type_keys('^C')
    s=pywinauto.clipboard.GetData().replace('\t',',')
    pywinauto.clipboard.EmptyClipboard()
    cang_df = pd.read_csv(StringIO(s),dtype={'证券代码': object,'可用余额':int},usecols=[0,1,2,3,4,5,6,7,8,9,10])
    cang_df.drop(cang_df[cang_df['可用余额'] == 0].index, inplace=True)
    return cang_df
def get_money():
    global hwnd,left_window,main_window
    d={}
    left_window.select('\\查询[F4]\\资金股份')
    money_hwnd = pywinauto.findwindows.find_windows(top_level_only=False, class_name='CVirtualGridCtrl', parent=hwnd)[1]
    money_window = pywinauto.controls.common_controls.TreeViewWrapper(money_hwnd)
    money_window.click()
    money_window.type_keys('^C')
    s=pywinauto.clipboard.GetData().replace('\t',',').split(',')
    d['资金余额']=float(s[8]);d['可用余额']=float(s[9]);d['总市值']=float(s[10]);d['总资产']=float(s[11])
    left_window.select('\\双向委托')
    main_window.type_keys('{F6}')
    return d
#异常处理 弹窗
def close_pop():
    global app
    time.sleep(0.2)
    try:
        pophwnd = win32gui.GetForegroundWindow()
        if pophwnd!=hwnd:
            bpop_hwnd = pywinauto.findwindows.find_windows(top_level_only=False, class_name='Button', parent=pophwnd)
            bp_window = app.window(handle=bpop_hwnd[0]) 
            bp_window.click()
    except:pass
#买入股票
def buy(code,price,number):
    global edit_windows_list,button_window_list
    edit_windows_list[0].type_keys(code)
    edit_windows_list[1].type_keys(price)
    edit_windows_list[2].type_keys(number)
    button_window_list[0].click()
    close_pop()
#卖出股票
def sell(code,price,number):
    global edit_windows_list,button_window_list
    edit_windows_list[3].type_keys(code)
    edit_windows_list[4].type_keys(price)
    edit_windows_list[5].type_keys(number)
    button_window_list[1].click()
    close_pop()
def chedan():
    global hwnd,button_window_list
    time.sleep(0.1)
    win32gui.SetForegroundWindow(hwnd) 
    button_window_list[2].click()
    time.sleep(0.1)
    close_pop()
