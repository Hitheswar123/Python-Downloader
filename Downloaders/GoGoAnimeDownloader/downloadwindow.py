"""
    Trying to create a Downloadable app window
    1. Download URL: URL Textbox - Download Button
    2. Starting Episode
    3. Ending Episode
    4. Download Location
"""

#------------------Import Packages------------------------------#
import _thread
from tkinter import *
from tkinter import messagebox, filedialog
import os
from urllib.request import urlopen


#------------------Initialization of variables------------------------------#
root= Tk()
url= StringVar()
startep=StringVar()
endep= StringVar()
filename= StringVar()
download_progress= StringVar()
download_percentage= StringVar()
fln=''
filesize=''

#------------------Method/ functions used by wrapper attributes------------------------------#
def startDownload():
    global fln
    fln= filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save File", filetypes=(("All Files",".*"),))
    filename.set(os.path.basename(fln))
    _thread.start_new_thread(initDownload,())

def initDownload():
    furl= url.get()
    target= urlopen(furl)
    meta= target.info()
    filesize= float(meta['Content-Length'])
    filesize_mb= round((filesize/1024 /1024), 2)
    downloaded =0
    chunks= 1024 * 5
    with open(fln,'wb') as f:
        while True:
            parts = target.read(chunks)
            if not parts:
                messagebox.showinfo("Download Complete","Your Download Has Been Completed Successfully")
                break
            downloaded += chunks
            perc= round((downloaded/filesize)*100,2)
            if perc >100:
                perc=100
            download_progress.set(str(round((downloaded/1024 /1024), 2))+ "MB/"+ str(filesize_mb)+" MB")
            download_percentage.set(str(perc)+"%")
            f.write(parts)
    f.close()

def exitProgram():
    if messagebox.askyesno("Exit Program?","Are you sure you want to exit the program?") == False:
        return False
    exit()


""" Creating Wrapper sections on the Download Window"""

wrapper_1= LabelFrame(root,text="File URL")
wrapper_1.pack(fill="both", expand="yes", padx=10, pady=10)

wrapper_2= LabelFrame(root,text="File URL")
wrapper_2.pack(fill="both", expand="yes", padx=10, pady=10)


#-------------------------Download URL link ------------------------------#
label_1= Label(wrapper_1,text="Download URL: ")
label_1.grid(row=0, column=0, padx=10, pady=10)

entry_1= Entry(wrapper_1, textvariable=url)
entry_1.grid(row=0, column=1, padx=5, pady=10)

button_1= Button(wrapper_1, text="Download", command= startDownload)
button_1.grid(row=0, column=2, padx=5, pady=10)


#-------------------------Start Episode ------------------------------#
label_2= Label(wrapper_1,text="Start Episode: ")
label_2.grid(row=1, column=0, padx=10, pady=10)

entry_2= Entry(wrapper_1, textvariable=startep)
entry_2.grid(row=1, column=1, padx=5, pady=10)

#-------------------------End Episode ------------------------------#
label_3= Label(wrapper_1,text="End Episode: ")
label_3.grid(row=2, column=0, padx=10, pady=10)

entry_3= Entry(wrapper_1, textvariable=endep)
entry_3.grid(row=2, column=1, padx=5, pady=10)

#-------------------------Download Information ------------------------------#
Total_Downloads=''
Downloads_Failed=''


#-------------------------End Episode ------------------------------#
Button(wrapper_2, text="Exit Downloader", command=exitProgram).grid(row=3, column=0, padx=10, pady=10)



#-------------------------Download Display ------------------------------#
root.geometry("450x400")
root.title("Indian Downloader")
root.resizable(False,False)
root.mainloop()