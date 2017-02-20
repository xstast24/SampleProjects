#include <stdio.h>
#include <stdlib.h>
#include <cstring>
#include <unistd.h>
#include <iostream>
#include <fstream>
#include <ctype.h>
#include <limits.h>
#include <netdb.h>
#include <netinet/in.h>
#include <sys/types.h>
#include <sys/socket.h>


#define REDIRECT_MAX 5


using namespace std;

//enum for error codes
enum errorCodes{
    NOERROR = 0,
    ERRREDIRECTION,
    ERRREDIRECTION2,
    ERRERR,
    ERRPARAMS,
    ERRHTTP,
    ERRHTTP10,
    ERRPORT1,
    ERRPORT2,
    ERRPORT3,
    ERRCREATESOCKET,
    ERRGETHOST,
    ERRCONNECT,
    ERRSEND,
    ERRGETRESPONSE,
    ERRCLOSESOCKET,
    ERRFILEWRITE
};

//url info (domain, port, ...)
typedef struct urlInfo {
    int port;  //port
    string domain;  //domain name
    string path; //path on the web
    string fileName;
} TUrl;


//print help message to standard output
void printHelp();

//print an error message for a given code
void printError(int code);

//print connection error returned by server
void printConnectionErrorType(string connectionErrorCode);

//check correct program arguments
int checkParams(int argc, char **argv);

//parse url
int parseUrl (char *url, TUrl *data);

//connect to host via newly created socket
int createSocketAndConnect(TUrl data, int *socket_pointer);

//Communicate with server and save the response
int getServerResponse(TUrl data, int sock, string *message, int *chunked);

//Communicate with server on HTTP 1.0 and save the response
int getServerResponseHttp10(TUrl data, int sock, string *message, int *chunked);

//get error code from server response
int checkResponse (string *message, int httpVersion);

//search response for redirect URL
void redirect (string *message);

//Cut the message body and store it into a file
int writeAndSave (string message, int chunked, TUrl data);


