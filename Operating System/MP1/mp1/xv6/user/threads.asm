
user/_threads:     file format elf64-littleriscv


Disassembly of section .text:

0000000000000000 <thread_create>:
static jmp_buf env_st;
//static jmp_buf env_tmp;
// TODO: necessary declares, if any


struct thread *thread_create(void (*f)(void *), void *arg){
   0:	7179                	addi	sp,sp,-48
   2:	f406                	sd	ra,40(sp)
   4:	f022                	sd	s0,32(sp)
   6:	ec26                	sd	s1,24(sp)
   8:	e84a                	sd	s2,16(sp)
   a:	e44e                	sd	s3,8(sp)
   c:	1800                	addi	s0,sp,48
   e:	89aa                	mv	s3,a0
  10:	892e                	mv	s2,a1
    struct thread *t = (struct thread*) malloc(sizeof(struct thread));
  12:	0b000513          	li	a0,176
  16:	00001097          	auipc	ra,0x1
  1a:	a52080e7          	jalr	-1454(ra) # a68 <malloc>
  1e:	84aa                	mv	s1,a0
    //unsigned long stack_p = 0;
    unsigned long new_stack_p;
    unsigned long new_stack;
    new_stack = (unsigned long) malloc(sizeof(unsigned long)*0x100);
  20:	6505                	lui	a0,0x1
  22:	80050513          	addi	a0,a0,-2048 # 800 <vprintf+0x62>
  26:	00001097          	auipc	ra,0x1
  2a:	a42080e7          	jalr	-1470(ra) # a68 <malloc>
    new_stack_p = new_stack +0x100*8-0x2*8;
    t->fp = f;
  2e:	0134b023          	sd	s3,0(s1)
    t->arg = arg;
  32:	0124b423          	sd	s2,8(s1)
    t->ID  = id;
  36:	00001717          	auipc	a4,0x1
  3a:	bde70713          	addi	a4,a4,-1058 # c14 <id>
  3e:	431c                	lw	a5,0(a4)
  40:	08f4a823          	sw	a5,144(s1)
    t->buf_set = 0;
  44:	0804aa23          	sw	zero,148(s1)
    t->stack = (void*) new_stack;
  48:	e888                	sd	a0,16(s1)
    new_stack_p = new_stack +0x100*8-0x2*8;
  4a:	7f050513          	addi	a0,a0,2032
    t->stack_p = (void*) new_stack_p;
  4e:	ec88                	sd	a0,24(s1)
    id++;
  50:	2785                	addiw	a5,a5,1
  52:	c31c                	sw	a5,0(a4)
    return t;
}
  54:	8526                	mv	a0,s1
  56:	70a2                	ld	ra,40(sp)
  58:	7402                	ld	s0,32(sp)
  5a:	64e2                	ld	s1,24(sp)
  5c:	6942                	ld	s2,16(sp)
  5e:	69a2                	ld	s3,8(sp)
  60:	6145                	addi	sp,sp,48
  62:	8082                	ret

0000000000000064 <thread_add_runqueue>:
void thread_add_runqueue(struct thread *t){
  64:	1101                	addi	sp,sp,-32
  66:	ec06                	sd	ra,24(sp)
  68:	e822                	sd	s0,16(sp)
  6a:	e426                	sd	s1,8(sp)
  6c:	1000                	addi	s0,sp,32
  6e:	84aa                	mv	s1,a0
    if(current_thread == NULL){
  70:	00001797          	auipc	a5,0x1
  74:	ba87b783          	ld	a5,-1112(a5) # c18 <current_thread>
  78:	cb8d                	beqz	a5,aa <thread_add_runqueue+0x46>
        current_thread = t;
        current_thread->left = current_thread->right = current_thread->parent = t;
    }
    else{
        // TODO
        t->left=t;
  7a:	ecc8                	sd	a0,152(s1)
        t->right=t;
  7c:	f0c8                	sd	a0,160(s1)
        if(current_thread->left==current_thread)
  7e:	6fd8                	ld	a4,152(a5)
  80:	04e78163          	beq	a5,a4,c2 <thread_add_runqueue+0x5e>
        {
            current_thread->left=t;
            t->parent=current_thread;
        }
        else if(current_thread->right==current_thread)
  84:	73d8                	ld	a4,160(a5)
  86:	04e78163          	beq	a5,a4,c8 <thread_add_runqueue+0x64>
            current_thread->right=t;
            t->parent=current_thread;
        }
        else
        {
            free(t->stack);
  8a:	6908                	ld	a0,16(a0)
  8c:	00001097          	auipc	ra,0x1
  90:	954080e7          	jalr	-1708(ra) # 9e0 <free>
            free(t->stack_p);
  94:	6c88                	ld	a0,24(s1)
  96:	00001097          	auipc	ra,0x1
  9a:	94a080e7          	jalr	-1718(ra) # 9e0 <free>
            free(t);
  9e:	8526                	mv	a0,s1
  a0:	00001097          	auipc	ra,0x1
  a4:	940080e7          	jalr	-1728(ra) # 9e0 <free>
        }
        
    }
}
  a8:	a801                	j	b8 <thread_add_runqueue+0x54>
        current_thread = t;
  aa:	00001797          	auipc	a5,0x1
  ae:	b6a7b723          	sd	a0,-1170(a5) # c18 <current_thread>
        current_thread->left = current_thread->right = current_thread->parent = t;
  b2:	f4c8                	sd	a0,168(s1)
  b4:	f0c8                	sd	a0,160(s1)
  b6:	ecc8                	sd	a0,152(s1)
}
  b8:	60e2                	ld	ra,24(sp)
  ba:	6442                	ld	s0,16(sp)
  bc:	64a2                	ld	s1,8(sp)
  be:	6105                	addi	sp,sp,32
  c0:	8082                	ret
            current_thread->left=t;
  c2:	efc8                	sd	a0,152(a5)
            t->parent=current_thread;
  c4:	f55c                	sd	a5,168(a0)
  c6:	bfcd                	j	b8 <thread_add_runqueue+0x54>
            current_thread->right=t;
  c8:	f3c8                	sd	a0,160(a5)
            t->parent=current_thread;
  ca:	f55c                	sd	a5,168(a0)
  cc:	b7f5                	j	b8 <thread_add_runqueue+0x54>

00000000000000ce <schedule>:
        longjmp(current_thread->env, 1);
    }
    current_thread->fp(current_thread->arg);
    thread_exit();
}
void schedule(void){
  ce:	1141                	addi	sp,sp,-16
  d0:	e406                	sd	ra,8(sp)
  d2:	e022                	sd	s0,0(sp)
  d4:	0800                	addi	s0,sp,16
    // TODO
    
    if(current_thread == current_thread->left && current_thread == current_thread->right)
  d6:	00001797          	auipc	a5,0x1
  da:	b427b783          	ld	a5,-1214(a5) # c18 <current_thread>
  de:	6fd8                	ld	a4,152(a5)
  e0:	04e78163          	beq	a5,a4,122 <schedule+0x54>
                  break;
           }
        
    }
    else if(current_thread != current_thread->left)
    current_thread = current_thread->left;
  e4:	00001797          	auipc	a5,0x1
  e8:	b2e7ba23          	sd	a4,-1228(a5) # c18 <current_thread>
    else if(current_thread != current_thread->right)
    current_thread = current_thread->right;

    printf("喵:       ID:%d  left:%d  right:%d  parent:%d\n",current_thread->ID,current_thread->left->ID,current_thread->right->ID,current_thread->parent->ID);
  ec:	00001797          	auipc	a5,0x1
  f0:	b2c7b783          	ld	a5,-1236(a5) # c18 <current_thread>
  f4:	77d8                	ld	a4,168(a5)
  f6:	73d4                	ld	a3,160(a5)
  f8:	6fd0                	ld	a2,152(a5)
  fa:	09072703          	lw	a4,144(a4)
  fe:	0906a683          	lw	a3,144(a3)
 102:	09062603          	lw	a2,144(a2)
 106:	0907a583          	lw	a1,144(a5)
 10a:	00001517          	auipc	a0,0x1
 10e:	abe50513          	addi	a0,a0,-1346 # bc8 <longjmp_1+0xa>
 112:	00001097          	auipc	ra,0x1
 116:	898080e7          	jalr	-1896(ra) # 9aa <printf>
}
 11a:	60a2                	ld	ra,8(sp)
 11c:	6402                	ld	s0,0(sp)
 11e:	0141                	addi	sp,sp,16
 120:	8082                	ret
    if(current_thread == current_thread->left && current_thread == current_thread->right)
 122:	73d8                	ld	a4,160(a5)
 124:	00e78763          	beq	a5,a4,132 <schedule+0x64>
    current_thread = current_thread->right;
 128:	00001797          	auipc	a5,0x1
 12c:	aee7b823          	sd	a4,-1296(a5) # c18 <current_thread>
 130:	bf75                	j	ec <schedule+0x1e>
 132:	4601                	li	a2,0
 134:	4585                	li	a1,1
 136:	a829                	j	150 <schedule+0x82>
               if(current_thread == current_thread->parent->left && current_thread->parent == current_thread->parent->right)
 138:	735c                	ld	a5,160(a4)
 13a:	00f70763          	beq	a4,a5,148 <schedule+0x7a>
                   current_thread = current_thread->parent->right;
 13e:	00001717          	auipc	a4,0x1
 142:	acf73d23          	sd	a5,-1318(a4) # c18 <current_thread>
                   break;
 146:	b75d                	j	ec <schedule+0x1e>
 148:	862e                	mv	a2,a1
               if(current_thread == current_thread->parent)
 14a:	77d8                	ld	a4,168(a5)
 14c:	00f70c63          	beq	a4,a5,164 <schedule+0x96>
               if(current_thread == current_thread->parent->left && current_thread->parent == current_thread->parent->right)
 150:	77d8                	ld	a4,168(a5)
 152:	6f54                	ld	a3,152(a4)
 154:	fef682e3          	beq	a3,a5,138 <schedule+0x6a>
               else if(current_thread == current_thread->parent->right)
 158:	7354                	ld	a3,160(a4)
 15a:	fef698e3          	bne	a3,a5,14a <schedule+0x7c>
                  current_thread = current_thread->parent;
 15e:	87ba                	mv	a5,a4
 160:	862e                	mv	a2,a1
 162:	b7e5                	j	14a <schedule+0x7c>
 164:	d641                	beqz	a2,ec <schedule+0x1e>
 166:	00001717          	auipc	a4,0x1
 16a:	aaf73923          	sd	a5,-1358(a4) # c18 <current_thread>
 16e:	bfbd                	j	ec <schedule+0x1e>

