# # #coding: utf-8
# # import smtplib
# # from email.mime.text import MIMEText
# # from email.header import Header
# #
# # sender = '1483511346@qq.com'
# # receiver = '1483511346@qq.com'
# # subject = '离崩溃一线之遥'
# # smtpserver = 'smtp.qq.com'
# # username = '1483511346@qq.com'
# # password = 'bamtipnyrhucjahh'
# #
# # msg = MIMEText( 'Hello Python', 'text', 'utf-8' )
# # msg['Subject'] = Header( subject, 'utf-8' )
# #
# # smtp = smtplib.SMTP()
# # smtp.connect( smtpserver )
# # smtp.login( username, password )
# # smtp.sendmail( sender, receiver, msg.as_string() )
# # smtp.quit()
#
# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# # @File  : Main.py
# # @Author: MoMing
# # @Date  : 2019/7/5
# # @Desc  : 学习测试
#
# from time import sleep
# from socket import socket, AF_INET, SOCK_STREAM
#
#
# def get_conn_init():  # SMTP服务器初始化
#     host = 'mx1.qq.com'
#     port = 25
#     bufsize = 1024
#     s = socket(AF_INET, SOCK_STREAM)
#     try:
#         s.connect((host, port))
#     except TimeoutError:  # 链接超时
#         return False
#     s.recv(1024).decode('utf-8')
#     s.send('HELO qzone.work\r\nMAIL FROM:<admin@qzone.work>\r\n'.encode('utf-8'))
#     tmp = s.recv(bufsize).decode('utf-8')
#     msg = tmp.split('\r\n')
#     if len(msg) > 1 and msg[2][:3] == '250':
#         return s
#     else:
#         sleep(3)
#         return get_conn_init()
#
#
# def check(mail_):
#     global conn
#     conn.send(('RCPT TO:<' + mail_ + '>\r\n').encode('utf-8'))
#     reback = (conn.recv(1024).decode('utf-8'))[:3]
#     if not conn:
#         print('STMP服务器连接失败，马上重试！')
#         conn = get_conn_init()
#     elif reback == '452':  # 失效重连
#         conn.close()
#         conn = get_conn_init()
#     elif reback == '250':
#         return '已开通'
#     elif reback == '550':
#         return '未开通'
#     else:
#         return reback
#
#
# if __name__ == '__main__':
#     conn = get_conn_init()
#     check_list = ['23123@qq.com', '236546123@qq.com', 'fdsdf@qq.com', 'njfd@qq.com', 'mfgg@qq.com',
#                   '1538236552@qq.com']  # 待检测列表
#     for mail in check_list:
#         print(mail, check(mail))
#     else:
#         conn.close()

# var myChart_Cloud = echarts.init(document.getElementById('Cloud'));
# $(
#     function () {
#     //         fetchData(myChart_Cloud);
#     //         setInterval(getDynamicData, 2000)
#     //     }
#     // );
#     //
#     // function fetchData() {
#     //     $.ajax({
#     //         type: "GET",
#     //         url: "http://127.0.0.1:5000/WordCloud",
#     //         dataType: "json",
#     //         success: function (result) {
#     //             myChart_Cloud.setOption(result);
#     //             old_data = myChart_Cloud.getOption().series[0].data
#     //         }
#     //     });
#     // }
#     //
#     // function getDynamicData() {
#     //     $.ajax({
#     //         type: "GET",
#     //         url: "http://127.0.0.1:5000/getDynamicWordCloud",
#     //         dataType: "json",
#     //         success: function (result) {
#     //             old_data.push([result.name, result.value]);
#     //             myChart_Cloud.setOption({
#     //
#     //             })
#     //         }
#     //     })
#     // }
#     // // 指定图表的配置项和数据
#     // var option_Cloud = {{ Cloud_options | safe }};
#     //
#     // // 使用刚指定的配置项和数据显示图表。
#     // myChart_Cloud.setOption(option_Cloud);
#     // 基于准备好的dom，初始化echarts实例
print([i for i in range(10)])