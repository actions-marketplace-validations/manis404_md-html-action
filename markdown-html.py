#!/bin/python3

print("- Markdown-HTML -")

import markdown, natsort, os, json, pathlib

REPO_PATH = pathlib.Path(os.environ['GITHUB_WORKSPACE'])
INPUT_LIST = json.loads(os.environ['INPUT_INPUT_FILES'])
BUILTIN_STYLESHEET : str = ""
EXTENSIONS : list = ["pymdownx.extra"]
EXTENSION_CONFIGS : dict = json.loads(os.environ['INPUT_EXTENSION_CONFIGS'])

md = markdown.Markdown(extensions=EXTENSIONS, extension_configs=EXTENSION_CONFIGS, output_format="html5")

if not isinstance(INPUT_LIST, list) or not all([isinstance(sublist, list) for sublist in INPUT_LIST]):
    raise ValueError("input_files must be a JSON list of lists")

if BUILTIN_STYLESHEET != "":
    with open(REPO_PATH.joinpath(BUILTIN_STYLESHEET), 'r') as stylesheet_file:
        style = "<style>\n" + stylesheet_file.read() + "</style>\n"
else:
    style = ""

for input_sublist in INPUT_LIST:
    
    for input_path_glob_str in input_sublist:
        input_path_list = natsort.natsorted([str(p) for p in REPO_PATH.glob(input_path_glob_str)])
        for input_path_str in input_path_list:
                
                md.reset()
                md_str = ""

                with open(input_path_str, 'r') as input_file:
                    # skip first line
                    next(input_file)

                    md_str = input_file.read() + "\n"

                    fileName = os.path.basename(input_path_str)[:-3]

                    output_dir = os.environ['GITHUB_WORKSPACE'] + "/html/"
                    output_file_path = output_dir + fileName + ".html"

                    if not os.path.exists(output_dir):      
                        os.makedirs(output_dir)
                    
                    print("Generating", output_file_path)

                    html = "<!DOCTYPE html>\n" + style + "\n" + md.convert(md_str)

                    cleaned_html = html.replace("<strong>", "<b>").replace("</strong>", "</b>").replace("<em>", "<i>").replace("</em>", "</i>")


                    
                    with open(output_file_path, 'w') as output_file:
                        output_file.write(cleaned_html)


print("Markdown-HTML complete")
