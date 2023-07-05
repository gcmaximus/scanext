import json
from os import makedirs
from pathlib import Path
import shutil
from zipfile import ZipFile
import jsbeautifier

# output_file = "tmp1.json"

# with open(output_file, "r") as static_result_file:
#     results = json.load(static_result_file)["results"]
#     sorted_results = sorted(results, key=lambda e: e["path"])
#     sorted_results = sorted(sorted_results, key=lambda e: e["check_id"])


extension_dir = "SHARED/EXTENSIONS"
extraction_dir = "SHARED/EXTRACTED"


types = ("*.zip", "*.crx")
extensions = []
for type in types:
    extensions.extend(Path(extension_dir).glob(type))


opts = jsbeautifier.default_options()
opts.end_with_newline = True
opts.wrap_line_length = 80
opts.space_after_anon_function = True


if Path(extraction_dir).exists():
    shutil.rmtree(extraction_dir)
makedirs(extraction_dir)


for extension in extensions:
    extension: Path
    indi_dir = Path(extraction_dir, extension.stem)
    makedirs(indi_dir)
    with ZipFile(extension, "r") as zip:
        zip.extractall(indi_dir)
    for file in indi_dir.glob("*"):
        if file.is_file():
            pretty = jsbeautifier.beautify_file(file, opts)
            tmp = jsbeautifier.BeautifierOptions()
            # print("beautified " + str(file))
            jsbeautifier.write_beautified_output(pretty,tmp , str(file))
