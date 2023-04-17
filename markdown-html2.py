#!/bin/python3

print("- Markdown-HTML -")

import markdown, natsort, os, json, pathlib

REPO_PATH = pathlib.Path(os.environ['GITHUB_WORKSPACE'])
INPUT_LIST = json.loads(os.environ['INPUT_INPUT_FILES'])
OUTPUT_LIST = json.loads(os.environ['INPUT_OUTPUT_FILES'])
EXCLUDE_DUPLICATES : bool = json.loads(os.environ['INPUT_EXCLUDE_DUPLICATES'])
BUILTIN_STYLESHEET : str = os.environ['INPUT_BUILTIN_STYLESHEET']
EXTENSIONS : list = json.loads(os.environ['INPUT_EXTENSIONS'])
EXTENSION_CONFIGS : dict = json.loads(os.environ['INPUT_EXTENSION_CONFIGS'])

md = markdown.Markdown(extensions=EXTENSIONS, extension_configs=EXTENSION_CONFIGS, output_format="html5")

if not isinstance(INPUT_LIST, list) or not all([isinstance(sublist, list) for sublist in INPUT_LIST]):
    raise ValueError("input_files must be a JSON list of lists")

if not isinstance(OUTPUT_LIST, list):
    raise ValueError("output_files must be a JSON list")

if BUILTIN_STYLESHEET != "":
    with open(REPO_PATH.joinpath(BUILTIN_STYLESHEET), 'r') as stylesheet_file:
        style = "<style>\n" + stylesheet_file.read() + "</style>\n"
else:
    style = ""

for input_sublist in INPUT_LIST:
    md.reset()
    md_str = ""
    
    for input_path_glob_str in input_sublist:
        input_path_list = natsort.natsorted([str(p) for p in REPO_PATH.glob(input_path_glob_str)])
        for input_path_str in input_path_list:
                
                with open(input_path_str, 'r') as input_file:
                    md_str = input_file.read() + "\n"

                    print("Generating", input_path_str + "/../markdown/")
                    output_path = input_path_str + "/../markdown"
                    html = "<!DOCTYPE html>\n" + style + "\n" + md.convert(md_str)
                    with open(output_path, 'w') as output_file:
                        output_file.write(html)


print("Markdown-HTML complete")
