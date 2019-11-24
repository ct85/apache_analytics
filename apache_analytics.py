#重要：このプログラムを実行するにはモジュール「apache-log-parser」をインストールしてください！
#$ py -m pip install apache-log-parser
#重要：このプログラムを実行するにはモジュール「pytz」をインストールしてください！
#$ py -m pip install pytz
#https://qiita.com/shotakaha/items/05287cd625176945322a
import apache_log_parser
#1行で成功するかやってみた
#line_parser = apache_log_parser.make_parser("%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"")
#test_data ='xxx.xxx.xxx.xxx - - [18/Feb/2019:23:58:36 +0900] "GET /ja/index.html HTTP/1.1" 301 240 "-" "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)"'
#log_line_data = line_parser(test_data)
#pprint(log_line_data)

def read_apache_log(ifn, logformat='%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"'):
    parser = apache_log_parser.make_parser(logformat)
    P = []
    E = []
    with open(ifn) as f:
        for line in f:
            try:
                parsed_line = parser(line)
                P.append(parsed_line)
            except ValueError:
                E.append(line)
    #pprint('=== Read Summary ===')
    #pprint('Parsed     : {0}'.format(len(P)))
    #pprint('ValueError : {0}'.format(len(E)))
    #pprint('====================')
    return P
ifn = '/var/log/httpd/access_log'
dic=read_apache_log(ifn)
#時間での解析
timecnt=[0 for _ in range(24)]
for i in range(len(dic)):
    t=dic[i]['time_received_tz_datetimeobj']
    timecnt[t.hour]+=1
for j in range(23):
    print(str(j)+"時台のアクセス件数は"+str(timecnt[j])+"件です。")
#リモートホストのアクセス件数
class Counter(dict):
    def __missing__(self, k):
        return 0
rcnt=Counter()
for i in range(len(dic)):
    r=dic[i]['remote_host']
    rcnt[r]+=1
print("リモートホスト:アクセス件数")
for i in range(len(rcnt)):
    print(list(rcnt.items())[i])
