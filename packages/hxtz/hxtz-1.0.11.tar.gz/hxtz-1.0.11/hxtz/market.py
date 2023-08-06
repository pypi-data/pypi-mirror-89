import requests,json,time
import pandas as pd
import http.client

#从百度网获取网格时间
def get_web_time():
    host='www.baidu.com'
    conn=http.client.HTTPConnection(host)
    conn.request("GET", "/")
    r=conn.getresponse()
    #r.getheaders() #获取所有的http头
    ts=  r.getheader('date') #获取http头date部分
     #将GMT时间转换成北京时间
    ltime= time.strptime(ts[5:25], "%d %b %Y %H:%M:%S")
    ttime=time.localtime(time.mktime(ltime)+8*60*60)
    dat="%u-%02u-%02u"%(ttime.tm_year,ttime.tm_mon,ttime.tm_mday)
    tm="%02u:%02u:%02u"%(ttime.tm_hour,ttime.tm_min,ttime.tm_sec)
    dt = dat+' '+tm
    return dt
#从集思录获取可转债信息
def get_kzz_list():
    n=0
    url = 'https://www.jisilu.cn/data/cbnew/cb_list/?___jsl=LST___t=1606733540803'
    headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"}
    while True:
        try:
            response = requests.get(url,headers=headers)
            break
        except:time.sleep(0.5);n+=1
        if n==2:return 0
    res_dict = json.loads(response.text)
    a_list=[];b_list=[];c_list=[];d_list=[];e_list=[];f_list=[];g_list=[];h_list=[];i_list=[];j_list=[];k_list=[];l_list=[];m_list=[]
    stock_list={'转债代码' : a_list,'转债名称' : b_list,'现价' : c_list,'涨跌幅' : d_list,'正股代码' : e_list,'正股名称' : f_list,
    '正股价' : g_list,'正股涨跌' : h_list,'溢价率' : i_list,'剩余年限' : j_list,'成交额' : k_list,'换手率' : l_list,'强赎' : m_list}
    for data in res_dict['rows']:
        a_list.append(data['cell']['pre_bond_id']);b_list.append(data['cell']['bond_nm'])
        c_list.append(data['cell']['price']);d_list.append(data['cell']['increase_rt'][:-1])
        e_list.append(data['cell']['stock_id']);f_list.append(data['cell']['stock_nm'])
        g_list.append(data['cell']['sprice']);h_list.append(data['cell']['sincrease_rt'][:-1])
        i_list.append(data['cell']['premium_rt'][:-1]);j_list.append(data['cell']['year_left'])
        k_list.append(data['cell']['volume']);l_list.append(data['cell']['turnover_rt'])
        m_list.append(data['cell']['force_redeem'])
    data=pd.DataFrame(stock_list)#将字典转换成为数据框
    data[['现价','涨跌幅','正股价','正股涨跌','溢价率','剩余年限','成交额','换手率']]=data[['现价',
            '涨跌幅','正股价','正股涨跌','溢价率','剩余年限','成交额','换手率']].astype('float')
    data['强赎']=data['强赎'].fillna(True)
    data=data[~data['强赎'].str.contains('最后交易日',na=False)]#.contains('最后交易日')]
    data.drop('强赎',axis=1,inplace=True)
    data = data.sort_values(by="涨跌幅",ascending=False)
    data = data.reset_index(drop=True)
    return data

#获取腾讯实时行情
def get_real_data(code):
    d = {};n=0
    url='http://qt.gtimg.cn/q='+code
    headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"}
    while True:
        try:
            response = requests.get(url,headers=headers)
            break
        except:time.sleep(0.5);n+=1
        if n==2:return 0
    html = response.text.split('~')
    d['code'] = code;d['name'] = html[1]
    d['open'] = float(html[5]);d['close'] = float(html[4])
    d['price'] = float(html[3]);d['high'] = float(html[33])
    d['low'] = float(html[34]);d['b_1'] = float(html[9])
    d['s_1'] = float(html[19]);d['vs_1'] = int(html[20])     #20是卖一的量
    d['vb_1'] = int(html[10]);d['dt_price'] = float(html[48])  #跌停价  
    d['zt_price'] = float(html[47]);d['liangbi'] = float(html[49]) #量比
    d['dt']=html[30]
    return d