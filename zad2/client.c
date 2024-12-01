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

#define MAX_STR_LEN 50
#define MAX_ELEM_SIZE 60

typedef uint8_t byte;

typedef struct element {
    uint32_t id;
    uint16_t charlen;
    char *string;
} element;

void print_elem(element e) {
    printf("id:%05d, len:%02d : %s\n", e.id, e.charlen, e.string);
}

typedef struct node {
    struct element elem;
    struct node* next;
} node;

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

char* serializeList(node* head) {
    size_t bufferSizeStep = 4096;
    size_t bufferSize = bufferSizeStep;
    char* buffer = (char*)malloc(bufferSize);
    size_t offset = 0;
    for (node *trav = head; trav != NULL; trav = trav->next) {
        if (bufferSize < offset + MAX_ELEM_SIZE) {
            bufferSize += bufferSizeStep;
            buffer = realloc(buffer, bufferSize);
        }
        uint32_t id = htonl(trav->elem.id);
        uint16_t charlen = htons(trav->elem.charlen);
        char* where = buffer + offset;
        memcpy(buffer + offset, &id, sizeof(uint32_t));
        offset += sizeof(uint32_t);
        memcpy(buffer + offset, &charlen, sizeof(uint16_t));
        offset += sizeof(uint16_t);
        memcpy(buffer + offset, trav->elem.string, trav->elem.charlen);
        offset += trav->elem.charlen;

    }

    return buffer;
}



int main(int argc, char *argv[]) {

    node* head = createList((int)1e5, 5, MAX_STR_LEN);

    // for (node *trav = head; trav != NULL; trav = trav->next) {
    //     print_elem(trav->elem);
    // }

    char * serialized = serializeList(head);
    printf("%100s \n", serialized);

    free(serialized);
    deleteList(head);

    return 0;
}