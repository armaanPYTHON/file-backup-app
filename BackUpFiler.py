from tkinter import *
import tkinter.ttk as ttk
from tkinter import filedialog
import threading
import os
import shutil
import time
from tkinter import messagebox



def main():


    root = Tk()
    root.title('BackUpFiler')
    root.geometry('1000x700')
    root.iconbitmap('icon/icon.ico')

    dark = '#212120'
    light = 'white'
    title = []
    src = []
    copy = []
    tsdict  ={}
    scdict = {}



    def cmode():
        f = open('files/colormode.dat', 'r')
        mode = f.read()
        f.close()

        if 'dark' in mode:
            frame.config(bg=dark)
            btnframe.config(bg=dark)
            lb.config(bg=dark, fg=light)
            backupbtn.config(bg=light, fg=dark)
            addbtn.config(bg=light, fg=dark)
            deselectbtn.config(bg=light, fg=dark)
            delbtn.config(bg=light, fg=dark)
            detailsbtn.config(bg=light, fg=dark)

        else:
            frame.config(bg=light)
            btnframe.config(bg=light)
            lb.config(bg=light, fg=dark)
            backupbtn.config(bg=dark, fg=light)
            addbtn.config(bg=dark, fg=light)
            deselectbtn.config(bg=dark, fg=light)
            delbtn.config(bg=dark, fg=light)
            detailsbtn.config(bg=dark, fg=light)

    def dmode(e=None):
        f = open('files/colormode.dat', 'w')
        f.write('dark')
        f.close()
        cmode()

    def lmode(e=None):
        f = open('files/colormode.dat', 'w')
        f.write('light')
        f.close()
        cmode()


    def files(e=None):
        lb.delete(0, END)
        title.clear()
        copy.clear()
        src.clear()
        tsdict.clear()
        scdict.clear()

        f = open('files/title.dat', 'r')
        for line in f.readlines():
            line = line.strip('\n')
            title.append(line)
        f.close()
        f = open('files/src.dat', 'r')
        for line in f.readlines():
            line = line.strip('\n')
            src.append(line)
        f.close()
        f = open('files/copy.dat', 'r')
        for line in f.readlines():
            line = line.strip('\n')
            copy.append(line)
        f.close()

        for i in range(len(src)):
            tsdict[title[i]] = src[i]
        for i in range(len(src)):
            scdict[src[i]] = copy[i]
        for item in title:
            lb.insert(0, item)





    def backup(e=None):
        selection = lb.get(ANCHOR)
        srcdir = tsdict[selection]
        destdir = scdict[srcdir]
        dirname, fname = os.path.split(srcdir)

        try:
            if os.path.isdir(destdir+'/'+fname):
                shutil.rmtree(destdir+'/'+fname)
                shutil.copytree(srcdir, destdir+'/'+fname)
                time.sleep(1)
                messagebox.showinfo('BackUpFiler', 'Your Folder has been backed Up!!')
            else:
                shutil.copytree(srcdir, destdir+'/'+fname)
                time.sleep(1)
                messagebox.showinfo('BackUpFiler', 'Your Folder has been backed Up!!')
            
        except:
            messagebox.showerror('BackUpFiler', 'An Error Occured!!\nCheck if file directory is available!')





    def add(e=None):
        win = Toplevel()
        win.title('BackUpFiler - Add')
        win.geometry('400x500')
        win.iconbitmap('icon/icon.ico')

        Label(win, text='Name:').grid(row=0, column=0, padx=10, pady=5)
        nameentry = Entry(win, bd=1, width=40)
        nameentry.grid(row=0, column=1, padx=10, pady=5, columnspan=2)


        def srcfile(e=None):
            dirname = filedialog.askdirectory(title='Choose Folder')
            sourceentry.insert(END, dirname)


        def destfile(e=None):
            dirname = filedialog.askdirectory(title='Choose Folder')
            destentry.insert(END, dirname)

        def sub1(e=None):
            srcdir = sourceentry.get()
            destdir = destentry.get()
            name = nameentry.get()

            src.append(srcdir)
            copy.append(destdir)
            title.append(name)

            f = open('files/title.dat', 'w')
            for line in title:
                f.write(line+'\n')
            f.close()
            f = open('files/src.dat', 'w')
            for line in src:
                f.write(line+'\n')
            f.close()
            f = open('files/copy.dat', 'w')
            for line in copy:
                f.write(line+'\n')
            f.close()

            nameentry.delete(0, END)
            sourceentry.delete(0, END)
            destentry.delete(0, END)

            files()




        Label(win, text='Source Folder:').grid(row=1, column=0, padx=2, pady=5)
        sourceentry = Entry(win, bd=1, width=30)
        sourceentry.grid(row=1, column=1, padx=5, pady=5, columnspan=1)
        ttk.Button(win, text='Choose Folder', command = srcfile).grid(row=1, column=2, padx=2, pady=5)

        Label(win, text='Destination:').grid(row=2, column=0, padx=2, pady=5)
        destentry = Entry(win, bd=1, width=30)
        destentry.grid(row=2, column=1, padx=5, pady=5, columnspan=1)
        ttk.Button(win, text='Choose Folder', command=destfile).grid(row=2, column=2, padx=2, pady=5)

        ttk.Button(win, text='Submit', command=sub1).grid(row=3, column=0, columnspan=3, pady=10, padx=40)
        win.bind('<Return>', sub1)






    def deselect(e=None):
        lb.selection_clear(ANCHOR)

    def delete(e=None):
        selection = lb.get(ANCHOR)
        srcdir = tsdict[selection]
        destdir = scdict[srcdir]
        name = selection

        src.remove(srcdir)
        copy.remove(destdir)
        title.remove(name)

        f = open('files/title.dat', 'w')
        for line in title:
            f.write(line+'\n')
        f.close()
        f = open('files/src.dat', 'w')
        for line in src:
            f.write(line+'\n')
        f.close()
        f = open('files/copy.dat', 'w')
        for line in copy:
            f.write(line+'\n')
        f.close()

        files()


    def details(e=None):
        win = Toplevel()
        win.title('BackUpFiler - Detials')
        win.geometry('300x200')

        Label(win, text='Name: '+lb.get(ANCHOR)).grid(row=0, column = 0, padx=10, pady=5)
        Label(win, text='Source: '+tsdict[lb.get(ANCHOR)]).grid(row=1, column=0, padx=10, pady=5)
        Label(win, text='Destination'+scdict[tsdict[lb.get(ANCHOR)]]).grid(row=2, column=0, padx=10, pady=5)

    def restart(e=None):
        root.destroy()
        time.sleep(1)
        main()

    def resize(e=None):
        root.geometry('1000x700')




    titleframe = Frame(root, bg='#1c1c1b')
    titleframe.place(relheight=0.1, relwidth=1, relx=0, rely=0)

    Label(titleframe, bg='#1c1c1b', fg=light, font=("Arial", 20, 'bold', 'italic'), text='BackUpFiler').pack(side=LEFT, padx=10)

    frame = Frame(root)
    frame.place(relheight=0.9, relwidth=1, relx=0, rely=0.1)

    lbframe = Frame(frame)
    lbframe.place(relheight=0.7, relwidth=0.5, relx=0.05, rely=0.05)

    lb = Listbox(lbframe, activestyle='none', bd=0, highlightthickness=0)
    #sx = Scrollbar(lbframe, orient=HORIZONTAL)
    #sx.pack(side=BOTTOM, fill=X)
    sy = Scrollbar(frame, orient=VERTICAL, command=lb.yview)
    sy.pack(side=LEFT, fill=Y)
    lb.pack(fill=BOTH, expand=1)
    lb.config(yscrollcommand=sy.set)

    btnframe = Frame(frame)
    btnframe.place(relheight=0.7, relwidth=0.3, relx=0.6, rely=0.15)
    backupthread = threading.Thread(target=backup)

    def x():
        backupthread.start()

    backupbtn = Button(btnframe, text='Back Up', height=2, width=15, bd=0, cursor='hand2', command=x)
    backupbtn.grid(row=0, column=0, padx=1, pady=1)
    addbtn = Button(btnframe, text='Add', height=2, width=15, bd=0, cursor='hand2', command=add)
    addbtn.grid(row=1, column=0, padx=1, pady=1)
    deselectbtn = Button(btnframe, text='Deselect', height=2, width=15, bd=0, cursor='hand2', command=deselect)
    deselectbtn.grid(row=2, column=0, padx=1, pady=1)
    delbtn = Button(btnframe, text='Delete', height=2, width=15, bd=0, cursor='hand2', command=delete)
    delbtn.grid(row=3, column=0, padx=1, pady=1)
    detailsbtn = Button(btnframe, text='Details', height=2, width=15, bd=0, cursor='hand2', command=details)
    detailsbtn.grid(row=4, column=0, padx=1, pady=1)





    menu = Menu(root)
    root.config(menu=menu)
    file = Menu(menu, tearoff=0)
    menu.add_cascade(label='File', menu=file)
    file.add_command(label='Back Up        (Enter)', command=backup)
    file.add_separator()
    file.add_command(label='Dark mode          (d)', command=dmode)
    file.add_command(label='Light Mode           (l)', command=lmode)
    file.add_separator()
    file.add_command(label='Resize Window     ', command=resize)
    file.add_command(label='Restart         (Ctrl+r)', command=restart)
    file.add_command(label='Exit App', command=root.destroy)
  
    select = Menu(menu, tearoff=0)
    menu.add_cascade(label='Selection', menu=select)
    select.add_command(label='Back Up        (Enter)', command=backup)
    select.add_separator() 
    select.add_command(label='Add           (Ctrl+a)', command=add)
    select.add_separator()
    select.add_command(label='Deselect             (d)', command=deselect)
    select.add_command(label='Delete             (Del)', command=delete)
    select.add_separator()
    select.add_command(label='Details       (Ctrl+d)', command=details)


    lb.bind('<Delete>', delete)
    lb.bind('<d>', deselect)
    lb.bind('<Return>', backup)
    lb.bind('<Control-d>', details)
    root.bind('<d>', dmode)
    root.bind('<l>', lmode)
    root.bind('<Control-a>', add)
    root.bind('<Control-r>', restart)

    files()
    cmode()
    mainloop()


main()