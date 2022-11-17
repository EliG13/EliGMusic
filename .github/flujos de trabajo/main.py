import telebot
import os
import pytube

bot = telebot.TeleBot('5743659822:AAEu14gb0f3Q-Cv7mSBa4aKZarhgJi_5gFI')

#directorio donde guardar la descarga
path = "../Telegram/"

def main():
        bot.polling()

@bot.message_handler(commands=['musica'])
def musica(message):
    texto = message.text
    chat = message.chat.id
    l = len(texto)
    url = texto[8:l]  
    #URL del video de Youtube
    try:    
        yt = pytube.YouTube(url)
        imagen = yt.thumbnail_url

        #Filtramos las descargas por audio solamente, orden descendiente de calidad y
        # el primero que será el que tiene la calidad más alta
        stream = yt.streams.filter(mime_type='audio/mp4',only_audio=True).desc().first()
        nombre = stream.default_filename
        #quitamos espacios y paréntesis y cambiamos el tipo de fichero a mp3
        nombre = stream.default_filename
        nombre = ''.join(char for char in nombre if char.isalnum())
        nombre = nombre.replace(" ", "")
        nombre = nombre.replace("(", "-")
        nombre = nombre.replace(")", "-")
        nombre = nombre.replace("mp4", ".mp3")
        #Descargamos el audio seleccionado en el directorio escogido
        stream.download(output_path=path,filename=nombre)
        #enviar imagen del audio (portada, es el thumbnail del video);
        bot.send_photo(chat_id=chat,photo=imagen)
        #enviar audio:
        bot.send_document(chat_id=chat , document=open(path+nombre,'rb'))

        #borrar archivo de musica (solo pasa si se envia sin error)
        operation = 'rm '+path+nombre
        os.system(operation)
    except pytube.exceptions.RegexMatchError:
        bot.send_message(chat,'URL de vídeo no existe')
        print("URL no encontrada")

if __name__ == '__main__':
    main()
