# Simple-TCP-HTML-Server-Client
A simple TCP Server and Client that implements a cache to perform conditional get requests in addition to normal get requests to send files from the server to client upon request.

# Resources
Python Libraries:
<ul><li>System Library
<li>Random Library
<li>Time Library
<li>DateTime Library
<li>os.path Library
<li>Socket Library
<li>Struct Library
</ul>

# The Client
<ol><li>Parse IP and PORT from system arguments as well as URL to specific file on the server.
<li>Create TCP socket and connect to the server's IP and PORT
<li>Create the HTTP request:
<ul><li>If the cache for the URL exists, send a conditional request to see if the entire webpage needs to be retransmitted
<li>Otherwise send a normal HTTP GET request for the URL</ul>
<li>Sent request to the TCP server
<li>Wait for and recieve sever response
<li>Parse the server HTTP response:
<ul><li>If status code is 304, use the cached file since the sever has not modified the file since it was last cached
<li>If status code is 404, the file was not found
<li>If status code is 202, the file was retrieved from the server and it should be cached</ul>
<li>Display file and close socket</ol>

# The Server
<ol><li>Parse IP and PORT from system arguments
<li>Create a TCP "welcoming" socket and assign it the parsed IP and PORT
<li>Begin listening for incoming connection requests
<li>Accept and incoming connection request and allocate a new socket for data transmission
<li>Wait for HTTP request on new socket
<li>Upon recieving the HTTP request, parse it's information and build the response:
<ul><li>If the request is a CONDITIONAL GET compare cache times to the last time the file on the server was modified
<ul><li>If cache has expired, send a normal 200 response with the requested file
<li>If cache is valid, send a 304 response with the status phrase Not Modified</ul>
<li>If the request is a normal GET, search for the requested file
<ul><li>If it doesn't exist, send a 404 response with the status phrase "File Not Found"
<li>If it does exist, append the information to the body of the response</ul></ul>
<li>Send the response the client and close the socket</ol>
