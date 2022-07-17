##INDISPENSABLES
#from webserver import keep_alive
##
import discord
import random
import datetime
import logging
import logging.config
import json
import math

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
preventLogExc = False
capiVersion = '1.3'

#Log
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
})
filenamelog = f"./logs/logfile {str(datetime.datetime.now()).replace(':','.')}.txt"
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
                        url = i.url
                        #Verificar .png o .gif
                        if not formatValid(url):
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


                #Comando CAPI, utilizado para el setup de los canales
                if ('-capi' in message.content) and authRole(message.guild,message.author,message.author.roles):
                    log(guild,f'>Llamando el comando privado de: -capi para {message.author} en el canal {message.channel}',1)
                    await message.delete()
                    ##AÑADIR CANAL CAPI
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
                    #QUITAR CANAL CAPI
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
                    #AÑADIR CANAL PNGONLY
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
                    #QUITAR CANAL PNGONLY
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
                    #LLAMADO CUANDO NO SE ESCRIBE UN SUBCOMANDO VALIDO
                    else:
                        await message.author.send('El comando -capi requiere de un subcomando válido para operar. Consulta el manual de usuario.')

                #COMANDO PARA ESTABLECER COMPORTAMIENTOS DE LOS CHALLENGE
                if ('-challenge' in message.content) and authRole(message.guild,message.author,message.author.roles):
                    log(guild,f'>Llamando el comando privado de: -challenge para {message.author} en el canal {message.channel}',1)
                    await message.delete()
                    #ESTABLECER LA CONFIGURACION INICIAL DEL CANAL CHALLENGE
                    if ('-start' in message.content):
                        log(guild,f'>Llamando el subcomando privado de -challenge: -start para {message.author} en el canal {message.channel}',2)
                        try:
                            os.mkdir(f'./{message.guild.id}')
                        except FileExistsError:
                            pass
                        try:
                            os.mkdir(f'./{message.guild.id}/output')
                        except FileExistsError:
                            pass
                        try:
                            os.mkdir(f'./{message.guild.id}/podium')
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
                            os.mkdir(f'./{message.guild.id}/podium')
                            dumpJson('./res/data.json',data)
                            log(guild,f'>Id {message.channel.id} establecido para la guild {message.guild.id} en data.json',3)
                            c_challenge = loadJson('./res/data.json')["challenge"]
                            await message.author.send(f'El canal **[{message.channel.name}#{message.channel.id}]** se ha establecido para el servidor **[{message.guild.name}#{message.guild.id}]** como el canal actual del challenge')
                    #COMPORTAMIENTO CUANDO SE TERMINA EL CHALLENGE
                    elif '-end' in message.content:
                        log(guild,f'>Llamando el subcomando privado de -challenge: -end para {message.author} en el canal {message.channel}',2)
                        time = 1
                        if message.content.find('-time:') != -1:
                            log(guild,f'>Llamando el subcomando privado de -challenge: -end -time para {message.author} en el canal {message.channel}',2)
                            time = float(message.content[message.content.find('-time:')+6:message.content.find('-time:')+9])
                        await message.author.send('Ejecutando -end, podría tardar unos momentos en cargar resultados!')
                        #GIF
                        makeGif(guild, message.author, message.channel.name, f'./{message.guild.id}/', f'./{message.guild.id}/output/movie.gif',time)
                        #COLLAGE
                        images = []
                        filenames = [f for f in listdir(f'./{message.guild.id}/') if isfile(join(f'./{message.guild.id}/', f))]
                        for i in filenames:
                            img = Image.open(f'./{message.guild.id}/{i}')
                            img = img.resize((160, 160),Image.NEAREST)
                            images.append(img)
                        columns = math.floor(math.sqrt(len(filenames)))
                        rows = columns + math.ceil((len(filenames) - columns**2) / columns)
                        new = Image.new("RGBA", (160*(columns+2),160*(rows+3)), (239, 249, 214))
                        new.paste(Image.open('./res/textOverlay.png'), (math.floor(((160*(columns+2))/2)-250),80))
                        current = 0
                        for x in range(0,rows):
                            for y in range(0,columns):
                                try:
                                    new.paste(images[current], ((y*160)+160,(x*160)+320))
                                    current+=1
                                except Exception:
                                    pass
                        new.save(f'./{message.guild.id}/output/collage.png')
                        #FETCH DATA
                        reactions = {}
                        data = [f for f in listdir(f'./{message.guild.id}/') if isfile(join(f'./{message.guild.id}/', f))]
                        data = [int(x.replace('.png',''))for x in data]
                        for i in data:
                            count = 0
                            work = await message.channel.fetch_message(i)
                            for j in work.reactions:
                                count += 1
                            reactions[i] = count
                        #GET 3 PODIUM
                        podium = []
                        for i in list(reactions.keys()):
                            if len(podium) == 3:
                                podium = podiumSort(podium,reactions)
                                if reactions[i] >= reactions[podium[2]]:
                                    podium[2] = i
                                    podium = podiumSort(podium,reactions)
                            if len(podium) < 3:
                                podium.append(i)
                        new = Image.new("RGBA", (1600,960))
                        new.paste(Image.open(f'./res/Overlay.png'), (0,0))
                        new.paste(Image.open(f'./{message.guild.id}/{podium[0]}.png'), (640,160))
                        new.paste(Image.open(f'./{message.guild.id}/{podium[1]}.png'), (160,320))
                        new.paste(Image.open(f'./{message.guild.id}/{podium[2]}.png'), (1120,320))
                        new.save(f'./{message.guild.id}/podium/podium.png')
                        msg1 = await message.channel.fetch_message(podium[0])
                        msg2 = await message.channel.fetch_message(podium[1])
                        msg3 = await message.channel.fetch_message(podium[2])

                        #OUTPUT
                        await message.channel.send(file=discord.File(f'./{message.guild.id}/output/movie.gif'), content='**:heart: Este challenge se da por finalizado. ¡Gracias por participar a todos! :heart:**\n‎')
                        remove(f'./{message.guild.id}/output/movie.gif')
                        await message.channel.send(file=discord.File(f'./{message.guild.id}/output/collage.png'), content='')
                        remove(f'./{message.guild.id}/output/collage.png')
                        await message.channel.send(file=discord.File(f'./{message.guild.id}/podium/podium.png'), content='‎\n**<<Los pixel-arts destacados por voto popular>>**\n‎')
                        remove(f'./{message.guild.id}/podium/podium.png')
                        await message.channel.send(f'‎\nFelicidades a [:first_place:]<@{msg1.author.id}> [:second_place:]<@{msg2.author.id}> [:third_place:]<@{msg3.author.id}>')

                    elif '-fetch' in message.content:
                        log(guild,f'>Llamando el subcomando privado de -challenge: -fetch para {message.author} en el canal {message.channel}',2)
                        data = await message.channel.history(limit=200).flatten()
                        count = 0
                        try:
                            for i in data:
                                url = i.attachments[0].url
                                if formatValid(url,jpg=True):
                                    r = requests.get(url, stream=True)
                                    imageName = f'{i.id}.png'
                                    with open(f'./{i.guild.id}/{imageName}', 'wb') as f:
                                        log(guild, f'Añadiendo {imageName} a la carpeta con id {i.guild.id}',3)
                                        shutil.copyfileobj(r.raw, f)
                                    img = Image.open(f'./{i.guild.id}/{imageName}')
                                    img = img.resize((320, 320), Image.NEAREST)
                                    img.save(f'./{i.guild.id}/{imageName}')
                                    count += 1
                            await message.author.send(f'Se han conseguido {count} imágenes en el canal challenge **[{message.channel.name}#{message.channel.id}]**')
                        except FileNotFoundError:
                            await message.author.send('Primero establece el canal como un canal challenge usando el comando: capi -challenge -set')
                    else:
                        await message.author.send('El comando -challenge requiere de un subcomando válido para operar. Consulta el manual de usuario.')

        except AttributeError as e:
            log('EXCEPTION',e)


        try:
            """
            Interacción en el canal challenge, donde las imagenes subidas se reescalan y guardan para su
            posterior uso
            """
            ##Para el canal de challenge
            if message.channel.id == c_challenge[str(message.guild.id)]:
                ##Guardar pics
                try:
                    url = message.attachments[0].url
                    if ((str(message.author) != str(self.user)) and (formatValid(url, jpg=True))):   # look to see if url is from discord
                        await message.add_reaction('❤')
                        r = requests.get(url, stream=True)
                        imageName = f'{message.id}.png'
                        with open(f'./{message.guild.id}/{imageName}', 'wb') as f:
                            log(guild, f'Añadiendo {imageName} a la carpeta con id {message.guild.id}')
                            shutil.copyfileobj(r.raw, f)
                        img = Image.open(f'./{message.guild.id}/{imageName}')
                        img = img.resize((320, 320),Image.NEAREST)
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
                    log(message.guild,f'Quitando {message.id}.png de la carpeta id {message.guild.id}')
                    remove(f'./{message.guild.id}/{message.id}.png')
                except Exception as e:
                    log('EXCEPTION',e)

        except Exception as e:
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

def formatValid(url, jpg=False):
    if not jpg:
        if ((url[0:26] == "https://cdn.discordapp.com") and ((url[-4:] == '.png') or (url[-4:] == '.gif'))):
            return True
        else:
            return False
    else:
        if ((url[0:26] == "https://cdn.discordapp.com") and ((url[-4:] == '.png') or (url[-4:] == '.gif') or (url[-4:] == '.jpg'))):
            return True
        else:
            return False

def podiumSort(podium,reactions):
    sorted = [0,0,0]
    max = 0
    for i in podium:
        if reactions[i] >= max:
            max = reactions[i]
            sorted[0] = i
    mid = 0
    for i in podium:
        if not i in sorted:
            if reactions[i] >= mid:
                mid = reactions[i]
                sorted[1] = i
    for i in podium:
        if not i in sorted:
            sorted[2] = i
    return sorted

def loadJson(dir):
    with open(dir, 'r') as f:
        return json.load(f)

def dumpJson(dir,data):
    with open(dir, 'w') as f:
        json.dump(data, f, indent = 4)

CapiBot().run('xx')
