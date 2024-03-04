from header import *
from print_utils import *


def select_file(acceptable_files, window_name):
	if(isinstance(acceptable_files, tuple)):
		acceptable_files = [acceptable_files]
	print("choose file: ", end="", flush=True)
	Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
	filename = askopenfilename(
		filetypes=acceptable_files,
		title = window_name
		) 
	print(filename)
	splitted_acceptable_files = [x[2:] for x in acceptable_files[0][1].split(';') if len(x) > 0]
	return filename

def remove_words(input_string, words_to_remove): 
	for item in words_to_remove:
		input_string = input_string.replace(item, "");
	return(input_string)

def get_frame(i):
	global FRAME_EXTEND_LENGTH
	return (i * FRAME_EXTEND_LENGTH + 1)

def generate_frame_markers(max_frame, fps):
	array = []
	print(f"fps: {fps} | frames: {FRAME_EXTEND_LENGTH}")
	i = 0
	while(i < max_frame):
		array.append({
			"frame": i,
			"extended": get_frame(i),
			"extended end": get_frame(i + 1) - 1,
			"extended str": str(get_frame(i)) + '-' + str(get_frame(i + 1) - 1),
			"time start": get_frame(i) / fps,
			"time end": get_frame(i + 1) / fps
		})
		i += 1
	return(array)

def print_frame_markers(array):
	print(array.__name__)
	print(f"	frame {array[-1]['frame']}: extended {array[-1]['extended']}:{array[-1]['extended end']} \"{array[-1]['extended str']}\" | {round(array[-1]['time start'], 3)}: {round(array[-1]['time end'], 3)}")

def check_if_extended(layers):
	guideline = [item['extended str'] for item in generate_frame_markers(max_frame=700, fps=12)]
	matching_layers = []
	for layer in layers:
		for frame in layer.findall('elementSeq'):
			if frame.attrib['exposures'] in guideline:
				matching_layers.append(frame)
	
	if (len(matching_layers) > 1):
		for item in matching_layers:
			print(f"	drawing {item.attrib['val']} | {item.attrib['exposures']} ")
		user_input = print_warning("The following frames appear to have already been extended. Are you sure you want to extend all frames?", "Y/N:")
		if user_input not in YES:
			return(True)

def extend(file_path):
	global FRAME_EXTEND_LENGTH
	with open(file_path, 'r') as file:
		
		#read file and extract column
		file_contents = file.read()
		root = ET.fromstring(file_contents)
		layers = root.find('scenes').find('scene').find('columns').findall('column')

		#guideline is to compare against the file
		if(check_if_extended(layers)):
			return None
		
		#iterate through layers
		for layer in layers: 
			frames = layer.findall('elementSeq')

			#iterate through frames
			for frame in frames:
				exposures_array = frame.attrib['exposures'].split(",")
				exposures_splitted = [exposure.split('-') for exposure in exposures_array]
				for i in range(0, len(exposures_splitted)):
					if len(exposures_splitted[i]) == 1:
						exposures_splitted[i].append(int(exposures_splitted[i][0]) + 1)
					exposures_splitted[i][0] = get_frame(int(exposures_splitted[i][0]))
					exposures_splitted[i][1] = get_frame(int(exposures_splitted[i][1])) - 1
				
				final_exposures = ','.join(['-'.join([str(k) for k in exposure]) for exposure in exposures_splitted])
				print(f"    Range: {frame.attrib['exposures']}, Drawing: \"{frame.attrib['val']}\"{final_exposures}")
				frame.attrib['exposures'] = final_exposures
	with open(file_path, 'w') as file:
		file.write(ET.tostring(root).decode())

def srt2arr(filename, destination, word_to_remove):
	subs = pysrt.open(filename)
	buffer = PROMPT_MSG

	rows = []
	i = 1
	for sub in subs:
		if len(sub.text) > 1:
			row = [sub.text, sub.start, sub.end]
			buffer += f"<{i}> {row[0]}\n"
			rows.append(row)
			i += 1
	
	print(f"Length: {len(rows)}")
	print(f"{Fore.GREEN}{buffer}{Style.RESET_ALL}")
	print(f"{Fore.GREEN}\n*SRT file created {destination}/{Fore.BLUE}{os.path.basename(filename)[0:-4]}.csv{Style.RESET_ALL}")
	print(f"{Fore.GREEN}*Copied to buffer{Style.RESET_ALL}")
	print()
	print(f"{Back.GREEN}STEP TWO{Style.RESET_ALL}")
	print("Go to ChatGPT and ask it to translate the contents of your clipboard to the desired language\n")
	pyperclip.copy(buffer)
	webbrowser.open("https://chat.openai.com/")

	return(rows)

