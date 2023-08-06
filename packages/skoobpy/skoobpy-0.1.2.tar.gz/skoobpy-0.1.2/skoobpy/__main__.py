from skoobpy import *

def main():
    from sys import argv
    user_id = argv[1]

    books_json = get_all_books(user_id)
    save_desired_csv(books_json, user_id)



if __name__ == "__main__":
    main()