//main program structure
int main (int argc, char **argv) {
    char* url;
    TUrl data = {80, "", "/", "index.html"};
    int socketerino, tmpErrorCode;
    int chunked = 0;
    int errorCode = NOERROR;
    int ret = 0;
    int httpVersion;
    int urlRedirCount = 1;
    string err;
    string urlPrev;
    string message;
    string urlRed1;
    string urlRed2;
    string urlRed3;
    string urlRed4;
    string urlRed5;
    string urlNew1;
    string urlNew2;
    string urlNew3;
    string urlNew4;
    string urlNew5;

    urlRed1 = ""; urlRed2 = ""; urlRed3 = ""; urlRed4 = ""; urlRed5 = "";
    urlNew1 = ""; urlNew2 = ""; urlNew3 = ""; urlNew4 = ""; urlNew5 = "";

    //check arguments
    ret = checkParams(argc, argv);
    if(ret == 1) return EXIT_SUCCESS;
    else if(ret == 2) return EXIT_FAILURE;

    //parse URL from argument
    url = argv[1];
    errorCode = parseUrl(url, &data);
    if (errorCode != NOERROR) {
        printError(errorCode);
        return EXIT_FAILURE;
    }

    //create new socket and connect to host
    errorCode = createSocketAndConnect(data, &socketerino);
    if (errorCode != NOERROR) {
        printError(errorCode);
        return EXIT_FAILURE;
    }

    //get server response
    message = "";
    errorCode = getServerResponse(data, socketerino, &message, &chunked);
    if (errorCode != NOERROR) {
        printError(errorCode);
        return EXIT_FAILURE;
    }

    httpVersion = 11;
    err = message;
    //check server response
    tmpErrorCode = checkResponse(&err, httpVersion);

    //refused HTTP1.1, lets try 1.0
    if(tmpErrorCode == ERRHTTP10){
        //create new socket and connect to host
        errorCode = createSocketAndConnect(data, &socketerino);
        if (errorCode != NOERROR) {
            printError(errorCode);
            return EXIT_FAILURE;
        }

        //get server response
        message = "";
        errorCode = getServerResponseHttp10(data, socketerino, &message, &chunked);
        if (errorCode != NOERROR) {
            printError(errorCode);
            return EXIT_FAILURE;
        }

        httpVersion = 10;
        err = message;
        tmpErrorCode = checkResponse(&err, httpVersion);
    }

    //communication error
    if (tmpErrorCode == ERRERR) {
        printError(tmpErrorCode);
        return EXIT_FAILURE;
    }

    if (tmpErrorCode == ERRREDIRECTION or tmpErrorCode == ERRREDIRECTION2){
        err = message;
        redirect(&err);
        urlPrev = url;
        url = (char*)err.c_str();
        //check permanent redirect and save it
        if(tmpErrorCode == ERRREDIRECTION){
            urlRed1 = urlPrev;
            urlNew1 = url;
            urlRedirCount++;
        }
        if(urlRed1.find(url) != string::npos) url = (char*)urlNew1.c_str();

        for (int i=0; i < REDIRECT_MAX; i++) {
            TUrl data = {80, "", "/", "index.html"};

            errorCode = parseUrl(url, &data);
            if (errorCode != NOERROR) {
                printError(errorCode);
                return EXIT_FAILURE;
            }

            errorCode = createSocketAndConnect(data, &socketerino);
            if (errorCode != NOERROR) {
                printError(errorCode);
                return EXIT_FAILURE;
            }

            message = "";
            errorCode = getServerResponse(data, socketerino, &message, &chunked);
            if (errorCode != NOERROR) {
                printError(errorCode);
                return EXIT_FAILURE;
            }

            err = message;
            httpVersion = 11;
            tmpErrorCode = checkResponse(&err, httpVersion);
            //refused HTTP1.1, lets try 1.0
            if(tmpErrorCode == ERRHTTP10){
                //create new socket and connect to host
                errorCode = createSocketAndConnect(data, &socketerino);
                if (errorCode != NOERROR) {
                    printError(errorCode);
                    return EXIT_FAILURE;
                }

                //get server response
                message = "";
                errorCode = getServerResponseHttp10(data, socketerino, &message, &chunked);
                if (errorCode != NOERROR) {
                    printError(errorCode);
                    return EXIT_FAILURE;
                }

                httpVersion = 10;
                err = message;
                tmpErrorCode = checkResponse(&err, httpVersion);
            }

            if (tmpErrorCode == NOERROR or tmpErrorCode == ERRERR)
                break;
            else {
                err = message;
                redirect(&err);
                url = (char*)err.c_str();
                //check permanent redirect and save it
                if(tmpErrorCode == ERRREDIRECTION){
                    switch(urlRedirCount){
                        case 1:
                            urlRed1 = urlPrev;
                            urlNew1 = url;
                            break;
                        case 2:
                            urlRed2 = urlPrev;
                            urlNew2 = url;
                            break;
                        case 3:
                            urlRed3 = urlPrev;
                            urlNew3 = url;
                            break;
                        case 4:
                            urlRed4 = urlPrev;
                            urlNew4 = url;
                            break;
                        case 5:
                            urlRed5 = urlPrev;
                            urlNew5 = url;
                            break;
                        default:
                            break;
                    }
                    urlRedirCount++;
                }
                if(urlRed1.find(url) != string::npos) url = (char*)urlNew1.c_str();
                if(urlRed2.find(url) != string::npos) url = (char*)urlNew2.c_str();
                if(urlRed3.find(url) != string::npos) url = (char*)urlNew3.c_str();
                if(urlRed4.find(url) != string::npos) url = (char*)urlNew4.c_str();
                if(urlRed5.find(url) != string::npos) url = (char*)urlNew5.c_str();

            }
        }
    }

    //communication error
    if (tmpErrorCode == ERRERR) {
        printError(tmpErrorCode);
        return EXIT_FAILURE;
    }

    if(tmpErrorCode != NOERROR){
        printError(tmpErrorCode);
        return EXIT_FAILURE;
    }

    //save file
    errorCode = writeAndSave(message, chunked, data);
    if (errorCode != NOERROR) {
        printError(errorCode);
        return EXIT_FAILURE;
    }

    //if no errors appeared during the execution, exit program successfully, otherwise it would be ended earlier
    return EXIT_SUCCESS;
}


