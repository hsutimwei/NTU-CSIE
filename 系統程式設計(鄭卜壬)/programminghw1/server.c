#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <sys/socket.h>
#include <fcntl.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <sys/select.h>

#define ERR_EXIT(a) do { perror(a); exit(1); } while(0)
int savefd[300];
typedef struct 
{
    int first;
    int second;
} pair;
int curnum=0;
typedef struct {
    char hostname[512];  // server's hostname
    unsigned short port;  // port to listen
    int listen_fd;  // fd to wait for a new connection
} server;

typedef struct {
    char host[512];  // client's host
    int conn_fd;  // fd to talk with client
    char buf[512];  // data sent by/to client
    size_t buf_len;  // bytes used by buf
    int checklock;
    // you don't need to change this.
    int id;
    int wait_for_write;  // used by handle_read to know if the header is read or not.
} request;

server svr;  // server
request* requestP = NULL;  // point to a list of requests
int maxfd;  // size of open file descriptor table, size of request list

const char* accept_read_header = "ACCEPT_FROM_READ";
const char* accept_write_header = "ACCEPT_FROM_WRITE";

static void init_server(unsigned short port);
// initailize a server, exit for error

static void init_request(request* reqP);
// initailize a request instance

static void free_request(request* reqP);
// free resources used by a request instance

typedef struct {
    int id;          //902001-902020
    int AZ;          
    int BNT;         
    int Moderna;     
}registerRecord;

void del(int fd)
{   
    for(int i=0;i<300;i++)
      if(savefd[i]==fd)
      {  
         savefd[i]=-1;
         int j=i;
         //fprintf(stderr, "in dell j:%d\n",j);
         while(1)
         {  
           if(j==299)
           break;
           if(savefd[j]!=savefd[j+1] && savefd[j]==-1)
              {  // fprintf(stderr, "in del j:%d fdj:%d fdj+1:%d\n",j,savefd[j+1],savefd[j]);
                  savefd[j]=savefd[j+1];
                  savefd[j+1]=-1;
                  j=i;
                  curnum--;
              }
              j++;
           
         }
      }

}
int handle_read(request* reqP) {
    int r;
    char buf[512];
    
    // Read in request from client
    r = read(reqP->conn_fd, buf, sizeof(buf));
    if (r < 0) return -1;
    if (r == 0) return 0;
    char* p1 = strstr(buf, "\015\012");
    int newline_len = 2;
    if (p1 == NULL) {
       p1 = strstr(buf, "\012");
        if (p1 == NULL) {
            ERR_EXIT("this really should not happen...");
        }
    }
    size_t len = p1 - buf + 1;
    memmove(reqP->buf, buf, len);
    reqP->buf[len - 1] = '\0';
    reqP->buf_len = len-1;
    return 1;
}

