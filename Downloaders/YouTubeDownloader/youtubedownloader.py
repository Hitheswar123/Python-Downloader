from pytube import YouTube
from colorama import init, Fore

def on_complete(stream, file_path):
    print(stream)
    print(file_path)
    print('Download Complete')

def on_progress(stream, chunk, bytes_remaining):
    print(f'{100-round(bytes_remaining/stream.filesize *100)}%')

init()
link=str(input("Enter the YouTube link :"))
video_object=YouTube(link, on_complete_callback= on_complete, on_progress_callback= on_progress)

#Information
print(Fore.RED+ f'Title : \033[39m {video_object.title}')
print(Fore.RED+ f'Length : \033[39m {round(video_object.length /60,2)} minutes')
print(Fore.RED+ f'Views : \033[39m {video_object.views /1000000} million')
print(Fore.RED+ f'Author : \033[39m {video_object.author}')

#Download
print(
    Fore.RED+'download:' +
    Fore.GREEN+'(a)Video \033[39m|'+
    Fore.YELLOW+'(b)Audio\033[39m')
download_choice= input('choice: ')

if download_choice =='a':
    video_object.streams.get_highest_resolution().download(r'C:\Users\mvhit\Downloads\Youtube\Video')
elif download_choice == 'b':
    video_object.streams.get_audio_only().download(r'C:\Users\mvhit\Downloads\Youtube\Audio')
