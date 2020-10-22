from tkinter import *
def callback():
	pass
	

window = Tk()
window.title("hihi tittle thoi ma ^^")
window.geometry('600x150')


lbl = Label(window, text="PWM Out:       ")
lbl.grid(column=0, row=0)


spin = Spinbox(window, from_=1100, to=2000, width=10, command=callback)
spin.grid(column=2,row=0)

window.mainloop()