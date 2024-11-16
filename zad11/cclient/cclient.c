#include <netdb.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>

#define RESPONSE_SIZE 1024
#define DATA_GRAM_NUMBER 1      // ile razy potwórzyć wysłanie pakietu o danym rozmiarze
const int DATA_GRAM_SIZES[] = {100, 200, 500, 1000, 2000, 65507, 65508}; // rozmiary pakietów

struct arguments {
    struct hostent *host_address;
    u_int16_t port;
};

typedef struct arguments Arguments;

void generate_data(char *buffer, size_t size) {
    size_t n;
    // zakodowanie rozmiaru pakietu na dwóch pierwszych bajtach datagramu
    buffer[0] = (size >> 8) & 0xFF;
    buffer[1] = size & 0xFF;

    // zapełnienie pozostałej części datagramu literami A - Z
    for (n = 2; n < size; ++n) {
        int shift = (n - 2) % 26;
        buffer[n] = 'A' + shift;
    }
}

void parse_arguments(int argc, char *argv[], Arguments *arguments) {
    char *host;
    u_int16_t port;

    // parsowanie argumentów adres hosta i port (jeśli zostały podane)
    if (argc < 3) {
        host = "localhost";
        port = htons(8000);
    } else {
        host = argv[1];
        if (port = atoi(argv[2]))
            port = htons(port);
        else {
            perror("Error, not able to parse provided arguments.");
            exit(1);
        }
    }

    struct hostent *host_info;
    host_info = gethostbyname(host);

    if (host_info == (struct hostent *)0) {
        fprintf(stderr, "%s: unknown host\n", host);
        exit(2);
    }

    printf("Will send to %s:%d\n", host, ntohs(port));

    arguments->host_address = host_info;
    arguments->port = port;
}

void print_response(char *response, size_t size){
    size_t n;
    printf("Server response: ");
    for (n = 0; n < size; ++n) {
        if (isprint(response[n]))
            printf("%c", response[n]);
        else
            printf(".");
    }
    printf("\n");
}

int main(int argc, char *argv[]) {
    int sock;
    struct sockaddr_in name;
    Arguments arguments;
    u_int8_t i, j;

    printf("C client for zadanie 1.1\n");
    parse_arguments(argc, argv, &arguments);

    memcpy((char *)&name.sin_addr, (char *)arguments.host_address->h_addr, arguments.host_address->h_length);

    name.sin_family = AF_INET;
    name.sin_port = arguments.port;

    sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock == -1) {
        perror("opening datagram socket");
        exit(1);
    }

    if (connect(sock, (struct sockaddr *)&name, sizeof(name)) < 0) {
        perror("Connect");
        exit(3);
    }
    size_t nr_datagrams = sizeof(DATA_GRAM_SIZES) / sizeof(DATA_GRAM_SIZES[0]);
    for (i = 0; i < nr_datagrams; i++){
        char buffer[DATA_GRAM_SIZES[i] + 1];
        buffer[DATA_GRAM_SIZES[i]] = '\0';

        for (j = 0; j < DATA_GRAM_NUMBER; ++j) {
            generate_data(buffer, DATA_GRAM_SIZES[i]);
            printf("Sending datagram #%d, size: %d\n", j+1+ i*DATA_GRAM_NUMBER, DATA_GRAM_SIZES[i]);

            if (send(sock, buffer, DATA_GRAM_SIZES[i], 0) == -1) {
                perror("sending datagram message");
                exit(4);
            }
            char response[RESPONSE_SIZE];
            int bytes_received = recv(sock, response, RESPONSE_SIZE, 0);
            if (bytes_received < 0) {
                perror("Error while receiving response from server");
            } else {
                print_response(response, bytes_received);
            }
        }
    }

    printf("Client finished.\n");
    fflush(stdout);

    close(sock);
    return 0;
}