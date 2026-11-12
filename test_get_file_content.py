from functions.get_file_content import get_file_content

def print_file_details(folder: str, file_name: str):
    result = get_file_content(folder, file_name)
    print(f"{file_name} length: {len(result)}")
    print(f"{file_name} truncated: {'truncated' in result}")

print_file_details("calculator", "lorem.txt")
print(get_file_content("calculator", "main.py"))
print(get_file_content("calculator", "pkg/calculator.py"))
print(get_file_content("calculator", "/bin/cat"))
print(get_file_content("calculator", "pkg/does_not_exist.py"))
