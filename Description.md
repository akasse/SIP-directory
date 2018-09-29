Here's the challenge. You must write a program in the language of your choice that corresponds to the following description. You may use libraries. You may ask us questions.

Attached is a dump of SIP registrations. The program must first parse the file and load it in memory. Once that is done, the program will start listening on a TCP socket.

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


Good luck!
