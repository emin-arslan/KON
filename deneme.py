def check_empty_line(file_path):
    with open(file_path) as file:
        lines = file.readlines()
        if len(lines) == 0:
            print("Dosya boş")
        elif not lines[0].strip():
            print("1. satır boş")
        elif len(lines) > 1 and not lines[1].strip():
            print("2. satır boş")
        else:
            print("Herhangi bir satır boş değil")

file_path = "chat_id.txt"
check_empty_line(file_path)