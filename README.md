# Description

The program must first parse the file and load it in memory. Once that is done, the program will start listening on a TCP socket.

When a client connects, it can make lookup requests. It sends one AOR per line. The server responds with the corresponding JSON object.

For example, if a client sends:

```
0142e2fa3543cb32bf000100620002
```

The server will return:

```
{"addressOfRecord":"0142e2fa3543cb32bf000100620002","tenantId":"0127d974-f9f3-0704-2dee-000100420001","uri":"sip:0142e2fa3543cb32bf000100620002@10.21.21.127;jbcuser=cpe70;x-ebcid=AsfApcJMpgA","contact":"<sip:0142e2fa3543cb32bf000100620002@10.21.21.127;jbcuser=cpe70;x-ebcid=AsfApcJMpgA>;methods=\"INVITE, ACK, BYE, CANCEL, OPTIONS, INFO, MESSAGE, SUBSCRIBE, NOTIFY, PRACK, UPDATE, REFER\"","path":["<sip:Mi0xOTkuMTkyLjE2NS4xOTQtMTk2MjI@10.119.255.103:5060;lr>"],"source":"199.192.165.194:19622","target":"162.250.60.10:5061","userAgent":"polycom.vvx.600","rawUserAgent":"PolycomVVX-VVX_600-UA/5.4.5.6770","created":"2016-12-12T22:40:40.764Z","lineId":"013db2ba-2175-6d29-6157-000100620002"}
```

The client may send as many requests as it wants, one after the other.  If a TCP connection is inactive for more than 10 seconds, the server closes it. If an AOR cannot be found, the server returns an empty line.

# Usage

How to use the application list of option available : 

```
$ python server/server.py -h
usage: server.py [-h] [--data DATA] [--ip IP] [--log LOG] [--port PORT]
                 [--verbose]

Sever to provide SIP directory

optional arguments:
  -h, --help            show this help message and exit
  --data DATA, -d DATA  SIP AOR the load
  --ip IP, -i IP        define ip to bind service
  --log LOG, -l LOG     define log file
  --port PORT, -p PORT  define port for tcp listening
  --verbose, -v         Unable Verbose mode
```


Example of utilization, data available here : [regs](./data/regs) :

```
$ python server/server.py --data ./data/regs --port 8080  -v
INFO: 2018-09-30 20:40:29,216 hoshi X3:server.py[28487]: (xerus) msg:Opening socket : 127.0.0.1:8080
INFO: 2018-09-30 20:40:29,226 hoshi X3:server.py[28487]: (xerus) msg:System loaded : 501 entry
INFO: 2018-09-30 20:40:29,226 hoshi X3:server.py[28487]: (xerus) msg:Server is listening for connections

```

Testing it with telnet 

```
$ telnet 127.0.0.1 8080 
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
no a good one

0148c1f489badb837d000100620002
{'addressOfRecord': '0148c1f489badb837d000100620002', 'tenantId': '0127d974-f9f3-0704-2dee-000100420001', 'uri': 'sip:0148c1f489badb837d000100620002@9.98.167.222;jbcuser=cpe70', 'contact': '<sip:0148c1f489badb837d000100620002@120.133.72.122;jbcuser=cpe70>;methods="INVITE, ACK, BYE, CANCEL, OPTIONS, INFO, MESSAGE, SUBSCRIBE, NOTIFY, PRACK, UPDATE, REFER"', 'path': ['<sip:Mi0xOTkuMTkyLjE2NS4xOTQtMTk2MjI@61.0.24.25:5060;lr>'], 'source': '191.12.63.101:19622', 'target': '69.92.33.38:5061', 'userAgent': 'polycom.vvx.500', 'rawUserAgent': 'PolycomVVX-VVX_500-UA/59.124.31.194', 'created': '2016-12-13T04:48:30.889Z', 'lineId': '0148c1f4-8913-4d7f-d37d-000100620002'}^]
telnet> q
Connection closed.
```

# For Dev

If you perform modification to the application a uniitest is available :

```
$ python unittestSip.py 
test_01_SocketConnection (__main__.ValisationServerSip)
First Test : validating TCP connexion work ... ok
test_02_RequestAOR (__main__.ValisationServerSip)
Second Test : Request one AOR existing in the directory ... ok
test_03_Wrong_RequestAOR (__main__.ValisationServerSip)
Third Test : Request a wrong AOR ... ok
test_04_RequestAOR_3_time (__main__.ValisationServerSip)
fourth Test : make multiple AOR request ... ok
test_05_timeout_10_sec (__main__.ValisationServerSip)
fifth Test : validate server timeout after 10 second ... Need to be done issue #5
ok

----------------------------------------------------------------------
Ran 5 tests in 10.022s

OK
```

Log file is available :

```
$ head -20 logfile 
INFO: 2018-09-30 20:42:43,884 hoshi X3:server.py[29911]: (xerus) msg:Opening socket : 127.0.0.1:1234
INFO: 2018-09-30 20:42:43,894 hoshi X3:server.py[29911]: (xerus) msg:System loaded : 501 entry
INFO: 2018-09-30 20:42:43,894 hoshi X3:server.py[29911]: (xerus) msg:Server is listening for connections

INFO: 2018-09-30 20:42:45,888 hoshi X3:server.py[29922]: (xerus) msg:Opening socket : 127.0.0.1:1234
INFO: 2018-09-30 20:42:45,898 hoshi X3:server.py[29922]: (xerus) msg:System loaded : 501 entry
INFO: 2018-09-30 20:42:45,898 hoshi X3:server.py[29922]: (xerus) msg:Server is listening for connections

INFO: 2018-09-30 20:42:46,836 hoshi X3:server.py[29922]: (xerus) msg:Server is listening for connections

INFO: 2018-09-30 20:42:46,836 hoshi X3:server.py[29922]: (xerus) msg:Accepted connection from: 127.0.0.1:47754
INFO: 2018-09-30 20:42:46,836 hoshi X3:server.py[29922]: (xerus) msg:Client requested : 0142e2fa3543cb32bf000100620002
INFO: 2018-09-30 20:42:46,836 hoshi X3:server.py[29922]: (xerus) msg: Answer : 
INFO: 2018-09-30 20:42:46,836 hoshi X3:server.py[29922]: (xerus) msg:{'addressOfRecord': '0142e2fa3543cb32bf000100620002', 'tenantId': '0127d974-f9f3-0704-2dee-000100420001', 'uri': 'sip:0142e2fa3543cb32bf000100620002@109.149.135.172;jbcuser=cpe70', 'contact': '<sip:0142e2fa3543cb32bf000100620002@207.169.118.8;jbcuser=cpe70>;methods="INVITE, ACK, BYE, CANCEL, OPTIONS, INFO, MESSAGE, SUBSCRIBE, NOTIFY, PRACK, UPDATE, REFER"', 'path': ['<sip:Mi0xOTkuMTkyLjE2NS4xOTQtMTk2MjI@8.63.250.250:5060;lr>'], 'source': '29.211.204.173:19622', 'target': '60.124.57.147:5061', 'userAgent': 'polycom.vvx.600', 'rawUserAgent': 'PolycomVVX-VVX_600-UA/132.244.41.145', 'created': '2016-12-12T22:40:40.764Z', 'lineId': '013db2ba-2175-6d29-6157-000100620002'}
```

# Licence

Application in GPL v3 , complete licence available [LICENCE](./LICENCE)
