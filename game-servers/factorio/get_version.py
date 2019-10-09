import requests
from bs4 import BeautifulSoup
import subprocess

data = requests.get("https://wiki.factorio.com/Version_history")
soup = BeautifulSoup(data.content, "html.parser")

number = 0
for i in soup.findAll("a"):
    if "0." in i.text:
        number += 1
        print(number)
        subprocess.run(["./update.sh", "{}".format(i.text)])