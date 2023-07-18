import fileinput
import os
from os import path
import hashlib
import logging
import json
from itertools import cycle
from random import choices
from pathlib import Path
import shutil

# preconfigure
def preconfigure(dir):

    a = ""
    extracted_path = Path(dir)
    tmp_dir = Path("tmp")
    if tmp_dir.exists():
        shutil.rmtree(tmp_dir)
    tmp_dir.mkdir()
    tmp_ext_dir = tmp_dir.joinpath(extracted_path.name)
    tmp_ext_dir.mkdir()
    for file in extracted_path.glob("**/*.*"):
        t = tmp_ext_dir.joinpath(file.name)
        t.touch()
        if file.suffix == ".js":
            with file.open("r") as ext, t.open("a") as tmp:
                for line in ext:
                    if "active: !0" in line:
                        a = "active: !0"
                        line = line.replace(a, "active: false")
                    elif "active: true" in line:
                        a = "active: true"
                        line = line.replace(a, "active: false")
                    tmp.write(line)
        else:
            shutil.copyfile(file, t)

    # for root, dirs, files in os.walk(folder_path):
    #     # Perform the find and replace operation on each JavaScript file in the folder
    #     for filename in files:
    #         if filename.endswith(".js"):
    #             file_path = os.path.join(root, filename)

    #             # Perform the find and replace operation
    #             with fileinput.FileInput(file_path, inplace=True,) as file:
    #                 for line in file:
    #                     # Replace "active: true" with "active: false"
    #                     if "active: !0" in line:
    #                         a = "active: !0"
    #                         line = line.replace(a, "active: false")
    #                     elif "active: true" in line:
    #                         a = "active: true"
    #                         line = line.replace(a, "active: false")
    #                     print(line, end="")
  
# interpreter
def interpreter(data):
    tainted = []
    for i in data:
        taint = {}
        taint_sink = i["extra"]["dataflow_trace"]["taint_sink"][1][1]
        taint_source = i["extra"]["dataflow_trace"]["taint_source"][1][1]
        metavars = {}
        try:
            if i["extra"]["metavars"]["$MESSAGEPASSWORD"]:
                metavars["MESSAGEPASSWORD"] = i["extra"]["metavars"]["$MESSAGEPASSWORD"]["abstract_content"]
            if i["extra"]["metavars"]["$MESSAGEPROPERTY"]:
                metavars["MESSAGEPROPERTY"] = i["extra"]["metavars"]["$MESSAGEPROPERTY"]["abstract_content"]
        except:
            pass
        try:
            if i["extra"]["metavars"]["$PORT"]:
                metavars["PORT"] = i["extra"]["metavars"]["$PORT"]["abstract_content"]
            try:
                if i["extra"]["metavars"]["$PORTPASSWORD"]:
                    metavars["PORTPASSWORD"] = i["extra"]["metavars"]["$PORTPASSWORD"]["abstract_content"]
                if i["extra"]["metavars"]["$PORTPROPERTY"]:
                    metavars["PORTPROPERTY"] = i["extra"]["metavars"]["$PORTPROPERTY"]["abstract_content"]
            except:
                pass
        except:
            pass
        try:
            if i["extra"]["metavars"]["$COOKIE"]:
                metavars["COOKIE"] = i["extra"]["metavars"]["$COOKIE"]["abstract_content"]
            if i["extra"]["metavars"]["$DETAILS"]:
                metavars["DETAILS"] = i["extra"]["metavars"]["$DETAILS"]["abstract_content"]
            if i["extra"]["metavars"]["$FUNC"]:
                metavars["FUNC"] = i["extra"]["metavars"]["$FUNC"]["abstract_content"]
        except:
            pass
        try:
            if i["extra"]["metavars"]["$X"]:
                metavars["X"] = i["extra"]["metavars"]["$X"]["abstract_content"]
            if i["extra"]["metavars"]["$W"]:
                metavars["W"] = i["extra"]["metavars"]["$W"]["abstract_content"]
        except:
            pass
        try:
            if i["extra"]["metavars"]["$Y"]:
                metavars["Y"] = i["extra"]["metavars"]["$Y"]["abstract_content"]
            try:
                if i["extra"]["metavars"]["$Y"]["propagated_value"]:
                    metavars["yvalue"] = i["extra"]["metavars"]["$Y"]["propagated_value"]["svalue_abstract_content"]
            except:
                pass
        except:
            pass
        try:
            if i["extra"]["metavars"]["$OBJ"]:
                metavars["OBJ"] = i["extra"]["metavars"]["$OBJ"]["abstract_content"]
        except:
            pass
        metavar = []
        var = ""
        try:
            for j in i["extra"]["dataflow_trace"]["intermediate_vars"]:
                metavar.append(j["content"])
            try:
                if metavar[1]:
                    var = metavar[1]
            except:
                var = metavar[0]
            metavars["content"] = var
            taint["metavars"] = metavars
        except:
            taint["metavars"] = metavars
        # added this
        line_start = i["extra"]["dataflow_trace"]["taint_source"][1][0]['start']['line']
        line_end = i["extra"]["dataflow_trace"]["taint_sink"][1][0]['end']['line']
        # added this
        message = i["extra"]["message"]
        taint["message"] = message
        taint["source"] = taint_source
        taint["sink"] = taint_sink
        # added this
        taint["line_start"] = line_start 
        taint["line_end"] = line_end 
        # added this
        tainted.append(taint)
    return tainted

# obtain relevant extension information'
def get_ext_id(path_to_extension):
    abs_path = path.abspath(path_to_extension)
    m = hashlib.sha256()
    m.update(abs_path.encode("utf-8"))
    ext_id = "".join([chr(int(i, base=16) + 97) for i in m.hexdigest()][:32])
    url_path = f"chrome-extension://{ext_id}/popup.html"
    return url_path, abs_path, ext_id

# definind payloads
def payloads(path_to_payload):
    payload_array = []
    try:
        with open(path_to_payload, 'r') as file:
            # Read the contents of the file
            for line in file:
                payload_array.append(line)
    except FileNotFoundError:
        print("File not found.")
    except IOError:
        print("An error occurred while reading the file.")
    
    return payload_array


# new payload function (use this)
def payloads_cycle(n: int, pct: int, file_path: str):
    c = cycle(range(n))
    meta_payloads = [[] for _ in range(n)]
    with open(file_path, "r") as file:
        for line in file:
            if line != "\n":
                meta_payloads[c.__next__()].append(line.rstrip())
    totals = [round(pct/100*len(pylds)) for pylds in meta_payloads]
    meta_payloads = (tuple(choices(pylds, k=total)) for total, pylds in zip(totals, meta_payloads))
    return tuple(totals), tuple(meta_payloads) 








