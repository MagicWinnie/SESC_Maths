import os
from shutil import copy
from argparse import ArgumentParser
from pathlib import Path

parser = ArgumentParser(
    description="Merge several .tex files into one. It should be used only with semesters."
)
parser.add_argument(
    "-i",
    "--input",
    type=str,
    required=True,
    help="Path to directory with folders containing .tex files.",
)
parser.add_argument(
    "-o",
    "--output",
    type=str,
    required=True,
    help="Path to directory where the file should be created.",
)
parser.add_argument(
    "-v", "--version", type=str, required=True, help="Version of the generated file."
)
args = parser.parse_args()

if not (os.path.exists(args.input)):
    raise Exception("[ERROR] Given input directory does not exist.")
Path(os.path.join(args.output, args.version)).mkdir(parents=True, exist_ok=True)
Path(os.path.join(args.output, args.version, "images")).mkdir(
    parents=True, exist_ok=True
)

output_file = open(
    os.path.join(args.output, args.version, "main.tex"), "w", encoding="utf-8"
)

with open("template.tex", "r", encoding="utf-8") as template:
    for line in template:
        output_file.write(line)
        if line.replace("\n", "").strip() == "\\begin{document}":
            break

folders = filter(
    lambda x: os.path.isdir(os.path.join(args.input, x)), os.listdir(args.input)
)
for folder in sorted(folders, key=int):
    if "images" in os.listdir(os.path.join(args.input, folder)):
        imgs = list(
            filter(
                lambda x: x.split(".")[-1] in ["png", "jpg", "jpeg", "gif"],
                os.listdir(os.path.join(os.path.join(args.input, folder, "images"))),
            )
        )
        for img in imgs:
            copy(
                os.path.join(args.input, folder, "images", img),
                os.path.join(args.output, args.version, "images"),
            )
    if "main.tex" in os.listdir(os.path.join(args.input, folder)):
        output_file.write(
            "\input{{../../{}}}\n".format(
                os.path.join(args.input, folder, "main").replace("\\", "/")
            )
        )

output_file.write("\\end{document}")
output_file.close()