def csv2srt(csv_filename, save_directory):
	subs = pysrt.SubRipFile()
	with open(csv_filename, 'r', newline='', encoding='utf-8') as file:
		reader = csv.reader(file)
		next(reader)
		for index, row in enumerate(reader, start=1):
			start = pysrt.srttime.SubRipTime.from_string(row[1])
			end = pysrt.srttime.SubRipTime.from_string(row[2])
			text = row[3]
			item = pysrt.SubRipItem(index, start=start, end=end, text=text)
			subs.append(item)
	print(save_directory)
	subs.save(f"{save_directory}/translated.srt", encoding='utf-8')

def generate_srt_guide(amount, fps):
	timestamp_array = generate_frame_markers(amount, fps)
	subs = pysrt.SubRipFile()
	i = 1
	for item in timestamp_array:
		start_time = pysrt.SubRipTime(seconds=item['time start'], hours=1)
		end_time = start_time + 100
		subs.append(pysrt.SubRipItem(i, start=start_time, end=end_time,text=f"s: {str(i)}"))
		i += 1
	subs.save('my_subtitles.srt', encoding='utf-8')
	print(f"{Fore.GREEN}*my_subtitles.srt generated{Style.RESET_ALL}")

	subs2 = pysrt.SubRipFile()
	i = 1
	for item in timestamp_array:
		start_time = pysrt.SubRipTime(seconds=item['time start'], hours=1)
		end_time = start_time + 2000
		subs2.append(pysrt.SubRipItem(i, start=start_time, end=end_time,text=f"frame: {str(i)}"))
		i += 1
	subs2.save('transition guides.srt', encoding='utf-8')
	print(f"{Fore.GREEN}*transition guides.srt generated{Style.RESET_ALL}")

def text_edit(buffer_name, buffer_contents, mode):
	# create a new buffer file
	if(mode == "edit"):
		pass
	else:
		with open(buffer_name, 'w') as file:
			file.write(buffer_contents)

	# open the editor
	subprocess.run(['notepad.exe', buffer_name], check=True)
	user_input = ""

	while (user_input in ["e", "r", ""]):
		user_input = input("finished? y-yes c-cancel r-redo e-edit: ")
		if (user_input == "c"):
			return(None)
		elif (user_input == "e"):
			open(buffer_name, 'r')
			subprocess.run(['notepad.exe', buffer_name], check=True)
		elif (user_input == "r"):
			with open(buffer_name, 'w') as file:
				file.write(buffer_contents)
			subprocess.run(['notepad.exe', buffer_name], check=True)
	with open(buffer_name, 'r', encoding='utf-8') as file:
		file_contents = file.readlines()
	
	# remove ending newlines if any
	modified_list = list(map(lambda s: s.rstrip('\n') if s.endswith('\n') else s, file_contents))

	if not BUFFER_MSG_INSERT_TXT in  modified_list or BUFFER_MSG_REMOVE_TXT not in modified_list:
		print_error("Does not contain required titles")
		return(None)

	# extract the part of the list that matters
	script = modified_list[modified_list.index(BUFFER_MSG_INSERT_TXT) + 1:modified_list.index(BUFFER_MSG_REMOVE_TXT)]

	words_to_remove = modified_list[modified_list.index(BUFFER_MSG_REMOVE_TXT)+1:]
	return(script, words_to_remove)

