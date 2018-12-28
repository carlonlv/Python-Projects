We are trying to decrypt a message written to you in a language where you know all the words. Unfortunately the sender has forgotten to put any spaces into the message. So if the language includes the words abra, cada, c, ad and the message is ”abracadabra”, you should split it into ”abra c ad abra”. You will need to write a python code for the problem. The set of words will be given on the ﬁrst line of input (comma-separated), and the input string on the second. So if the ﬁle input.txt contains
he,head,admonished headmonished  
we will expect the output   
he admonished when we execute % python decode.py input.txt  
If there are multiple decodings you can print any of them. If there is no decoding you should print nothing. We expect you to be able to handle 1000+ word vocabularies in a reasonable amount of time. 
