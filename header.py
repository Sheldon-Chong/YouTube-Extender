
import xml.etree.ElementTree as ET
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from colorama import Back, Fore, Style, init
import pysrt
from datetime import datetime
from googletrans import Translator
import pygetwindow as gw
import nltk
import os
import pyperclip
import webbrowser
import re
import subprocess
from translate import Translator
import csv

Translator = Translator(provider='mymemory',to_lang="en", from_lang="es")