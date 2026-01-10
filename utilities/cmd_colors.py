red = "\033[91m"
green = "\033[92m"
yellow = "\033[93m"
blue = "\033[94m"
magenta = "\033[95m"
cyan = "\033[96m"
reset = "\033[0m"


def errorElement(elementName):
    print(f"[{red}Error{reset}] Cant find {yellow}'{elementName}'{reset}, make sure {blue}\"elements.json\"{reset} is updated")


def filesCreation(fileType,path):
    print(f"[{magenta}Files{reset}] Successfully Created {cyan}{fileType}{reset} at \"{yellow}{path}{reset}\" ")