0000000000000170 <thread_exit>:
void thread_exit(void){
 170:	1101                	addi	sp,sp,-32
 172:	ec06                	sd	ra,24(sp)
 174:	e822                	sd	s0,16(sp)
 176:	e426                	sd	s1,8(sp)
 178:	1000                	addi	s0,sp,32
    if(current_thread == current_thread->parent && current_thread->left == current_thread && current_thread->right == current_thread){
 17a:	00001497          	auipc	s1,0x1
 17e:	a9e4b483          	ld	s1,-1378(s1) # c18 <current_thread>
 182:	74dc                	ld	a5,168(s1)
 184:	00f48963          	beq	s1,a5,196 <thread_exit+0x26>
        free(current_thread->stack);
        free(current_thread->stack_p);
        free(current_thread);
        longjmp(env_st, 1);
    }
    else if(current_thread->left == current_thread && current_thread->right == current_thread)
 188:	6cd8                	ld	a4,152(s1)
 18a:	87a6                	mv	a5,s1
 18c:	4601                	li	a2,0
 18e:	04e48a63          	beq	s1,a4,1e2 <thread_exit+0x72>
 192:	4585                	li	a1,1
 194:	a871                	j	230 <thread_exit+0xc0>
    if(current_thread == current_thread->parent && current_thread->left == current_thread && current_thread->right == current_thread){
 196:	6cd8                	ld	a4,152(s1)
 198:	87a6                	mv	a5,s1
 19a:	4601                	li	a2,0
 19c:	fee49be3          	bne	s1,a4,192 <thread_exit+0x22>
 1a0:	70d8                	ld	a4,160(s1)
 1a2:	fee498e3          	bne	s1,a4,192 <thread_exit+0x22>
        free(current_thread->stack);
 1a6:	6888                	ld	a0,16(s1)
 1a8:	00001097          	auipc	ra,0x1
 1ac:	838080e7          	jalr	-1992(ra) # 9e0 <free>
        free(current_thread->stack_p);
 1b0:	00001497          	auipc	s1,0x1
 1b4:	a6848493          	addi	s1,s1,-1432 # c18 <current_thread>
 1b8:	609c                	ld	a5,0(s1)
 1ba:	6f88                	ld	a0,24(a5)
 1bc:	00001097          	auipc	ra,0x1
 1c0:	824080e7          	jalr	-2012(ra) # 9e0 <free>
        free(current_thread);
 1c4:	6088                	ld	a0,0(s1)
 1c6:	00001097          	auipc	ra,0x1
 1ca:	81a080e7          	jalr	-2022(ra) # 9e0 <free>
        longjmp(env_st, 1);
 1ce:	4585                	li	a1,1
 1d0:	00001517          	auipc	a0,0x1
 1d4:	a5850513          	addi	a0,a0,-1448 # c28 <env_st>
 1d8:	00001097          	auipc	ra,0x1
 1dc:	9ac080e7          	jalr	-1620(ra) # b84 <longjmp>
 1e0:	a0f9                	j	2ae <thread_exit+0x13e>
    else if(current_thread->left == current_thread && current_thread->right == current_thread)
 1e2:	70d8                	ld	a4,160(s1)
 1e4:	fae497e3          	bne	s1,a4,192 <thread_exit+0x22>
    {
        struct thread *a = current_thread;
        schedule();
 1e8:	00000097          	auipc	ra,0x0
 1ec:	ee6080e7          	jalr	-282(ra) # ce <schedule>
        if(a->parent->left==a)
 1f0:	74dc                	ld	a5,168(s1)
 1f2:	6fd8                	ld	a4,152(a5)
 1f4:	02e48563          	beq	s1,a4,21e <thread_exit+0xae>
        a->parent->left=a->parent;
        else if(a->parent->right==a)
 1f8:	73d8                	ld	a4,160(a5)
 1fa:	02e48463          	beq	s1,a4,222 <thread_exit+0xb2>
        a->parent->right=a->parent;
        //printf("meow       a:  ID:%d  left:%d  right:%d  parent:%d\n",a->ID,a->left->ID,a->right->ID,a->parent->ID);
        free(a->stack);
 1fe:	6888                	ld	a0,16(s1)
 200:	00000097          	auipc	ra,0x0
 204:	7e0080e7          	jalr	2016(ra) # 9e0 <free>
        free(a->stack_p);
 208:	6c88                	ld	a0,24(s1)
 20a:	00000097          	auipc	ra,0x0
 20e:	7d6080e7          	jalr	2006(ra) # 9e0 <free>
        free(a);
 212:	8526                	mv	a0,s1
 214:	00000097          	auipc	ra,0x0
 218:	7cc080e7          	jalr	1996(ra) # 9e0 <free>
    {
 21c:	a849                	j	2ae <thread_exit+0x13e>
        a->parent->left=a->parent;
 21e:	efdc                	sd	a5,152(a5)
 220:	bff9                	j	1fe <thread_exit+0x8e>
        a->parent->right=a->parent;
 222:	f3dc                	sd	a5,160(a5)
 224:	bfe9                	j	1fe <thread_exit+0x8e>
        ///printf("meow current:  ID:%d  left:%d  right:%d  parent:%d\n",current_thread->ID,current_thread->left->ID,current_thread->right->ID,current_thread->parent->ID);
    }
    else{
        // TODO
        struct thread *a = current_thread;
        while(current_thread->left != current_thread || current_thread->right != current_thread)
 226:	73d8                	ld	a4,160(a5)
 228:	00e78c63          	beq	a5,a4,240 <thread_exit+0xd0>
        {
            if(current_thread->right!=current_thread)
            current_thread=current_thread->right;
 22c:	87ba                	mv	a5,a4
 22e:	862e                	mv	a2,a1
        while(current_thread->left != current_thread || current_thread->right != current_thread)
 230:	6fd4                	ld	a3,152(a5)
 232:	fed78ae3          	beq	a5,a3,226 <thread_exit+0xb6>
            if(current_thread->right!=current_thread)
 236:	73d8                	ld	a4,160(a5)
 238:	fee79ae3          	bne	a5,a4,22c <thread_exit+0xbc>
            else if(current_thread->left!=current_thread)
            current_thread=current_thread->left;
 23c:	87b6                	mv	a5,a3
 23e:	bfc5                	j	22e <thread_exit+0xbe>
 240:	c609                	beqz	a2,24a <thread_exit+0xda>
 242:	00001797          	auipc	a5,0x1
 246:	9ce7bb23          	sd	a4,-1578(a5) # c18 <current_thread>
        }
        if(current_thread->parent->left==current_thread)
 24a:	775c                	ld	a5,168(a4)
 24c:	6fd4                	ld	a3,152(a5)
 24e:	06d70963          	beq	a4,a3,2c0 <thread_exit+0x150>
              current_thread->parent->left=current_thread->parent;
        else if(current_thread->parent->right==current_thread)
 252:	73d4                	ld	a3,160(a5)
 254:	06d70863          	beq	a4,a3,2c4 <thread_exit+0x154>
              current_thread->parent->right=current_thread->parent;
        if(a->parent!=a)
 258:	74dc                	ld	a5,168(s1)
 25a:	06f48b63          	beq	s1,a5,2d0 <thread_exit+0x160>
        {  
           current_thread->parent=a->parent;
 25e:	f75c                	sd	a5,168(a4)
           if(a->parent->left==a)
 260:	6fd4                	ld	a3,152(a5)
 262:	06d48363          	beq	s1,a3,2c8 <thread_exit+0x158>
              a->parent->left=current_thread;
           else if(a->parent->right==a)
 266:	73d4                	ld	a3,160(a5)
 268:	06d48263          	beq	s1,a3,2cc <thread_exit+0x15c>
              a->parent->right=current_thread;
        }
        else
        current_thread->parent=current_thread;
        if(a->left!=a)
 26c:	6cdc                	ld	a5,152(s1)
 26e:	06f48363          	beq	s1,a5,2d4 <thread_exit+0x164>
        {
           current_thread->left=a->left;
 272:	ef5c                	sd	a5,152(a4)
           if(a->left!=current_thread)
 274:	00f70363          	beq	a4,a5,27a <thread_exit+0x10a>
           a->left->parent=current_thread;
 278:	f7d8                	sd	a4,168(a5)
        }
        else
        current_thread->left=current_thread;
        //printf("what!!!:  ID:%d  left:%d  right:%d  parent:%d\n",current_thread->ID,current_thread->left->ID,current_thread->right->ID,current_thread->parent->ID);
        if(a->right!=a)
 27a:	70dc                	ld	a5,160(s1)
 27c:	04f48e63          	beq	s1,a5,2d8 <thread_exit+0x168>
        {
           current_thread->right=a->right;
 280:	f35c                	sd	a5,160(a4)
           if(a->right!=current_thread)
 282:	00f70363          	beq	a4,a5,288 <thread_exit+0x118>
           a->right->parent=current_thread;
 286:	f7d8                	sd	a4,168(a5)
        }
        else
        current_thread->right=current_thread;
        //printf("what???:  ID:%d  left:%d  right:%d  parent:%d\n",current_thread->ID,current_thread->left->ID,current_thread->right->ID,current_thread->parent->ID);
        //printf("before:   ID:%d  left:%d  right:%d  parent:%d\n",current_thread->ID,current_thread->left->ID,current_thread->right->ID,current_thread->parent->ID);
        schedule();
 288:	00000097          	auipc	ra,0x0
 28c:	e46080e7          	jalr	-442(ra) # ce <schedule>
        //printf("      a:  ID:%d  left:%d  right:%d  parent:%d\n",a->ID,a->left->ID,a->right->ID,a->parent->ID);
        //printf("current:  ID:%d  left:%d  right:%d  parent:%d\n",current_thread->ID,current_thread->left->ID,current_thread->right->ID,current_thread->parent->ID);
        free(a->stack);
 290:	6888                	ld	a0,16(s1)
 292:	00000097          	auipc	ra,0x0
 296:	74e080e7          	jalr	1870(ra) # 9e0 <free>
        free(a->stack_p);
 29a:	6c88                	ld	a0,24(s1)
 29c:	00000097          	auipc	ra,0x0
 2a0:	744080e7          	jalr	1860(ra) # 9e0 <free>
        free(a);
 2a4:	8526                	mv	a0,s1
 2a6:	00000097          	auipc	ra,0x0
 2aa:	73a080e7          	jalr	1850(ra) # 9e0 <free>
    }
    dispatch();
 2ae:	00000097          	auipc	ra,0x0
 2b2:	02e080e7          	jalr	46(ra) # 2dc <dispatch>
}
 2b6:	60e2                	ld	ra,24(sp)
 2b8:	6442                	ld	s0,16(sp)
 2ba:	64a2                	ld	s1,8(sp)
 2bc:	6105                	addi	sp,sp,32
 2be:	8082                	ret
              current_thread->parent->left=current_thread->parent;
 2c0:	efdc                	sd	a5,152(a5)
 2c2:	bf59                	j	258 <thread_exit+0xe8>
              current_thread->parent->right=current_thread->parent;
 2c4:	f3dc                	sd	a5,160(a5)
 2c6:	bf49                	j	258 <thread_exit+0xe8>
              a->parent->left=current_thread;
 2c8:	efd8                	sd	a4,152(a5)
 2ca:	b74d                	j	26c <thread_exit+0xfc>
              a->parent->right=current_thread;
 2cc:	f3d8                	sd	a4,160(a5)
 2ce:	bf79                	j	26c <thread_exit+0xfc>
        current_thread->parent=current_thread;
 2d0:	f758                	sd	a4,168(a4)
 2d2:	bf69                	j	26c <thread_exit+0xfc>
        current_thread->left=current_thread;
 2d4:	ef58                	sd	a4,152(a4)
 2d6:	b755                	j	27a <thread_exit+0x10a>
        current_thread->right=current_thread;
 2d8:	f358                	sd	a4,160(a4)
 2da:	b77d                	j	288 <thread_exit+0x118>

00000000000002dc <dispatch>:
void dispatch(void){
 2dc:	1141                	addi	sp,sp,-16
 2de:	e406                	sd	ra,8(sp)
 2e0:	e022                	sd	s0,0(sp)
 2e2:	0800                	addi	s0,sp,16
    if (current_thread->buf_set)
 2e4:	00001517          	auipc	a0,0x1
 2e8:	93453503          	ld	a0,-1740(a0) # c18 <current_thread>
 2ec:	09452783          	lw	a5,148(a0)
 2f0:	eb9d                	bnez	a5,326 <dispatch+0x4a>
    if (setjmp(current_thread->env) == 0) {
 2f2:	00001517          	auipc	a0,0x1
 2f6:	92653503          	ld	a0,-1754(a0) # c18 <current_thread>
 2fa:	02050513          	addi	a0,a0,32
 2fe:	00001097          	auipc	ra,0x1
 302:	84e080e7          	jalr	-1970(ra) # b4c <setjmp>
 306:	c905                	beqz	a0,336 <dispatch+0x5a>
    current_thread->fp(current_thread->arg);
 308:	00001797          	auipc	a5,0x1
 30c:	9107b783          	ld	a5,-1776(a5) # c18 <current_thread>
 310:	6398                	ld	a4,0(a5)
 312:	6788                	ld	a0,8(a5)
 314:	9702                	jalr	a4
    thread_exit();
 316:	00000097          	auipc	ra,0x0
 31a:	e5a080e7          	jalr	-422(ra) # 170 <thread_exit>
}
 31e:	60a2                	ld	ra,8(sp)
 320:	6402                	ld	s0,0(sp)
 322:	0141                	addi	sp,sp,16
 324:	8082                	ret
        longjmp(current_thread->env, 1);
 326:	4585                	li	a1,1
 328:	02050513          	addi	a0,a0,32
 32c:	00001097          	auipc	ra,0x1
 330:	858080e7          	jalr	-1960(ra) # b84 <longjmp>
 334:	bf7d                	j	2f2 <dispatch+0x16>
        current_thread->env->sp = (unsigned long)current_thread->stack_p;
 336:	00001517          	auipc	a0,0x1
 33a:	8e253503          	ld	a0,-1822(a0) # c18 <current_thread>
 33e:	6d1c                	ld	a5,24(a0)
 340:	e55c                	sd	a5,136(a0)
        current_thread->buf_set = 1;
 342:	4785                	li	a5,1
 344:	08f52a23          	sw	a5,148(a0)
        longjmp(current_thread->env, 1);
 348:	4585                	li	a1,1
 34a:	02050513          	addi	a0,a0,32
 34e:	00001097          	auipc	ra,0x1
 352:	836080e7          	jalr	-1994(ra) # b84 <longjmp>
 356:	bf4d                	j	308 <dispatch+0x2c>

0000000000000358 <thread_yield>:
void thread_yield(void){
 358:	1141                	addi	sp,sp,-16
 35a:	e406                	sd	ra,8(sp)
 35c:	e022                	sd	s0,0(sp)
 35e:	0800                	addi	s0,sp,16
    if (setjmp(current_thread->env) == 0){     
 360:	00001517          	auipc	a0,0x1
 364:	8b853503          	ld	a0,-1864(a0) # c18 <current_thread>
 368:	02050513          	addi	a0,a0,32
 36c:	00000097          	auipc	ra,0x0
 370:	7e0080e7          	jalr	2016(ra) # b4c <setjmp>
 374:	c509                	beqz	a0,37e <thread_yield+0x26>
}
 376:	60a2                	ld	ra,8(sp)
 378:	6402                	ld	s0,0(sp)
 37a:	0141                	addi	sp,sp,16
 37c:	8082                	ret
        schedule();
 37e:	00000097          	auipc	ra,0x0
 382:	d50080e7          	jalr	-688(ra) # ce <schedule>
        dispatch();
 386:	00000097          	auipc	ra,0x0
 38a:	f56080e7          	jalr	-170(ra) # 2dc <dispatch>
}
 38e:	b7e5                	j	376 <thread_yield+0x1e>

0000000000000390 <thread_start_threading>:
void thread_start_threading(void){
 390:	1141                	addi	sp,sp,-16
 392:	e406                	sd	ra,8(sp)
 394:	e022                	sd	s0,0(sp)
 396:	0800                	addi	s0,sp,16
    // TODO
    if (setjmp(env_st) != 0) {
 398:	00001517          	auipc	a0,0x1
 39c:	89050513          	addi	a0,a0,-1904 # c28 <env_st>
 3a0:	00000097          	auipc	ra,0x0
 3a4:	7ac080e7          	jalr	1964(ra) # b4c <setjmp>
 3a8:	c509                	beqz	a0,3b2 <thread_start_threading+0x22>
        return;
    }
    schedule();
    dispatch();
}
 3aa:	60a2                	ld	ra,8(sp)
 3ac:	6402                	ld	s0,0(sp)
 3ae:	0141                	addi	sp,sp,16
 3b0:	8082                	ret
    schedule();
 3b2:	00000097          	auipc	ra,0x0
 3b6:	d1c080e7          	jalr	-740(ra) # ce <schedule>
    dispatch();
 3ba:	00000097          	auipc	ra,0x0
 3be:	f22080e7          	jalr	-222(ra) # 2dc <dispatch>
 3c2:	b7e5                	j	3aa <thread_start_threading+0x1a>

00000000000003c4 <strcpy>:
#include "kernel/fcntl.h"
#include "user/user.h"

char*
strcpy(char *s, const char *t)
{
 3c4:	1141                	addi	sp,sp,-16
 3c6:	e422                	sd	s0,8(sp)
 3c8:	0800                	addi	s0,sp,16
  char *os;

  os = s;
  while((*s++ = *t++) != 0)
 3ca:	87aa                	mv	a5,a0
 3cc:	0585                	addi	a1,a1,1
 3ce:	0785                	addi	a5,a5,1
 3d0:	fff5c703          	lbu	a4,-1(a1)
 3d4:	fee78fa3          	sb	a4,-1(a5)
 3d8:	fb75                	bnez	a4,3cc <strcpy+0x8>
    ;
  return os;
}
 3da:	6422                	ld	s0,8(sp)
 3dc:	0141                	addi	sp,sp,16
 3de:	8082                	ret

00000000000003e0 <strcmp>:

int
strcmp(const char *p, const char *q)
{
 3e0:	1141                	addi	sp,sp,-16
 3e2:	e422                	sd	s0,8(sp)
 3e4:	0800                	addi	s0,sp,16
  while(*p && *p == *q)
 3e6:	00054783          	lbu	a5,0(a0)
 3ea:	cb91                	beqz	a5,3fe <strcmp+0x1e>
 3ec:	0005c703          	lbu	a4,0(a1)
 3f0:	00f71763          	bne	a4,a5,3fe <strcmp+0x1e>
    p++, q++;
 3f4:	0505                	addi	a0,a0,1
 3f6:	0585                	addi	a1,a1,1
  while(*p && *p == *q)
 3f8:	00054783          	lbu	a5,0(a0)
 3fc:	fbe5                	bnez	a5,3ec <strcmp+0xc>
  return (uchar)*p - (uchar)*q;
 3fe:	0005c503          	lbu	a0,0(a1)
}
 402:	40a7853b          	subw	a0,a5,a0
 406:	6422                	ld	s0,8(sp)
 408:	0141                	addi	sp,sp,16
 40a:	8082                	ret

000000000000040c <strlen>:

uint
strlen(const char *s)
{
 40c:	1141                	addi	sp,sp,-16
 40e:	e422                	sd	s0,8(sp)
 410:	0800                	addi	s0,sp,16
  int n;

  for(n = 0; s[n]; n++)
 412:	00054783          	lbu	a5,0(a0)
 416:	cf91                	beqz	a5,432 <strlen+0x26>
 418:	0505                	addi	a0,a0,1
 41a:	87aa                	mv	a5,a0
 41c:	4685                	li	a3,1
 41e:	9e89                	subw	a3,a3,a0
 420:	00f6853b          	addw	a0,a3,a5
 424:	0785                	addi	a5,a5,1
 426:	fff7c703          	lbu	a4,-1(a5)
 42a:	fb7d                	bnez	a4,420 <strlen+0x14>
    ;
  return n;
}
 42c:	6422                	ld	s0,8(sp)
 42e:	0141                	addi	sp,sp,16
 430:	8082                	ret
  for(n = 0; s[n]; n++)
 432:	4501                	li	a0,0
 434:	bfe5                	j	42c <strlen+0x20>

0000000000000436 <memset>:

void*
memset(void *dst, int c, uint n)
{
 436:	1141                	addi	sp,sp,-16
 438:	e422                	sd	s0,8(sp)
 43a:	0800                	addi	s0,sp,16
  char *cdst = (char *) dst;
  int i;
  for(i = 0; i < n; i++){
 43c:	ca19                	beqz	a2,452 <memset+0x1c>
 43e:	87aa                	mv	a5,a0
 440:	1602                	slli	a2,a2,0x20
 442:	9201                	srli	a2,a2,0x20
 444:	00a60733          	add	a4,a2,a0
    cdst[i] = c;
 448:	00b78023          	sb	a1,0(a5)
  for(i = 0; i < n; i++){
 44c:	0785                	addi	a5,a5,1
 44e:	fee79de3          	bne	a5,a4,448 <memset+0x12>
  }
  return dst;
}
 452:	6422                	ld	s0,8(sp)
 454:	0141                	addi	sp,sp,16
 456:	8082                	ret

0000000000000458 <strchr>:

char*
strchr(const char *s, char c)
{
 458:	1141                	addi	sp,sp,-16
 45a:	e422                	sd	s0,8(sp)
 45c:	0800                	addi	s0,sp,16
  for(; *s; s++)
 45e:	00054783          	lbu	a5,0(a0)
 462:	cb99                	beqz	a5,478 <strchr+0x20>
    if(*s == c)
 464:	00f58763          	beq	a1,a5,472 <strchr+0x1a>
  for(; *s; s++)
 468:	0505                	addi	a0,a0,1
 46a:	00054783          	lbu	a5,0(a0)
 46e:	fbfd                	bnez	a5,464 <strchr+0xc>
      return (char*)s;
  return 0;
 470:	4501                	li	a0,0
}
 472:	6422                	ld	s0,8(sp)
 474:	0141                	addi	sp,sp,16
 476:	8082                	ret
  return 0;
 478:	4501                	li	a0,0
 47a:	bfe5                	j	472 <strchr+0x1a>

000000000000047c <gets>:

char*
gets(char *buf, int max)
{
 47c:	711d                	addi	sp,sp,-96
 47e:	ec86                	sd	ra,88(sp)
 480:	e8a2                	sd	s0,80(sp)
 482:	e4a6                	sd	s1,72(sp)
 484:	e0ca                	sd	s2,64(sp)
 486:	fc4e                	sd	s3,56(sp)
 488:	f852                	sd	s4,48(sp)
 48a:	f456                	sd	s5,40(sp)
 48c:	f05a                	sd	s6,32(sp)
 48e:	ec5e                	sd	s7,24(sp)
 490:	1080                	addi	s0,sp,96
 492:	8baa                	mv	s7,a0
 494:	8a2e                	mv	s4,a1
  int i, cc;
  char c;

  for(i=0; i+1 < max; ){
 496:	892a                	mv	s2,a0
 498:	4481                	li	s1,0
    cc = read(0, &c, 1);
    if(cc < 1)
      break;
    buf[i++] = c;
    if(c == '\n' || c == '\r')
 49a:	4aa9                	li	s5,10
 49c:	4b35                	li	s6,13
  for(i=0; i+1 < max; ){
 49e:	89a6                	mv	s3,s1
 4a0:	2485                	addiw	s1,s1,1
 4a2:	0344d863          	bge	s1,s4,4d2 <gets+0x56>
    cc = read(0, &c, 1);
 4a6:	4605                	li	a2,1
 4a8:	faf40593          	addi	a1,s0,-81
 4ac:	4501                	li	a0,0
 4ae:	00000097          	auipc	ra,0x0
 4b2:	19c080e7          	jalr	412(ra) # 64a <read>
    if(cc < 1)
 4b6:	00a05e63          	blez	a0,4d2 <gets+0x56>
    buf[i++] = c;
 4ba:	faf44783          	lbu	a5,-81(s0)
 4be:	00f90023          	sb	a5,0(s2)
    if(c == '\n' || c == '\r')
 4c2:	01578763          	beq	a5,s5,4d0 <gets+0x54>
 4c6:	0905                	addi	s2,s2,1
 4c8:	fd679be3          	bne	a5,s6,49e <gets+0x22>
  for(i=0; i+1 < max; ){
 4cc:	89a6                	mv	s3,s1
 4ce:	a011                	j	4d2 <gets+0x56>
 4d0:	89a6                	mv	s3,s1
      break;
  }
  buf[i] = '\0';
 4d2:	99de                	add	s3,s3,s7
 4d4:	00098023          	sb	zero,0(s3)
  return buf;
}
 4d8:	855e                	mv	a0,s7
 4da:	60e6                	ld	ra,88(sp)
 4dc:	6446                	ld	s0,80(sp)
 4de:	64a6                	ld	s1,72(sp)
 4e0:	6906                	ld	s2,64(sp)
 4e2:	79e2                	ld	s3,56(sp)
 4e4:	7a42                	ld	s4,48(sp)
 4e6:	7aa2                	ld	s5,40(sp)
 4e8:	7b02                	ld	s6,32(sp)
 4ea:	6be2                	ld	s7,24(sp)
 4ec:	6125                	addi	sp,sp,96
 4ee:	8082                	ret

00000000000004f0 <stat>:

int
stat(const char *n, struct stat *st)
{
 4f0:	1101                	addi	sp,sp,-32
 4f2:	ec06                	sd	ra,24(sp)
 4f4:	e822                	sd	s0,16(sp)
 4f6:	e426                	sd	s1,8(sp)
 4f8:	e04a                	sd	s2,0(sp)
 4fa:	1000                	addi	s0,sp,32
 4fc:	892e                	mv	s2,a1
  int fd;
  int r;

  fd = open(n, O_RDONLY);
 4fe:	4581                	li	a1,0
 500:	00000097          	auipc	ra,0x0
 504:	172080e7          	jalr	370(ra) # 672 <open>
  if(fd < 0)
 508:	02054563          	bltz	a0,532 <stat+0x42>
 50c:	84aa                	mv	s1,a0
    return -1;
  r = fstat(fd, st);
 50e:	85ca                	mv	a1,s2
 510:	00000097          	auipc	ra,0x0
 514:	17a080e7          	jalr	378(ra) # 68a <fstat>
 518:	892a                	mv	s2,a0
  close(fd);
 51a:	8526                	mv	a0,s1
 51c:	00000097          	auipc	ra,0x0
 520:	13e080e7          	jalr	318(ra) # 65a <close>
  return r;
}
 524:	854a                	mv	a0,s2
 526:	60e2                	ld	ra,24(sp)
 528:	6442                	ld	s0,16(sp)
 52a:	64a2                	ld	s1,8(sp)
 52c:	6902                	ld	s2,0(sp)
 52e:	6105                	addi	sp,sp,32
 530:	8082                	ret
    return -1;
 532:	597d                	li	s2,-1
 534:	bfc5                	j	524 <stat+0x34>

0000000000000536 <atoi>:

int
atoi(const char *s)
{
 536:	1141                	addi	sp,sp,-16
 538:	e422                	sd	s0,8(sp)
 53a:	0800                	addi	s0,sp,16
  int n;

  n = 0;
  while('0' <= *s && *s <= '9')
 53c:	00054603          	lbu	a2,0(a0)
 540:	fd06079b          	addiw	a5,a2,-48
 544:	0ff7f793          	andi	a5,a5,255
 548:	4725                	li	a4,9
 54a:	02f76963          	bltu	a4,a5,57c <atoi+0x46>
 54e:	86aa                	mv	a3,a0
  n = 0;
 550:	4501                	li	a0,0
  while('0' <= *s && *s <= '9')
 552:	45a5                	li	a1,9
    n = n*10 + *s++ - '0';
 554:	0685                	addi	a3,a3,1
 556:	0025179b          	slliw	a5,a0,0x2
 55a:	9fa9                	addw	a5,a5,a0
 55c:	0017979b          	slliw	a5,a5,0x1
 560:	9fb1                	addw	a5,a5,a2
 562:	fd07851b          	addiw	a0,a5,-48
  while('0' <= *s && *s <= '9')
 566:	0006c603          	lbu	a2,0(a3)
 56a:	fd06071b          	addiw	a4,a2,-48
 56e:	0ff77713          	andi	a4,a4,255
 572:	fee5f1e3          	bgeu	a1,a4,554 <atoi+0x1e>
  return n;
}
 576:	6422                	ld	s0,8(sp)
 578:	0141                	addi	sp,sp,16
 57a:	8082                	ret
  n = 0;
 57c:	4501                	li	a0,0
 57e:	bfe5                	j	576 <atoi+0x40>

0000000000000580 <memmove>:

void*
memmove(void *vdst, const void *vsrc, int n)
{
 580:	1141                	addi	sp,sp,-16
 582:	e422                	sd	s0,8(sp)
 584:	0800                	addi	s0,sp,16
  char *dst;
  const char *src;

  dst = vdst;
  src = vsrc;
  if (src > dst) {
 586:	02b57463          	bgeu	a0,a1,5ae <memmove+0x2e>
    while(n-- > 0)
 58a:	00c05f63          	blez	a2,5a8 <memmove+0x28>
 58e:	1602                	slli	a2,a2,0x20
 590:	9201                	srli	a2,a2,0x20
 592:	00c507b3          	add	a5,a0,a2
  dst = vdst;
 596:	872a                	mv	a4,a0
      *dst++ = *src++;
 598:	0585                	addi	a1,a1,1
 59a:	0705                	addi	a4,a4,1
 59c:	fff5c683          	lbu	a3,-1(a1)
 5a0:	fed70fa3          	sb	a3,-1(a4)
    while(n-- > 0)
 5a4:	fee79ae3          	bne	a5,a4,598 <memmove+0x18>
    src += n;
    while(n-- > 0)
      *--dst = *--src;
  }
  return vdst;
}
 5a8:	6422                	ld	s0,8(sp)
 5aa:	0141                	addi	sp,sp,16
 5ac:	8082                	ret
    dst += n;
 5ae:	00c50733          	add	a4,a0,a2
    src += n;
 5b2:	95b2                	add	a1,a1,a2
    while(n-- > 0)
 5b4:	fec05ae3          	blez	a2,5a8 <memmove+0x28>
 5b8:	fff6079b          	addiw	a5,a2,-1
 5bc:	1782                	slli	a5,a5,0x20
 5be:	9381                	srli	a5,a5,0x20
 5c0:	fff7c793          	not	a5,a5
 5c4:	97ba                	add	a5,a5,a4
      *--dst = *--src;
 5c6:	15fd                	addi	a1,a1,-1
 5c8:	177d                	addi	a4,a4,-1
 5ca:	0005c683          	lbu	a3,0(a1)
 5ce:	00d70023          	sb	a3,0(a4)
    while(n-- > 0)
 5d2:	fee79ae3          	bne	a5,a4,5c6 <memmove+0x46>
 5d6:	bfc9                	j	5a8 <memmove+0x28>

00000000000005d8 <memcmp>:

int
memcmp(const void *s1, const void *s2, uint n)
{
 5d8:	1141                	addi	sp,sp,-16
 5da:	e422                	sd	s0,8(sp)
 5dc:	0800                	addi	s0,sp,16
  const char *p1 = s1, *p2 = s2;
  while (n-- > 0) {
 5de:	ca05                	beqz	a2,60e <memcmp+0x36>
 5e0:	fff6069b          	addiw	a3,a2,-1
 5e4:	1682                	slli	a3,a3,0x20
 5e6:	9281                	srli	a3,a3,0x20
 5e8:	0685                	addi	a3,a3,1
 5ea:	96aa                	add	a3,a3,a0
    if (*p1 != *p2) {
 5ec:	00054783          	lbu	a5,0(a0)
 5f0:	0005c703          	lbu	a4,0(a1)
 5f4:	00e79863          	bne	a5,a4,604 <memcmp+0x2c>
      return *p1 - *p2;
    }
    p1++;
 5f8:	0505                	addi	a0,a0,1
    p2++;
 5fa:	0585                	addi	a1,a1,1
  while (n-- > 0) {
 5fc:	fed518e3          	bne	a0,a3,5ec <memcmp+0x14>
  }
  return 0;
 600:	4501                	li	a0,0
 602:	a019                	j	608 <memcmp+0x30>
      return *p1 - *p2;
 604:	40e7853b          	subw	a0,a5,a4
}
 608:	6422                	ld	s0,8(sp)
 60a:	0141                	addi	sp,sp,16
 60c:	8082                	ret
  return 0;
 60e:	4501                	li	a0,0
 610:	bfe5                	j	608 <memcmp+0x30>

0000000000000612 <memcpy>:

void *
memcpy(void *dst, const void *src, uint n)
{
 612:	1141                	addi	sp,sp,-16
 614:	e406                	sd	ra,8(sp)
 616:	e022                	sd	s0,0(sp)
 618:	0800                	addi	s0,sp,16
  return memmove(dst, src, n);
 61a:	00000097          	auipc	ra,0x0
 61e:	f66080e7          	jalr	-154(ra) # 580 <memmove>
}
 622:	60a2                	ld	ra,8(sp)
 624:	6402                	ld	s0,0(sp)
 626:	0141                	addi	sp,sp,16
 628:	8082                	ret

000000000000062a <fork>:
# generated by usys.pl - do not edit
#include "kernel/syscall.h"
.global fork
fork:
 li a7, SYS_fork
 62a:	4885                	li	a7,1
 ecall
 62c:	00000073          	ecall
 ret
 630:	8082                	ret

0000000000000632 <exit>:
.global exit
exit:
 li a7, SYS_exit
 632:	4889                	li	a7,2
 ecall
 634:	00000073          	ecall
 ret
 638:	8082                	ret

000000000000063a <wait>:
.global wait
wait:
 li a7, SYS_wait
 63a:	488d                	li	a7,3
 ecall
 63c:	00000073          	ecall
 ret
 640:	8082                	ret

0000000000000642 <pipe>:
.global pipe
pipe:
 li a7, SYS_pipe
 642:	4891                	li	a7,4
 ecall
 644:	00000073          	ecall
 ret
 648:	8082                	ret

000000000000064a <read>:
.global read
read:
 li a7, SYS_read
 64a:	4895                	li	a7,5
 ecall
 64c:	00000073          	ecall
 ret
 650:	8082                	ret

0000000000000652 <write>:
.global write
write:
 li a7, SYS_write
 652:	48c1                	li	a7,16
 ecall
 654:	00000073          	ecall
 ret
 658:	8082                	ret

000000000000065a <close>:
.global close
close:
 li a7, SYS_close
 65a:	48d5                	li	a7,21
 ecall
 65c:	00000073          	ecall
 ret
 660:	8082                	ret

0000000000000662 <kill>:
.global kill
kill:
 li a7, SYS_kill
 662:	4899                	li	a7,6
 ecall
 664:	00000073          	ecall
 ret
 668:	8082                	ret

000000000000066a <exec>:
.global exec
exec:
 li a7, SYS_exec
 66a:	489d                	li	a7,7
 ecall
 66c:	00000073          	ecall
 ret
 670:	8082                	ret

0000000000000672 <open>:
.global open
open:
 li a7, SYS_open
 672:	48bd                	li	a7,15
 ecall
 674:	00000073          	ecall
 ret
 678:	8082                	ret

000000000000067a <mknod>:
.global mknod
mknod:
 li a7, SYS_mknod
 67a:	48c5                	li	a7,17
 ecall
 67c:	00000073          	ecall
 ret
 680:	8082                	ret

0000000000000682 <unlink>:
.global unlink
unlink:
 li a7, SYS_unlink
 682:	48c9                	li	a7,18
 ecall
 684:	00000073          	ecall
 ret
 688:	8082                	ret

000000000000068a <fstat>:
.global fstat
fstat:
 li a7, SYS_fstat
 68a:	48a1                	li	a7,8
 ecall
 68c:	00000073          	ecall
 ret
 690:	8082                	ret

0000000000000692 <link>:
.global link
link:
 li a7, SYS_link
 692:	48cd                	li	a7,19
 ecall
 694:	00000073          	ecall
 ret
 698:	8082                	ret

000000000000069a <mkdir>:
.global mkdir
mkdir:
 li a7, SYS_mkdir
 69a:	48d1                	li	a7,20
 ecall
 69c:	00000073          	ecall
 ret
 6a0:	8082                	ret

00000000000006a2 <chdir>:
.global chdir
chdir:
 li a7, SYS_chdir
 6a2:	48a5                	li	a7,9
 ecall
 6a4:	00000073          	ecall
 ret
 6a8:	8082                	ret

00000000000006aa <dup>:
.global dup
dup:
 li a7, SYS_dup
 6aa:	48a9                	li	a7,10
 ecall
 6ac:	00000073          	ecall
 ret
 6b0:	8082                	ret

00000000000006b2 <getpid>:
.global getpid
getpid:
 li a7, SYS_getpid
 6b2:	48ad                	li	a7,11
 ecall
 6b4:	00000073          	ecall
 ret
 6b8:	8082                	ret

00000000000006ba <sbrk>:
.global sbrk
sbrk:
 li a7, SYS_sbrk
 6ba:	48b1                	li	a7,12
 ecall
 6bc:	00000073          	ecall
 ret
 6c0:	8082                	ret

00000000000006c2 <sleep>:
.global sleep
sleep:
 li a7, SYS_sleep
 6c2:	48b5                	li	a7,13
 ecall
 6c4:	00000073          	ecall
 ret
 6c8:	8082                	ret

00000000000006ca <uptime>:
.global uptime
uptime:
 li a7, SYS_uptime
 6ca:	48b9                	li	a7,14
 ecall
 6cc:	00000073          	ecall
 ret
 6d0:	8082                	ret

00000000000006d2 <putc>:

static char digits[] = "0123456789ABCDEF";

static void
putc(int fd, char c)
{
 6d2:	1101                	addi	sp,sp,-32
 6d4:	ec06                	sd	ra,24(sp)
 6d6:	e822                	sd	s0,16(sp)
 6d8:	1000                	addi	s0,sp,32
 6da:	feb407a3          	sb	a1,-17(s0)
  write(fd, &c, 1);
 6de:	4605                	li	a2,1
 6e0:	fef40593          	addi	a1,s0,-17
 6e4:	00000097          	auipc	ra,0x0
 6e8:	f6e080e7          	jalr	-146(ra) # 652 <write>
}
 6ec:	60e2                	ld	ra,24(sp)
 6ee:	6442                	ld	s0,16(sp)
 6f0:	6105                	addi	sp,sp,32
 6f2:	8082                	ret

00000000000006f4 <printint>:

static void
printint(int fd, int xx, int base, int sgn)
{
 6f4:	7139                	addi	sp,sp,-64
 6f6:	fc06                	sd	ra,56(sp)
 6f8:	f822                	sd	s0,48(sp)
 6fa:	f426                	sd	s1,40(sp)
 6fc:	f04a                	sd	s2,32(sp)
 6fe:	ec4e                	sd	s3,24(sp)
 700:	0080                	addi	s0,sp,64
 702:	84aa                	mv	s1,a0
  char buf[16];
  int i, neg;
  uint x;

  neg = 0;
  if(sgn && xx < 0){
 704:	c299                	beqz	a3,70a <printint+0x16>
 706:	0805c863          	bltz	a1,796 <printint+0xa2>
    neg = 1;
    x = -xx;
  } else {
    x = xx;
 70a:	2581                	sext.w	a1,a1
  neg = 0;
 70c:	4881                	li	a7,0
 70e:	fc040693          	addi	a3,s0,-64
  }

  i = 0;
 712:	4701                	li	a4,0
  do{
    buf[i++] = digits[x % base];
 714:	2601                	sext.w	a2,a2
 716:	00000517          	auipc	a0,0x0
 71a:	4ea50513          	addi	a0,a0,1258 # c00 <digits>
 71e:	883a                	mv	a6,a4
 720:	2705                	addiw	a4,a4,1
 722:	02c5f7bb          	remuw	a5,a1,a2
 726:	1782                	slli	a5,a5,0x20
 728:	9381                	srli	a5,a5,0x20
 72a:	97aa                	add	a5,a5,a0
 72c:	0007c783          	lbu	a5,0(a5)
 730:	00f68023          	sb	a5,0(a3)
  }while((x /= base) != 0);
 734:	0005879b          	sext.w	a5,a1
 738:	02c5d5bb          	divuw	a1,a1,a2
 73c:	0685                	addi	a3,a3,1
 73e:	fec7f0e3          	bgeu	a5,a2,71e <printint+0x2a>
  if(neg)
 742:	00088b63          	beqz	a7,758 <printint+0x64>
    buf[i++] = '-';
 746:	fd040793          	addi	a5,s0,-48
 74a:	973e                	add	a4,a4,a5
 74c:	02d00793          	li	a5,45
 750:	fef70823          	sb	a5,-16(a4)
 754:	0028071b          	addiw	a4,a6,2

  while(--i >= 0)
 758:	02e05863          	blez	a4,788 <printint+0x94>
 75c:	fc040793          	addi	a5,s0,-64
 760:	00e78933          	add	s2,a5,a4
 764:	fff78993          	addi	s3,a5,-1
 768:	99ba                	add	s3,s3,a4
 76a:	377d                	addiw	a4,a4,-1
 76c:	1702                	slli	a4,a4,0x20
 76e:	9301                	srli	a4,a4,0x20
 770:	40e989b3          	sub	s3,s3,a4
    putc(fd, buf[i]);
 774:	fff94583          	lbu	a1,-1(s2)
 778:	8526                	mv	a0,s1
 77a:	00000097          	auipc	ra,0x0
 77e:	f58080e7          	jalr	-168(ra) # 6d2 <putc>
  while(--i >= 0)
 782:	197d                	addi	s2,s2,-1
 784:	ff3918e3          	bne	s2,s3,774 <printint+0x80>
}
 788:	70e2                	ld	ra,56(sp)
 78a:	7442                	ld	s0,48(sp)
 78c:	74a2                	ld	s1,40(sp)
 78e:	7902                	ld	s2,32(sp)
 790:	69e2                	ld	s3,24(sp)
 792:	6121                	addi	sp,sp,64
 794:	8082                	ret
    x = -xx;
 796:	40b005bb          	negw	a1,a1
    neg = 1;
 79a:	4885                	li	a7,1
    x = -xx;
 79c:	bf8d                	j	70e <printint+0x1a>

000000000000079e <vprintf>:
}

// Print to the given fd. Only understands %d, %x, %p, %s.
void
vprintf(int fd, const char *fmt, va_list ap)
{
 79e:	7119                	addi	sp,sp,-128
 7a0:	fc86                	sd	ra,120(sp)
 7a2:	f8a2                	sd	s0,112(sp)
 7a4:	f4a6                	sd	s1,104(sp)
 7a6:	f0ca                	sd	s2,96(sp)
 7a8:	ecce                	sd	s3,88(sp)
 7aa:	e8d2                	sd	s4,80(sp)
 7ac:	e4d6                	sd	s5,72(sp)
 7ae:	e0da                	sd	s6,64(sp)
 7b0:	fc5e                	sd	s7,56(sp)
 7b2:	f862                	sd	s8,48(sp)
 7b4:	f466                	sd	s9,40(sp)
 7b6:	f06a                	sd	s10,32(sp)
 7b8:	ec6e                	sd	s11,24(sp)
 7ba:	0100                	addi	s0,sp,128
  char *s;
  int c, i, state;

  state = 0;
  for(i = 0; fmt[i]; i++){
 7bc:	0005c903          	lbu	s2,0(a1)
 7c0:	18090f63          	beqz	s2,95e <vprintf+0x1c0>
 7c4:	8aaa                	mv	s5,a0
 7c6:	8b32                	mv	s6,a2
 7c8:	00158493          	addi	s1,a1,1
  state = 0;
 7cc:	4981                	li	s3,0
      if(c == '%'){
        state = '%';
      } else {
        putc(fd, c);
      }
    } else if(state == '%'){
 7ce:	02500a13          	li	s4,37
      if(c == 'd'){
 7d2:	06400c13          	li	s8,100
        printint(fd, va_arg(ap, int), 10, 1);
      } else if(c == 'l') {
 7d6:	06c00c93          	li	s9,108
        printint(fd, va_arg(ap, uint64), 10, 0);
      } else if(c == 'x') {
 7da:	07800d13          	li	s10,120
        printint(fd, va_arg(ap, int), 16, 0);
      } else if(c == 'p') {
 7de:	07000d93          	li	s11,112
    putc(fd, digits[x >> (sizeof(uint64) * 8 - 4)]);
 7e2:	00000b97          	auipc	s7,0x0
 7e6:	41eb8b93          	addi	s7,s7,1054 # c00 <digits>
 7ea:	a839                	j	808 <vprintf+0x6a>
        putc(fd, c);
 7ec:	85ca                	mv	a1,s2
 7ee:	8556                	mv	a0,s5
 7f0:	00000097          	auipc	ra,0x0
 7f4:	ee2080e7          	jalr	-286(ra) # 6d2 <putc>
 7f8:	a019                	j	7fe <vprintf+0x60>
    } else if(state == '%'){
 7fa:	01498f63          	beq	s3,s4,818 <vprintf+0x7a>
  for(i = 0; fmt[i]; i++){
 7fe:	0485                	addi	s1,s1,1
 800:	fff4c903          	lbu	s2,-1(s1)
 804:	14090d63          	beqz	s2,95e <vprintf+0x1c0>
    c = fmt[i] & 0xff;
 808:	0009079b          	sext.w	a5,s2
    if(state == 0){
 80c:	fe0997e3          	bnez	s3,7fa <vprintf+0x5c>
      if(c == '%'){
 810:	fd479ee3          	bne	a5,s4,7ec <vprintf+0x4e>
        state = '%';
 814:	89be                	mv	s3,a5
 816:	b7e5                	j	7fe <vprintf+0x60>
      if(c == 'd'){
 818:	05878063          	beq	a5,s8,858 <vprintf+0xba>
      } else if(c == 'l') {
 81c:	05978c63          	beq	a5,s9,874 <vprintf+0xd6>
      } else if(c == 'x') {
 820:	07a78863          	beq	a5,s10,890 <vprintf+0xf2>
      } else if(c == 'p') {
 824:	09b78463          	beq	a5,s11,8ac <vprintf+0x10e>
        printptr(fd, va_arg(ap, uint64));
      } else if(c == 's'){
 828:	07300713          	li	a4,115
 82c:	0ce78663          	beq	a5,a4,8f8 <vprintf+0x15a>
          s = "(null)";
        while(*s != 0){
          putc(fd, *s);
          s++;
        }
      } else if(c == 'c'){
 830:	06300713          	li	a4,99
 834:	0ee78e63          	beq	a5,a4,930 <vprintf+0x192>
        putc(fd, va_arg(ap, uint));
      } else if(c == '%'){
 838:	11478863          	beq	a5,s4,948 <vprintf+0x1aa>
        putc(fd, c);
      } else {
        // Unknown % sequence.  Print it to draw attention.
        putc(fd, '%');
 83c:	85d2                	mv	a1,s4
 83e:	8556                	mv	a0,s5
 840:	00000097          	auipc	ra,0x0
 844:	e92080e7          	jalr	-366(ra) # 6d2 <putc>
        putc(fd, c);
 848:	85ca                	mv	a1,s2
 84a:	8556                	mv	a0,s5
 84c:	00000097          	auipc	ra,0x0
 850:	e86080e7          	jalr	-378(ra) # 6d2 <putc>
      }
      state = 0;
 854:	4981                	li	s3,0
 856:	b765                	j	7fe <vprintf+0x60>
        printint(fd, va_arg(ap, int), 10, 1);
 858:	008b0913          	addi	s2,s6,8
 85c:	4685                	li	a3,1
 85e:	4629                	li	a2,10
 860:	000b2583          	lw	a1,0(s6)
 864:	8556                	mv	a0,s5
 866:	00000097          	auipc	ra,0x0
 86a:	e8e080e7          	jalr	-370(ra) # 6f4 <printint>
 86e:	8b4a                	mv	s6,s2
      state = 0;
 870:	4981                	li	s3,0
 872:	b771                	j	7fe <vprintf+0x60>
        printint(fd, va_arg(ap, uint64), 10, 0);
 874:	008b0913          	addi	s2,s6,8
 878:	4681                	li	a3,0
 87a:	4629                	li	a2,10
 87c:	000b2583          	lw	a1,0(s6)
 880:	8556                	mv	a0,s5
 882:	00000097          	auipc	ra,0x0
 886:	e72080e7          	jalr	-398(ra) # 6f4 <printint>
 88a:	8b4a                	mv	s6,s2
      state = 0;
 88c:	4981                	li	s3,0
 88e:	bf85                	j	7fe <vprintf+0x60>
        printint(fd, va_arg(ap, int), 16, 0);
 890:	008b0913          	addi	s2,s6,8
 894:	4681                	li	a3,0
 896:	4641                	li	a2,16
 898:	000b2583          	lw	a1,0(s6)
 89c:	8556                	mv	a0,s5
 89e:	00000097          	auipc	ra,0x0
 8a2:	e56080e7          	jalr	-426(ra) # 6f4 <printint>
 8a6:	8b4a                	mv	s6,s2
      state = 0;
 8a8:	4981                	li	s3,0
 8aa:	bf91                	j	7fe <vprintf+0x60>
        printptr(fd, va_arg(ap, uint64));
 8ac:	008b0793          	addi	a5,s6,8
 8b0:	f8f43423          	sd	a5,-120(s0)
 8b4:	000b3983          	ld	s3,0(s6)
  putc(fd, '0');
 8b8:	03000593          	li	a1,48
 8bc:	8556                	mv	a0,s5
 8be:	00000097          	auipc	ra,0x0
 8c2:	e14080e7          	jalr	-492(ra) # 6d2 <putc>
  putc(fd, 'x');
 8c6:	85ea                	mv	a1,s10
 8c8:	8556                	mv	a0,s5
 8ca:	00000097          	auipc	ra,0x0
 8ce:	e08080e7          	jalr	-504(ra) # 6d2 <putc>
 8d2:	4941                	li	s2,16
    putc(fd, digits[x >> (sizeof(uint64) * 8 - 4)]);
 8d4:	03c9d793          	srli	a5,s3,0x3c
 8d8:	97de                	add	a5,a5,s7
 8da:	0007c583          	lbu	a1,0(a5)
 8de:	8556                	mv	a0,s5
 8e0:	00000097          	auipc	ra,0x0
 8e4:	df2080e7          	jalr	-526(ra) # 6d2 <putc>
  for (i = 0; i < (sizeof(uint64) * 2); i++, x <<= 4)
 8e8:	0992                	slli	s3,s3,0x4
 8ea:	397d                	addiw	s2,s2,-1
 8ec:	fe0914e3          	bnez	s2,8d4 <vprintf+0x136>
        printptr(fd, va_arg(ap, uint64));
 8f0:	f8843b03          	ld	s6,-120(s0)
      state = 0;
 8f4:	4981                	li	s3,0
 8f6:	b721                	j	7fe <vprintf+0x60>
        s = va_arg(ap, char*);
 8f8:	008b0993          	addi	s3,s6,8
 8fc:	000b3903          	ld	s2,0(s6)
        if(s == 0)
 900:	02090163          	beqz	s2,922 <vprintf+0x184>
        while(*s != 0){
 904:	00094583          	lbu	a1,0(s2)
 908:	c9a1                	beqz	a1,958 <vprintf+0x1ba>
          putc(fd, *s);
 90a:	8556                	mv	a0,s5
 90c:	00000097          	auipc	ra,0x0
 910:	dc6080e7          	jalr	-570(ra) # 6d2 <putc>
          s++;
 914:	0905                	addi	s2,s2,1
        while(*s != 0){
 916:	00094583          	lbu	a1,0(s2)
 91a:	f9e5                	bnez	a1,90a <vprintf+0x16c>
        s = va_arg(ap, char*);
 91c:	8b4e                	mv	s6,s3
      state = 0;
 91e:	4981                	li	s3,0
 920:	bdf9                	j	7fe <vprintf+0x60>
          s = "(null)";
 922:	00000917          	auipc	s2,0x0
 926:	2d690913          	addi	s2,s2,726 # bf8 <longjmp_1+0x3a>
        while(*s != 0){
 92a:	02800593          	li	a1,40
 92e:	bff1                	j	90a <vprintf+0x16c>
        putc(fd, va_arg(ap, uint));
 930:	008b0913          	addi	s2,s6,8
 934:	000b4583          	lbu	a1,0(s6)
 938:	8556                	mv	a0,s5
 93a:	00000097          	auipc	ra,0x0
 93e:	d98080e7          	jalr	-616(ra) # 6d2 <putc>
 942:	8b4a                	mv	s6,s2
      state = 0;
 944:	4981                	li	s3,0
 946:	bd65                	j	7fe <vprintf+0x60>
        putc(fd, c);
 948:	85d2                	mv	a1,s4
 94a:	8556                	mv	a0,s5
 94c:	00000097          	auipc	ra,0x0
 950:	d86080e7          	jalr	-634(ra) # 6d2 <putc>
      state = 0;
 954:	4981                	li	s3,0
 956:	b565                	j	7fe <vprintf+0x60>
        s = va_arg(ap, char*);
 958:	8b4e                	mv	s6,s3
      state = 0;
 95a:	4981                	li	s3,0
 95c:	b54d                	j	7fe <vprintf+0x60>
    }
  }
}
 95e:	70e6                	ld	ra,120(sp)
 960:	7446                	ld	s0,112(sp)
 962:	74a6                	ld	s1,104(sp)
 964:	7906                	ld	s2,96(sp)
 966:	69e6                	ld	s3,88(sp)
 968:	6a46                	ld	s4,80(sp)
 96a:	6aa6                	ld	s5,72(sp)
 96c:	6b06                	ld	s6,64(sp)
 96e:	7be2                	ld	s7,56(sp)
 970:	7c42                	ld	s8,48(sp)
 972:	7ca2                	ld	s9,40(sp)
 974:	7d02                	ld	s10,32(sp)
 976:	6de2                	ld	s11,24(sp)
 978:	6109                	addi	sp,sp,128
 97a:	8082                	ret

000000000000097c <fprintf>:

void
fprintf(int fd, const char *fmt, ...)
{
 97c:	715d                	addi	sp,sp,-80
 97e:	ec06                	sd	ra,24(sp)
 980:	e822                	sd	s0,16(sp)
 982:	1000                	addi	s0,sp,32
 984:	e010                	sd	a2,0(s0)
 986:	e414                	sd	a3,8(s0)
 988:	e818                	sd	a4,16(s0)
 98a:	ec1c                	sd	a5,24(s0)
 98c:	03043023          	sd	a6,32(s0)
 990:	03143423          	sd	a7,40(s0)
  va_list ap;

  va_start(ap, fmt);
 994:	fe843423          	sd	s0,-24(s0)
  vprintf(fd, fmt, ap);
 998:	8622                	mv	a2,s0
 99a:	00000097          	auipc	ra,0x0
 99e:	e04080e7          	jalr	-508(ra) # 79e <vprintf>
}
 9a2:	60e2                	ld	ra,24(sp)
 9a4:	6442                	ld	s0,16(sp)
 9a6:	6161                	addi	sp,sp,80
 9a8:	8082                	ret

00000000000009aa <printf>:

void
printf(const char *fmt, ...)
{
 9aa:	711d                	addi	sp,sp,-96
 9ac:	ec06                	sd	ra,24(sp)
 9ae:	e822                	sd	s0,16(sp)
 9b0:	1000                	addi	s0,sp,32
 9b2:	e40c                	sd	a1,8(s0)
 9b4:	e810                	sd	a2,16(s0)
 9b6:	ec14                	sd	a3,24(s0)
 9b8:	f018                	sd	a4,32(s0)
 9ba:	f41c                	sd	a5,40(s0)
 9bc:	03043823          	sd	a6,48(s0)
 9c0:	03143c23          	sd	a7,56(s0)
  va_list ap;

  va_start(ap, fmt);
 9c4:	00840613          	addi	a2,s0,8
 9c8:	fec43423          	sd	a2,-24(s0)
  vprintf(1, fmt, ap);
 9cc:	85aa                	mv	a1,a0
 9ce:	4505                	li	a0,1
 9d0:	00000097          	auipc	ra,0x0
 9d4:	dce080e7          	jalr	-562(ra) # 79e <vprintf>
}
 9d8:	60e2                	ld	ra,24(sp)
 9da:	6442                	ld	s0,16(sp)
 9dc:	6125                	addi	sp,sp,96
 9de:	8082                	ret

00000000000009e0 <free>:
static Header base;
static Header *freep;

void
free(void *ap)
{
 9e0:	1141                	addi	sp,sp,-16
 9e2:	e422                	sd	s0,8(sp)
 9e4:	0800                	addi	s0,sp,16
  Header *bp, *p;

  bp = (Header*)ap - 1;
 9e6:	ff050693          	addi	a3,a0,-16
  for(p = freep; !(bp > p && bp < p->s.ptr); p = p->s.ptr)
 9ea:	00000797          	auipc	a5,0x0
 9ee:	2367b783          	ld	a5,566(a5) # c20 <freep>
 9f2:	a805                	j	a22 <free+0x42>
    if(p >= p->s.ptr && (bp > p || bp < p->s.ptr))
      break;
  if(bp + bp->s.size == p->s.ptr){
    bp->s.size += p->s.ptr->s.size;
 9f4:	4618                	lw	a4,8(a2)
 9f6:	9db9                	addw	a1,a1,a4
 9f8:	feb52c23          	sw	a1,-8(a0)
    bp->s.ptr = p->s.ptr->s.ptr;
 9fc:	6398                	ld	a4,0(a5)
 9fe:	6318                	ld	a4,0(a4)
 a00:	fee53823          	sd	a4,-16(a0)
 a04:	a091                	j	a48 <free+0x68>
  } else
    bp->s.ptr = p->s.ptr;
  if(p + p->s.size == bp){
    p->s.size += bp->s.size;
 a06:	ff852703          	lw	a4,-8(a0)
 a0a:	9e39                	addw	a2,a2,a4
 a0c:	c790                	sw	a2,8(a5)
    p->s.ptr = bp->s.ptr;
 a0e:	ff053703          	ld	a4,-16(a0)
 a12:	e398                	sd	a4,0(a5)
 a14:	a099                	j	a5a <free+0x7a>
    if(p >= p->s.ptr && (bp > p || bp < p->s.ptr))
 a16:	6398                	ld	a4,0(a5)
 a18:	00e7e463          	bltu	a5,a4,a20 <free+0x40>
 a1c:	00e6ea63          	bltu	a3,a4,a30 <free+0x50>
{
 a20:	87ba                	mv	a5,a4
  for(p = freep; !(bp > p && bp < p->s.ptr); p = p->s.ptr)
 a22:	fed7fae3          	bgeu	a5,a3,a16 <free+0x36>
 a26:	6398                	ld	a4,0(a5)
 a28:	00e6e463          	bltu	a3,a4,a30 <free+0x50>
    if(p >= p->s.ptr && (bp > p || bp < p->s.ptr))
 a2c:	fee7eae3          	bltu	a5,a4,a20 <free+0x40>
  if(bp + bp->s.size == p->s.ptr){
 a30:	ff852583          	lw	a1,-8(a0)
 a34:	6390                	ld	a2,0(a5)
 a36:	02059713          	slli	a4,a1,0x20
 a3a:	9301                	srli	a4,a4,0x20
 a3c:	0712                	slli	a4,a4,0x4
 a3e:	9736                	add	a4,a4,a3
 a40:	fae60ae3          	beq	a2,a4,9f4 <free+0x14>
    bp->s.ptr = p->s.ptr;
 a44:	fec53823          	sd	a2,-16(a0)
  if(p + p->s.size == bp){
 a48:	4790                	lw	a2,8(a5)
 a4a:	02061713          	slli	a4,a2,0x20
 a4e:	9301                	srli	a4,a4,0x20
 a50:	0712                	slli	a4,a4,0x4
 a52:	973e                	add	a4,a4,a5
 a54:	fae689e3          	beq	a3,a4,a06 <free+0x26>
  } else
    p->s.ptr = bp;
 a58:	e394                	sd	a3,0(a5)
  freep = p;
 a5a:	00000717          	auipc	a4,0x0
 a5e:	1cf73323          	sd	a5,454(a4) # c20 <freep>
}
 a62:	6422                	ld	s0,8(sp)
 a64:	0141                	addi	sp,sp,16
 a66:	8082                	ret

0000000000000a68 <malloc>:
  return freep;
}

void*
malloc(uint nbytes)
{
 a68:	7139                	addi	sp,sp,-64
 a6a:	fc06                	sd	ra,56(sp)
 a6c:	f822                	sd	s0,48(sp)
 a6e:	f426                	sd	s1,40(sp)
 a70:	f04a                	sd	s2,32(sp)
 a72:	ec4e                	sd	s3,24(sp)
 a74:	e852                	sd	s4,16(sp)
 a76:	e456                	sd	s5,8(sp)
 a78:	e05a                	sd	s6,0(sp)
 a7a:	0080                	addi	s0,sp,64
  Header *p, *prevp;
  uint nunits;

  nunits = (nbytes + sizeof(Header) - 1)/sizeof(Header) + 1;
 a7c:	02051493          	slli	s1,a0,0x20
 a80:	9081                	srli	s1,s1,0x20
 a82:	04bd                	addi	s1,s1,15
 a84:	8091                	srli	s1,s1,0x4
 a86:	0014899b          	addiw	s3,s1,1
 a8a:	0485                	addi	s1,s1,1
  if((prevp = freep) == 0){
 a8c:	00000517          	auipc	a0,0x0
 a90:	19453503          	ld	a0,404(a0) # c20 <freep>
 a94:	c515                	beqz	a0,ac0 <malloc+0x58>
    base.s.ptr = freep = prevp = &base;
    base.s.size = 0;
  }
  for(p = prevp->s.ptr; ; prevp = p, p = p->s.ptr){
 a96:	611c                	ld	a5,0(a0)
    if(p->s.size >= nunits){
 a98:	4798                	lw	a4,8(a5)
 a9a:	02977f63          	bgeu	a4,s1,ad8 <malloc+0x70>
 a9e:	8a4e                	mv	s4,s3
 aa0:	0009871b          	sext.w	a4,s3
 aa4:	6685                	lui	a3,0x1
 aa6:	00d77363          	bgeu	a4,a3,aac <malloc+0x44>
 aaa:	6a05                	lui	s4,0x1
 aac:	000a0b1b          	sext.w	s6,s4
  p = sbrk(nu * sizeof(Header));
 ab0:	004a1a1b          	slliw	s4,s4,0x4
        p->s.size = nunits;
      }
      freep = prevp;
      return (void*)(p + 1);
    }
    if(p == freep)
 ab4:	00000917          	auipc	s2,0x0
 ab8:	16c90913          	addi	s2,s2,364 # c20 <freep>
  if(p == (char*)-1)
 abc:	5afd                	li	s5,-1
 abe:	a88d                	j	b30 <malloc+0xc8>
    base.s.ptr = freep = prevp = &base;
 ac0:	00000797          	auipc	a5,0x0
 ac4:	1d878793          	addi	a5,a5,472 # c98 <base>
 ac8:	00000717          	auipc	a4,0x0
 acc:	14f73c23          	sd	a5,344(a4) # c20 <freep>
 ad0:	e39c                	sd	a5,0(a5)
    base.s.size = 0;
 ad2:	0007a423          	sw	zero,8(a5)
    if(p->s.size >= nunits){
 ad6:	b7e1                	j	a9e <malloc+0x36>
      if(p->s.size == nunits)
 ad8:	02e48b63          	beq	s1,a4,b0e <malloc+0xa6>
        p->s.size -= nunits;
 adc:	4137073b          	subw	a4,a4,s3
 ae0:	c798                	sw	a4,8(a5)
        p += p->s.size;
 ae2:	1702                	slli	a4,a4,0x20
 ae4:	9301                	srli	a4,a4,0x20
 ae6:	0712                	slli	a4,a4,0x4
 ae8:	97ba                	add	a5,a5,a4
        p->s.size = nunits;
 aea:	0137a423          	sw	s3,8(a5)
      freep = prevp;
 aee:	00000717          	auipc	a4,0x0
 af2:	12a73923          	sd	a0,306(a4) # c20 <freep>
      return (void*)(p + 1);
 af6:	01078513          	addi	a0,a5,16
      if((p = morecore(nunits)) == 0)
        return 0;
  }
}
 afa:	70e2                	ld	ra,56(sp)
 afc:	7442                	ld	s0,48(sp)
 afe:	74a2                	ld	s1,40(sp)
 b00:	7902                	ld	s2,32(sp)
 b02:	69e2                	ld	s3,24(sp)
 b04:	6a42                	ld	s4,16(sp)
 b06:	6aa2                	ld	s5,8(sp)
 b08:	6b02                	ld	s6,0(sp)
 b0a:	6121                	addi	sp,sp,64
 b0c:	8082                	ret
        prevp->s.ptr = p->s.ptr;
 b0e:	6398                	ld	a4,0(a5)
 b10:	e118                	sd	a4,0(a0)
 b12:	bff1                	j	aee <malloc+0x86>
  hp->s.size = nu;
 b14:	01652423          	sw	s6,8(a0)
  free((void*)(hp + 1));
 b18:	0541                	addi	a0,a0,16
 b1a:	00000097          	auipc	ra,0x0
 b1e:	ec6080e7          	jalr	-314(ra) # 9e0 <free>
  return freep;
 b22:	00093503          	ld	a0,0(s2)
      if((p = morecore(nunits)) == 0)
 b26:	d971                	beqz	a0,afa <malloc+0x92>
  for(p = prevp->s.ptr; ; prevp = p, p = p->s.ptr){
 b28:	611c                	ld	a5,0(a0)
    if(p->s.size >= nunits){
 b2a:	4798                	lw	a4,8(a5)
 b2c:	fa9776e3          	bgeu	a4,s1,ad8 <malloc+0x70>
    if(p == freep)
 b30:	00093703          	ld	a4,0(s2)
 b34:	853e                	mv	a0,a5
 b36:	fef719e3          	bne	a4,a5,b28 <malloc+0xc0>
  p = sbrk(nu * sizeof(Header));
 b3a:	8552                	mv	a0,s4
 b3c:	00000097          	auipc	ra,0x0
 b40:	b7e080e7          	jalr	-1154(ra) # 6ba <sbrk>
  if(p == (char*)-1)
 b44:	fd5518e3          	bne	a0,s5,b14 <malloc+0xac>
        return 0;
 b48:	4501                	li	a0,0
 b4a:	bf45                	j	afa <malloc+0x92>

0000000000000b4c <setjmp>:
 b4c:	e100                	sd	s0,0(a0)
 b4e:	e504                	sd	s1,8(a0)
 b50:	01253823          	sd	s2,16(a0)
 b54:	01353c23          	sd	s3,24(a0)
 b58:	03453023          	sd	s4,32(a0)
 b5c:	03553423          	sd	s5,40(a0)
 b60:	03653823          	sd	s6,48(a0)
 b64:	03753c23          	sd	s7,56(a0)
 b68:	05853023          	sd	s8,64(a0)
 b6c:	05953423          	sd	s9,72(a0)
 b70:	05a53823          	sd	s10,80(a0)
 b74:	05b53c23          	sd	s11,88(a0)
 b78:	06153023          	sd	ra,96(a0)
 b7c:	06253423          	sd	sp,104(a0)
 b80:	4501                	li	a0,0
 b82:	8082                	ret

0000000000000b84 <longjmp>:
 b84:	6100                	ld	s0,0(a0)
 b86:	6504                	ld	s1,8(a0)
 b88:	01053903          	ld	s2,16(a0)
 b8c:	01853983          	ld	s3,24(a0)
 b90:	02053a03          	ld	s4,32(a0)
 b94:	02853a83          	ld	s5,40(a0)
 b98:	03053b03          	ld	s6,48(a0)
 b9c:	03853b83          	ld	s7,56(a0)
 ba0:	04053c03          	ld	s8,64(a0)
 ba4:	04853c83          	ld	s9,72(a0)
 ba8:	05053d03          	ld	s10,80(a0)
 bac:	05853d83          	ld	s11,88(a0)
 bb0:	06053083          	ld	ra,96(a0)
 bb4:	06853103          	ld	sp,104(a0)
 bb8:	c199                	beqz	a1,bbe <longjmp_1>
 bba:	852e                	mv	a0,a1
 bbc:	8082                	ret

0000000000000bbe <longjmp_1>:
 bbe:	4505                	li	a0,1
 bc0:	8082                	ret
