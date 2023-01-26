import matplotlib.pyplot as plt
import tkinter as tk
import csv
from tkinter.filedialog import askopenfilename

global columns
global head
columns = []
head = []

def read_data(frame, x_choice, y_choice):

    head.clear()
    
    filename = askopenfilename()
    file = open(filename, mode="r")
    reader = csv.reader(file, delimiter="\t")

    data = []

    for line in reader:
        data.append(line)
    
    #Collect information about the head
    
    for entry in data[0]:
        head.append(entry.replace("\t", ""))

    print(head)

    for k in range(0, len(data[0])):
        column = []
        for i in range(1, len(data)):
            #Try to convert entry to a Float or leave it as a String
            try:
                column.append(float(data[i][k].replace("\t", "")))
            except:
                column.append(data[i][k])
        columns.append(column)

        """radiobuttons"""
    radio_btn_values = {}

    for i in range(0, len(head)):
        radio_btn_values[head[i]] = i

    items = radio_btn_values.items()
    k = 4
    for (text, value) in items:
        tk.Radiobutton(frame, text=text, variable=x_choice,
            value=value, indicatoron=1).grid(row=k, column=0)
        k = k+1
    
    k = 4
    for (text, value) in items:
        tk.Radiobutton(frame, text=text, variable=y_choice,
            value=value, indicatoron=1).grid(row=k, column=1)
        k = k+1
        
def show_data(frame, x_choice, y_choice, title):
    save_image(x_choice, y_choice, title)
    window = tk.Toplevel(frame)
    #canvas = tk.Canvas(window, bg="black")
    img = tk.PhotoImage(file= title + ".png")
    #img = img.subsample(2, 2)
    label = tk.Label(window, image=img)
    label.image = img
    label.grid(column=0, row=0)
    #canvas.create_image(200, 200, anchor="nw", image = img)
    #canvas.grid(column=3, row=2)

def save_image(x_choice, y_choice, title):
    x = columns[x_choice]
    y = columns[y_choice]
    x_axis = head[x_choice]
    y_axis = head[y_choice]
    plt.close()
    plt.plot(x, y)
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.title(title)
    img_string = title + ".png"
    plt.savefig(img_string)

root = tk.Tk()
root.geometry('800x600')
root.title("CSV - Visualizer")
frame = tk.Frame(root)
frame.grid()
tk.Label(frame, text="CSV - Visualizer").grid(column=0, row=0)
tk.Label(frame, text="Diagrammtitel:").grid(column=0, row=2)
tk.Button(frame, text="Datei öffnen", command = lambda: read_data(frame, x_choice, y_choice)).grid(column=0, row=1)
tk.Label(frame, text="x - Werte").grid(column=0, row=3)
tk.Label(frame, text="y - Werte").grid(column=1, row=3)
title = tk.StringVar(root, "Diagram")
text = tk.Entry(frame, textvariable=title).grid(column=1, row=2)

x_choice = tk.StringVar(root, "0")
y_choice = tk.StringVar(root, "0")

tk.Button(frame, text="Diagramm speichern", command= lambda: save_image(int(x_choice.get()), int(y_choice.get()), title.get())).grid(column=1, row=1)
tk.Button(frame, text="Diagramm anzeigen", command = lambda: show_data(frame, int(x_choice.get()), int(y_choice.get()), title.get())).grid(column=2, row=1)

root.mainloop()


