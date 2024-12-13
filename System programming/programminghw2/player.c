#include <unistd.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv){
 /// fprintf(stderr, "cccccc\n");  
  if(argc != 3){
        fprintf(stderr, "argc error\n");
        exit(1);
    }
    
    int guess;
    /* initialize random seed: */
   

    const int ID = atoi(argv[2]);

    if(ID < 0 || ID > 12 )
    {
        fprintf(stderr, "ID not valid\n");
        exit(1);
    }
    else if(ID==0 && strcmp(argv[2], "0"))
    {
        fprintf(stderr, "ID not to be char\n");
        exit(1);
    }

    for(int i = 1; i <= 10; i++)
    {
        srand ((ID + i) * 323);
        /* generate guess between 1 and 1000: */
        guess = rand() % 1001;
        
        printf("%d %d\n", ID, guess);
       // fprintf(stderr, "bbbb %d %d\n",ID,guess);
        fflush(stdout);
        fsync(1);
    }
    return 0; 
}