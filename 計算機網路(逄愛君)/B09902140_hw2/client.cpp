#include<sys/socket.h> 
#include<arpa/inet.h>
#include<sys/ioctl.h>
#include<net/if.h>
#include<unistd.h>
#include<string.h>
#include<stdio.h>
#include <dirent.h>
#include<stdlib.h>
#include <sys/stat.h>
#include "opencv2/opencv.hpp"
#define BUFF_SIZE 1024
#define PORT 8989
#define ERR_EXIT(a){ perror(a); exit(1); }
using namespace cv;
using namespace std;
int main(int argc , char *argv[]){
    int sockfd, read_byte;
    struct sockaddr_in addr;
    char buffer[2*BUFF_SIZE] = {};
    char input[20*BUFF_SIZE] = {};
    char inputs[20*BUFF_SIZE] = {};
    // Get socket file descriptor
    if((sockfd = socket(AF_INET, SOCK_STREAM, 0)) < 0){
        ERR_EXIT("socket failed\n");
    }

    char* port=strchr(argv[2],':');
    port++;
    char* ip=strtok(argv[2],":");
    mkdir("client_dir",0777);
    
    // Set server address
    bzero(&addr,sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = inet_addr(ip);
    addr.sin_port = htons(atoi(port));

    // Connect to the server
    if(connect(sockfd, (struct sockaddr*)&addr, sizeof(addr)) < 0){
        ERR_EXIT("connect failed\n");
    }
    printf("User %s successfully logged in.\n",argv[1]);
    
    write(sockfd,argv[1],sizeof(argv[1]));
    while(1)
    {   
        printf("$ ");
        fflush(stdout);
        fgets(input,sizeof(input),stdin);
        if(strcmp(input,"\n")==0)
            strcpy(input,"hello");
        sprintf(inputs,"%s ",argv[1]);
        strcat(inputs,input);
        //send(sockfd,inputs,sizeof(inputs),0);
        char *pch=strtok(input," \n");
        if(strcmp(pch,"put")==0)//策略:先傳size，再傳指令
        {   
            bzero((buffer), sizeof(buffer));
            DIR *dir =opendir("./client_dir/");
            struct dirent *ptr;
            int flag = 0;
            pch=strtok(NULL, " \n");
            while((ptr = readdir(dir)) != NULL)
            {
                if(strcmp(pch, ptr->d_name) == 0)
                {
                    flag = 1;
                    break;
                }
            }
               
            bzero((buffer), sizeof(buffer));
            char buffer1[2048];
            if(flag==1)
            {
                sprintf(buffer1,"./client_dir/%s",pch);
                FILE *fp = fopen(buffer1, "r");
                fseek(fp, 0, SEEK_END);
                int size = ftell(fp);
                fseek(fp, 0, SEEK_SET);
                fclose(fp);
                sprintf(buffer," %d",size);
                strcat(inputs," true");
                strcat(inputs,buffer);//在input後面新增資料的size
            }
            else
                strcat(inputs," false");

            int size=strlen(inputs);
            sprintf(buffer,"%d",size);
            send(sockfd,buffer,sizeof(buffer),0);//傳指令的長度

            bzero(buffer,sizeof(buffer));
            recv(sockfd, buffer, sizeof(buffer), 0);//同步
            bzero((buffer), sizeof(buffer));

            strcat(buffer,inputs);
            send(sockfd,buffer,sizeof(buffer),0);//傳指令(put是一次傳過去)
            

            bzero(buffer,sizeof(buffer));
            recv(sockfd, buffer, sizeof(buffer), 0);//同步
            if(strcmp(buffer,"Permission denied.")==0)
            {
                cout << "Permission denied." << '\n';
                continue;
            }
            if(flag==1)
            {   
                printf("putting %s...\n",pch);
                FILE *fp = fopen(buffer1, "r");
                fseek(fp, 0, SEEK_END);
                int size = ftell(fp);
                fseek(fp, 0, SEEK_SET);
                while(size > 0)
                {   
                    
                    bzero((buffer), sizeof(buffer));
		            int byte = fread(buffer, sizeof(char), sizeof(buffer), fp);
                    if(byte < 0)
                    {
                        break;
                    }
		            byte = send(sockfd, buffer, byte, 0);
                    size -= byte;
                }
                bzero(buffer,sizeof(buffer));
                recv(sockfd, buffer, sizeof(buffer), 0);//同步
                bzero((buffer), sizeof(buffer));
                
                fclose(fp);
            }
            else
            {   
                printf("%s doesn’t exist.\n",pch);
            }
            
        }
        else if(strcmp(pch,"get")==0)
        {   
            int size = strlen(inputs);
            sprintf(buffer,"%d",size);
            send(sockfd,buffer,sizeof(buffer),0);//傳指令的長度

            bzero(buffer,sizeof(buffer));
            recv(sockfd, buffer, sizeof(buffer), 0);//同步
            bzero((buffer), sizeof(buffer));

            strcat(buffer,inputs);
            send(sockfd,buffer,sizeof(buffer),0);//傳指令(一次傳過去)
            //printf("%s\n",buffer);
            bzero(buffer, sizeof(buffer));
            recv(sockfd,buffer,sizeof(buffer),0);//得到是Yes size 或是NO或是Permission denied.
            if(strcmp(buffer,"Permission denied.")==0)
            {
                cout << "Permission denied." << '\n';
                continue;
            }
            pch=strtok(NULL, " \n");
            char *ppch=strtok(buffer," \n");

            if(strcmp(ppch,"Yes")==0)
            {   
                printf("getting %s...\n",pch);
                send(sockfd,"hello", sizeof("hello"), 0);//同步
                ppch=strtok(NULL," \n");
                int size=atoi(ppch);
                sprintf(buffer,"./client_dir/%s",pch);
                FILE *fp = fopen(buffer, "w");
                while(size > 0)
                {   
                    bzero(buffer,sizeof(buffer));
                    int byte = recv(sockfd, buffer, sizeof(buffer), 0);
                    //printf("%d %ld aa\n",byte,strlen(buffer));
		            byte = fwrite(buffer, sizeof(char), byte, fp);
                    if(byte < 0)
                    {
                        break;
                    }
		            
                    size -= byte;
                }
                bzero(buffer,sizeof(buffer));
                fclose(fp);
                //printf("get finish\n");
            }
            else if(strcmp(ppch,"No")==0)
            {
                printf("%s doesn’t exist.\n",pch);
            }
            
        }
        else if(strcmp(pch,"play")==0)
        {   
            pch=strtok(NULL," \n");
            int size = strlen(inputs);
            sprintf(buffer,"%d",size);
            send(sockfd,buffer,sizeof(buffer),0);//傳指令的長度

            bzero(buffer,sizeof(buffer));
            recv(sockfd, buffer, sizeof(buffer), 0);//同步
            bzero((buffer), sizeof(buffer));

            strcat(buffer,inputs);
            send(sockfd,buffer,sizeof(buffer),0);//傳指令(一次傳過去)
            //printf("%s\n",buffer);
            bzero(buffer, sizeof(buffer));
            recv(sockfd,buffer,sizeof(buffer),0);//得到是Yes size 或是NO或是Permission denied. 
            if(strcmp(buffer,"Permission denied.")==0)
            {
                cout << "Permission denied." << '\n';
                continue;
            }
            char *ppch=strtok(buffer," \n");
            
            if(strcmp(ppch,"Yes")==0)
            {   
                printf("playing the video…\n");
                send(sockfd,"hello",sizeof("hello"),0);//同步
                int imgsize;
                bzero(buffer, sizeof(buffer));
                recv(sockfd,buffer,sizeof(buffer),0);//得到寬度
                int width=atoi(buffer);

                send(sockfd,"hello",sizeof("hello"),0);//同步
                
                bzero(buffer, sizeof(buffer));
                recv(sockfd,buffer,sizeof(buffer),0);//得到高度
                int height=atoi(buffer);

                send(sockfd,"hello",sizeof("hello"),0);//同步

                Mat client_img;
                client_img = Mat::zeros(height, width, CV_8UC3);
                if(!client_img.isContinuous())
                {
                    client_img = client_img.clone();
                }

                while(1)
                {   
                    bzero(buffer,sizeof(buffer));
                    recv(sockfd, buffer, sizeof(buffer), 0);//得到image大小
                    send(sockfd, "hello", sizeof("hello"), 0);//同步，分開size跟影片
                    imgsize=atoi(buffer);
                    char large[imgsize]={};
                    size=imgsize;
                    if(imgsize==0)
                        break;
                    int byte=0,i=0;
                    while(imgsize > 0)
                    {       
                        //bzero(buffer,sizeof(buffer));
                        int byte = recv(sockfd, large+i, sizeof(large)-i, 0);
                        //printf("%d %ld aa\n",byte,strlen(buffer));
                        imgsize -= byte;
                        i+=byte;
                        //cout << imgsize << '\n';
                    }
                    uchar *iptr = client_img.data;              
                    memcpy(iptr, large, size);
                    imshow("Video", client_img);
                    char c = (char)waitKey(10);

                    bzero(buffer,sizeof(buffer));
                    sprintf(buffer,"%d",c);
                    send(sockfd,buffer, sizeof(buffer), 0);//確認frame傳完，傳waitkey
                    bzero(buffer,sizeof(buffer));
                    recv(sockfd, buffer,sizeof(buffer), 0);//總之同步一下
                    if(c==27)
                            break;
                }
                destroyAllWindows();
            }
            else if(strcmp(ppch,"Noo")==0)
            {
                printf("%s is not an mpg file.\n",pch);
            }
            else if(strcmp(ppch,"No")==0)
            {
                printf("%s doesn’t exist.\n",pch);
            }
        }
        else if(strcmp(pch,"ls")==0 || strcmp(pch,"blocklist")==0)
        {   
            
            int size = strlen(inputs);
            sprintf(buffer,"%d",size);
            
            send(sockfd,buffer,sizeof(buffer),0);//傳指令的長度

            bzero(buffer,sizeof(buffer));
            recv(sockfd, buffer, sizeof(buffer), 0);//同步
            bzero((buffer), sizeof(buffer));

            strcat(buffer,inputs);
            send(sockfd,buffer,sizeof(buffer),0);//傳指令(一次傳過去)

            bzero(buffer, sizeof(buffer));
            recv(sockfd,buffer,sizeof(buffer),0);//得到接下來要接受的指令長度size或是Permission denied.
            if(strcmp(buffer,"Permission denied.")==0)
            {
                cout << "Permission denied." << '\n';
                continue;
            }

            if(strcmp(buffer,"Permission denied.")==0)
            {
                printf("Permission denied.");
                continue;
            }
            send(sockfd,"hello",sizeof("hello"),0);//同步
            size=atoi(buffer);
            int j=0;
            char large1[200000]={};
            while(size>0)
            {
                int byte=recv(sockfd,large1+j,2048,0);
                size-=byte;
                j+=byte;
            }
            if(strlen(large1)>0)
                printf("%s",large1);
        
        }
        else if(strcmp(pch,"ban")==0 || strcmp(pch,"unban")==0)//注意ban跟unban的超長指令
        {   
            int size=strlen(inputs);
            sprintf(buffer,"%d",size);
            send(sockfd,buffer,sizeof(buffer),0);//傳指令長度過去
            
            bzero(buffer,sizeof(buffer));
            recv(sockfd, buffer, sizeof(buffer), 0);//同步
            bzero((buffer), sizeof(buffer));
            
            int byte=0;
            while(size>0)
            {   
                strncpy(buffer,inputs,2048);
		        byte = send(sockfd,buffer, sizeof(buffer), 0);
                memcpy(inputs,inputs+byte,sizeof(inputs)-byte);
                size -= byte;
            }
            bzero(buffer,sizeof(buffer));
            recv(sockfd,buffer,sizeof(buffer),0);//得到結果的長度
            if(strcmp(buffer,"Permission denied.")==0)
            {
                printf("Permission denied.\n");
                continue;
            }
            size=atoi(buffer);
            int j=0;
            char large1[200000];
            bzero(large1,sizeof(large1));
            send(sockfd,"hello",sizeof("hello"),0);//同步
            while(size>0)
            {
                int byte=recv(sockfd,large1+j,2048,0);
                size-=byte;
                j+=byte;
            }
            if(strlen(large1)>0)
                printf("%s\n",large1);
        
        }
        else 
        {   
            sprintf(inputs,"%s hello",argv[1]);
            int size = strlen(inputs);
            sprintf(buffer,"%d",size);
            send(sockfd,buffer,sizeof(buffer),0);//傳指令的長度

            bzero(buffer,sizeof(buffer));
            recv(sockfd, buffer, sizeof(buffer), 0);//同步
            bzero((buffer), sizeof(buffer));
            strcat(buffer,inputs);
            send(sockfd,buffer,sizeof(buffer),0);//傳指令(一次傳過去)
            //printf("%s\n",buffer);
            bzero(buffer, sizeof(buffer));
            recv(sockfd,buffer,sizeof(buffer),0);//得到是Command not found.或是Permission denied.
            cout << buffer << '\n';
        }
    }
    
    close(sockfd);
    return 0;
}

