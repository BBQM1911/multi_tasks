#coding=utf-8
import multiprocessing as mp
import time
import logging
logging.basicConfig(filename='tasks.log',level=logging.INFO,format='%(asctime)s %(levelname)s:%(message)s',filemode='w')
import argparse
import mybasetools

def do_task(task):
    return 0
def write_result(tasks):
    return 0

def sub_process(que_tasks,que_output,que_flag):
    '''
    '''
    #p=mp.current_process()
    #pid=str(p.pid)
    
    while not que_tasks.empty():
        task=que_tasks.get()
        try:
            #任务处理过程
            result=do_task(task)
            que_output.put(result)
            que_tasks.task_done()
        except Exception as e:
            logging.error(str(task)+'--task error::'+str(e),exc_info=True)
            que_tasks.task_done()
            continue
    
    que_flag.put(['sub_producer_over'])
    return 0

def sub_process_1(que_output,que_flag,break_amount):
    '''
    '''
    while True:
        #if not que_flag.empty():
            #f_list=que_flag.get()
            #if f_list[0]=='sub_producer_over':
                #break_amount=break_amount-1
        
        if que_output.empty():
            if que_flag.qsize()==break_amount:
                break
            time.sleep(2)
            continue

        task=que_output.get()
        try:
            #任务处理过程
            write_result(task)
            que_output.task_done()
        except Exception as e:
            logging.error(str(e),exc_info=True)
            que_output.task_done()
            continue
    return 0

def tasks_load(que_tasks,input_list,input_directory):
    '''
    将输入的数据处理后放入任务队列中
    输入任务判断处理可以在此处完成
    '''    
    tasks_num=0
    try:
        if input_list:
            with open(input_list,mode='r',encoding='utf-8') as f:
                for i in f.readlines:
                    s=i.strip()
                    if s:
                        que_tasks.put(s)
                        tasks_num+=1
                        
        if input_directory:
            for (root,dirs,files) in os.walk(input_directory):
                for file in files:
                    f_path=os.path.join(root,file)
                    que_tasks.put(f_path)
                    tasks_num+=1
        #if other:
            #pass
        time.sleep(3)
        if tasks_num==0 or que_tasks.empty():
            raise Exception("task load !error!,tasks amount:0")
        logging.info("task load complete,tasks amount："+str(tasks_num))
    except Exception as e:
        logging.error("Erorr tasks_load::"+str(e),exc_info=True)
        exit(1)
    return tasks_num

def main():
    logging.info('任务完成')
    pass

if __name__=='__main__':
    parser = argparse.ArgumentParser(description="程序开头描述",epilog="参数后显示信息")
    parser.add_argument("-l", help="任务列表输入,帮助信息")
    parser.add_argument("-d", help="任务文件目录输入,帮助信息")
    parser.add_argument("-o", help="输出,帮助信息")
    proc_num=mybasetools.getcpu_count()
    parser.add_argument("-p",type=int,default=proc_num,help="设置并行数")
    parser.add_argument("--timeout",type=int,default=None,help="子任务最大执行时间(超时时间),不设置及不进行子任务超时检查")
    args = parser.parse_args()
    
    que_tasks=mp.JoinableQueue()
    que_output=mp.JoinableQueue()
    que_flag=mp.Queue()
    tasks_amount=tasks_load(que_tasks,args.l,args.d)
    
    if args.p<2:args.p=2
    producer_amount=args.p-1
    for i in range(producer_amount):
        p=mp.Process(target=sub_process,args=(que_tasks,que_output,que_flag,))
        p.start()
    p=mp.Process(target=sub_process_1,args=(que_output,que_flag,producer_amount,args.o,))
    p.start()    
    
    #进程池内的进程间共享队列必须使用 Manager下的queue队列
    #if args.p<2:args.p=2
    #pool=mp.Pool(processes=args.p)
    #producer_amount=args.p-1
    #for i in range(producer_amount):
        #pool.apply_async(sub_process,(que_tasks,que_output,que_flag,))
    #pool.apply_async(sub_process_1,(que_output,que_flag,producer_amount,args.o,))
    #pool.close()
    #with mp.Pool(processes=args.p) as pool:
        #if args.p<2:args.p=2
        #producer_amount=args.p-1
        #for i in range(producer_amount):
            #pool.apply_async(sub_process,(que_tasks,que_output,que_flag,))
        #pool.apply_async(sub_process_1,(que_output,que_flag,producer_amount,args.o,))
        #pool.close()
    try:
        while not que_tasks.empty():
            print('tasks done:'+str(que_tasks.qsize())+'/'+str(tasks_amount))
            time.sleep(5)     
        que_tasks.join()
        que_output.join()
        #pool.join()        
    except KeyboardInterrupt:
        choice=input("强制退出，是否保存未完成的任务为列表quit_save.txt：[y,n]")
        if choice=='y':
            with open('quit_save.txt','w') as f:
                while not que_tasks.empty():
                    task=str(que_tasks.get())+'\n'
                    f.write(task)
        exit(1)
    
    main()
    
    