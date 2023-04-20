######################################################## IMPORT ########################################################

from tkinter import *
from tkinter import messagebox
from random import randint
from PIL import ImageTk, Image
import pyglet

########################################################################################################################

################################################### GRAPH CLASS ########################################################

class Graph:
    def __init__(self,val,player,children=[],del_num=-1,op=""):
        self.val=val
        self.children=children
        self.player=player
        self.heuristic_measure=-2
        self.del_num=del_num
        self.op=op

########################################################################################################################

################################################## GRAPH FUNCTIONS #####################################################

def create_graph(list, player, player_score, computer_score,gen_num,del_num=-1,op=""):
    prev=-1
    children=[]
    lenlist=len(list)
    for value in list:
        if value==prev: continue
        prev=value
        if(lenlist>=1):
            l = list.copy()
            l.remove(value)
            if  (player=="player"):
                gmult=create_graph(l,"computer", (player_score * value) % (gen_num), computer_score,gen_num,value,"*")
                gsum=create_graph(l, "computer", (player_score + value) % (gen_num), computer_score,gen_num,value,"+")

            else:
                gmult=create_graph(l, "player",player_score, (computer_score * value) % (gen_num), gen_num,value,"*")
                gsum=create_graph(l, "player" ,player_score, (computer_score + value) % (gen_num), gen_num,value,"+")
            children.append(gmult)
            children.append(gsum)
    return Graph((player_score,str(list),computer_score),player,children,del_num,op)

def minimax(G,gen_num):
    if G.children==[]:
        if(G.val[0]==G.val[2]):
            G.heuristic_measure=0
            return 0
        elif(gen_num-G.val[0]>gen_num-G.val[2]):
            G.heuristic_measure = 1
            return 1
        else:
            G.heuristic_measure = -1
            return -1
    if(G.player=="computer"):
        max=minimax(G.children[0],gen_num)
        for child in G.children[1:]:
            val=minimax(child,gen_num)
            if val > max:
                max=val
        G.heuristic_measure=max
        return max
    else:
        min = minimax(G.children[0],gen_num)
        for child in G.children[1:]:
            val=minimax(child, gen_num)
            if val< min:
                min = val
        G.heuristic_measure = min
        return min

########################################################################################################################

################################################### MENU FUNCTIONS #####################################################

def restart():
    end_game(-1,0,1)
    btn_clicked()

def helping():
    messagebox.showinfo("Rules",
                        """The rules of the game is to use the numbers to increase our score to be as close as possible to the generated numbers when it will have no numbers left. \n 
The winner is the player who is the closest to the generated number at the end. \n 
Be aware do not reach the number because your score would be reset to 0. \n
You can exceed the gen_number but in this case a modulo will apply. \n
Good Luck...""")

########################################################################################################################

################################################### GAME FUNCTIONS #####################################################

def update_score(p,score):
    if(p=="player"):
        if(score<10): player_score_str.set("0"+str(score))
        else: player_score_str.set(str(score))
    else:
        if (score < 10): computer_score_str.set("0" + str(score))
        else: computer_score_str.set(str(score))

def delete_num(num):
    if(num==4):
        states[0]=DISABLED
        four_but.configure(state=DISABLED)
    elif(num==6):
        states[1]=DISABLED
        six_but.configure(state=DISABLED)
    elif(num==7):
        if(states[2]!=DISABLED):
            states[2]=DISABLED
            seven_but.configure(state=DISABLED)
        elif(states[3]!=DISABLED):
            states[3]=DISABLED
            seven_but_bis.configure(state=DISABLED)
    elif(num==8):
        states[4]==DISABLED
        eight_but.configure(state=DISABLED)
    else:
        states[5]=DISABLED
        nine_but.configure(state=DISABLED)

def end_game(player_score,computer_score,gen_num):
    description_label_str.set("")
    subdescription_label_str.set("")

    if (player_score==computer_score):
        result_label_str.set("This is a wonderful draw. What a game this has been.")
    elif(gen_num-computer_score<gen_num-player_score):
        result_label_str.set("I'm sorry that you loose, but I'm sure you will win the next game.")
    else:
        result_label_str.set("Congratulations, you win. We will have to improve our computer intelligence.")
    for i in range(len(states)): states[i]=NORMAL
    btn_clicked(0)
    play.configure(state=NORMAL)
    mult.configure(state=DISABLED)
    sum.configure(state=DISABLED)

