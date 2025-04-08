import tkinter as tk
from tkinter import ttk, messagebox
from src.database import DataBase
from src.ranking import *
from src.gui import *

db = DataBase()
GUI(db)


db=None # Close data base connection by calling __del__ method