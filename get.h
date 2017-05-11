#ifndef GET_H
#define GET_H

#include <stdlib.h>
#include <curl/curl.h>

typedef struct curl_get {
    CURL *_handle;

} get, *p_get;

typedef struct curl_response {
    CURLcode code;
    unsigned char *buffer;

} response, *p_response;


p_get get_init();
void get_free(p_get instance);

p_response response_init();
void response_free(p_response instance);


#endif
