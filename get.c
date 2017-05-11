#include "get.h"

p_get get_init(){
    p_get instance = malloc(sizeof(p_get));

    if (!instance) {
        return NULL;
    }

    instance->_handle = curl_easy_init();
    if (!instance->_handle) {
        free(instance);
        return NULL;
    }

    return instance;
}

void get_free(p_get instance){
    curl_easy_cleanup(instance->_handle);

    free(instance);
    instance = NULL;
}

p_response response_init(){
    p_response re = malloc(sizeof(p_response));

    if (!re) {
        return NULL;
    }

    re->code = 0;
    re->buffer = NULL;

    return re;
}

void response_free(p_response instance){
    free(instance->buffer);
    instance->buffer = NULL;

    free(instance);
    instance = NULL;

}
