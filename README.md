# multi_tasks
python3多进程处理任务模板

​	python的一个练手demo，之前遇到的很多处理多个文件数据的情况，就像写一个简单模板以便后续写小工具的时候节省时间。

​	目前这个demo模板还存在很对问题：

1. 进程间可能存在数据交换，目前使用queue队列进行数据共享，当交互数据过大时可能存在问题
2. 进程间的协同性还不行，目前用的时一个que_flag队列，生产者、消费者主进程循环监控队列来实现判断。用manager服务进程来协同进程间的信号应该更好一点。
3. 没有实现子进程的超时监控，主要还是想让子进程自己循环从队列中取任务来执行，这就照成了子进程自己不会知道自己的假死超时，需要在子进程没执行一个新任务时有一个信号通知监控进程。