def launch_game():
    global chosen_num,chosen_op

    chosen_num = IntVar()
    chosen_op = StringVar()
    chosen_op.set("")
    initial_state = randint(6, 9)

    player = ("player" if messagebox.askquestion("Starting Player","Are you gonna start ?") =="yes" else "computer")
    generated_number = randint(43, 67)
    description_label_str.set("The number that you should be as close as possible is "+str(generated_number)+".")

    list_num = [4, 6, 7, 7, 8, 9]
    player_score = initial_state
    computer_score = initial_state
    g = create_graph([4,6,7,7,8,9], player, player_score, computer_score, generated_number)
    minimax(g, generated_number)

    update_score("player",player_score)
    update_score("computer",computer_score)

    while len(list_num)!=0:
        if player=="player":
            subdescription_label_str.set("It's your turn, choose a number below.")
            root.wait_variable(chosen_num)
            subdescription_label_str.set("Choose an operation to apply on chosen number and score.")
            root.wait_variable(chosen_op)
            if (chosen_op.get() == "*"):
                player_score *= chosen_num.get()
            else:
                player_score += chosen_num.get()
            player_score %= (generated_number)
            update_score("player",player_score)
            list_num.remove(chosen_num.get())
            for item in g.children:
                if (player_score, str(list_num), computer_score) == item.val:
                    g = item
                    break
        else:
            subdescription_label_str.set("The computer is thinking about its next move.")
            root.after(5)
            index = 0
            for i in range(1, len(g.children)):
                if (g.children[i].val[0] == g.val[0] and
                        g.children[i].heuristic_measure > g.children[index].heuristic_measure):
                    index = i
            g = g.children[index]
            new_list=eval(g.val[1])
            subdescription_label_str.set("It choose "+str(g.del_num)+" for the number.")
            delete_num(g.del_num)
            subdescription_label_str.set("It choose " + str(g.op) + " for the op.")
            computer_score = g.val[2]
            update_score("computer",computer_score)
            list_num = new_list
        if (player == "player"):player = "computer"
        else:player = "player"
    end_game(player_score,computer_score,generated_number)

########################################################################################################################

############################################## INTERACTION GAME/GUI ####################################################

def btn_clicked(button=9):
    global chosen_num,chosen_op
    if button<7:
        mult.configure(state=NORMAL)
        sum.configure(state=NORMAL)
        four_but.configure(state=DISABLED)
        six_but.configure(state=DISABLED)
        seven_but.configure(state=DISABLED)
        seven_but_bis.configure(state=DISABLED)
        eight_but.configure(state=DISABLED)
        nine_but.configure(state=DISABLED)
        if button == 1:
            states[0] = DISABLED
            chosen_num.set(4)
        elif button == 2:
            states[1] = DISABLED
            chosen_num.set(6)
        elif button == 3:
            states[2] = DISABLED
            chosen_num.set(7)
        elif button == 4:
            states[3] = DISABLED
            chosen_num.set(7)
        elif button == 5:
            states[4] = DISABLED
            chosen_num.set(8)
        elif button == 6:
            states[5] = DISABLED
            chosen_num.set(9)
    else:
        mult.configure(state=DISABLED)
        sum.configure(state=DISABLED)
        four_but.configure(state=states[0])
        six_but.configure(state=states[1])
        seven_but.configure(state=states[2])
        seven_but_bis.configure(state=states[3])
        eight_but.configure(state=states[4])
        nine_but.configure(state=states[5])
        if button==7:
            chosen_op.set("*")
        elif button==8:
            chosen_op.set("+")
        elif button==9:
            play.configure(state=DISABLED)
            result_label_str.set("")
            launch_game()

########################################################################################################################


############################################### DEFINING GUI INTERFACE #################################################

pyglet.font.add_file("Imprima-Regular.ttf")

