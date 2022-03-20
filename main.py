from command import dispatch

if __name__ == '__main__':
    dispatch()

# write and read from csv
# register user (should write to csv)
# - insensitive username
# - safe password (length at least 8, 1 cipher, 1 letter, 1 big letter)
# - user regexp to verify if the password meets requirements
# - reading password should not print it to the console (writing?)
# - there should not be absolute path to csv file
# - csv file should be in another module under resources/db/db.csv
# login registered user
# delete user
