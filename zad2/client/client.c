#include <arpa/inet.h>
#include <netdb.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>

#include <stdint.h>
#include <string.h>
#include <memory.h>

// #include "linkedlist.h"
// -- LINKED LIST --

#define MAX_STR_LEN 50
#define MAX_ELEM_SIZE 60

typedef uint8_t byte;

typedef struct element {
    uint32_t id;
    uint16_t charlen;
    char *string;
} element;


typedef struct node {
    struct element elem;
    struct node* next;
} node;

void printElement(element e) {
    printf("id:%05d, len:%02d : %s\n", e.id, e.charlen, e.string);
}

void generateConsecutiveLetters(char* buffer, uint16_t charlen) {
    for (int i = 0; i < charlen; i++) {
        buffer[i] = (i % 26) + 'A';
    }
}

node* createNode(uint32_t id, uint16_t charlen) {
    node* nn = (node*)malloc(sizeof(node));
    nn->next = NULL;
    nn->elem.id = id;
    nn->elem.charlen = (charlen < MAX_STR_LEN) ? charlen : MAX_STR_LEN;
    nn->elem.string = (char*)malloc(charlen + 1);

    generateConsecutiveLetters(nn->elem.string, nn->elem.charlen);
    nn->elem.string[nn->elem.charlen] = '\0';
    
    return nn;
}

node* createList(size_t size, uint16_t min_charlen, uint16_t max_charlen) {
    node *head = createNode(0, min_charlen);
    node *trav = head;
    for (int i = 1; i < size; i++) {
        uint16_t charlen = min_charlen + rand() % (max_charlen - min_charlen) ;
        trav->next = createNode(i, charlen);
        trav = trav->next;
    }
    return head;
}

void deleteList(node* head) {
    node *trav = head;
    node *prev;
    while (trav) {
        prev = trav;
        trav = trav->next;
        free(prev->elem.string);
        free(prev);
    }
}

char* serializeList(node* head, size_t* size) {

    size_t bufferSizeStep = 4096;
    size_t bufferSize = bufferSizeStep;
    char* buffer = (char*)malloc(bufferSize);
    size_t offset = 0;

    for (node *trav = head; trav != NULL; trav = trav->next) {
        if (bufferSize < offset + MAX_ELEM_SIZE) {
            bufferSize += bufferSizeStep;
            buffer = realloc(buffer, bufferSize);
        }

        uint32_t net_id = htonl(trav->elem.id);
        memcpy(buffer + offset, &net_id, sizeof(uint32_t));
        offset += sizeof(uint32_t);

        uint16_t net_charlen = htons(trav->elem.charlen);
        memcpy(buffer + offset, &net_charlen, sizeof(uint16_t));
        offset += sizeof(uint16_t);
        
        memcpy(buffer + offset, trav->elem.string, trav->elem.charlen);
        offset += trav->elem.charlen;
    }

    *size = offset;

    return buffer;
}

// -- LINKED LIST -- (end)

#define SERVER_PORT 8000
#define SERVER_IP "127.0.0.1"


int main(int argc, char *argv[]) {

    printf("PSI zad 2, TCP client\n");

    size_t nodeCount = (int)1e5;
    uint16_t minCharLen = 5, maxCharLen = MAX_STR_LEN;

    node* head = createList(nodeCount, minCharLen, maxCharLen);

    // for (node *trav = head; trav != NULL; trav = trav->next) {
    //     printElement(trav->elem);
    // }

    size_t byteSize;
    char * serialized = serializeList(head, &byteSize);


    int sockfd;
    struct sockaddr_in server_addr;

    sockfd = socket(AF_INET, SOCK_STREAM, 0);

    if (sockfd == -1) {
        perror("socket creation failed");
        exit(EXIT_FAILURE);
    }


    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(SERVER_PORT);
    server_addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK); // #TODO: change to normal ip

    if (inet_pton(AF_INET, SERVER_IP, &server_addr.sin_addr) <= 0) {
        perror("Invalid address/ Address not supported");
        close(sockfd);
        exit(EXIT_FAILURE);
    }

    if (connect(sockfd, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("Connection to the server failed");
        close(sockfd);
        exit(EXIT_FAILURE);
    }
    printf("Connected to the server.\n");

    if (send(sockfd, serialized, byteSize, 0) < 0) {
        perror("Failed to send data");
    }
    printf("Succesfully sent %ld bytes of data\n", byteSize);
    printf("Sent list with %ld nodes", nodeCount);
    close(sockfd);

    free(serialized);
    deleteList(head);

    return 0;
}