def shell():
	
	print(TITLE_MSG)
	completer = WordCompleter(
		[f"exit", "help", "srt", "extend", "translate", "csv2srt"],
		ignore_case=True)
	history = FileHistory('.command_history')  # Save command history to a file
	
	global FRAME_EXTEND_LENGTH

	while(True):
		try:
			user_input = prompt(f">>> Frame Extender: ", completer=completer, history=history)
			if not user_input: continue
			tokens = nltk.word_tokenize(user_input)
			if tokens[0] == "exit": exit()
			elif tokens[0] == "help": print(HELP_MSG)
			elif tokens[0] == "srt": generate_srt_guide(300, 12)
			elif tokens[0] == "extend":
				filename = select_file([("acceptable files", "*.srt;*.csv;*.xstage;*.txt")], "select file")
				if len(filename) < 0:
					print_error(f"No file selected")
				if not ".xstage" in filename:
					print_error(f"Invalid file: {filename}")
					continue
				try:
					if(len(tokens) > 1):
						FRAME_EXTEND_LENGTH = int(tokens[1])
					extend(filename)
					print(f"Sucess: {filename} extended by {FRAME_EXTEND_LENGTH} frames")
				except UnicodeDecodeError as e:
					print_error("file cannot be read properly. Does this xtage file contain incorrect syntax?")
			elif tokens[0] == 'stats':
				filename = select_file([("acceptable files", "*.srt;*.csv;*.xstage;*.txt")], "select file")
				try:
					with open(filename, 'r') as file:
						file_contents = file.read()
						root = ET.fromstring(file_contents)
						drawings = root.find('scenes').find('scene').find('columns').findall('column')
						for drawing in drawings:
							print(f"NAME: {drawing.attrib['name']} | unique drawings count: {len(drawing.findall('elementSeq'))}")
							for frames in drawing.findall('elementSeq'):
								print(f"	{frames.attrib['exposures']}")
				except UnicodeDecodeError:
					print("file cannot be read properly. Does this xtage file contain incorrect syntax?")
			elif tokens[0] == 'csv2srt':
				selected_file = select_file([("acceptable files", "*.csv;")], "select CSV")
				if not ".csv" in selected_file:
					print_error(f"Invalid file: {selected_file}: Not an csv file")
					continue
				basename = os.path.basename(selected_file).split('.')[0]
				filepath = f"{os.path.dirname(selected_file)}/{basename} CN.srt"
				print(filepath)
				csv2srt(selected_file, filepath)
			elif tokens[0] == 'translate':
				flag = "default"

				# prompt user to select a srt file
				selected_file = select_file([("acceptable files", "*.srt;")], "select SRT")
			
				if(len(selected_file) < 1) or not selected_file:
					print_error("Error: No file selected. Operation cancel")
					continue
				# convert the selected srt file into a 2D array
				csv_rows = srt2arr(selected_file, os.path.dirname(selected_file), [])

				#repeat this step as many times until need to do something
				while(True):
					
					# read from user input
					txt_rows, word_to_remove = text_edit("buffer", BUFFER_MSG, flag)
					if not txt_rows:
						flag = "cancelled"
						break
					
					# convert each item from "<100> test" into "||| test"
					for i in range(0, len(txt_rows)):
						if('>' in txt_rows[i]):
							txt_rows[i] = '|||' + txt_rows[i][txt_rows[i].find('>') + 1:]
					
					# join all newlines
					input_string = '\n'.join(txt_rows)

					# split by "|||" character, and remove the first item which is guarantee
					txt_rows = [x[1:] for x in input_string.split('|||')[1:]]
				
					# process input
					if len(txt_rows) != len(csv_rows):
						print_warning("The input you provided does not contain the same amount of lines as the provided srt file\n")
						print(f"{len(txt_rows)}/{len(csv_rows)}")
						user_input = input("r-redo, e-edit, c-cancel: ")
						if (user_input == 'r'):
							flag = "default"
							selected_file = select_file([("acceptable files", "*.srt;")], "select SRT")
							csv_rows = srt2arr(selected_file, os.path.dirname(selected_file), word_to_remove)
							continue
						elif (user_input == 'e'):
							flag = "edit"
							continue
						elif (user_input == 'c'):
							flag = "cancel"
							break
					else:
						break
				if (flag == "cancel"):
					continue
				for row_num in range(0, len(txt_rows)):
					txt_rows[row_num] = txt_rows[row_num][:-1]
					if '\n' in txt_rows[row_num]:
						seperated_input_rows = txt_rows[row_num].split('\n')
						seperated_csv_rows = [row[0] for row in csv_rows][row_num].split('\n')
						for item in range(0, len(seperated_input_rows)):
							print(f"{str(row_num) + '.' if item == 0 else ''} {seperated_input_rows[item]} {seperated_csv_rows[item]}")
					else:
						print(f"{Fore.GREEN}{row_num + 1}. {txt_rows[row_num]} {Fore.BLUE}{[row[0] for row in csv_rows][row_num]}")
					csv_rows[row_num].append(txt_rows[row_num])

				#save file
				directory = os.path.dirname(selected_file)
				base_filename = os.path.basename(selected_file)[0:-4]
				csv_filename = f"{directory}/{base_filename}.csv"
				print(f"{Fore.GREEN}File saved: {csv_filename}{Style.RESET_ALL}")

				# write changes
				with open(csv_filename, 'w', newline='', encoding='utf-8') as file:
					writer = csv.writer(file)
					writer.writerow(["text", "start", "end", "translated version"])
					for row in csv_rows:
						writer.writerow(row)

				csv2srt(csv_filename, directory)
				subprocess.Popen('explorer {}'.format(os.path.dirname(selected_file).replace('/', '\\')))
			else:
				print_error(f"{tokens[0]}: command not found")
		except KeyboardInterrupt:
			pass

if __name__ == "__main__":
	init()
	shell()

# pyinstaller --onefile .\frame_extension.pyom