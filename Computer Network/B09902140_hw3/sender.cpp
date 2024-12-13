#include<stdio.h>
#include<sys/socket.h>
#include<arpa/inet.h>
#include<sys/ioctl.h>
#include<net/if.h>
#include<unistd.h> 
#include<string.h>
#include<stdlib.h>
#include <iostream>
#include<math.h>
#include <zlib.h>
#include "opencv2/opencv.hpp"
#define BUFF_SIZE 1024
#define PORT 8787
#define ERR_EXIT(a){ perror(a); exit(1); }
using namespace cv;
using namespace std;
typedef struct {
	int length;//傳imgSize
	int seqNumber;
	int ackNumber;
	int fin;
	int syn;
	int ack;
    unsigned long checksum;
} HEADER;

typedef struct{
	HEADER header;
	char data[1000];
} SEGMENT;
/* 
1.ooh
2.flush的位置
*/

int main(int argc, char *argv[]){
    struct sockaddr_in addr, agent;
    char buffer[2 * BUFF_SIZE] = {};
    char agentIP[50];
    int agentPort,sockfd;

    // Get socket file descriptor
    sockfd = socket(PF_INET, SOCK_DGRAM, 0);

    // Set own address
    bzero(&addr,sizeof(addr));
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
    socklen_t agent_size=sizeof(agent);
    /* bind socket */
    struct timeval tv={1,0};

    setsockopt( sockfd, SOL_SOCKET, SO_RCVTIMEO, ( char * )&tv, sizeof(tv) );

    bind(sockfd,(struct sockaddr *)&addr,sizeof(addr));


    SEGMENT seg[1000],recvseg;


    VideoCapture cap(argv[3]);
    
    int width = cap.get(CAP_PROP_FRAME_WIDTH);
    int height = cap.get(CAP_PROP_FRAME_HEIGHT);
    
    //設定參數
    int winSize=1,threshold=16,cur=0,seqNumber=1;

    Mat img;
    
    img = Mat::zeros(height, width, CV_8UC3);
    if(!img.isContinuous())
    {
        img = img.clone();
    }
    
    cap >> img;
    int imgSize = img.total() * img.elemSize();

    
    memset(seg,0,sizeof(seg[0])*1000);

    sprintf(seg[0].data,"%d %d %d",width,height,imgSize);
    seg[0].header={1,seqNumber,0,0,0,0,crc32(0L, (const Bytef *)seg[0].data, 1000)};
    printf("send\tdata\t#%d\twinSize = %d\n",seg[0].header.seqNumber,winSize);
    seqNumber++;
    sendto(sockfd, &seg[0], sizeof(seg[0]), 0, (struct sockaddr *)&agent, agent_size);//送寬、高、幀大小過去

    while (1)
    {
        bzero(&recvseg,sizeof(recvseg));
        int byte=recvfrom(sockfd, &recvseg, sizeof(recvseg), 0, (struct sockaddr *)&agent, &agent_size);
        if(byte==-1)
        {   
            printf("time\tout,\t\tthreshold = %d\n",max(winSize/2,1));
            printf("resnd\tdata\t#%d\twinSize = %d\n",seg[cur].header.seqNumber,winSize);
            sendto(sockfd, &seg[0], sizeof(seg[0]), 0, (struct sockaddr *)&agent, agent_size);
            threshold=max(winSize/2,1);
        }
        else
        {
            printf("recv\tack\t#%d\n",recvseg.header.ackNumber);
            if(recvseg.header.ackNumber!=1)
            {
                continue;
            }
            else
            {
                break;
            }
                
        }
    }
    winSize=2;
    cur=0;
    memset(&seg[0],0,sizeof(seg[0]));
    int fincheck=0;
    while(1)
    {      
        if(imgSize==0)
            fincheck=1;
        
        char imgbuffer[imgSize];
        
        // Copy a frame to the buffer
        memcpy(imgbuffer, img.data, imgSize);
        int byte,j=0;
        while(j<imgSize || fincheck)//傳image
        {   
            if(seg[cur].header.length==0)
            {   
                if(fincheck)
                {
                    seg[cur].header={1,seqNumber,0,1,0,0,crc32(0L, (const Bytef *)seg[cur].data, 1000)};
                    printf("send\tfin\n");
                    
                }
                else
                {   
                    if(j+900<imgSize)
                        memcpy(seg[cur].data,imgbuffer+j,900);
                    else
                        memcpy(seg[cur].data,imgbuffer+j,imgSize-j);
                    seg[cur].header={1,seqNumber,0,0,0,0,crc32(0L, (const Bytef *)seg[cur].data, 1000)};//指定seg[cur]的值
                    printf("send\tdata\t#%d\twinSize = %d\n",seg[cur].header.seqNumber,winSize);
                    j+=900;
                    
                }
                sendto(sockfd, &seg[cur], sizeof(seg[cur]), 0, (struct sockaddr *)&agent, agent_size);
                seqNumber++;
                
            }
            else
            {   
                seqNumber++;
                if(seg[cur].header.fin==1)
                    printf("resnd\tfin\n");
                else
                    printf("resnd\tdata\t#%d\twinSize = %d\n",seg[cur].header.seqNumber,winSize);
                byte = sendto(sockfd, &seg[cur], sizeof(seg[cur]), 0, (struct sockaddr *)&agent, agent_size);
            }
            
            cur++;

            if(cur==winSize || seg[cur-1].header.fin==1)
            {   
                int reack;
                //這裡的如果說win是246~272，winsize是27，則seqNumber是273，
                for(int i=seqNumber-cur;i<seqNumber;i++)
                {   
                    bzero(&recvseg,sizeof(recvseg));
                    byte=recvfrom(sockfd, &recvseg, sizeof(recvseg), 0, (struct sockaddr *)&agent, &agent_size);
                    if(byte==-1)
                    {   
                        printf("time\tout,\t\tthreshold = %d\n",max(winSize/2,1));
                        break;
                    }
                    else if(recvseg.header.fin==1)
                    {
                        printf("recv\tfinack\n");
                        fincheck=2;
                    }
                    else
                    {
                        printf("recv\tack\t#%d\n",recvseg.header.ackNumber);
                        
                        if(reack<=recvseg.header.ackNumber)//cumulative ack
                        {
                            reack=recvseg.header.ackNumber;
                        }
                        
                        if(reack<i)
                        {
                            i--;
                        }
                            
                    }
                    
                }
                                                                                                //272?-->X
                if(reack!=seqNumber-1)//如果回傳的不是272而是其他則有error，可能是255，所以要重送256~1000，在seg 0~1000中的第10~1000裡
                {                     //可能還沒resend完就又error   //seqNumber-reack-1如果是17
                    for(int i=0;i<1000-(reack+cur-seqNumber+1);i++)//把沒ack的packet送到seg前面
                    {
                        seg[i]=seg[i+reack+cur-seqNumber+1];
                    }
                    for(int i=1000-(reack+cur-seqNumber+1);i<1000;i++)//後面的bzero掉
                    {
                        bzero(&seg[i],sizeof(seg[i]));
                    }
                    seqNumber=seg[0].header.seqNumber;
                    cur=0;//cur是當下要送的第n個packet，歸零
                    threshold=max(winSize/2,1);
                    winSize=1;
                }
                else
                {   
                    for(int i=0;i<1000-cur;i++)//把沒ack的packet送到seg前面
                    {
                        seg[i]=seg[i+cur];
                    }
                    for(int i=1000-cur;i<1000;i++)
                    {
                        bzero(&seg[i],sizeof(seg[i]));
                    }
                    cur=0;
                    if(winSize<threshold)
                        winSize*=2;
                    else
                        winSize++;
                }

            }
            if(fincheck==2)
                break;
            
        }
        if(fincheck==2)
                break;
        cap >> img;
        imgSize = img.total() * img.elemSize();
        //imgSize=0;
        
        
    }
    

    cap.release();
	//destroyAllWindows();
    close(sockfd);
    return 0;
}