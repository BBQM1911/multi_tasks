
def getcpu_count():
    try:
        return mp.cpu_count()
    except Exception:
        return 2

def exit_check(proc_obj):
    '''
    检查所有子任务进程是否全部退出
    '''     
    if len(proc_obj.values())==0:
        print(str(len(proc_obj.values())))
        return True
    for l in proc_obj.values():
        if l[0].is_alive():
            return False
    return True

#ferror=open('error_task.txt','a',encoding='utf-8')
#while not exit_check(proc_obj):
    #'''
    #循环检查进程池中进程的状态如果有超时的任务结束进程，并将进程任务记录输出
    #再创建新的子任务进程到进程池
    #'''
    #for pid,pinfo in proc_obj.items():
        #if pinfo[0].exitcode:
            #del proc_obj[pid]
            #del manager_ptime[pid]
            #continue
        #usetime=manager_ptime[pid]['ptime']-pinfo[1]
        #if usetime>300:
            #pinfo[0].kill()
            #logging.warning("timeout_check::某个子任务运行超时,现已结束此任务记录至error_task.txt")
            #ferror.write(str(manager_ptime[pid]['task'])+",ErrorTimeout")
            #del proc_obj[pid]
            #del manager_ptime[pid]
            #p=mp.Process(target=sub_process,args=(que_tasks,manager_info,que_output))
            
        #else:
            #pinfo[1]=manager_ptime[pid][ptime]
    #time.sleep(5)
#ferror.close()
