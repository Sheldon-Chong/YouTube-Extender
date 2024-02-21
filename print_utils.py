from header import *

YES = ['yes', "Yes", "YES", "y", "Y"]
FRAME_EXTEND_LENGTH = 32
WORDS_TO_REMOVE = ["<b>", "</b>"]
PROMPT_MSG = """
These are the instructions for this prompt.
1. Translate all the words below into chinese.
2. do not translate words inside the brackets: [] as the words inside the brackets are names.
3. Do not translate any existing chinese words. 
each of the numbers in brackets behind the words are a line. For example: "(10) woah! I can dash so quickly!" this is a number in a bracket. So all these numbers, e.g (10), (11), (50), (100), etc are lines. Make sure your final output with the words translated to chinese contains the same amount of lines and numbers as the words original in english. 

translate here:

"""
HELP_MSG = """
help: show commands
exit: exit program
extend <xstage filename>: extend the file
srt <xstage filename>: generate srt based on file
translate: convert a srt file into csv, then paste the translated csv to form a new srt file
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
help: show commands
exit: exit program
extend <xstage filename>: extend the file
srt <xstage filename>: generate srt based on file
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
