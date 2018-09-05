from settings import reed
import sys
import os

if __name__ == "__main__":
	name = raw_input('Enter a username: ')
	board = ""

subscribe = False
boards = []

#Create a log file/overwrite old log


#Create an instance of Redis pubsub
pub2sub = reed.pubsub()

#Print name of the board
print "Welcome. You are not on a board. Choose one with the \"Select\" command."

while True:
    try:
        #If subscribed to a board, the user only listens
        if subscribe:
            print "You are listening on board {board}".format(**locals())
            for i in pub2sub.listen():
                print i["data"]

        #Get user message
        message = raw_input("Input your command. Commands are \"exit\", \"select\", \"read\", \"write\", \"listen\" and \"stop\": ")

        #Split the message up by Spaces into an array. Each array index is a word
        message_split = message.split(" ")

        #Check for "Exit" command
        if message_split[0].lower() == "exit":
    		break

        #Check for "Select" command
        elif message_split[0].lower() == "select":
            board = message_split[1]
            boards.append(board)
            #log = open(board + ".txt","a+")
            print "You have switched to board {board}".format(**locals())

        #Check for "Read" command
        elif message_split[0].lower() == "read" and board != "":
            temp = reed.lrange(board,0,-1)
            for i in temp:
                print(i)

            '''
            log = open(board + ".txt","r")
            if log.mode == "r":
                lines = log.readlines()
                print("\n")
                for x in lines:
                    print(x.rstrip('\n'))
                print("\n")
            else:
                print("Open failed!")
            '''

        #Check for "Write" command
        elif message_split[0].lower() == "write" and board != "":
            message_text = message.split(" ", 1)[1]
            message_text = "{name} says: {message_text}".format(**locals())
            reed.publish(board, message_text)
            reed.rpush(board, message_text)

            '''
            log = open(board + ".txt","a+")
            log.write(message_text)
            log.write("\n")
            log.close()
            '''

        #Check for "Listen" command
        elif message_split[0].lower() == "listen" and board != "":
            pub2sub.subscribe(board)
            subscribe = True

        #Check for "Stop" command
        elif message_split[0].lower() == "stop" and board != "" and subscribe != False:
            pub2sub.unsubscribe(board)
            subscribe = False
            print "You have unsubscribed from {board}".format(**locals())

        #Handle invalid input
        else:
            if board == "":
                print("You must select a board.")
            elif subscribe == False:
                print("You are not listening to a board.")
            else:
                print("Invalid input!")

    except KeyboardInterrupt:
        subscribe = False

#Clean up log to avoid file clutter
'''
try:
    for i in boards:
        os.remove(i + ".txt")
except OSError as e:
    print ("Error: %s - %s." % (e.filename, e.strerror))
'''