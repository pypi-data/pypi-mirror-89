

import zipfile
import tempfile
import os
import argparse
import sys
import pathlib
import subprocess

def run(cmd, tempdir):
    ph = subprocess.Popen(cmd,shell=True,cwd=tempdir, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err = ph.communicate()
    return (out+err).decode()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path_to_zips", help="Where are the zips to search")
    parser.add_argument("-c","--cmd_to_run", help="Command line to run on each zip") 
    args = parser.parse_args()

    if not args.cmd_to_run:
        cmd = input("What command would you like to run?: ")
    else:
        cmd = " ".join(args.cmd_to_run)
        cmd = args.cmd_to_run

    try:
        tgt_dir = pathlib.Path(args.path_to_zips)
    except Exception as e:
        print(f"Invalid ZIP Path:{args.path_to_zips}")
        print(str(e))
        sys.exit(1)

    if tgt_dir.is_dir():
        zipfiles = tgt_dir.glob("*.zip")
    elif tgt_dir.parent.is_dir():
        zipfiles = tgt_dir.parent.glob(tgt_dir.name)

    for eachfile in zipfiles:
        with tempfile.TemporaryDirectory() as tmpdirname:    
            try:
                with zipfile.ZipFile(eachfile,"r") as zip_ref:
                    zip_ref.extractall(tmpdirname)
            except:
                print(f"Unable to process {eachfile}")
            #print(cmd, str(tmpdirname))
            result = run(cmd, str(tmpdirname))
            if result:
                print(f"Processing {eachfile}:")
                print(result)

if __name__ == "__main__":
    main()
        
