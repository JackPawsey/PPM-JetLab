#Imports
import tkinter as tk

#Class to create custom table widget
class Table(tk.Frame):
    def __init__(self, parent, columns, rows):
        tk.Frame.__init__(self, parent, background="#20a6cb")

        #List of label widgets that will form the table
        self.widgets = []

        #For each column that the table will have...
        for column in range(columns):
            #Create a list of widgets for every column
            a_column = []
            #For each row that each column will have...
            for row in range(rows):

                #Create a cell/label
                a_cell = tk.Label(self, borderwidth=0, width=17)
                a_cell.grid(column=column, row=row, sticky="nsew", padx=1, pady=1)

                #Add the cell to the column list
                a_column.append(a_cell)

            #Add the column list to the widget list
            self.widgets.append(a_column)

    #Set the text value for a cell
    def set(self, column, row, value):
        a_widget = self.widgets[column][row]
        a_widget.configure(text=value)