import matplotlib.pyplot as plt
import tkinter as tk
import csv
from tkinter.filedialog import askopenfilename
from tkcalendar import Calendar, DateEntry
from datetime import datetime

global columns
global head
global radio_buttons
columns = []
head = []
radio_buttons = []

def create_fame(root):
    frame = tk.Frame(root)
    frame.grid()
    tk.Label(frame, text="CSV - Visualizer").grid(column=0, row=0)
    tk.Label(frame, text="Diagrammtitel:").grid(column=0, row=2)
    tk.Button(frame, text="Datei öffnen", command = lambda: read_data(frame, root, x_choice, y_choice)).grid(column=0, row=1)
    tk.Label(frame, text="x - Werte").grid(column=0, row=3)
    tk.Label(frame, text="y - Werte").grid(column=1, row=3)
    tk.Entry(frame, textvariable=title).grid(column=1, row=2)
    date_entry = DateEntry(frame, date_pattern="dd.MM.yyyy")
    date_entry.grid(column=2, row=2)
    tk.Checkbutton(frame, text="Datum anzeigen", variable=date_check).grid(row=2, column=3)

    def save_image_date():
        if(date_check):
            date = str(date_entry.get_date().strftime("%d.%m.%Y"))
            save_image(int(x_choice.get()), int(y_choice.get()), title.get(), date)
        else:
            save_image(int(x_choice.get()), int(y_choice.get()), title.get(), "")

    def show_image_date():
        if(date_check):
            date = str(date_entry.get_date().strftime("%d.%m.%Y"))
            show_data(frame, int(x_choice.get()), int(y_choice.get()), title.get(), date)
        else:
            show_data(frame, int(x_choice.get()), int(y_choice.get()), title.get(), "")
    tk.Button(frame, text="Speichern", command= lambda: save_image_date()).grid(column=1, row=1)
    tk.Button(frame, text="Speichern & Anzeigen", command = lambda: show_image_date()).grid(column=2, row=1)
    return frame

def get_delimiter(file_path, bytes = 4096):
    sniffer = csv.Sniffer()
    data = open(file_path, "r").read(bytes)
    delimiter = sniffer.sniff(data, "\t ;").delimiter
    return delimiter

def read_data(frame, root, x_choice, y_choice):
    frame.destroy()
    frame = create_fame(root)
    head.clear()
    
    filename = askopenfilename()
    file = open(filename, mode="r")
    delimiter = get_delimiter(file_path=filename)
    reader = csv.reader(file, delimiter=delimiter)

    data = []

    for line in reader:
        data.append(line)
    
    #Collect information about the head
    for entry in data[0]:
        head.append(entry.replace("\t", ""))

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
    j = 4
    for (text, value) in items:
        tk.Radiobutton(frame, text=text, variable=x_choice,
            value=value, indicatoron=1).grid(row=j, column=0)
        j = j+1
    
    k = 4
    for (text, value) in items:
        tk.Radiobutton(frame, text=text, variable=y_choice,
            value=value, indicatoron=1).grid(row=k, column=1)
        k = k+1
        
def show_data(frame, x_choice, y_choice, title, date):
    save_image(x_choice, y_choice, title, date)
    window = tk.Toplevel(frame)
    #canvas = tk.Canvas(window, bg="black")
    img = tk.PhotoImage(file= title + ".png")
    #img = img.subsample(2, 2)
    label = tk.Label(window, image=img)
    label.image = img
    label.grid(column=0, row=0)
    #canvas.create_image(200, 200, anchor="nw", image = img)
    #canvas.grid(column=3, row=2)

def save_image(x_choice, y_choice, title, date):
    x = columns[x_choice]
    y = columns[y_choice]
    x_axis = head[x_choice]
    y_axis = head[y_choice]
    plt.close()
    plt.plot(x, y)
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.title(title)
    plt.subplots_adjust(bottom=0.11)
    plt.gcf().text(0.78, 0.005, date)
    img_string = title + ".png"
    plt.savefig(img_string)

root = tk.Tk()
root.geometry('800x600')
root.title("CSV - Visualizer")

title = tk.StringVar(root, "Diagram")
x_choice = tk.StringVar(root, "0")
y_choice = tk.StringVar(root, "0")
date_check = tk.IntVar(root, 1)

create_fame(root)


root.mainloop()


