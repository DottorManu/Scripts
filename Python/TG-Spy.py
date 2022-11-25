#This script is still incomplete
#Ispired by the botnet of @Epock and @JacopoTediosi on Telegram
#This script must be the "Telegram-God-Eye"
#ACTUALLY USING PYROGRAM
import asyncio
import time
import mysql.connector
from pyrogram import Client, enums, errors
from pyrogram.enums import ChatType
from pyrogram.raw import functions, types
from pyrogram.types import Chat
from pyrogram.errors import RPCError, BadRequest, FloodWait

api_id = xxx
api_hash = "xxx"
#Account TG + Account DB
mydb = mysql.connector.connect(
  host="localhost",
  user="xxx",
  password="xxx",
  database="xxx"
)

mycursor = mydb.cursor()

def Clear_DB():
    mycursor.execute("TRUNCATE TABLE `GRUPPI`")
    mycursor.execute("TRUNCATE TABLE `UTENTI`")
    mycursor.execute("TRUNCATE TABLE `CORRELAZIONI`")
    mydb.commit()

def Console_Output(group, member):
    print(group)
    print("GRUPPO: " + str(group.title) + " Con ID: " + str(group.id))
    print("Utente: " + str(member.user.first_name) + " " + str(member.user.last_name) + " con Username: " + str(member.user.username) + " e con ID: " + str(member.user.id) + " presente nel gruppo: " + str(group.title) + " con ID: " + str(group.id))

def Inserisci_Correlazione(id_gruppo, id_utente):
    sql = "INSERT INTO `CORRELAZIONI` (id_gruppo, id_utente) VALUES (%s, %s)"
    val = (id_gruppo, id_utente)
    print("INSERTING INTO CORRELATIONS: " + str(id_gruppo) + " AND " + str(id_utente))
    mycursor.execute(sql, val)
    mydb.commit()


def Inserisci_Gruppo(id_gruppo, nome_gruppo, descrizione_gruppo, username_gruppo, numero_partecipanti):
    sql = "INSERT INTO `GRUPPI` (id_gruppo, nome_gruppo, descrizione_gruppo, username_gruppo, numero_partecipanti) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE nome_gruppo = %s, descrizione_gruppo = %s, username_gruppo = %s, numero_partecipanti = %s"
    val = (id_gruppo, str(nome_gruppo), str(descrizione_gruppo), str(username_gruppo), numero_partecipanti, str(nome_gruppo), str(descrizione_gruppo), str(username_gruppo), numero_partecipanti)
    mycursor.execute(sql, val)
    mydb.commit()

def Inserisci_Utente(id_utente, nome_utente, cognome_utente, username_utente):
    sql = "INSERT INTO `UTENTI` (id_utente, nome_utente, cognome_utente, username_utente) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE nome_utente = %s, cognome_utente = %s, username_utente = %s"
    val = (id_utente, str(nome_utente), str(cognome_utente), str(username_utente), str(nome_utente), str(cognome_utente), str(username_utente))
    mycursor.execute(sql, val)
    mydb.commit()

#MAIN ENTRYPOINT
async def main():
        async with Client("my_account", api_id, api_hash) as app:

            Clear_DB()

            mycursor.execute("SELECT * FROM LISTA_GRUPPI")
            righe_gruppi = mycursor.fetchall()
            lista_gruppi = [righe[0] for righe in righe_gruppi]
            print(lista_gruppi)

            for group in lista_gruppi:
                print(group)
                #TRY/EXCEPT for BadRequest AND FloodWait Exceptions
                try:
                    group = await app.get_chat(group)
                except(BadRequest):
                    print("ERROR: BAD REQUEST! GROUP NOT FOUND!... SKIPPING...")
                    continue
                except FloodWait as e:
                    print("WARNING: FLOOD WAIT! Need to wait: " + str(e.value) + " seconds...")
                    await asyncio.sleep(e.value)
                    group = await app.get_chat(group)

                #CHECK AND SKIP PRIVATE GROUPS/CHANNELS
                if(isinstance(group, Chat) == False or group.type == ChatType.CHANNEL):
                    print("PRIVATE GROUP OR CHANNEL FOUND!... SKIPPING...")
                    continue
                
                #INSERTING GROUP INTO GROUPS TABLE
                Inserisci_Gruppo(group.id, group.title, group.description, group.username, group.members_count)

                #GET MEMBERS
                async for member in app.get_chat_members(group.id):

                    Console_Output(group, member)

                    #time.sleep(0.001) #Sleep for avoiding crash/flood wait

                    Inserisci_Utente(member.user.id, member.user.first_name, member.user.last_name, member.user.username)
                    
                    Inserisci_Correlazione(group.id, member.user.id)

asyncio.run(main())

#FUNZIONI DA TESTARE/USARE:
#httpss://docs.pyrogram.org/api/methods/join_chat#pyrogram.Client.join_chat
#httpss://docs.pyrogram.org/api/methods/get_chat_history#pyrogram.Client.get_chat_history

#AGGIUNGERE AL DB:
#DATI: (LINK DEL GRUPPO SE PRESENTE - ADMIN DEI GRUPPO - CRONOLOGIA)

#TO DO LIST:
#1)Allargare la lista dei gruppi della botnet, magari partendo da flames network o equivalenti
#2)Fare in modo che, eventuali link d'invito per altri gruppi nei messaggi vengano automaticamente seguiti
#3)Velocizzare il tutto con account multipli
#4)OPTIONAL: Salvare i messaggi e finanziare lo spazio vendendo un rene
#5)Trovare un modo efficiente per aggiornare la botnet, possibilmente senza doverla ricreare da zero
#6)Storico/Cronologia dei cambi di Username/Nome/Cognome (tanto l'ID utente rimane lo stesso)
