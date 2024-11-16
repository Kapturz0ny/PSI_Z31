#include <arpa/inet.h>
#include <errno.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>

#define BUFSIZE 1 << 16

struct arguments {
    struct hostent *host_address;
    u_int16_t port;
};

typedef struct arguments Arguments;

int parse_argument(int argc, char *argv[]) {
    u_int16_t port;

    if (argc < 2) {
        port = htons(8000);
    } else {
        if (port=atoi(argv[1]))
            port=htons(port);
        else{
            perror("Error, not able to parse provided arguments.");
            exit(1);
        }
    }

    printf("Will listen on 0.0.0.0:%d\n", ntohs(port));
    fflush(stdout);

    return port;
}

size_t decode_message(char *buffer, size_t size){
    size_t decoded_size = ((unsigned char)buffer[0] << 8) | (unsigned char)buffer[1];
    printf("Datagram size: (%zu) ", decoded_size);

    // ODKOMENTOWAĆ ABY WYŚWIETLAĆ ZAWARTOŚĆ PRZYCHODZĄCYCH PAKIETÓW

    // size_t n;
    // printf("Content: ");
    // for (n = 2; n < size; ++n) {
    //     if (isprint(buffer[n]))
    //         printf("%c", buffer[n]);
    //     else
    //         printf(".");
    // }
    // printf("\n");
    return decoded_size;
}

int main(int argc, char *argv[]) {
    int sfd;
    struct sockaddr_in server_address;
    struct sockaddr_in client_address;
    char buffer[BUFSIZE + 1];
    socklen_t client_address_length = sizeof client_address;
    char *client_address_string;

    printf("C server for zadanie 1.1\n");
    if ((sfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
        perror("Error while opening datagram socket");
        exit(1);
    }

    server_address.sin_family = AF_INET;
    server_address.sin_addr.s_addr = INADDR_ANY;
    server_address.sin_port = parse_argument(argc, argv);

    if (bind(sfd, (struct sockaddr *)&server_address, sizeof(server_address)) == -1) {
        perror("binding datagram socket");
        exit(2);
    }

    while (1) {
            int bytes_read = recvfrom(sfd, buffer, BUFSIZE, 0, (struct sockaddr *)&client_address,
                                    &client_address_length);

            if (bytes_read < 0) {
                perror("Exception while receiving datagram packet");
            } else {
                size_t decoded_size = decode_message(buffer, bytes_read);
                client_address_string = inet_ntoa(client_address.sin_addr);
                if (client_address_string != 0) {
                    printf("Client address: %s:%d\n", client_address_string, ntohs(client_address.sin_port));
                }
                const char *response = NULL; // Stały wskaźnik na łańcuch znaków
                if (decoded_size == bytes_read) {
                    response = "CORRECT datagram\n";
                } else {
                    response = "INCORRECT datagram\n";
                }

                // Wysłanie odpowiedzi do klienta
                int bytes_sent = sendto(sfd, response, strlen(response), 0,
                                        (struct sockaddr *)&client_address, client_address_length);

                if (bytes_sent < 0) {
                    perror("Error while sending response to client");
                }
                fflush(stdout);
            }
    }

    close(sfd);
    return 0;
}