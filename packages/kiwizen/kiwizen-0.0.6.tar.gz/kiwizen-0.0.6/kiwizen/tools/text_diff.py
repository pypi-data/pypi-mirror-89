import difflib
import sys
import os


def TextDiff(file1, file2):
    htm_diff = difflib.HtmlDiff(tabsize=4, wrapcolumn=130)
    with open(file1, "r") as f:
        f1 = f.readlines()
    with open(file2, "r") as f:
        f2 = f.readlines()

    savefile = os.path.join(os.getcwd(), "diff.html")

    with open(savefile, 'w') as f:
        f.write(htm_diff.make_file(f1, f2))
    print("Successfully generated diff file: %s" % savefile)
