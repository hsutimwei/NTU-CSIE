#include <sys/socket.h>
#include <arpa/inet.h>
#include <sys/ioctl.h>
#include <net/if.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <zlib.h>
#include "opencv2/opencv.hpp"
#include <errno.h>
#define BUFF_SIZE 1024
#define PORT 8787
#define ERR_EXIT(a) \
    {               \
        perror(a);  \
        exit(1);    \
    }
using namespace std;
using namespace cv;
typedef struct
{
    int length;
    int seqNumber;
    int ackNumber;
    int fin;
    int syn;
    int ack;
    unsigned long checksum;
} HEADER;

typedef struct
{
    HEADER header;
    char data[1000];
} SEGMENT;

int main(int argc, char *argv[])
{
    int sockfd, read_byte, buffersize = 0;
    struct sockaddr_in addr, agent, tmp_addr;
    int agentPort;
    char agentIP[50];
    SEGMENT seg, recvseg[260];
    // Get socket file descriptor
    sockfd = socket(PF_INET, SOCK_DGRAM, 0);

    // Set own address
    bzero(&addr, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_port = htons(atoi(argv[1]));
    addr.sin_addr.s_addr = htonl(INADDR_ANY);
    memset(addr.sin_zero, '\0', sizeof(addr.sin_zero));

    /* Configure settings in agent struct */
    sscanf(argv[2], "%[^:]:%d", agentIP, &agentPort);
    agent.sin_family = AF_INET;
    agent.sin_port = htons(agentPort);
    agent.sin_addr.s_addr = inet_addr(agentIP);
    memset(agent.sin_zero, '\0', sizeof(agent.sin_zero));
    socklen_t agent_size = sizeof(agent);
    /* bind socket */
    bind(sockfd, (struct sockaddr *)&addr, sizeof(addr));

    int waitack = 1;

    int width, height, size=1000;

    int check = 0; // 不要第一個buffer
    Mat img;

    // Receive message from server
    char *large;
    bzero(&recvseg, sizeof(recvseg));
    int i = 0, j = 0; // j-->目前的影片的data位置
    while (1)
    {
        int imgSize = size;

        // Copy a frame to the buffer
        int byte;

        bzero(&recvseg[buffersize], sizeof(recvseg[buffersize]));
        bzero(&seg, sizeof(seg));

        byte = recvfrom(sockfd, &recvseg[buffersize], sizeof(recvseg[buffersize]), 0, (struct sockaddr *)&agent, &agent_size);
        if (byte <= 0)
            break;

        if (recvseg[buffersize].header.seqNumber != waitack)
        {
            if (recvseg[buffersize].header.fin == 0)
                printf("drop\tdata\t#%d\t(out of order)\n", recvseg[buffersize].header.seqNumber);
            else
                printf("drop\tfin\t\t(out of order)\n");
            seg.header.ack = 1;
            seg.header.ackNumber = waitack - 1;
            sendto(sockfd, &seg, sizeof(seg), 0, (struct sockaddr *)&agent, agent_size);
            printf("send\tack\t#%d\n", waitack - 1);
        }
        else if (recvseg[buffersize].header.checksum != crc32(0L, (const Bytef *)recvseg[buffersize].data, 1000))
        {   
            if (recvseg[buffersize].header.fin == 0)
                printf("drop\tdata\t#%d\t(corrupted)\n", recvseg[buffersize].header.seqNumber);
            else
                printf("drop\tfin\t\t(corrupted)\n");
            seg.header.ack = 1;
            seg.header.ackNumber = waitack - 1;
            sendto(sockfd, &seg, sizeof(seg), 0, (struct sockaddr *)&agent, agent_size);
            printf("send\tack\t#%d\n", waitack - 1);
        }
        else if (buffersize >= 256)
        {
            if (recvseg[buffersize].header.fin == 0)
                printf("drop\tdata\t#%d\t(buffer overflow)\n", recvseg[buffersize].header.seqNumber);
            else
                printf("drop\tfin\t\t(buffer overflow)\n");
            buffersize = 0;
            seg.header.ack = 1;
            seg.header.ackNumber = waitack - 1;
            sendto(sockfd, &seg, sizeof(seg), 0, (struct sockaddr *)&agent, agent_size);
            printf("send\tack\t#%d\n", waitack - 1);
            printf("flush\n");
            int k = 0; // 目前flush到第幾個buffer
            while (j < imgSize && k < 256)
            {

                if (check == 0)
                {   
                    char *pch = strtok(recvseg[0].data, " \n");
                    width = atoi(pch);
                    pch = strtok(NULL, " \n");
                    height = atoi(pch);
                    pch = strtok(NULL, " \n");
                    size = atoi(pch);
                    imgSize=size;
                    large=new char[imgSize];
                    img = Mat::zeros(height, width, CV_8UC3);
                    if (!img.isContinuous())
                    {
                        img = img.clone();
                    }
                    check++;
                    k++;
                    continue;
                }
                if (j + 900 < imgSize)
                    memcpy(large + j, recvseg[k].data, 900);
                else
                    memcpy(large + j, recvseg[k].data, imgSize - j);
                k++;
                j += 900;
                if (j >= imgSize)
                {

                    uchar *iptr = img.data;
                    memcpy(iptr, large, size);
                    // show the frame
                    imshow("Video", img);
                    char c = (char)waitKey(1000);
                    if (c == 27)
                        break;
                    j = 0;
                    bzero(large, sizeof(large));
                }
            }

            buffersize = 0;

            bzero(&recvseg, sizeof(recvseg));
        }
        else if (recvseg[buffersize].header.fin == 1)
        {
            printf("recv\tfin\n"); // 影片結束
            seg.header.ack = 1;
            seg.header.ackNumber = recvseg[0].header.seqNumber;
            seg.header.fin = 1;
            sendto(sockfd, &seg, sizeof(seg), 0, (struct sockaddr *)&agent, agent_size);
            printf("send\tfinack\n");
            printf("flush\n");
            int k = 0; // 目前flush到第幾個buffer
            while (j < imgSize && k < buffersize)
            {
                if (check == 0)
                {
                    char *pch = strtok(recvseg[0].data, " \n");
                    width = atoi(pch);
                    pch = strtok(NULL, " \n");
                    height = atoi(pch);
                    pch = strtok(NULL, " \n");
                    size = atoi(pch);
                    imgSize=size;
                    large=new char[imgSize];
                    img = Mat::zeros(height, width, CV_8UC3);
                    if (!img.isContinuous())
                    {
                        img = img.clone();
                    }
                    check++;
                    k++;
                    continue;
                }
                if (j + 900 < imgSize)
                    memcpy(large + j, recvseg[k].data, 900);
                else
                    memcpy(large + j, recvseg[k].data, imgSize - j);
                k++;
                j += 900;
                if (j >= imgSize)
                {
                    uchar *iptr = img.data;
                    memcpy(iptr, large, size);
                    // show the frame
                    imshow("Video", img);
                    char c = (char)waitKey(1000);
                    if (c == 27)
                        break;
                    j = 0;
                    break;
                }
            }
            break;
        }
        else
        {
            printf("recv\tdata\t#%d\n", recvseg[buffersize].header.seqNumber);
            waitack++;
            seg.header.ack = 1;
            seg.header.ackNumber = recvseg[buffersize].header.seqNumber;
            sendto(sockfd, &seg, sizeof(seg), 0, (struct sockaddr *)&agent, agent_size);
            printf("send\tack\t#%d\n", recvseg[buffersize].header.seqNumber);
            buffersize++;
        }

        // Here, we assume that the buffer is transmitted from the server to the client
        // Copy a frame from the buffer to the container of the client

        // Here, we assume that the buffer is transmitted from the server to the client
        // Copy a frame from the buffer to the container of the client
    }
    delete [] large;
    close(sockfd);
    return 0;
}
