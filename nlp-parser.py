import os, sys, io, re, glob
import pprint, argparse

# 3rd party import
import docx2txt

# local imports
from func import make_prompts, write_output_file
from cli_args import args

from openai_api import openai

# decide between file flow and directory flow
if args.file:
    if ".doc" in args.file:
        txt = docx2txt.process(os.path.normpath(args.file))

        # get prompts parsed from file and print text to out put file
        prompts = make_prompts(txt=txt, LIMIT=args.wlimit)
        write_output_file(prompts)

    elif ".txt" in args.file:
        # get prompts parsed from file and print text to out put file
        prompts = make_prompts(txt_file=os.path.normpath(args.file), LIMIT=args.wlimit)

        # make API calls for each prompt
        output_txt = []
        for p in prompts:
            response = openai.Completion.create(
                engine="davinci", prompt=p, max_tokens=100, top_p=0.4
            )
            for r in response["choices"]:
                output_txt.append(r["text"])

        write_output_file(prompts)
        
        write_output_file(
            output_txt,
            file_name=f"response_{arg.file.replace(' ', '_').replace('.docx', '.txt')}",
        )

elif args.directory:

    for file_name in glob.iglob(f"{args.directory}/*"):
        if ".doc" in file_name:
            txt = docx2txt.process(os.path.normpath(file_name))

            # get prompts parsed from file and print text to out put file
            prompts = make_prompts(txt=txt, LIMIT=args.wlimit)
            write_output_file(prompts, file_name=file_name)

        elif ".txt" in file_name:
            # get prompts parsed from file and print text to out put file
            prompts = make_prompts(
                txt_file=os.path.normpath(file_name), LIMIT=args.wlimit
            )
            write_output_file(prompts, file_name=file_name)