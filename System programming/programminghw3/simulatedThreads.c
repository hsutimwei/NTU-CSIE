#include "threadtools.h"

// Please complete this three functions. You may refer to the macro function defined in "threadtools.h"

// yntain Climbing
// You are required to solve this function via iterative method, instead of recursion.
void MountainClimbing(int thread_id, int number){
    ThreadInit(thread_id, number);
    
    int ss=setjmp(Current->Environment);
	if(ss==0)
    return;

    Current->w=1;
    Current->x=1;

    for(Current->i=2;Current->i<=Current->z;Current->i++)
    {  //printf("mountain id: %d\n",Current->Thread_id);
        sleep(1);
        Current->y=Current->w+Current->x;
        printf("Mountain Climbing: %d\n",Current->y);
        Current->x=Current->w;
        Current->w=Current->y;
        ThreadYield();
    }
    
    ThreadExit();
}

// Reduce Integer
// You are required to solve this function via iterative method, instead of recursion.
void ReduceInteger(int thread_id, int number){
    ThreadInit(thread_id, number);
    
    int ss=setjmp(Current->Environment);
	if(ss==0)
    return;


    Current->x=0;

	while(1)
    {   //printf("reduce id: %d\n",Current->Thread_id);
        sleep(1);
        if(Current->z%2==0)
        Current->z/=2;
        else if( Current->z == 3 || Current->z % 4 == 1) 
            Current->z--;
        else
            Current->z++;
        Current->x++;
        printf("Reduce Integer: %d\n", Current->x);
               
        ThreadYield();
        if(Current->z==1)
        break;
    }
    
    ThreadExit();
}

// Operation Count
// You are required to solve this function via iterative method, instead of recursion.
void OperationCount(int thread_id, int number){
    ThreadInit(thread_id, number);
    
    int ss=setjmp(Current->Environment);
	if(ss==0)
    return;

    Current->x=0;


    for(Current->i=0;Current->i<Current->z/2;Current->i++)
    {   //printf("reduce id: %d\n",Current->Thread_id);
    
        sleep(1);
        if(Current->z%2==0)
        Current->x+=2*Current->i+1;
        else
        Current->x+=2*Current->i;
        if(Current->z==0 || Current->z==1)
        Current->x=0;
        printf("Operation Count: %d\n",Current->x);
        //因為從中間往旁邊挑，中間的+1 or +0，然後+3 or +2，然後+5 or +4，就這樣寫了。
        //還有，有一種理解是每做完一次operation就printf一次，但這明顯跟sample衝突。所以就只能這樣了。
        
        ThreadYield();
    }
    
    ThreadExit();


}