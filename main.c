#include <stdlib.h>
#include <stdio.h>
#include <curl/curl.h>

#include "get.h"

// Make get request

int main(void) {


    CURL *curl;
    CURLcode code;

    //

    curl = curl_easy_init();

    if (curl) {

        curl_easy_setopt(curl, CURLOPT_URL, "http://google.com");
        curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1);

        code = curl_easy_perform(curl);

    }
    return 0;
}
