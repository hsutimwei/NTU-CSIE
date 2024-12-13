#include "kernel/param.h"
#include "kernel/types.h"
#include "kernel/stat.h"
#include "user/user.h"
#include "kernel/fs.h"
#include "kernel/fcntl.h"
#include "kernel/syscall.h"
#include "kernel/memlayout.h"
#include "kernel/riscv.h"
int check[10],num[2]={0};
char* fmtname(char *path)
{
  static char buf[DIRSIZ+1];
  char *p;
  
  // Find first character after last slash.
  for(p=path+strlen(path); p >= path && *p != '/'; p--)
    ;
  p++;
  
  // Return blank-padded name.
  if(strlen(p) >= DIRSIZ)
    return p;
  memset(buf, '\0', DIRSIZ);
  memmove(buf, p, strlen(p));
  //printf("the path is %s and the name is %s\n", path , buf);
  return buf;
}
void tree(char *path,int level)
{
  char buf[256], *p;
  int fd;
  struct dirent de;
  struct stat st;
  
  if((fd = open(path, 0)) < 0){
    fprintf(2, "%s [error opening dir]\n", path);
    return;
  }
 
  if(fstat(fd, &st) < 0){
    fprintf(2, "tree: cannot stat %s\n", path);
    close(fd);
    return;
  }
  if(level==1)
  printf("%s\n", path);
  char a1[]=".";
  char a2[]="..";
  switch(st.type){
    case T_FILE:
      num[1]++;
      //printf("path name is %s and file name is %s\n", path,fmtname(path));
      /*if(strcmp(fmtname(path),a1) && strcmp(fmtname(path),a2))
           printf("%s\n", fmtname(path));*/
      break;

    case T_DIR:
      
      if(strlen(path) + 1 + DIRSIZ + 1 > sizeof buf){
        printf("tree: path too long\n");
        break;
      }
    strcpy(buf, path);
    p = buf+strlen(buf);
    *p++ = '/';
    if(strcmp(fmtname(path),a1) && strcmp(fmtname(path),a2) && level!=1)
       num[0]++;
    if(read(fd, &de, sizeof(de)) == sizeof(de))
    check[level]=1;

    while(check[level]){
      if(de.inum == 0)
        continue;
      memmove(p, de.name, DIRSIZ);
      p[DIRSIZ] = 0;
      if(stat(buf, &st) < 0){
        printf("tree: cannot stat %s\n", buf);
        continue;
      }
      char buff[256];
      strcpy(buff,buf);
      //memmove(buf+strlen(buf), path, strlen(path));
      if(read(fd, &de, sizeof(de)) == sizeof(de))
         check[level]=1;
      else
         check[level]=0;
      //printf("path name is %s and file name is %s\n", buf,fmtname(buf));
      if(strcmp(fmtname(buf),a1) && strcmp(fmtname(buf),a2))
      {
        
        for(int i=1;i<level;i++)
        {
          if(check[i]==1)
              printf("|   ");
          else
              printf("    ");
        }
        printf("|\n");
        for(int i=1;i<level;i++)
        { 
          if(check[i]==1)
              printf("|   ");
          else
              printf("    ");
        }
        printf("+-- %s\n", fmtname(buff));
        tree(buff,level+1);
      }
     
          
    }
    check[level]=1;
    break;
  }
  close(fd);
}
int main(int argc, char *argv[]) {
    // add your code!
    check[0]=1;
    check[1]=1;
    check[2]=1;
    check[3]=1;
    check[4]=1;
    check[5]=1;
    check[6]=1;
    check[7]=1;
    check[8]=1;
    int fd[2];
    pipe(fd);
    int pid = fork();
    if(pid == 0){
      close(fd[0]);
      if(argc < 2){
        tree(".",1);
        exit(0);
      }
      else
      {
        tree(argv[1],1);
      }
      write(fd[1],num,sizeof(num));
      close(fd[1]);
      exit(0);
    }
    if(pid > 0){
      close(fd[1]);
      read(fd[0],num,sizeof(num));
      printf("\n%d directories, %d files\n",num[0],num[1]);
      close(fd[0]);
      wait(0);
    }
    exit(0);
}
