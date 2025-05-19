# PDF File Read
# Reference: https://thepythoncode.com/article/make-pdf-viewer-with-tktinter-in-python
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import PhotoImage
import os
import pymupdf
# importing the PDFMiner class from the miner file
from Miner import PDFMiner


class PDFViewer:
    # initializing the __init__ / special method
    def __init__(self, master):
        self.img_file = None
        self.stringified_current_page = None
        self.miner = None
        self.path = None  # path for the pdf doc
        self.file_isOpen = None  # state of the pdf doc, open or closed
        self.author = None  # author of the pdf doc
        self.name = None  # name for the pdf doc
        self.current_page = 0  # the current page for the pdf
        self.numPages = None  # total number of pages for the pdf doc
        self.master = master  # creating the window
        self.master.title('PDF Viewer')  # gives title to the main window
        self.master.geometry('580x520+440+180')  # gives dimensions to main window
        self.master.resizable(width=0, height=0)  # this disables the minimize/maximize button on the main window
        icon = PhotoImage(file="pdf_file_icon.png")
        self.master.iconphoto(True, icon)  # loads the icon and adds it to the main window
        self.menu = Menu(self.master)  # creating the menu
        self.master.config(menu=self.menu)  # adding it to the main window
        self.file_menu = Menu(self.menu)  # creating a sub menu
        self.menu.add_cascade(label="File", menu=self.file_menu)  # giving the sub menu a label
        # adding two buttons to the sub menus
        self.file_menu.add_command(label="Open File", command=self.open_file)
        self.file_menu.add_command(label="Exit", command=self.master.destroy)
        self.top_frame = ttk.Frame(self.master, width=580, height=460)  # creating the top frame
        self.top_frame.grid(row=0, column=0)  # placing the frame using inside main window using grid()
        self.top_frame.grid_propagate(False)  # the frame will not propagate
        self.bottom_frame = ttk.Frame(self.master, width=580, height=50)  # creating the bottom frame
        self.bottom_frame.grid(row=1, column=0)  # placing the frame using inside main window using grid()
        self.bottom_frame.grid_propagate(False)  # the frame will not propagate
        self.scrolly = Scrollbar(self.top_frame, orient=VERTICAL)  # creating a vertical scrollbar
        self.scrolly.grid(row=0, column=1, sticky=(N,S))  # adding the scrollbar
        self.scrollx = Scrollbar(self.top_frame, orient=HORIZONTAL)  # creating a horizontal scrollbar
        self.scrollx.grid(row=1, column=0, sticky=(W, E))  # adding the scrollbar
        # Button to open a file
        # creating the canvas for display the PDF pages
        self.output = Canvas(self.top_frame, bg='#ECE8F3', width=560, height=435)
        # inserting both vertical and horizontal scrollbars to the canvas
        self.output.configure(yscrollcommand=self.scrolly.set, xscrollcommand=self.scrollx.set)
        self.output.grid(row=0, column=0)  # adding the canvas
        # configuring the horizontal scrollbar to the canvas
        self.scrolly.configure(command=self.output.yview)
        # configuring the vertical scrollbar to the canvas
        self.scrollx.configure(command=self.output.xview)
        # configuring the vertical scrollbar to the canvas
        self.scrollx.configure(command=self.output.xview)
        # Label inside top_frame displaying a message
        # Label centered in top_frame, displayed before opening a file
        self.viewer_label = Label(self.top_frame, text="This is PDF Viewer", font=("Arial", 24, "bold"),
                                  background="#ECE8F3", foreground="black")
        self.viewer_label.place(relx=0.5, rely=0.5, anchor=CENTER)
        # "Open a File" button placed just below the label
        self.viewer_open_button = Button(self.top_frame, text="Open a File",
                                         command=self.open_file, highlightbackground="#ECE8F3")
        self.viewer_open_button.place(relx=0.5, rely=0.65, anchor=CENTER)
        # creating an up button with an icon
        self.upbutton = ttk.Button(self.bottom_frame, text='↑', width=5, command=self.previous_page)
        # adding the button
        self.upbutton.grid(row=0, column=0, padx=(120, 5), pady=8)
        # creating a down button with an icon
        self.downbutton = ttk.Button(self.bottom_frame, text='↓', width=5, command=self.next_page)
        # adding the button
        self.downbutton.grid(row=0, column=2, pady=8)
        # label for displaying page numbers
        self.page_label = ttk.Label(self.bottom_frame, text='page')
        # adding the label
        self.page_label.grid(row=0, column=4, padx=5)
        # Button to go to a specific page
        self.goto_button = ttk.Button(self.bottom_frame, text='Go to', command=self.go_to_page)
        self.goto_button.grid(row=0, column=5, padx=(4, 0))
        # Entry widget for entering a specific page number
        self.page_entry = ttk.Entry(self.bottom_frame, width=5)
        self.page_entry.grid(row=0, column=6, padx=(5, 0))

    # function for opening pdf files
    def open_file(self):
        # open the file dialog
        filepath = fd.askopenfilename(title='Select a PDF file', initialdir=os.getcwd(), filetypes=(('PDF', '*.pdf'), ))
        # checking if the file exists
        if filepath:
            # declaring the path
            self.path = filepath
            # extracting the pdf file from the path
            filename = os.path.basename(self.path)
            # passing the path to PDFMiner
            self.miner = PDFMiner(self.path)
            # getting data and numPages
            data, numPages = self.miner.get_metadata()
            # setting the current page to 0
            self.current_page = 0
            # checking if numPages exists
            if numPages:
                # getting the title
                self.name = data.get('title', filename[:-4])
                # getting the author
                self.author = data.get('author', None)
                self.numPages = numPages
                # setting fileopen to True
                self.file_isOpen = True
                # calling the display_page() function
                self.display_page()
                # replacing the window title with the PDF document name
                self.master.title(self.name)
        # Remove the welcome label if it exists
        if self.viewer_label:
            self.viewer_label.destroy()
            self.viewer_label = None
        if self.viewer_open_button:
            self.viewer_open_button.destroy()
            self.viewer_open_button = None

    # the function to display the page
    def display_page(self):
        # checking if numPages is less than current_page and if current_page is less than
        # or equal to 0
        if 0 <= self.current_page < self.numPages:
            # getting the page using get_page() function from miner
            self.img_file = self.miner.get_page(self.current_page)
            # inserting the page image inside the Canvas
            self.output.create_image(0, 0, anchor='nw', image=self.img_file)
            # the variable to be stringified
            self.stringified_current_page = self.current_page + 1
            # updating the page label with number of pages
            self.page_label['text'] = str(self.stringified_current_page) + ' of ' + str(self.numPages)
            # creating a region for inserting the page inside the Canvas
            region = self.output.bbox(ALL)
            # making the region to be scrollable
            self.output.configure(scrollregion=region)

    # function for displaying next page
    def next_page(self):
        # checking if file is open
        if self.file_isOpen:
            # checking if current_page is less than or equal to numPages-1
            if self.current_page <= self.numPages - 1:
                # updating the page with value 1
                self.current_page += 1
                # displaying the new page
                self.display_page()

    # function for displaying the previous page
    def previous_page(self):
        # checking if file_isOpen
        if self.file_isOpen:
            # checking if current_page is greater than 0
            if self.current_page > 0:
                # decrementing the current_page by 1
                self.current_page -= 1
                # displaying the previous page
                self.display_page()

    def go_to_page(self):
        if self.file_isOpen:
            try:
                page_num = int(self.page_entry.get()) - 1  # Convert to 0-indexed
                if 0 <= page_num < self.numPages:
                    self.current_page = page_num
                    self.display_page()
                else:
                    print("Invalid page number")  # or show a messagebox
            except ValueError:
                print("Please enter a valid number")  # or show a messagebox


# creating the root window using Tk() class
root = Tk()
# instantiating/creating object app for class PDFViewer
app = PDFViewer(root)
# calling the mainloop to run the app infinitely until user closes it
root.mainloop()
