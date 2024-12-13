#include "types.h"
#include "riscv.h"
#include "defs.h"
#include "date.h"
#include "param.h"
#include "memlayout.h"
#include "spinlock.h"
#include "proc.h"

uint64
sys_exit(void)
{
  int n;
  if(argint(0, &n) < 0)
    return -1;
  exit(n);
  return 0;  // not reached
}

uint64
sys_getpid(void)
{
  return myproc()->pid;
}

uint64
sys_fork(void)
{
  return fork();
}

uint64
sys_wait(void)
{
  uint64 p;
  if(argaddr(0, &p) < 0)
    return -1;
  return wait(p);
}

uint64
sys_sbrk(void)
{
  int addr;
  int n;

  if(argint(0, &n) < 0)
    return -1;
  addr = myproc()->sz;
  if(growproc(n) < 0)
    return -1;
  return addr;
}

uint64
sys_sleep(void)
{
  int n;
  uint ticks0;

  if(argint(0, &n) < 0)
    return -1;
  acquire(&tickslock);
  ticks0 = ticks;
  while(ticks - ticks0 < n){
    if(myproc()->killed){
      release(&tickslock);
      return -1;
    }
    sleep(&ticks, &tickslock);
  }
  release(&tickslock);
  return 0;
}

uint64
sys_kill(void)
{
  int pid;

  if(argint(0, &pid) < 0)
    return -1;
  return kill(pid);
}

// return how many clock tick interrupts have occurred
// since start.
uint64
sys_uptime(void)
{
  uint xticks;

  acquire(&tickslock);
  xticks = ticks;
  release(&tickslock);
  return xticks;
}


// for mp3
uint64
sys_thrdstop(void)
{
  int delay, thrdstop_context_id;
  uint64 handler, handler_arg;
  if (argint(0, &delay) < 0)
    return -1;
  if (argint(1, &thrdstop_context_id) < 0)
    return -1;
  if (argaddr(2, &handler) < 0)
    return -1;
  if (argaddr(3, &handler_arg) < 0)
    return -1;
  
  struct proc *p = myproc();
  p->thrdstop_ticks = 0;
  p->thrdstop_delay = delay;
  p->thrdstop_handler_pointer = handler;
  p->thrdstop_handler_arg=handler_arg;

  if (thrdstop_context_id < 0) 
  {
      for (int i=0; i < MAX_THRD_NUM; i++)
        if (p->thrdstop_context_check[i]!=1)
        {
            p->thrdstop_context_id = i;
            p->thrdstop_context_check[i] = 1;
            return i;
        }
  }
  else
  {
      p->thrdstop_context_id = thrdstop_context_id;
      p->thrdstop_context_check[thrdstop_context_id] = 1;
      return thrdstop_context_id;
  }
     return -1;
}

// for mp3
uint64
sys_cancelthrdstop(void)
{
  int thrdstop_context_id, is_exit;
  if (argint(0, &thrdstop_context_id) < 0)
    return -1;
  if (argint(1, &is_exit) < 0)
    return -1;
  
  struct proc *p = myproc();
  p->thrdstop_delay = -1;

  if(is_exit==0)
  {
    if (thrdstop_context_id != -1)
    {
        struct thrd_context *c = &p->thrdstop_context[thrdstop_context_id];
        c->epc = p->trapframe->epc;
        c->ra= p->trapframe->ra;
        c->sp= p->trapframe->sp;
        c->gp= p->trapframe->gp;
        c->tp= p->trapframe->tp;
        c->t0= p->trapframe->t0;
        c->t1= p->trapframe->t1;
        c->t2= p->trapframe->t2;
        c->s0= p->trapframe->s0;
        c->s1= p->trapframe->s1;
        c->a0= p->trapframe->a0;
        c->a1= p->trapframe->a1;
        c->a2= p->trapframe->a2;
        c->a3= p->trapframe->a3;
        c->a4= p->trapframe->a4;
        c->a5= p->trapframe->a5;
        c->a6= p->trapframe->a6;
        c->a7= p->trapframe->a7;
        c->s2= p->trapframe->s2;
        c->s3= p->trapframe->s3;
        c->s4= p->trapframe->s4;
        c->s5= p->trapframe->s5;
        c->s6= p->trapframe->s6;
        c->s7= p->trapframe->s7;
        c->s8= p->trapframe->s8;
        c->s9= p->trapframe->s9;
        c->s10= p->trapframe->s10;
        c->s11= p->trapframe->s11;
        c->t3= p->trapframe->t3;
        c->t4= p->trapframe->t4;
        c->t5= p->trapframe->t5;
        c->t6= p->trapframe->t6;
    }
  }
  else
    p->thrdstop_context_check[thrdstop_context_id] = 0;
  
  return p->thrdstop_ticks;
}

// for mp3
uint64
sys_thrdresume(void)
{
  int  thrdstop_context_id;
  if (argint(0, &thrdstop_context_id) < 0)
    return -1;
  struct proc *p = myproc();
  struct thrd_context *c = &p->thrdstop_context[p->thrdstop_context_id];
        p->trapframe->epc = c->epc;
        p->trapframe->ra = c->ra;
        p->trapframe->sp = c->sp;
        p->trapframe->gp = c->gp;
        p->trapframe->tp = c->tp;
        p->trapframe->t0 = c->t0;
        p->trapframe->t1 = c->t1;
        p->trapframe->t2 = c->t2;
        p->trapframe->s0 = c->s0;
        p->trapframe->s1 = c->s1;
        p->trapframe->a0 = c->a0;
        p->trapframe->a1 = c->a1;
        p->trapframe->a2 = c->a2;
        p->trapframe->a3 = c->a3;
        p->trapframe->a4 = c->a4;
        p->trapframe->a5 = c->a5;
        p->trapframe->a6 = c->a6;
        p->trapframe->a7 = c->a7;
        p->trapframe->s2 = c->s2;
        p->trapframe->s3 = c->s3;
        p->trapframe->s4 = c->s4;
        p->trapframe->s5 = c->s5;
        p->trapframe->s6 = c->s6;
        p->trapframe->s7 = c->s7;
        p->trapframe->s8 = c->s8;
        p->trapframe->s9 = c->s9;
        p->trapframe->s10 = c->s10;
        p->trapframe->s11 = c->s11;
        p->trapframe->t3 = c->t3;
        p->trapframe->t4 = c->t4;
        p->trapframe->t5 = c->t5;
        p->trapframe->t6 = c->t6;
  return 0;
}
