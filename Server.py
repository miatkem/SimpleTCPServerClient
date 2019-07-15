# Name: Madison Miatke
# UCID: mdm56
# Section: 002

import sys, time, random, datetime, os.path, calendar
from socket import *
from struct import *

#RETURN current time in GMT
def getCurrentTime():
    return time.strftime("%a, %d %b %Y %H:%M:%S %Z", datetime.datetime.utcnow().timetuple())

#PRINT formatted header of an HTTP response or request
def printHeader(header):
    preq=header
    preq=repr(preq)
    preq=preq.replace("'","")
    preq=preq.replace("\\n","\\n\n")
    if preq[0:1]=="u": preq=preq[1:]
    print(preq)
    return 0

#Load command line arguments
argv = sys.argv
serverIP = argv[1]
serverPort = int(argv[2])
dataLen = 100000

# Create a TCP "welcoming" socket. Notice the use of SOCK_STREAM for TCP packets
serverSocket = socket(AF_INET, SOCK_STREAM)
# Assign IP address and port number to socket
serverSocket.bind((serverIP, serverPort))
# Listen for incoming connection requests
serverSocket.listen(1)

print('The server is ready to receive on port: ' + str(serverPort))

# loop forever listening for incoming connection requests on "welcoming" soecket
while True:
    # Accept incoming connection requests, and allocate a new socket for data communication
    connectionSocket, address = serverSocket.accept()
    print("Socket created for client " + address[0] + ", " + str(address[1]))
    #wait to recieve a HTTP Request from the client
    request = connectionSocket.recv(dataLen).decode()
    printHeader(request)
    
    #Parse HTTP Request
    sendBody=True
    statusCode=200
    statusPhrase="OK"    
    file = request[request.index("/")+1:request.index(".html")+5] #get the file name
    print("The client has requested a file: " + file)
    if not os.path.exists(file): #Check to see if file exists
        print("The file was not found, responding to client with an error.")
        statusCode=404
        statusPhrase="Not Found"
        sendBody=False
    elif "If-Modified-Since" in request: #Check if HTTP Request is conditional GET
        #load cache time to seconds since ephoch GMT
        cacheDate = request[request.index("Since:")+7:request.index("GMT")+7]
        t = time.strptime(cacheDate, "%a, %d %b %Y %H:%M:%S %Z\r\n")
        cacheFileTime = calendar.timegm(t)
        
        #load file modification time to seconds since ephoch GMT
        serverFileTime = os.path.getmtime(file)
        
        #if cache file is more recent than sever file the client has a sufficient cache
        if serverFileTime < cacheFileTime:
            print("The client has a sufficient cache, responding with 'Not Mofified'.")
            statusCode=304
            statusPhrase="Not Modified"
            sendBody=False
        else:
            print("The client has does not have sufficient cache.")
    
    # Create HTTP Response to send to the client
    response="HTTP/1.1 " + str(statusCode) + " " + statusPhrase + "\r\n"
    response+="Date: " + getCurrentTime() + "\r\n"
    if sendBody:
        print("Sending " + file + " to client.")
        response+="Last-Modified: " + timeSinceModification(file) + "\r\n"
        response+="Content-Length: " + str(os.path.getsize(file)) + "\r\n"
        response+="\r\n"
        with open(file, 'r') as file:
            data = file.read().replace('\n', '')    
        response+=data
    else:
        response+="\r\n"

    #send response and close socket
    connectionSocket.send(response.encode())
    connectionSocket.close() 