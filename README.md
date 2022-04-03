This is a python program made as PJATK assignment project.

## How to run
In order to run the program you should type in the terminal following syntax:  

`python main.py <command> <argument>`  

The commands can be combined so multiple commands might be given at the same time.  
The only thing to keep in mind is the  number of required arguments for each command.

Available commands:  
-

- `register`
    * **_Arguments:_** None
    * **_Example:_** `python main.py register` 
    * **_Result:_** Prompts user to provide its username and password.
- `login <username>`
  * **_Arguments:_** username
  * **_Example:_** `python main.py login admin`
  * **_Result:_** Prompts user to provide password
- `list_all <filter>` **_User has to be logged in_**
  * **_Arguments:_** filter proceeded by two dashes.
  * **_Example:_** `python main.py login admin list_all -- list_all --a` 
  * **_Error:_** Throws `You are not authorized to do this operation` error if used before logging in.
  * **_Result:_** Lists all users matching provided filter. Filter searches for string occurrences within username.
- `delete <username>` **_User has to be logged in_**
  * **_Arguments:_** username
  * **_Example:_** `python main.py login admin delete admin` 
  * **_Error:_** Throws `You are not authorized to do this operation` error if used before logging in.
  * **_Result:_** Deletes user from database.
  
I am aware that this program contains hella lot of bugs. I accepted it and I live with it.