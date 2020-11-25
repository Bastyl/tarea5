import imaplib

SERVER = 'imap.gmail.com'
USER = 'bastian.lopez@mail.udp.cl'
PASS = 'tel4cr31st3w333'
MAIL = 'bastian.lopez@mail.udp.cl'

server = imaplib.IMAP4_SSL(SERVER, 993)

server.login(USER, PASS)


status, count = server.select('Inbox') 

contador = int(count[0].decode("utf-8") ) #cuenta los mails totales

m = 0

"""  #ESTE WHILE SE USA SOLAMENTE PARA RECOLECTAR LOS 20 EMAILS Y SACARLES EL MESSAGE ID
while contador >= 0:
	
	status, data1 = server.fetch( bytes(str(contador), 'utf-8')    , "(BODY[HEADER.FIELDS (FROM)])") #from
	enviado_por = data1[0][1].decode("utf-8")

	if "no-reply@ieee-collabratec.org" in enviado_por:
		
		status, data = server.fetch( bytes(str(contador), 'utf-8')    , '(BODY[HEADER.FIELDS (MESSAGE-ID)])')
		print (data[0][1])
		print("========================================================")
		m += 1

	if m == 20:
		break

	contador -= 1
"""

#EMAIL SPOOFING 

expresion = "[a-z0-9]{16}\-[a-z0-9]{8}\-[a-z0-9]{4}\-[a-z0-9]{4}\-[a-z0-9]{4}\-[a-z0-9]{12}\-[0]{6}@email\.amazonses\.com"
datos = expresion.split('@') #Divid la expresion en dos partes y se trabaja con la de la izquierda
str_final = datos[0].split('\-') #quita los caracters de guion, quedando solo los subloques.

Emisor = 'no-reply@ieee-collabratec.org' #emisor del correo real.

status, data = server.fetch( bytes(str(contador), 'utf-8')    , '(BODY[HEADER.FIELDS (MESSAGE-ID)])') #toma el mensaje id del ultimo correo recibido
mensaje_id = data[0][1].decode("utf-8") # ej de salida: 7D479456B7794FCE887D2CE3F6D56C82@corp.parking.ru

status, data3 = server.fetch( bytes(str(contador), 'utf-8')    , "(BODY[HEADER.FIELDS (FROM)])") #toma el emisor del ultimo correo recibido
enviado_por = data3[0][1].decode("utf-8") # ej de salida: no-reply@ieee-collabratec.org

print(mensaje_id)
print(enviado_por)
#false = "7D479456B7794FCE887D2CE3F6D56C82@corp.parking.ru" # Usado para la prueba del message-ID
#false = "0100017177b044cf-055525c5-e6e2-463a-abe9-ea855256bae7-000000@email.amazonses.com"  Usado para la prueba del message-ID

false = mensaje_id[13:-5]
false = false.split('@') #sirve para trabajar con la parte izquierda del correo recibido
bloques = false[0].split('-') #subbloques


if len(str_final) != len(bloques or Emisor != enviado_por[7:-5]): #si el correo rcibido tiene distinta cantidad de bloques o el emisor es distinto, entonces es falso
	print("Es falso")

elif len(bloques[0]) != 16 or len(bloques[1]) != 8 or len(bloques[2]) != 4 or len(bloques[3]) != 4 or len(bloques[4]) != 4 or len(bloques[5]) != 12 or len(bloques[6]) != 6:
	print("Es false") #compara los largos de los bloques del correo recibido con el de la expresion regular.

else:
	print("Es verdadero")



server.close()
server.logout()

