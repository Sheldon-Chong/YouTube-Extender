from header import *

WORDS_TO_REMOVE = """<b>
</b>"""

BUFFER_MSG_INSERT_TXT = "<INSERT TEXT HERE>"
BUFFER_MSG_REMOVE_TXT = "<REMOVE THE FOLLOWING WORDS>"
BUFFER_MSG_SAVE_NAME = "<FILENAME>"

BUFFER_MSG = f"""{BUFFER_MSG_INSERT_TXT}

{BUFFER_MSG_REMOVE_TXT}
{WORDS_TO_REMOVE}
{BUFFER_MSG_SAVE_NAME}
"""

LANGUAGE_TRANSLATE_TO = "chinese"
LANGUAGES = {
	"english": "en",
	"chinese": "zh",
	"spanish": "es",
}

WORDS_TO_REMOVE = ["<b>", "</b>"]

YES = ['yes', "Yes", "YES", "y", "Y"]
FRAME_EXTEND_LENGTH = 32

PROMPT_MSG = """
These are the instructions for this prompt.
1. Translate all the words below into {}.
2. do not translate words inside the brackets: [] as the words inside the brackets are names.
3. Do not translate any existing {} words. 
each of the numbers in brackets behind the words are a line. For example: "(10) woah! I can dash so quickly!" this is a number in a bracket. So all these numbers, e.g (10), (11), (50), (100), etc are lines. Make sure your final output with the words translated to {} contains the same amount of lines and numbers as the words original in english. 

translate here:

"""
HELP_MSG = """
help:		show available commands
exit:		exit terminal
extend <frames>: select a file to extend based on the default, or given number of frames
translate:	initiate part 1 of the translation process. Returns a csv file
csv2srt:	initiates part 2 of the translation process
"""
TITLE_MSG = f"""
{Fore.GREEN}
{Style.BRIGHT}
███████╗██████╗  █████╗ ███╗   ███╗███████╗    ███████╗██╗  ██╗████████╗███████╗███╗   ██╗██████╗ ███████╗██████╗ 
██╔════╝██╔══██╗██╔══██╗████╗ ████║██╔════╝    ██╔════╝╚██╗██╔╝╚══██╔══╝██╔════╝████╗  ██║██╔══██╗██╔════╝██╔══██╗
█████╗  ██████╔╝███████║██╔████╔██║█████╗      █████╗   ╚███╔╝    ██║   █████╗  ██╔██╗ ██║██║  ██║█████╗  ██████╔╝
██╔══╝  ██╔══██╗██╔══██║██║╚██╔╝██║██╔══╝      ██╔══╝   ██╔██╗    ██║   ██╔══╝  ██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗
██║     ██║  ██║██║  ██║██║ ╚═╝ ██║███████╗    ███████╗██╔╝ ██╗   ██║   ███████╗██║ ╚████║██████╔╝███████╗██║  ██║
╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝    ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝
  _                _____ _          _     _             
 | |          _   / ____| |        | |   | |            
 | |__  _   _(_) | (___ | |__   ___| | __| | ___  _ __  
 | '_ \| | | |    \___ \| '_ \ / _ \ |/ _` |/ _ \| '_ \ 
 | |_) | |_| |_   ____) | | | |  __/ | (_| | (_) | | | |
 |_.__/ \__, (_) |_____/|_| |_|\___|_|\__,_|\___/|_| |_|
         __/ |                                          
        |___/                                           
================================================================================================================
{HELP_MSG}
================================================================================================================

"""

def print_error(msg):
	print(Fore.RED + f"Error: {msg}" + Style.RESET_ALL)

def print_div():
	width = os.get_terminal_size().columns 
	print('-' * width)

def print_warning(msg, confirmation_msg=""):
	
	print(Fore.MAGENTA + f"Warning: {msg}" + Style.RESET_ALL)
	
	if confirmation_msg == "":
		return None
	try:
		user_input = prompt(confirmation_msg)
	except KeyboardInterrupt:
		print("\nInput cancelled by user.")
		return None
	return user_input