root = Tk()
root.geometry("531x447")
root.configure(bg = "#f0f0f0")
root.resizable(width=False,height=False)
root.title("Don't Reach That Number")
root.iconbitmap("icon.ico")

#Menu creation
menubar=Menu(root)
menubar.add_cascade(label="Play Another Game",command=restart)
menubar.add_command(label="Rules", command=helping)
menubar.add_cascade(label="Close",command=root.destroy)
root.configure(menu=menubar)

openbg=Image.open("background.png")
bg=ImageTk.PhotoImage(openbg)
labelbg=Label(root,image=bg)
labelbg.place(x=12,y=79)

states=[NORMAL]*7
files=["4.png","6.png","7.png","8.png",
       "9.png","mult.png","sum.png","play.png"]
images = []
for file in files:
    img = Image.open(file)
    photo = ImageTk.PhotoImage(img)
    images.append(photo)

player_score_str=StringVar()
player_score_str.set("00")
computer_score_str=StringVar()
computer_score_str.set("00")
description_label_str=StringVar()
subdescription_label_str=StringVar()
result_label_str=StringVar()


four_but = Button(image = images[0], state=DISABLED, borderwidth = 0, highlightthickness = 0, command = lambda:btn_clicked(1), relief = "flat")
four_but.place(x = 157, y = 127, width = 33, height = 33)

six_but = Button(image = images[1], state=DISABLED, borderwidth = 0, highlightthickness = 0, command = lambda:btn_clicked(2), relief = "flat")
six_but.place(x = 208, y = 128, width = 33, height = 33)

seven_but = Button(image = images[2], state=DISABLED, borderwidth = 0, highlightthickness = 0, command = lambda:btn_clicked(3), relief = "flat")
seven_but.place(x = 208, y = 172, width = 33, height = 33)

seven_but_bis= Button(image = images[2], state=DISABLED, borderwidth = 0, highlightthickness = 0, command = lambda:btn_clicked(4),  relief = "flat")
seven_but_bis.place(x = 283, y = 172, width = 33, height = 33)

eight_but = Button(image = images[3], state=DISABLED, borderwidth = 0, highlightthickness = 0, command = lambda:btn_clicked(5), relief = "flat")

eight_but.place(x = 283, y = 128, width = 33, height = 33)

nine_but = Button(image = images[4], state=DISABLED,borderwidth = 0, highlightthickness = 0, command = lambda:btn_clicked(6), relief = "flat")
nine_but.place(x = 334, y = 128, width = 33, height = 33)

mult = Button(image = images[5], state=DISABLED,borderwidth = 0, highlightthickness = 0, command = lambda:btn_clicked(7), relief = "flat")
mult.place(x = 208, y = 258, width = 33, height = 33)

sum = Button(image = images[6], state=DISABLED,borderwidth = 0, highlightthickness = 0, command = lambda:btn_clicked(8), relief = "flat")
sum.place(x = 283, y = 258, width = 33, height = 33)

play = Button(image = images[7], borderwidth = 0, highlightthickness = 0, command = lambda:btn_clicked(),relief = "flat")
play.place(x = 124, y = 324, width = 282, height = 70)

# Create and pack the first label
description_label = Label(root, textvariable=description_label_str,font=("Imprima-Regular",12))
description_label.pack(side=TOP, pady=10)

# Create and pack the second label
subdescription_label = Label(root, textvariable=subdescription_label_str, font=("Imprima-Regular",12))
subdescription_label.pack(side=TOP)

#Create and pack the player_score label
labelplayer = Label(root, bg="#d9d9d9",textvariable=player_score_str,font=("Imprima-Regular",48))
labelplayer.place(x=40,y=115)

# Create and pack the computer_score label
labelcomputer = Label(root, bg="#d9d9d9",textvariable=computer_score_str, font=("Imprima-Regular",48))
labelcomputer.place(x=413,y=115)

# Create and pack the first label
description_label = Label(root, textvariable=result_label_str,font=("Imprima-Regular",12))
description_label.pack(side=BOTTOM, pady=10)

########################################################################################################################

#Launching the GUI
root.mainloop()