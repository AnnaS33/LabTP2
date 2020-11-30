from tkinter import *
from tkinter import simpledialog


w=120
map=[[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
class Btn():
    global w

    def __init__(self,application):
        self.application = application
        self.window=None
        self.Button_list = []
        self.CrOrNo=None# 0 - ноликб 1 - крестик
        self.zero=[]
        self.cross=[]
        self.t=[]
        self.Again=None
        self.lable=None
        self.lable2 = None
        self.Exit = None


    def click1(self,event,Button1):
        if(self.application.N==0):#Блокируем чтобы человек не жал несколько раз подряд(t==1) & (k['idCl']==1)
            self.lable2['text'] = ''
            self.t.append(event)
            if(self.CrOrNo==1):
                Button1.config(text="X")
                self.cross.append(event)
            else:
                Button1.config(text="0")
                self.zero.append(event)

            Button1.unbind("<Button-1>")
            self.application.N=1

            Z,I=self.Prov(self.zero)
            if(Z):
                self.application.send(str(1)+str(I)+str(event)+str(self.CrOrNo))
                self.Win(str(1)+str(I))
            else:
                C,I=self.Prov(self.cross)
                if (C):
                    self.application.send(str(2)+str(I)+str(event)+str(self.CrOrNo))
                    self.Win(str(2) + str(I))
                else:
                    if(I==-1):
                        self.application.send(str(3)+str(0)+str(event)+str(self.CrOrNo))
                        self.Win(str(3))
                    else:
                        self.application.send(str(0)+str(0)+str(event)+str(self.CrOrNo))

    def click2(self):
        self.application.send(str(0)+str(0)+'-'+str(self.CrOrNo))

    def show_message(self,message):

        if (message.Load != None):
            if (message.Load == 'No1'):
                self.lable2['text'] = 'Увы, но ваш противник ещё не зашёл'
            else:
                if (message.Load == 'No2'):
                    self.lable2['text'] = 'Такое сохранение уже есть, либо вы ещё не сделали ни одного хода'
                else:
                    self.lable2['text'] = 'Такого сохранения нет, попробуйте снова'
            return False
        t=int(message.id+message.win+message.Number)
        if(t>9):
            S = str(t)
            self.t.append(int(S[2]))
            self.vspom(message,int(S[2]))
            if (message.idCl == '0'):#Просавляем ответ противника
                self.Button_list[int(S[2])].config(text="0")
                self.zero.append(int(S[2]))
            else:
                self.Button_list[int(S[2])].config(text="X")
                self.cross.append(int(S[2]))
            self.Button_list[int(S[2])].unbind("<Button-1>")
            self.Win(t)
        else:
            self.t.append(t)
            if (message.idCl == '0'):#Проставляем ответ противника
                self.Button_list[t].config(text="0")
                self.zero.append(t)
            else:
                self.Button_list[t].config(text="X")
                self.cross.append(t)
            self.Button_list[t].unbind("<Button-1>")

    def vspom(self,message,t):
        if (message.idCl == '0'):  # Просавляем ответ противника
            self.Button_list[t].config(text="0")
            self.zero.append(t)
        else:
            self.Button_list[t].config(text="X")
            self.cross.append(t)
        self.Button_list[t].unbind("<Button-1>")

    def loop(self):
        self.window.mainloop()

    def startplay(self):
        self.window = Tk()
        self.window.geometry('600x600')

        self.lable=Label(text="Результаты игры",font=("Comic Sans MS",12,"bold"))
        self.lable.config(bd=20)
        self.lable.pack()

        self.lable2 = Label(text="", font=("Comic Sans MS", 12, "bold"))
        #self.lable2.place(relx=.5, rely=.6)
        self.lable2.pack()

        self.Again = Button(text="Again")
        self.Again.place(x=520, y=130, anchor="c")
        self.Again.bind("<Button-1>", lambda event : self.click2())

        self.Exit = Button(text="Exit")
        self.Exit.place(x=520, y=300, anchor="c")
        self.Exit.bind("<Button-1>", lambda event: self.exit())

        Save = Button(text="Save")
        Save.place(x=520, y=170, anchor="c")
        Save.bind("<Button-1>", lambda event: self.saves())

        Load = Button(text="Load")
        Load.place(x=520, y=210, anchor="c")
        Load.bind("<Button-1>", lambda event: self.loads())

        self.window.title("Let's play")
        self.showw()
        return self.input_dialogs()

    def saves(self):
        self.window.lower()
        self.application.NameSave = simpledialog.askstring("Save", "Input the name of conservation", parent=self.window)
        if self.application.NameSave is None:
            return False
        self.application.savem()
        return True

    def loads(self):
        self.window.lower()
        self.application.NameSave = simpledialog.askstring("Load", "Input the name of conservation", parent=self.window)
        if self.application.NameSave is None:
            return False
        n = simpledialog.askinteger("You", "Input 0 or 1", parent=self.window)
        if ((n!=0) & (n!=1)):
            self.lable2['text']='Можно вводить только 0 и 1'
            return False
        self.application.loadm(str(n))
        self.lable2['text'] = ''
        return True

    def showw(self):
        id=0
        x=120
        y=120
        for i in range(3):
            for j in range(3):
                Button1 = Button(bg="white", bd=3,font=("Comic Sans MS", 24,"bold"))
                Button1.bind("<Button-1>", lambda event,id=id, Button1=Button1: self.click1(id, Button1))
                Button1.place(x=x, y=y, width=w, height=w)
                self.Button_list.append(Button1)
                x=x+w
                id+=1
            x=120
            y=y+w

    def input_dialogs(self):
        self.window.lower()
        self.application.host = simpledialog.askstring("Server Host", "Input Server Host",parent=self.window)
        if self.application.host is None:
            return False
        self.application.port = simpledialog.askinteger("Server Port", "Input Server Port",parent=self.window)
        if self.application.port is None:
            return False
        return True

    def Prov(self,lis):
        k=0
        for i in range(8):
            for j in range(3):
                if map[i][j] in lis:
                    k+=1
            if k==3:
                for g in range(9):
                    self.Button_list[g].unbind("<Button-1>")
                for g in range(3):
                    self.Button_list[map[i][g]].config(fg="green")
                return True,i
            else:
                k=0
        if(len(self.t)==9):
            return False,-1
        return False,k

    def Win(self,ms):
        S=str(ms)
        if(S[0]=='1'):
            for g in range(9):
                self.Button_list[g].unbind("<Button-1>")
            for g in range(3):
                self.Button_list[map[int(S[1])][g]].config(fg="green")
            if(self.CrOrNo==0):
                self.lable['text']='Вы победили'
            else:
                self.lable['text'] = 'Вы проиграли'
        if (S[0] == '2'):
            for g in range(9):
                self.Button_list[g].unbind("<Button-1>")
            for g in range(3):
                self.Button_list[map[int(S[1])][g]].config(fg="green")
            if (self.CrOrNo == 1):
                self.lable['text'] = 'Вы победили'
            else:
                self.lable['text'] = 'Вы проиграли'
        if (S[0] == '3'):
            self.lable['text'] = 'Ничья'

    def Stop(self):
        self.Button_list=[]
        self.showw()
        self.CrOrNo = None
        self.zero = []
        self.cross = []
        self.t = []
        self.Again = None
        self.lable['text'] = 'Результат'

    def exit(self):
        self.window.destroy()
        self.application.exit(str(self.CrOrNo))

if __name__ == "__main__":
    Btn().startplay()