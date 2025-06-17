# from functions.get_file_content import get_file_content
from functions.write_file import write_file

# from functions.get_files_info import get_files_info


def test():

    # result = get_files_info("calculator", ".")
    # print("results for current")
    # print(result)
    # print("")
    #
    # result = get_files_info("calculator", "pkg")
    # print("results for folder inside")
    # print(result)
    # print("")
    #
    # result = get_files_info("calculator", "./bin")
    # print("results for non existing folder")
    # print(result)
    # print("")
    #
    # result = get_files_info("calculator", "../")
    # print("results for folder outside")
    # print(result)
    # print("")

    # result = get_file_content("calculator", "lorem.txt")
    # print("results for current")
    # print(result)
    # print("")

    # result = get_file_content("calculator", "main.py")
    # print("results for a file in main folder")
    # print(result)
    # print("")
    #
    # result = get_file_content("calculator", "pkg/calculator.py")
    # print("results for a file inside a folder")
    # print(result)
    # print("")
    #
    # result = get_file_content("calculator", "/bin/cat")
    # print("results for folder outside")
    # print(result)
    # print("")

    result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print(result)

    result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print(result)

    result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print(result)


if __name__ == "__main__":
    test()
