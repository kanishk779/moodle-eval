import os
import zipfile
import csv

def evaluate(file_path, q_num):
	score = 0
	## RUN ANY CUSTOM SCRIPT FOR EVALUTING THE FILE AND RETURN RESPECTIVE SCORE

	# os.system("mpic++ '"+file_path+"'")
	# score = q_num+3

	return score

def moodle_check(dir, COMP_TYPE = '.zip', EVAL_FILETYPE = '.cpp', NUM_QUESTIONS = 3, MULTICHECK = True, OUTPUT_CSV = 'results.csv'):

	results = []

	## CHANGE ACCORDING TO CSV FILE HEADERS NEEDED AND NUMBER OF QUESTIONS
	result = { 'NAME': 'NAME', 'ROLL NO': 'ROLL NO', 'Q1': 'Q1', 'Q2': 'Q2', 'Q3': 'Q3'}

	csv_f = open(OUTPUT_CSV,'a')
	csv_w = csv.DictWriter(csv_f,result.keys())
	csv_w.writerow(result)

	student_dirs = os.listdir(dir)
	for student_dir in student_dirs:
		result = {}

		student_name = student_dir.partition('_')[0]
		result['NAME'] = student_name

		dir_path = os.path.join(dir,student_dir)
		submitted_files = os.listdir(dir_path)

		# Checks extension for submitted file viz zip
		comp_file = [file for file in submitted_files if file.endswith(COMP_TYPE)]
		if len(comp_file) == 0:
			print(student_name,"SUBMISSION NOT IN DESIRED COMPRESSION FORMAT")
			continue

		comp_file = comp_file[0]
		comp_file_path = os.path.join(dir_path, comp_file)
		comp_file_name = comp_file.partition('.')[0]
		result['ROLL NO'] = comp_file_name

		# For Zip File Submission
		with zipfile.ZipFile(comp_file_path,"r") as zip_ref:
		    zip_ref.extractall(dir_path)

		extracted_content = os.listdir(dir_path)
		extracted_content.remove(comp_file)

		# Checks if single folder is present
		if len(extracted_content) == 1:
			assign_folder = extracted_content[0]
			assign_folder_path = os.path.join(dir_path,assign_folder)
			assign_files = os.listdir(assign_folder_path)
		elif comp_file_name in extracted_content:
			assign_folder = comp_file_name
			assign_folder_path = os.path.join(dir_path,assign_folder)
			assign_files = os.listdir(assign_folder_path)
		else:
			assign_folder = student_dir
			assign_folder_path = dir_path
			assign_files = extracted_content

		eval_files = [file for file in assign_files if file.endswith(EVAL_FILETYPE)]

		if len(eval_files) == 0:
			print(student_name,"FILE NOT SUBMITTED")
			continue

		if len(eval_files) > NUM_QUESTIONS:
			print(student_name,"EXTRA FILES")
			continue

		for eval_file in eval_files:
			q_num = 1
			if MULTICHECK:
				num_str = eval_file[eval_file.find('.')-1]
				if not num_str.isdigit():
					print(student_name, "INCORRECT FILE FORMAT")
					break
				q_num = int(num_str)

			eval_file_path = os.path.join(assign_folder_path,eval_file)
			result['Q'+str(q_num)] = evaluate(eval_file_path, q_num)

		results.append(result)
		csv_w.writerow(result)

	csv_f.close()
	return results


if __name__ == '__main__':
	dir = 'S21CSE431-Assignment 1-25468'
	results = moodle_check(dir)
	# print(results)