int main(int argc, char** argv) {
    
    // Parse args.
    if (argc != 2) {
        fprintf(stderr, "usage: %s [port]\n", argv[0]);
        exit(1);
    }
    for(int i=0;i<300;i++)
    {
        savefd[i]=-1;
       /* checkfd[i].first=-1;
        checkfd[i].second=0;*/
    }
    struct sockaddr_in cliaddr;  // used by accept()
    int clilen;

    int conn_fd;  // fd for a new connection with client
    int file_fd;  // fd for file that we open for reading
    char buf[512];
    int buf_len;
    
    
    // Initialize server
    init_server((unsigned short) atoi(argv[1]));
    savefd[curnum]=svr.listen_fd;
    int ch=curnum,check=0;
    curnum++;
    //fprintf(stderr, "%d %dmmm\n",savefd[0],svr.listen_fd);
    /*for(int i=0;i<100;i++)
    {
        if(checkfd[i].first==savefd[ch])
        {
              checkfd[i].second=1;
              check=1;
              break;
        }
    }
    if(check==0)
       for(int i=0;i<100;i++)
       {
         if(checkfd[i].first==-1)
         {
              checkfd[i].first=savefd[ch];
              break;
         }
       }*/
    
    // Loop for handling connections
    fprintf(stderr, "\nstarting on %.80s, port %d, fd %d, maxconn %d...\n", svr.hostname, svr.port, svr.listen_fd, maxfd);
    int fdrr=open("registerRecord", O_RDWR | O_CREAT);
    while (1) {
        // TODO: Add IO multiplexing
       // fprintf(stderr," AA read_server\n");
        
        registerRecord  regir;
       // fprintf(stderr,"? AZ:%d BNT:%d Moderna:%d id:%d\n",regir.AZ,regir.BNT,regir.Moderna,regir.id);
        fprintf(stderr, "AA\n");
       /* for(int i=0;i<300;i++)
        if(savefd[i]!=-1)
        fprintf(stderr, "i:%d fd:%d\n",i,savefd[i]);*/
        
        fd_set fdset;
        FD_ZERO(&fdset);
        maxfd = getdtablesize();
        for(int i=0;i<300;i++)
        {   
            if(savefd[i]>=0)
            {
                 FD_SET(savefd[i],&fdset);
            }
        }
        for(int i=0;i<curnum;i++)
        {   
            if(savefd[i]>=0)
            {
                 if(requestP[savefd[i]].checklock==1)
                 {
                int k=requestP[conn_fd].id%100;
                 
                 
                 lseek(fdrr,sizeof( registerRecord)*(k-1),SEEK_SET);
                 fprintf(stderr,"prepare to write requestP[%d].checklock: %d\n",conn_fd,requestP[conn_fd].checklock);
                 struct flock fl;
                 fl.l_type=F_WRLCK;//設參數
                 fl.l_whence=SEEK_CUR;
                 fl.l_start=0;
                 fl.l_len=sizeof( registerRecord);
                 int g;
                 fprintf(stderr,"%d gota\n",g);
                 g=fcntl(fdrr,F_SETLK,&fl);
                 fprintf(stderr,"%d gotb\n",g);
                 }
            }
        }
        struct timeval tv;
        tv.tv_sec=1;
        tv.tv_usec=0;
        
          
        if(select(maxfd,&fdset,NULL,NULL,&tv))
        {   //for確認fd_set中那些可以，然後一個一個accpet
            //如果是要執行的是新的svrfd，就用助教的code然後
            // Check new connection
          //  fprintf(stderr,"%da",maxfd);
             fprintf(stderr, "%d %dpphs\n",savefd[0],svr.listen_fd);
            int check=0;
           for(int i=0;i<300;i++)
           {  
               //fprintf(stderr," else88 read_server\n");  
                if(savefd[i]!=-1)
             if((FD_ISSET(savefd[i],&fdset)))
            {  
            /* for(int j=0;j<300;j++)
             {
               if(checkfd[j].first==savefd[i] &&checkfd[j].second==1)
                {
                 check=1;
                 break;
                }
             }*/
        for(int i=0;i<300;i++)
        if(savefd[i]!=-1)
        fprintf(stderr, "isset i:%d fd:%d\n",i,savefd[i]);
              fprintf(stderr, "i:%d %d %dppp\n",i,savefd[i],svr.listen_fd);
           if(savefd[i]==svr.listen_fd)
           {
             clilen = sizeof(cliaddr);
             conn_fd = accept(svr.listen_fd, (struct sockaddr*)&cliaddr, (socklen_t*)&clilen);
             savefd[curnum]=conn_fd;//存連線中的clinet
             curnum++;
             if (conn_fd < 0) {
                 if (errno == EINTR || errno == EAGAIN) continue;  // try again
                 if (errno == ENFILE) {
                     (void) fprintf(stderr, "out of file descriptor table ... (maxconn %d)\n", maxfd);
                     continue;
                 }
                 ERR_EXIT("accept");
             }
             requestP[conn_fd].conn_fd = conn_fd;
             strcpy(requestP[conn_fd].host, inet_ntoa(cliaddr.sin_addr));
             fprintf(stderr, "getting a new request... fd %d from %s\n", conn_fd, requestP[conn_fd].host);
             sprintf(buf, "Please enter your id (to check your preference order):\n");
             write(conn_fd,buf,strlen(buf));
             
            /* fprintf(stderr, "ret = %d\n", ret);
    	     if (ret < 0) {
                fprintf(stderr, "bad request from %s\n", requestP[conn_fd].host);
                continue;
             }*/
             requestP[conn_fd].wait_for_write=1;
             continue;
             
           }
           
            fprintf(stderr," check %lu\n",sizeof( registerRecord));
              conn_fd=savefd[i];
             // parse data from client to requestP[conn_fd].buf
             int  ret = handle_read(&requestP[conn_fd]);
            
           
             fprintf(stderr," %d\n",ret);
             fprintf(stderr," %s\n",requestP[conn_fd].buf);
           /*  if (ret < 0) {
                fprintf(stderr, "bad request from %s\n", requestP[conn_fd].host);
                continue;
             }*/
            
            
              
                 
        

        
        
    // TODO: handle requests from clients
#ifdef READ_SERVER      
        
        fprintf(stderr," %lu\n",sizeof( registerRecord));
        int cnt=0;
        int checklock=0;
        if(strlen(requestP[conn_fd].buf)==6)
        {   
            
            if(requestP[conn_fd].buf[0]=='9' && requestP[conn_fd].buf[1]=='0' && requestP[conn_fd].buf[2]=='2' && requestP[conn_fd].buf[3]=='0' )
            {    
                 //int fdrr=open("registerRecord", O_RDONLY | O_CREAT);
                 
                 int k=-1;
                 for(int i=1;i<=20;i++)
                 {
                   if(i==((int)requestP[conn_fd].buf[4]-'0')*10+(int)requestP[conn_fd].buf[5]-'0')
                   {
                       k=i;
                       break;
                   }
                      
                 }
                 if(k==-1)
                 goto failr;
                 fprintf(stderr,"%d b\n",k);
                 lseek(fdrr,sizeof( registerRecord)*(k-1),SEEK_SET);
                 struct flock fl;
                 fl.l_type=F_WRLCK;//設參數
                 fl.l_whence=SEEK_CUR;
                 fl.l_start=0;
                 fl.l_len=sizeof( registerRecord);
                 int g;               
                 g=fcntl(fdrr,F_GETLK,&fl);
                 
                 if(fl.l_type==F_WRLCK)
                 {
                     requestP[conn_fd].checklock=0;
                     fprintf(stderr,"%d gotc\n",g);
                 }
                  
                 else
                 {
                      requestP[conn_fd].checklock=1;
                      fprintf(stderr,"%d gotd\n",g);
                 }
                  
                 if(read(fdrr,&regir, sizeof( registerRecord)) && requestP[conn_fd].checklock==1)
                    {   fprintf(stderr,"%da\n",regir.id);
                        
                        
                           
                            if(regir.AZ==1 && regir.Moderna==2 && regir.BNT==3 )
                            {
                                sprintf(buf, "Your preference order is AZ > Moderna > BNT.\n");
                                
                            }
                            if(regir.AZ==1 && regir.Moderna==3 && regir.BNT==2 )
                            {
                                sprintf(buf, "Your preference order is AZ > BNT > Moderna.\n");
                                
                            }
                            if(regir.AZ==2 && regir.Moderna==1 && regir.BNT==3 )
                            {
                                sprintf(buf, "Your preference order is Moderna > AZ > BNT.\n");
                                
                            }
                            if(regir.AZ==2 && regir.Moderna==3 && regir.BNT==1 )
                            {
                                sprintf(buf, "Your preference order is BNT > AZ > Moderna.\n");
                                
                            }
                            if(regir.AZ==3 && regir.Moderna==1 && regir.BNT==2 )
                            {
                                sprintf(buf, "Your preference order is Moderna > BNT > AZ.\n");
                               
                            }
                            if(regir.AZ==3 && regir.Moderna==2 && regir.BNT==1 )
                            {
                                sprintf(buf, "Your preference order is BNT > Moderna > AZ.\n");
                                
                            }
                                
                            cnt++;
                            
                        
                    }
                    else
                    {
                         sprintf(buf, "Locked.\n");
                         cnt++;
                    }
            }
            
            if(!cnt)
                {     
                    sprintf(buf, "[Error] Operation failed. Please try again.\n");
                    fprintf(stderr," else2 read_server %d\n", cnt);
                }          
        }
        else
        {     failr:
             fprintf(stderr," else read_server\n");
            sprintf(buf, "[Error] Operation failed. Please try again.\n");
        }
        write(conn_fd,buf,strlen(buf));
        close(conn_fd);
         fprintf(stderr," che3ck %lu\n",sizeof( registerRecord));
         
        del(conn_fd);
        
        free_request(requestP);//從clino清除conn_fd
       // fprintf(stderr, "%s", requestP[conn_fd].buf);
        //sprintf(buf,"%s : %s",accept_read_header,requestP[conn_fd].buf);
       // write(requestP[conn_fd].conn_fd, buf, strlen(buf));    
       fprintf(stderr," che2ck %lu\n",sizeof( registerRecord));

#elif defined WRITE_SERVER
        
        fprintf(stderr,"%lu kk %sc\n",strlen(requestP[conn_fd].buf),requestP[conn_fd].buf);
        int cnt=0;
        int checklock=0;
         fprintf(stderr,"%dc\n",requestP[conn_fd].wait_for_write);
        if(requestP[conn_fd].wait_for_write==1)
        if(strlen(requestP[conn_fd].buf)==6)
        {   
            if(requestP[conn_fd].buf[0]=='9' && requestP[conn_fd].buf[1]=='0' && requestP[conn_fd].buf[2]=='2' && requestP[conn_fd].buf[3]=='0' )
            {    
                 
                 
                 int k=-1;
                 for(int i=1;i<=20;i++)
                 {
                   if(i==((int)requestP[conn_fd].buf[4]-'0')*10+(int)requestP[conn_fd].buf[5]-'0')
                   {
                       k=i;
                       requestP[conn_fd].id=902000+i;
                       break;
                   }
                      
                 }
                 if(k==-1)
                   goto fail;        
                
                 fprintf(stderr,"%d b\n",k);
                 
                 lseek(fdrr,sizeof( registerRecord)*(k-1),SEEK_SET);
                 struct flock fl;
                 fl.l_type=F_WRLCK;//設參數
                 fl.l_whence=SEEK_CUR;
                 fl.l_start=0;
                 fl.l_len=sizeof( registerRecord);
                 int g;
                 fprintf(stderr,"%d gota\n",g);
                 g=fcntl(fdrr,F_SETLK,&fl);
                 fprintf(stderr,"%d gotb\n",g);
                 if(g==0)
                  requestP[conn_fd].checklock=1;
                 else
                   requestP[conn_fd].checklock=0;
                fprintf(stderr,"requestP[%d].checklock: %d\n",conn_fd,requestP[conn_fd].checklock);
                 if(read(fdrr,&regir, sizeof( registerRecord)) && requestP[conn_fd].checklock==1)
                    {   fprintf(stderr,"%da\n",regir.id);
                        checklock++;
                        fprintf(stderr,"%d %d %dg\n",regir.AZ,regir.Moderna, regir.BNT);
                           
                            if(regir.AZ==1 && regir.Moderna==2 && regir.BNT==3 )
                            {
                                sprintf(buf, "Your preference order is AZ > Moderna > BNT.\nPlease input your preference order respectively(AZ,BNT,Moderna):\n");
                                
                            }
                            if(regir.AZ==1 && regir.Moderna==3 && regir.BNT==2 )
                            {
                                sprintf(buf, "Your preference order is AZ > BNT > Moderna.\nPlease input your preference order respectively(AZ,BNT,Moderna):\n");
                                
                            }
                            if(regir.AZ==2 && regir.Moderna==1 && regir.BNT==3 )
                            {
                                sprintf(buf, "Your preference order is Moderna > AZ > BNT.\nPlease input your preference order respectively(AZ,BNT,Moderna):\n");
                                
                            }
                            if(regir.AZ==2 && regir.Moderna==3 && regir.BNT==1 )
                            {
                                sprintf(buf, "Your preference order is BNT > AZ > Moderna.\nPlease input your preference order respectively(AZ,BNT,Moderna):\n");
                                
                            }
                            if(regir.AZ==3 && regir.Moderna==1 && regir.BNT==2 )
                            {
                                sprintf(buf, "Your preference order is Moderna > BNT > AZ.\nPlease input your preference order respectively(AZ,BNT,Moderna):\n");
                               
                            }
                            if(regir.AZ==3 && regir.Moderna==2 && regir.BNT==1 )
                            {
                                sprintf(buf, "Your preference order is BNT > Moderna > AZ.\nPlease input your preference order respectively(AZ,BNT,Moderna):\n");
                                
                            }
                                
                            cnt++;
                            
                        
                    }
                    else
                    {
                         sprintf(buf, "Locked.\n");
                         cnt++;
                    }
            }
            fail:
            if(cnt==0)
                {     
                    sprintf(buf, "[Error] Operation failed. Please try again.\n");
                    fprintf(stderr," else2 read_server %d\n", cnt);
                }          
                
        }
        else
        {   fprintf(stderr," else read_server\n");
            sprintf(buf, "[Error] Operation failed. Please try again.\n");
        }
       
        if(requestP[conn_fd].wait_for_write==0 && strlen(requestP[conn_fd].buf)>=5)
        {               
                
                 fprintf(stderr,"Got in \n" );
                 
                 
                 int k=requestP[conn_fd].id%100;
                 
                 
                 lseek(fdrr,sizeof( registerRecord)*(k-1),SEEK_SET);
                 fprintf(stderr,"prepare to write requestP[%d].checklock: %d\n",conn_fd,requestP[conn_fd].checklock);
                 struct flock fl;
                 fl.l_type=F_WRLCK;//設參數
                 fl.l_whence=SEEK_CUR;
                 fl.l_start=0;
                 fl.l_len=sizeof( registerRecord);
                 int g;
                 fprintf(stderr,"%d gota\n",g);
                 g=fcntl(fdrr,F_SETLK,&fl);
                 fprintf(stderr,"%d gotb\n",g);
                 if(g==0)
                 requestP[conn_fd].checklock=1;
                 if(read(fdrr,&regir, sizeof( registerRecord)) &&  requestP[conn_fd].checklock==1)
                    {      
                           
                            if(1<=(int)requestP[conn_fd].buf[0]-'0'<=3)
                            regir.AZ=(int)requestP[conn_fd].buf[0]-'0';
                            if(1<=(int)requestP[conn_fd].buf[2]-'0'<=3)
                            regir.BNT=(int)requestP[conn_fd].buf[2]-'0';
                            if(1<=(int)requestP[conn_fd].buf[4]-'0'<=3)
                            regir.Moderna=(int)requestP[conn_fd].buf[4]-'0';
                            if(regir.AZ==1 && regir.BNT==2 && regir.Moderna==3)
                            {    lseek(fdrr,-sizeof( registerRecord),SEEK_CUR);
                                 write(fdrr,&regir, sizeof( registerRecord));
                                 sprintf(buf, "Preference order for %d modified successed, new preference order is AZ > BNT > Moderna.\n",regir.id);
                                 cnt++;
                            }
                            else if(regir.AZ==1 && regir.BNT==3 && regir.Moderna==2)
                            {
                                 lseek(fdrr,-sizeof( registerRecord),SEEK_CUR);
                                 write(fdrr,&regir, sizeof( registerRecord));
                                 sprintf(buf, "Preference order for %d modified successed, new preference order is AZ > Moderna > BNT.\n",regir.id);
                                 cnt++;
                            }
                            else if(regir.AZ==2 && regir.BNT==1 && regir.Moderna==3)
                            {
                                 lseek(fdrr,-sizeof( registerRecord),SEEK_CUR);
                                 write(fdrr,&regir, sizeof( registerRecord));
                                 sprintf(buf, "Preference order for %d modified successed, new preference order is BNT > AZ > Moderna.\n",regir.id);
                                 cnt++;
                            }
                            else if(regir.AZ==2 && regir.BNT==3 && regir.Moderna==1)
                            {
                                 lseek(fdrr,-sizeof(registerRecord),SEEK_CUR);
                                 write(fdrr,&regir, sizeof( registerRecord));
                                 sprintf(buf, "Preference order for %d modified successed, new preference order is Moderna > AZ > BNT.\n",regir.id);
                                 cnt++;
                            }
                            else if(regir.AZ==3 && regir.BNT==2 && regir.Moderna==1)
                            {
                                 lseek(fdrr,-sizeof( registerRecord),SEEK_CUR);
                                 write(fdrr,&regir, sizeof( registerRecord));
                                 sprintf(buf, "Preference order for %d modified successed, new preference order is Moderna > BNT > AZ.\n",regir.id);
                                 cnt++;
                            }
                            else if(regir.AZ==3 && regir.BNT==1 && regir.Moderna==2)
                            {
                                 lseek(fdrr,-sizeof( registerRecord),SEEK_CUR);
                                 write(fdrr,&regir, sizeof( registerRecord));
                                 sprintf(buf, "Preference order for %d modified successed, new preference order is BNT > Moderna > AZ.\n",regir.id);
                                 cnt++;
                            }
                            else 
                            sprintf(buf, "[Error] Operation failed. Please try again.\n");
                    }
                    if( requestP[conn_fd].checklock==0)
                          sprintf(buf, "Locked.\n");
                    else if(cnt==0)
                          sprintf(buf, "[Error] Operation failed. Please try again.\n");
                    
        }
        
        write(conn_fd,buf,strlen(buf));
        if(requestP[conn_fd].wait_for_write==1)
        requestP[conn_fd].wait_for_write=0;
        if(buf[0]=='[' || buf[0]=='L' || requestP[conn_fd].wait_for_write==1 || buf[0]=='P')
        {
            close(conn_fd);
            del(conn_fd);
            free_request(requestP);
        }
      
        fprintf(stderr," else444 read_server\n");
        //從clino清除conn_fd
       // fprintf(stderr, "%s", requestP[conn_fd].buf);
        //sprintf(buf,"%s : %s",accept_write_header,requestP[conn_fd].buf);
       // write(requestP[conn_fd].conn_fd, buf, strlen(buf));    
        #endif
            }

        }
            
            
        }
        

      
    }
    free(requestP);
    return 0;
}