//Cut the message body and store it into a file
int writeAndSave (string message, int chunked, TUrl data)
{
    size_t index;
    string hexa = "", tmpStr = "";
    long int number = 42;

    //delete msg header
    index = message.find("\r\n\r\n");
    if (index != string::npos) message.erase(0, index+4);

    //handle the chunked data format
    if (chunked == 1) {
        while (number != 0) {
            if ((index = message.find("\r\n")) != string::npos) {
                hexa = message.substr(0, index);
                hexa.append("\0");
                number = strtol(hexa.c_str(), NULL, 16);
                //delete line ending
                message.erase(0, index+2);
                //copy "number" of characters
                tmpStr.append(message, 0, number);
                //delete lineending
                message.erase(0, number+2);
            }
        }
        message = tmpStr;
    }

    if(chunked == 0 or chunked == 1) {
        //save message to file
        ofstream OutFile;
        OutFile.open(data.fileName.c_str(), ios::out | ios::binary);
        if (OutFile.fail())
            return ERRFILEWRITE;

        OutFile.write(message.c_str(), message.length());
        OutFile.close();
        return NOERROR;
    }

    return ERRFILEWRITE;
}

//search response for redirect URL
void redirect (string *message)
{
    size_t index;

    index = (*message).find("Location:");
    (*message).erase(0, index+10);
    index = (*message).find("\n");
    (*message).erase(index);
}

//get error code from server response
int checkResponse (string *message, int httpVersion)
{
    size_t index;

    //remove "HTTP 1.1 " or "HTTP 1.0 " from the response, so the return code is at index 0
    (*message).erase(0, 9);
    index = (*message).find("\n");
    (*message).erase(index, string::npos);

    //200 OK
    if((*message).find("200") != string::npos)
        return NOERROR;
    //301 permanent redirect
    else if((*message).find("301") != string::npos)
        return ERRREDIRECTION;
    //302 temporary redirect
    else if((*message).find("302") != string::npos)
        return ERRREDIRECTION2;
    //400 & 505 different client/server version if used http1.1, lets try 1.0
    else if((((*message).find("400") != string::npos) or ((*message).find("505") != string::npos)) and (httpVersion == 11)) return ERRHTTP10;
    else{
        printConnectionErrorType(*message);
        return ERRERR;
    }
}

//Communicate with server on HTTP 1.0 and save the response
int getServerResponseHttp10(TUrl data, int sock, string *message, int *chunked)
{
    int response;
    unsigned int buffer_size = 1024;
    char buffer[1024];
    string request;

    //initial GET request, '\r' is used because CRLF is needed, not only LF
    request = "GET " +  data.path + " HTTP/1.0\r\n"
            "Host: " + data.domain + "\r\n"
            "Connection: close\r\n\r\n";

    //send request
    if (write(sock, request.c_str(), request.size()) < 0 ) return ERRSEND;

    //get response
    memset(buffer, 0, sizeof(char) * buffer_size);
    while ((response = read(sock, buffer, buffer_size)) > 0){
        (*message).append(buffer, response);
        if (response < 0) return ERRGETRESPONSE;
    }

    if (response < 0) return ERRGETRESPONSE;

    //set chunked flag if data will be chunked
    if ((*message).find("Transfer-Encoding: chunked\r\n") != string::npos) *chunked = 1;
    else *chunked = 0;

    //close socket
    if (close(sock) < 0) return ERRCLOSESOCKET;

    return NOERROR;
}


