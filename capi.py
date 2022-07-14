##INDISPENSABLES
#from webserver import keep_alive
##
import discord
import random
import datetime
import logging
import logging.config
import json

##LIBRERIAS PARA EL GIF
import requests
import shutil
import os
from PIL import Image
from os import listdir, remove
from os.path import isfile, join
import imageio.v2 as imageio

###CAMBIAR CUANDO PASE DE PRUEBA AL ONLINE
###     LA PARTE DEL TOKEN
###CAMBIAR CUANDO PASE DE PRUEBA AL ONLINE
##Buscar ##CHECK DEBUG para lineas que tengo comentadas para debug
preventLogExc = True
capiVersion = 'b1'

#Log
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
})
filenamelog = f".\logs\logfile {str(datetime.datetime.now()).replace(':','.')}.txt"
logging.basicConfig(level=logging.DEBUG, filename=filenamelog, filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")

#Items
with open('./res/items.txt', encoding='utf-8') as f:
    c_items = f.read().splitlines()
#Sizes
with open('./res/sizes.txt', encoding='utf-8') as f:
    c_sizes = f.read().splitlines()
#Sizes
with open('./res/palettes.json', 'r') as f:
    c_palettes = json.load(f)

with open('./res/data.json', 'r') as f:
    c_capi = json.load(f)["capi"]

with open('./res/data.json', 'r') as f:
    c_challenge = json.load(f)["challenge"]

with open('./res/data.json', 'r') as f:
    c_pngOnly = json.load(f)["pngOnly"]

class CapiBot(discord.Client):
    ###Cuando inicia
    async def on_ready(self):
        """
        Mensaje de feedback cuando el bot esta activo
        """

        log('MAIN','======================================================================')
        log('MAIN',f'        [ {self.user} ] listo para trabajar!')
        log('MAIN',f'            >Items cargados: {len(c_items)}')
        log('MAIN',f'            >Tamaños cargados: {len(c_sizes)}')
        log('MAIN',f'            >Paletas cargadas: {len(c_palettes)}')
        log('MAIN','======================================================================')

    async def on_message(self, message):
        global c_items,c_sizes,c_palettes,c_capi,c_challenge,c_pngOnly
        """
        Base para la interacción entre el bot y los usuarios
        """

        #Establece el guild en el que se está llamando, indispensable para el funcionamiento de log()
        guild = message.guild

        """
        Interacción con los canales pngOnly.
        Borrar imagenes que no sean .gif o .png, además de avisar a los usuarios
        """
        try:
            #Canal pixel-art
            if message.channel.id in c_pngOnly:
                try:
                    #Manejar los attachments uno por uno
                    for i in message.attachments:
                        filename = i.filename
                        #Verificar .png o .gif
                        if not (filename[-4:] == '.png' or filename[-4:] == '.gif'):
                            #Archivos invalidos
                            log(guild,f'Formato de imagen incorrecto del usuario: {message.author} en el canal de pixel-art')
                            await message.delete()
                            log(guild,f'>Imagen borrada de {message.author} en el canal de pixel-art',1)
                            await message.author.send('Hola, ¡Soy Capi! He revisado el pixelart que has subido y he visto que no está en formato .png o .gif :sweat_smile: así que lo he tenido que borrar. \nIntenta volver a subirlo pero ahora con el formato .png o .gif Gracias! :heart: \nSi necesitas ayuda no dudes en pedirla en el Discord!')
                            log(guild,f'>Mensaje privado de ayuda enviado a {message.author}',1)
                except IndexError as e:
                    log('EXCEPTION',e)
        except AttributeError as e:
            log('EXCEPTION',e)

        try:
            """
            Interacción directa con los comandos de capi.
            Ver manual de usuario para descripciones
            """
            #Llamando al comando de capi
            if ('capi' in message.content.lower()) and not(message.author.bot):
                #Canal capi
                if message.channel.id in c_capi:
                    log(guild,f'Mensaje para capi recibido de {message.author}')

                    #Version
                    if 'info' in message.content.lower():
                        log(guild,'>Llamando el comando de: version',1)
                        await message.reply(f'Versión de Capi: {capiVersion}\nIdeas cargadas: {len(c_items)}\nTamaños cargados: {len(c_sizes)}\nPaletas cargadas: {len(c_palettes)}')

                    #Saludar
                    if 'hola' in message.content.lower():
                        log(guild,'>Llamando el comando de: hola',1)
                        await message.reply('Hola! :heart:')
                    #Idea
                    if 'idea' in message.content.lower():
                        log(guild,'>Llamando el comando de: idea',1)
                        await message.reply(f'>💡  Puedes dibujar algo relacionado con **[ {random.choice(c_items).upper()} ]**')

                    #Reto
                    if 'reto' in message.content.lower():
                        log(guild,'>Llamando el comando de: reto',1)
                        reply = f'>💡  Puedes dibujar algo relacionado con **[ {random.choice(c_items).upper()} ]**'
                        reply = f'{reply}\n  📐 Tamaño del canvas: \t\t**{random.choice(c_sizes)}**'
                        palette = random.choice(list(c_palettes.keys()))
                        reply = f'{reply}\n  🌈 Paleta de colores: \t\t**{palette}** \n\t\t\t\t\t\t\t\t\t\t\tCreada por: _{c_palettes[palette][1]}_'
                        for i in c_palettes[palette][2:]:
                            reply = f'{reply}\n\t\t\t#{i}'
                        await message.reply(file=discord.File(f'./res/palettes/{palette}.png'), content=reply)

                    #Colores
                    if 'colores' in message.content.lower():
                        log(guild,'>Llamando el comando de: colores',1)
                        palette = random.choice(list(c_palettes.keys()))
                        reply = f'🌈 Paleta de colores: **{palette}** _creada por: {c_palettes[palette][1]}_'
                        for i in c_palettes[palette][2:]:
                            reply = f'{reply}\n\t\t\t#{i}'
                        await message.reply(file=discord.File(f'./res/palettes/{palette}.png'), content=reply)

                    #Gracias
                    if 'gracias' in message.content.lower():
                        log(guild,'>Llamando el comando de: gracias',1)
                        await message.add_reaction('❤')

                    #Mensaje default
                    if 'capi' == message.content.lower():
                        log(guild,'>Llamando el comando de: default',1)
                        await message.add_reaction('❓')
                        await message.author.send('¡Hola! Soy Capi <3\nTe puedo ayudar si quieres dibujar algo pero no sabes que!\nMe puedes pedir una idea, reto o colores para tu próximo pixel-art!')

                #Comandos privados
                #Data
                if ('-data' in message.content) and authRole(message.guild,message.author,message.author.roles):
                    log(guild,f'>Llamando el comando privado de: -data para {message.author} en el canal {message.channel}',1)
                    await message.delete()
                    await message.author.send(f'         >CANALES\n{message.guild.text_channels}')
                    await message.author.send(f'         >ROLES\n{message.guild.roles}')
                    await message.author.send(f'         >DATOS\n{loadJson("./res/data.json")}')

                #Crear el gif de challenge
                if ('-challengeGif' in message.content) and authRole(message.guild,message.author,message.author.roles):
                    log(guild,f'>Llamando el comando privado de: -challengeGif para {message.author} en el canal {message.channel}',1)
                    await message.delete()
                    time = 1
                    if message.content.find('-time:') != -1:
                        log(guild,f'>Llamando el subcomando privado de -challengeGif: -time para {message.author} en el canal {message.channel}',2)
                        time = float(message.content[message.content.find('-time:')+6:message.content.find('-time:')+9])
                    if makeGif(guild, message.author, message.channel.name, f'./{message.guild.id}/', f'./{message.guild.id}/output/movie.gif',time):
                        await message.channel.send(file=discord.File(f'./{message.guild.id}/output/movie.gif'), content='Gif autogenerado por Capi')
                        remove(f'./{message.guild.id}/output/movie.gif')

                #Comando CAPI, utilizado para el setup de los canales
                if ('-capi' in message.content) and authRole(message.guild,message.author,message.author.roles):
                    log(guild,f'>Llamando el comando privado de: -capi para {message.author} en el canal {message.channel}',1)
                    await message.delete()
                    if ('-capiAdd' in message.content):
                        log(guild,f'>Llamando el subcomando privado de -capi: -capiAdd para {message.author} en el canal {message.channel}',2)
                        data = loadJson('./res/data.json')
                        if not message.channel.id in data["capi"]:
                            data["capi"].append(message.channel.id)
                            dumpJson('./res/data.json',data)
                            log(guild,f'>Id {message.id} guardado en capi de data.json',3)
                            await message.author.send(f'El canal **[{message.channel.name}#{message.channel.id}]** ha sido establecido como un canal Capi')
                        else:
                            log(guild,f'>Id {message.id} rechazada en el guardado en capi de data.json',3)
                            await message.author.send(f'El canal **[{message.channel.name}#{message.channel.id}]** ya está establecido como un canal Capi')
                        c_capi = loadJson('./res/data.json')["capi"]
                    elif ('-capiDel' in message.content):
                        log(guild,f'>Llamando el subcomando privado de -capi: -capiDel para {message.author} en el canal {message.channel}',2)
                        data = loadJson('./res/data.json')
                        if message.channel.id in data["capi"]:
                            data["capi"].remove(message.channel.id)
                            dumpJson('./res/data.json',data)
                            log(guild,f'>Id {message.id} eliminado en capi de data.json',3)
                            await message.author.send(f'El canal **[{message.channel.name}#{message.channel.id}]** se ha eliminado como un canal Capi')
                        else:
                            log(guild,f'>Id {message.id} rechazada en el eliminado en capi de data.json',3)
                        c_capi = loadJson('./res/data.json')["capi"]
                    elif ('-challengeSet' in message.content):
                        log(guild,f'>Llamando el subcomando privado de -capi: -challengeSet para {message.author} en el canal {message.channel}',2)
                        try:
                            os.mkdir(f'./{message.guild.id}')
                        except FileExistsError:
                            pass
                        try:
                            os.mkdir(f'./{message.guild.id}/output')
                        except FileExistsError:
                            pass
                        data = loadJson('./res/data.json')
                        if not str(message.guild.id) in list(data["challenge"].keys()):
                            data["challenge"][str(message.guild.id)] = 0
                        if not message.channel.id == data["challenge"][str(message.guild.id)]:
                            data["challenge"][str(message.guild.id)] = message.channel.id
                            folder = f'./{message.guild.id}'
                            for filename in os.listdir(folder):
                                file_path = os.path.join(folder, filename)
                                try:
                                    if os.path.isfile(file_path) or os.path.islink(file_path):
                                        os.unlink(file_path)
                                    elif os.path.isdir(file_path):
                                        shutil.rmtree(file_path)
                                except Exception as e:
                                    pass
                            os.mkdir(f'./{message.guild.id}/output')
                            dumpJson('./res/data.json',data)
                            log(guild,f'>Id {message.channel.id} establecido para la guild {message.guild.id} en data.json',3)
                            c_challenge = loadJson('./res/data.json')["challenge"]
                            await message.author.send(f'El canal **[{message.channel.name}#{message.channel.id}]** se ha establecido para el servidor **[{message.guild.name}#{message.guild.id}]** como el canal actual del challenge')

                    elif ('-pngAdd' in message.content):
                        log(guild,f'>Llamando el subcomando privado de -capi: -pngAdd para {message.author} en el canal {message.channel}',2)
                        data = loadJson('./res/data.json')
                        if not message.channel.id in data["pngOnly"]:
                            data["pngOnly"].append(message.channel.id)
                            dumpJson('./res/data.json',data)
                            log(guild,f'>Id {message.id} guardado en pngOnly de data.json',3)
                            await message.author.send(f'El canal **[{message.channel.name}#{message.channel.id}]** ha sido establecido como un canal pngOnly')
                        else:
                            log(guild,f'>Id {message.id} rechazada en el guardado en pngOnly de data.json',3)
                            await message.author.send(f'El canal **[{message.channel.name}#{message.channel.id}]** ya está establecido como un canal pngOnly')
                        c_pngOnly = loadJson('./res/data.json')["pngOnly"]

                    elif ('-pngDel' in message.content):
                        log(guild,f'>Llamando el subcomando privado de -capi: -pngDel para {message.author} en el canal {message.channel}',2)
                        data = loadJson('./res/data.json')
                        if message.channel.id in data["pngOnly"]:
                            data["pngOnly"].remove(message.channel.id)
                            dumpJson('./res/data.json',data)
                            log(guild,f'>Id {message.id} eliminado de pngOnly en data.json',3)
                            await message.author.send(f'El canal **[{message.channel.name}#{message.channel.id}]** ha sido eliminado como un canal pngOnly')
                        else:
                            log(guild,f'>Id {message.id} rechazada en el eliminado en pngOnly de data.json',3)
                        c_pngOnly = loadJson('./res/data.json')["pngOnly"]

                    else:
                        await message.author.send('El comando -capi requiere de un subcomando válido para operar. Consulta el manual de usuario.')

        except AttributeError as e:
            log('EXCEPTION',e)


        """
        Interacción en el canal challenge, donde las imagenes subidas se reescalan y guardan para su
        posterior uso
        """
        try:
            ##Para el canal de challenge
            if message.channel.id == c_challenge[str(message.guild.id)]:
                ##Guardar pics
                try:
                    url = message.attachments[0].url
                    if (str(message.author) != str(self.user)) and (url[0:26] == "https://cdn.discordapp.com"):   # look to see if url is from discord
                        r = requests.get(url, stream=True)
                        imageName = f'{message.id}.png'
                        with open(f'./{message.guild.id}/{imageName}', 'wb') as f:
                            log(guild, f'Añadiendo {imageName} a la carpeta con id {message.guild.id}')
                            shutil.copyfileobj(r.raw, f)
                        img = Image.open(f'./{message.guild.id}/{imageName}')
                        img = img.resize((320, 320), Image.ANTIALIAS)
                        img.save(f'./{message.guild.id}/{imageName}')
                except IndexError as e:
                    log('EXCEPTION',e)

        except Exception as e:
            log('EXCEPTION',e)

    async def on_message_delete(self, message):

        """
        Interacción en el canal challenge, donde los mensajes eliminados, se eliminan los respectivos
        dibujos guardados.
        """
        try:
            ##Para el canal de challenge
            if message.channel.id == c_challenge[str(message.guild.id)]:
                #Eliminar pics
                try:
                    remove(f'./{message.guild.id}/{message.id}.png')
                    log(guild,f'Quitando {message.id}.png de la carpeta id {message.guild.id}')
                except Exception as e:
                    log('EXCEPTION',e)

        except AttributeError as e:
            log('EXCEPTION',e)

def log(guild,input,ident=0):
    """
    Función de debug, donde el input se transforma en output en la consola y en el archivo de log
    """
    txtIdent = ident * "\t"
    if preventLogExc:
        if guild != 'EXCEPTION':
            print(f'[{guild}]{txtIdent}{input}')
            logging.info(f'[{guild}]{txtIdent}{input}')
    else:
        print(f'[{guild}]{txtIdent}{input}')
        logging.info(f'[{guild}]{txtIdent}{input}')

def authRole(guild,who,*roles):
    """
    Función para verificación de rol
    """
    log(guild,f'Autentificación solicitada por {who}')
    auth = False
    for i in roles:
        if ('ADMIN' in str(i)) or ('CONFIGURADOR' in str(i)):
            auth = True
    if auth:
        log(guild,f'>Autentificación aprobada a {who}',1)
    else:
        log(guild,f'>Autentificación rechazada a {who}',1)
    return auth

def makeGif(guild,who,channel,input,output,time):
    """
    Función que dado una carpeta de input, toma las imágenes y devuelve un gif en una carpeta de output
    """
    log(guild,f'>Creando gif en solicitud de {who} para el canal {channel}',2)
    try:
        images = []
        filenames = [f for f in listdir(input) if isfile(join(input, f))]
        for i in filenames:
            images.append(imageio.imread(f'{input}{i}'))
        imageio.mimsave(output, images, duration=time)
        log(guild,f'>Gif completado en solicitud de {who} para el canal {channel}',3)
        return True
    except Exception as e:
        log(guild,f'>Error en la solicitud de un gif de {who} para el canal {channel}',3)
        return False

def loadJson(dir):
    with open(dir, 'r') as f:
        return json.load(f)

def dumpJson(dir,data):
    with open(dir, 'w') as f:
        json.dump(data, f, indent = 4)

CapiBot().run('xx')

#keep_alive()
#TOKEN = os.environ.get("DISCORD_TOKEN")
#CapiBot().run(TOKEN)