// ======================================================================================================
// You don't need to know how the following codes are working
#include <fcntl.h>

static void init_request(request* reqP) {
    reqP->conn_fd = -1;
    reqP->buf_len = 0;
    reqP->id = 0;
}

static void free_request(request* reqP) {
    /*if (reqP->filename != NULL) {
        free(reqP->filename);
        reqP->filename = NULL;
    }*/
    init_request(reqP);
}

static void init_server(unsigned short port) {
    struct sockaddr_in servaddr;
    int tmp;

    gethostname(svr.hostname, sizeof(svr.hostname));
    svr.port = port;

    svr.listen_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (svr.listen_fd < 0) ERR_EXIT("socket");

    bzero(&servaddr, sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = htonl(INADDR_ANY);
    servaddr.sin_port = htons(port);
    tmp = 1;
    if (setsockopt(svr.listen_fd, SOL_SOCKET, SO_REUSEADDR, (void*)&tmp, sizeof(tmp)) < 0) {
        ERR_EXIT("setsockopt");
    }
    if (bind(svr.listen_fd, (struct sockaddr*)&servaddr, sizeof(servaddr)) < 0) {
        ERR_EXIT("bind");
    }
    if (listen(svr.listen_fd, 1024) < 0) {
        ERR_EXIT("listen");
    }

    // Get file descripter table size and initialize request table
    maxfd = getdtablesize();
    requestP = (request*) malloc(sizeof(request) * maxfd);
    if (requestP == NULL) {
        ERR_EXIT("out of memory allocating all requests");
    }
    for (int i = 0; i < maxfd; i++) {
        init_request(&requestP[i]);
    }
    requestP[svr.listen_fd].conn_fd = svr.listen_fd;
    strcpy(requestP[svr.listen_fd].host, svr.hostname);

    return;
}
