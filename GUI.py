from tkinter import *

root = Tk()
root.title("Gépírás gyakorlása")
root.attributes('-fullscreen', True)

def second():
    root.destroy()
    root2 = Tk()
    root2.title("Gépírás gyakorlása")
    root2.attributes('-fullscreen', True)

    def third():
        root2.destroy()
        root3 = Tk()
        root3.title("Gépírás gyakorlása")
        root3.attributes('-fullscreen', True)
        root3.configure(bg='#666A86')


        

        
    root2.configure(bg='#666A86')
    root2.columnconfigure([0,1,2,3,4,5,6,7,8,9], weight=1)
    root2.rowconfigure([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16], weight=1)

    milyen_nehez = Label(root2, text='Milyen nehézségű legyen?', bg='#666A86', font=('Inter', 30), foreground='#FCF7FF').grid(column=4, row=1, columnspan=1, rowspan=1)

    button_konnyu = Button(root2, command="", bg='#63C7B2', highlightbackground='#666A86', activebackground='#63C7B2', text='Könnyű', font=('Inter', 20), foreground='#FCF7FF', height=2, width=10 ).grid(column=2, row=2)
    button_kozepes = Button(root2, command="", bg='#63C7B2', highlightbackground='#666A86', activebackground='#63C7B2', text='Közepes', font=('Inter', 20), foreground='#FCF7FF', height=2, width=10 ).grid(column=4, row=2)
    button_nehez = Button(root2, command="", bg='#63C7B2', highlightbackground='#666A86', activebackground='#63C7B2', text='Nehéz', font=('Inter', 20), foreground='#FCF7FF', height=2, width=10 ).grid(column=6, row=2)

    milyen_tema = Label(root2, text='Milyen témát szeretnél gyakorolni?', bg='#666A86', font=('Inter', 30), foreground='#FCF7FF').grid(column=4, row=3, columnspan=1)

    szavak = Button(root2, command="", bg='#63C7B2', highlightbackground='#666A86', activebackground='#63C7B2', text='Szavak', font=('Inter', 20), foreground='#FCF7FF', height=2, width=10 ).grid(column=2, row=4)
    mondatok = Button(root2, command="", bg='#63C7B2', highlightbackground='#666A86', activebackground='#63C7B2', text='Mondatok', font=('Inter', 20), foreground='#FCF7FF', height=2, width=10 ).grid(column=4, row=4)
    szoveg = Button(root2, command="", bg='#63C7B2', highlightbackground='#666A86', activebackground='#63C7B2', text='Szöveg', font=('Inter', 20), foreground='#FCF7FF', height=2, width=10 ).grid(column=6, row=4)

    mennyi_ido = Label(root2, text='Mennyi legyen az időkorlát?', bg='#666A86', font=('Inter', 30), foreground='#FCF7FF').grid(column=4, row=5, columnspan=1)

    szoveg_doboz = Text(root2, width=21, height=6).grid(column=2, row=6)
    nincs_ido = Button(root2, command="", bg='#63C7B2', highlightbackground='#666A86', activebackground='#63C7B2', text='Nincs idő', font=('Inter', 20), foreground='#FCF7FF', height=2, width=10 ).grid(column=4, row=6)

    label_kesz = Label(root2, text='Készen állsz?', bg='#666A86', font=('Inter', 30), foreground='#FCF7FF').grid(column=4, row=10, columnspan=1)
    button = Button(root2, command=third, bg='#63C7B2', highlightbackground='#666A86', activebackground='#63C7B2', text='Mehet', font=('Inter', 20), foreground='#FCF7FF', height=2, width=10).grid(row=11, column=4)

    root2.mainloop()

root.configure(bg='#666A86')
root.columnconfigure([0,1,2,3,4], weight=1)
root.rowconfigure([0,1,2,3,4], weight=1)
canvas = Canvas(root, bg='#666A86', highlightbackground='#63C7B2', width=1000, height=650).grid(column=2, row=2)
label = Label(canvas, text='Gépírás Fejlesztő Program', bg='#666A86', font=('Inter', 55), foreground='#FCF7FF').grid(column=2, row=2)
label = Label(canvas, text='Készítette: Kun Balázs és Ambruzs Zsombor', bg='#666A86', font=('Inter', 20), foreground='#FCF7FF').grid(column=2, row=2, sticky=N)
button = Button(canvas, command=second, bg='#63C7B2', highlightbackground='#666A86', activebackground='#63C7B2', text='Mehet', font=('Inter', 20), foreground='#FCF7FF', height=2, width=10).grid(column=2, row=2, sticky=S)
root.mainloop()