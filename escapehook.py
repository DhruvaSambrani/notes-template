#! /usr/bin/env python3

import urllib.parse
import re
import sys

print(sys.argv[-1])
text = open(sys.argv[-1], encoding="utf8").read()
list_text = list(text)

mathsections = [r.span() for r in re.finditer(r"\$.*\$", text)]
print("Found", len(mathsections), "math sections")
wikilinksections = [r.span() for r in re.finditer(r"\[\[.*\]\]", text)]
print("Found", len(wikilinksections), "wikilink sections")

for section in mathsections:
    for i in range(*section):
        if list_text[i] in ["*", "|"] and list_text[i-1] != "\\":
            print("Replacing", list_text[i], "at", i)
            list_text[i] = "\\"+list_text[i]

for section in wikilinksections:
    for i in range(*section):
        if list_text[i] in ["|"] and list_text[i-1] != "\\":
            print("Replacing", list_text[i], "at", i)
            list_text[i] = "\\"+list_text[i]

text = "".join(list_text)
linkrefstart = re.search(r"\[//begin\]", text).span()[0]
linkrefs = text[linkrefstart:].split("\n")
print("Found", len(linkrefs)-2, "link refs")
for i in range(1, len(linkrefs)-2):
    linkrefs[i] = linkrefs[i].replace("\\|", "|")
    titleloc = re.search('".*"', linkrefs[i]).span()
    inhtml = re.search("\[(.*)\]", linkrefs[i]).group(1)
    if "|" in inhtml:
        newtitle = inhtml.split("|")[1]
        print("Replacing", linkrefs[i][titleloc[0]:titleloc[1]], "with", newtitle)
    else:
        newtitle = inhtml
    linkrefs[i] = linkrefs[i][:titleloc[0]]+"\""+newtitle+"\""
    parts = re.match("\[(.*)\]:\ (.*?)\ \"(.*)\"", linkrefs[i]).groups()
    linkparts = parts[0].split("|")[0].split("#")
    if len(linkparts) == 2:
        linkparts[1]=linkparts[1].replace(" ", "-").lower()
    link = "#".join(linkparts)
    linkrefs[i] = f'[{parts[0]}]: {link} "{parts[2]}"'
    
open(sys.argv[-1], "w").write(text[:linkrefstart]+"\n".join(linkrefs))

