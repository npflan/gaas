import re

string = "16.25 seconds"


print(re.sub("[\.][0-9]", " ", string)
