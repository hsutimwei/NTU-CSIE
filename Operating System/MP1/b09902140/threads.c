#include "kernel/types.h"
#include "user/setjmp.h"
#include "user/threads.h"
#include "user/user.h"
#define NULL 0

static struct thread* current_thread = NULL;
//static struct thread* root_thread = NULL;
static int id = 1;
static jmp_buf env_st;
//static jmp_buf env_tmp;
// TODO: necessary declares, if any


struct thread *thread_create(void (*f)(void *), void *arg){
    struct thread *t = (struct thread*) malloc(sizeof(struct thread));
    //unsigned long stack_p = 0;
    unsigned long new_stack_p;
    unsigned long new_stack;
    new_stack = (unsigned long) malloc(sizeof(unsigned long)*0x100);
    new_stack_p = new_stack +0x100*8-0x2*8;
    t->fp = f;
    t->arg = arg;
    t->ID  = id;
    t->buf_set = 0;
    t->stack = (void*) new_stack;
    t->stack_p = (void*) new_stack_p;
    id++;
    return t;
}
void thread_add_runqueue(struct thread *t){
    if(current_thread == NULL){
        // TODO
        current_thread = t;
        current_thread->left = current_thread->right = current_thread->parent = t;
    }
    else{
        // TODO
        t->left=t;
        t->right=t;
        if(current_thread->left==current_thread)
        {
            current_thread->left=t;
            t->parent=current_thread;
        }
        else if(current_thread->right==current_thread)
        {
            current_thread->right=t;
            t->parent=current_thread;
        }
        else
        {
            free(t->stack);
            free(t->stack_p);
            free(t);
        }
        
    }
}
void thread_yield(void){
    // TODO
    if (setjmp(current_thread->env) == 0){     
        schedule();
        dispatch();
    }
}
void dispatch(void){
    // TODO
    if (current_thread->buf_set)
        longjmp(current_thread->env, 1);
    if (setjmp(current_thread->env) == 0) {
        current_thread->env->sp = (unsigned long)current_thread->stack_p;
        current_thread->buf_set = 1;
        longjmp(current_thread->env, 1);
    }
    current_thread->fp(current_thread->arg);
    thread_exit();
}
void schedule(void){
    // TODO
    
    if(current_thread == current_thread->left && current_thread == current_thread->right)
    {
           while(1)
           {
               if(current_thread == current_thread->parent->left && current_thread->parent == current_thread->parent->right)
                  current_thread = current_thread->parent;
               else if(current_thread == current_thread->parent->left && current_thread->parent != current_thread->parent->right)
               {
                   current_thread = current_thread->parent->right;
                   break;
               }
               else if(current_thread == current_thread->parent->right)
                  current_thread = current_thread->parent;
               if(current_thread == current_thread->parent)
                  break;
           }
        
    }
    else if(current_thread != current_thread->left)
    current_thread = current_thread->left;
    else if(current_thread != current_thread->right)
    current_thread = current_thread->right;

    //printf("喵:       ID:%d  left:%d  right:%d  parent:%d\n",current_thread->ID,current_thread->left->ID,current_thread->right->ID,current_thread->parent->ID);
}
void thread_exit(void){
    if(current_thread == current_thread->parent && current_thread->left == current_thread && current_thread->right == current_thread){
        // TODO
        // Hint: No more thread to execute
        free(current_thread->stack);
        free(current_thread->stack_p);
        free(current_thread);
        longjmp(env_st, 1);
    }
    else if(current_thread->left == current_thread && current_thread->right == current_thread)
    {
        struct thread *a = current_thread;
        schedule();
        if(a->parent->left==a)
        a->parent->left=a->parent;
        else if(a->parent->right==a)
        a->parent->right=a->parent;
        //printf("meow       a:  ID:%d  left:%d  right:%d  parent:%d\n",a->ID,a->left->ID,a->right->ID,a->parent->ID);
        free(a->stack);
        free(a->stack_p);
        free(a);
        ///printf("meow current:  ID:%d  left:%d  right:%d  parent:%d\n",current_thread->ID,current_thread->left->ID,current_thread->right->ID,current_thread->parent->ID);
    }
    else{
        // TODO
        struct thread *a = current_thread;
        while(current_thread->left != current_thread || current_thread->right != current_thread)
        {
            if(current_thread->right!=current_thread)
            current_thread=current_thread->right;
            else if(current_thread->left!=current_thread)
            current_thread=current_thread->left;
        }
        if(current_thread->parent->left==current_thread)
              current_thread->parent->left=current_thread->parent;
        else if(current_thread->parent->right==current_thread)
              current_thread->parent->right=current_thread->parent;
        if(a->parent!=a)
        {  
           current_thread->parent=a->parent;
           if(a->parent->left==a)
              a->parent->left=current_thread;
           else if(a->parent->right==a)
              a->parent->right=current_thread;
        }
        else
        current_thread->parent=current_thread;
        if(a->left!=a)
        {
           current_thread->left=a->left;
           if(a->left!=current_thread)
           a->left->parent=current_thread;
        }
        else
        current_thread->left=current_thread;
        //printf("what!!!:  ID:%d  left:%d  right:%d  parent:%d\n",current_thread->ID,current_thread->left->ID,current_thread->right->ID,current_thread->parent->ID);
        if(a->right!=a)
        {
           current_thread->right=a->right;
           if(a->right!=current_thread)
           a->right->parent=current_thread;
        }
        else
        current_thread->right=current_thread;
        //printf("what???:  ID:%d  left:%d  right:%d  parent:%d\n",current_thread->ID,current_thread->left->ID,current_thread->right->ID,current_thread->parent->ID);
        //printf("before:   ID:%d  left:%d  right:%d  parent:%d\n",current_thread->ID,current_thread->left->ID,current_thread->right->ID,current_thread->parent->ID);
        schedule();
        //printf("      a:  ID:%d  left:%d  right:%d  parent:%d\n",a->ID,a->left->ID,a->right->ID,a->parent->ID);
        //printf("current:  ID:%d  left:%d  right:%d  parent:%d\n",current_thread->ID,current_thread->left->ID,current_thread->right->ID,current_thread->parent->ID);
        free(a->stack);
        free(a->stack_p);
        free(a);
    }
    dispatch();
}
void thread_start_threading(void){
    // TODO
    if (setjmp(env_st) != 0) {
        return;
    }
    schedule();
    dispatch();
}