//Communicate with server and save the response
int getServerResponse(TUrl data, int sock, string *message, int *chunked)
{
    int response;
    unsigned int buffer_size = 1024;
    char buffer[1024];
    string request;

    //initial GET request, '\r' is used because CRLF is needed, not only LF
    request = "GET " +  data.path + " HTTP/1.1\r\n"
            "Host: " + data.domain + "\r\n"
            "Connection: close\r\n\r\n";

    //send request
    if (write(sock, request.c_str(), request.size()) < 0 ) return ERRSEND;

    //get response
    memset(buffer, 0, sizeof(char) * buffer_size);
    while ((response = read(sock, buffer, buffer_size)) > 0){
        (*message).append(buffer, response);
        if (response < 0) return ERRGETRESPONSE;
    }

    if (response < 0) return ERRGETRESPONSE;

    //set chunked flag if data will be chunked
    if ((*message).find("Transfer-Encoding: chunked\r\n") != string::npos) *chunked = 1;
    else *chunked = 0;

    //close socket
    if (close(sock) < 0) return ERRCLOSESOCKET;

    return NOERROR;
}

//connect to host via newly created socket
int createSocketAndConnect(TUrl data, int *socket_pointer)
{
    struct sockaddr_in sin;
    struct hostent *host;

    //new socket
    *socket_pointer = socket(PF_INET, SOCK_STREAM, 0 );
    if (*socket_pointer >= 0){
        sin.sin_family = PF_INET;
        sin.sin_port = htons(data.port);

        //get host by name request
        host = gethostbyname(data.domain.c_str());
        if (host != NULL){
            memcpy (&sin.sin_addr, host->h_addr, host->h_length);

            //connect to host
            if (connect (*socket_pointer, (struct sockaddr *)&sin, sizeof(sin) ) < 0 ) return ERRCONNECT;

            return NOERROR;
        }
        else return ERRGETHOST;
    }
    else return ERRCREATESOCKET;
}

//parse input URL from argument
int parseUrl (char *url, TUrl *data) {
    size_t index;
    size_t indexPort;
    string tmpUrl;

    tmpUrl = url;  //tmp variable for url
    index = tmpUrl.find("http://");

    //delete http:// (7 chars) tag from url
    if(index != string::npos) tmpUrl.replace(index, 7, "");
    else return ERRHTTP;

    index = tmpUrl.find('/');
    indexPort = tmpUrl.find(':');

    //get domain name and port
    if (index < indexPort) {
        //no port in URL, domain name ends with /
        data->domain = tmpUrl.substr(0, index);
        tmpUrl.replace(0, index, "");
    }
    else {
        //port in URL, domain name ends with :
        data->domain = tmpUrl.substr(0, indexPort);
        tmpUrl.replace(0, indexPort, "");

        //get port
        if((index = tmpUrl.find(':')) == 0){
            //only domain with no port
            if (tmpUrl.size() == 1) return ERRPORT1;

            //port is not number or missing
            if((isdigit(tmpUrl[index + 1])) == 0) return ERRPORT2;

            tmpUrl.replace(0, 1, ""); //remove :
            unsigned int port = 0;
            while (isdigit(tmpUrl[index])) {
                port = port * 10 + (tmpUrl[index] - '0');
                if(port > 65535) return ERRPORT3;
                index++;
            }

            data->port = port;
            tmpUrl.replace(0, index, ""); //remove port
        }
    }

    //get path if there is one, otherwise leave the default one initialized in main()
    if (tmpUrl.length() > 0) {
        //replace whitespaces in URL
        while ((index = tmpUrl.find(" ")) != string::npos) tmpUrl.replace(index, 1, "%20");

        data->path = tmpUrl;
        //get file name if there is one, otherwise set it to the default index.html
        if(data->path.find("/") != string::npos) {
            index = data->path.rfind("/");
            //there is a file, get file name
            if (data->path.length() > 1) data->fileName = data->path.substr(index + 1);

            //'#' in name
            if ((index = data->fileName.find("#")) != string::npos) {
                data->fileName.erase(index);
                if (index == 0)  //if there was no file name, just fragment
                    data->fileName = "index.html";
            }

            //'?' in name
            if ((index = data->fileName.find("?")) != string::npos) {
                data->fileName.erase(index);
                if (index == 0)  //if there was no file name, just fragment
                    data->fileName = "index.html";
            }

            //return proper whitespaces
            while ((index = data->fileName.find("%20")) != string::npos)
                data->fileName.replace(index, 3, " ");
            }

        //delete '#' which could appear
        if((index = data->path.find('#')) != string::npos) data->path.erase(index);
    }

    return NOERROR;
}

