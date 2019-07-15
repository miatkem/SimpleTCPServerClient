# Name: Madison Miatke
# UCID: mdm56
# Section: 002

import sys, time, os.path
from socket import *
from struct import *

#RETURN true if a cache for the file exists
def isCached(file):
    return os.path.exists(getCacheName(file))

#RETURN a filename that is 'file"_cache.txt
def getCacheName(file):
    filename = file[file.index("/")+1:file.index(".")]
    filename.replace("/","_")
    return filename + "_cache.txt"  

#RETURN the date of last modification of 'file'
def timeSinceModification(file):
    secs = os.path.getmtime(file)
    t = time.gmtime(secs)
    return time.strftime("%a, %d %b %Y %H:%M:%S GMT\r\n", t)

#PRINT formatted header of an HTTP response or request
def printHeader(header):
    preq=header
    preq=repr(preq)
    preq=preq.replace("'","")
    preq=preq.replace("\\n","\\n\n")
    if preq[0:1]=="u": preq=preq[1:]
    print(preq)
    return 0

#Get the server hostname, port and filename as a url
argv = sys.argv
url = str(argv[1])

#parse ip, port, and file name from url
host = url[0:url.index(":")]
port = int(url[url.index(":")+1: url.index("/")])
if(host=="localhost"):
    host="127.0.0.1"
file = url[url.index("/"):]

dataLen = 100000
    
# Create TCP client socket. Note the use of SOCK_STREAM for TCP packet
clientSocket = socket(AF_INET, SOCK_STREAM)
# Create TCP connection to server
print("Connecting...")
clientSocket.connect((host, port))
print("Connection Successful!")

#Create HTTP request
conditional = False
request=  "GET   " + file + "   HTTP/1.1\r\n"
request+= "Host:  localhost:" + str(clientSocket.getsockname()[1]) + "\r\n"
if isCached(file): #Add conditonal statement if file found in cache
    print("File exists in cache.")
    conditional = True
    request+= "If-Modified-Since: " + timeSinceModification(getCacheName(file))
    print("Sending HTTP CONDITIONAL GET request for " + file)
else: #Otherwise send normal GET Request
    print("Sending HTTP GET request for " + file)
request+= "\r\n"

#Send request through TCP connection
print("\nHTTP REQUEST:")
printHeader(request)
clientSocket.send(request.encode())

# Receive the server response
response = clientSocket.recv(dataLen).decode()
print("Response recieved from server.")

#Print Response
print("\nHTTP RESPONSE:")
printHeader(response)

#Parse Sever Response
statusCode=response.split(" ")[1]
if statusCode=="304":
    print("The file has not been modified, using cached file.")
    cache=getCacheName(file)
    with open(cache, 'r') as file:
        body = file.read().replace('\n', '')
    print(body)
elif statusCode == "404":
    print("Error: The file was not found")
elif statusCode == "200":
    print("File retrieved from server...")
    body=response[response.index("\r\n\r\n")+4:]
    print(body)
    #Create cache for body or update existing one
    print("Placing file in cache.")
    f = open(getCacheName(file), "w")
    f.write(body)
    f.close()    
    
# Close the client socket
clientSocket.close()
    

    
    