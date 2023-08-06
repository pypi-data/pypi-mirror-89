import tkinter as tk
from tkinter import filedialog
import os.path
import tempfile
import zipfile
from bs4 import BeautifulSoup
import requests
import re

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            filepath = os.path.join(root, file)
            ziph.write(filename=filepath, arcname=filepath.replace(path, ""))

def downloadImage(url, directory):
    # download image from url to the specified directory. Also creates directory if not exists
    # returns the filename
    filename = re.sub('[^\w\-_\. ]', '_', url.split('/')[-1])
    
    if not os.path.exists(directory):
        os.makedirs(directory)
    filepath = os.path.join(directory, filename)
    r = requests.get(url, allow_redirects=True)
    open(filepath, 'wb').write(r.content)
    return filename


def Main():
    print("Download and save images back into the zip of Medium.com backup zip file.")
    HTMLArchive = None
    if len(sys.argv)>1:
        HTMLArchive = sys.argv[1]
        if not os.path.isfile(HTMLArchive):
            logging.error(f"The specified HTML Archive file is not exists: {HTMLArchive}")
            raise Exception() 
    
    if HTMLArchive:
        zipfilename = HTMLArchive
    else:
        print("Usage:")
        print("   HTMLPackImagesaver.py [HTMLArchive]")
        print("      HTMLArchive: path to a zipped HTML archive file. Opens a file selector dialog if missing.")

        root = tk.Tk()
        root.withdraw()
        zipfilename = filedialog.askopenfilename(title = "Select the Medium.com backup zip file",filetypes = (("zip files","*.zip"),("all files","*.*")))
        if not os.path.isfile(zipfilename):
            logging.error("No valid file selected")
            raise Exception() 

    logging.info(f"Selected zip: {zipfile}")

    with tempfile.TemporaryDirectory() as tempdir:
        logging.info(f"Tempdir: {tempdir}")

        with zipfile.ZipFile(zipfilename, 'r') as zipf:
            logging.info(f"Unzip: {zipfilename}")
            zipf.extractall(tempdir)
        
        for root, dirs, files in os.walk(tempdir):
            for file in files:
                filepath = os.path.join(root, file)
                filedir = os.path.dirname(filepath)
                logging.info(f"Search images in {file}")
                
                soup = None
                with open(filepath, "rb") as f:
                    try:
                        soup = BeautifulSoup(f, "html5lib")
                    except:
                        logging.debug(f"This is not a html file: {file}")
                
                if soup:
                    imgfound = False
                    links = soup.find_all('img')
                    for i in links:
                        imgfilename = downloadImage(i['src'], os.path.join(filedir, "images"))
                        i['src'] = os.path.join("images", imgfilename)
                        imgfound = True

                    if imgfound:
                        logging.info("Saving changes...")
                        with open(filepath, "w", encoding="utf-8") as file:
                            file.write(str(soup))
                    

        outfile = zipfilename
        if os.path.isfile(outfile):
            logging.info(f"Delete existing file: {outfile}")
            os.remove(outfile)
            
        with zipfile.ZipFile(outfile, 'w', zipfile.ZIP_DEFLATED) as zipf:
            logging.info(f"Compress files to zip")
            zipdir(tempdir, zipf)

### set up logging
import logging, sys, socket

machinename = socket.gethostname()
logging.basicConfig(
    level=logging.INFO,
    #format=f"%(message)s\t%(asctime)s\t{machinename}\t%(threadName)s\t%(levelname)s",
    format=f"%(message)s",
    handlers=[
        #logging.FileHandler(f"{logfile}.txt"),
        logging.StreamHandler(sys.stdout)
        #TalkerHandler()
    ]
)


# main run
try:
    Main()
except Exception:
    logging.exception("Fatal error")