//check correct program arguments
int checkParams(int argc, char **argv)
{
    //check help argument
    if (argc == 2 and (strcmp(argv[1], "-help") == 0 or strcmp(argv[1], "-h") == 0 or strcmp(argv[1], "--help") == 0 or strcmp(argv[1], "--h") == 0)) {
        printHelp();
        return 1;  //HELP
    }

    if (argc == 2) return 0;  //OK
    else {
        printError(ERRPARAMS);
        return 2;  //ERROR
    }
}

//print help message to standard output
void printHelp()
{
    string help;

    help = "Program implementuje stazeni zadaneho objektu pomoci URL z WWW serveru s vyuzitim protokolu HTTP do souboru ulozeneho v lokalnim souborovem systemu.\n";
    help.append("Program predpoklada jeden povinny parametr a to URL identifikujici objekt, ktery bude ulozen do aktualniho adresare.\n");
    help.append("Pokud v dotazu URL neni uvedeno jmeno souboru, obsah bude ulozen do souboru index.html.\n");

    cout<<help<<endl;
}

//print an error message for a given code
//error code is enum from "errorCodes" or corresponding number between 0 and 13
void printError(int code)
{
    switch (code){
        case NOERROR:
            cerr<<"Proces probehl uspesne.\n"<<endl;
            break;
        case ERRREDIRECTION:
            cerr<<"Error - vice nez 5 pokusu o presmerovani, posledni byl 301.\n"<<endl;
            break;
        case ERRREDIRECTION2:
            cerr<<"Error - vice nez 5 pokusu o presmerovani, posledni byl 302.\n"<<endl;
            break;
        case ERRERR:
            cerr<<"Error - Bohuzel nastala vyse zminena chyba.\n"<<endl;
            break;
        case ERRPARAMS:
            cerr<<"Error - nespravne parametry programu. Pouzijte '-help' pro napovedu.\n"<<endl;
            break;
        case ERRHTTP:
            cerr<<"Error - chybejici prefix 'http://' v zadane URL.\n"<<endl;
            break;
        case ERRHTTP10:
            cerr<<"Error - rozdilne verze klient/server.\n"<<endl;
            break;
        case ERRPORT1:
            cerr<<"Error - nekompletni PORT v URL.\n"<<endl;
            break;
        case ERRPORT2:
            cerr<<"Error - PORT v URL neni kladne cislo.\n"<<endl;
            break;
        case ERRPORT3:
            cerr<<"Error - neplatny PORT (mimo rozsah 0 - 65535).\n"<<endl;
            break;
        case ERRCREATESOCKET:
            cerr<<"Error - nepodarilo se vytvorit novy socket pro navazani spojeni.\n"<<endl;
            break;
        case ERRGETHOST:
            cerr<<"Error - nepodarilo se ziskat 'hostent' strukturu pozadavkem 'get host by name'.\n"<<endl;
            break;
        case ERRCONNECT:
            cerr<<"Error - nepodarilo se pripojit pres socket.\n"<<endl;
            break;
        case ERRSEND:
            cerr<<"Error - nepodarilo se odeslat/zapsat data do socketu.\n"<<endl;
            break;
        case ERRGETRESPONSE:
            cerr<<"Error - nepodarilo se precist data odpovedi ze socketu.\n"<<endl;
            break;
        case ERRCLOSESOCKET:
            cerr<<"Error - nepodarilo se uzavrit socket.\n"<<endl;
            break;
        case ERRFILEWRITE:
            cerr<<"Error - nepodarilo se zapsat data do souboru.\n"<<endl;
            break;
        default:
            cerr<<"Error\n"<<endl;
            break;
    }
}

void printConnectionErrorType(string connectionErrorCode)
{
    string outputMessage;

    outputMessage = "Chyba v komunikaci se serverem: ";
    outputMessage.append(connectionErrorCode);
    cerr<<outputMessage + "\n";
}