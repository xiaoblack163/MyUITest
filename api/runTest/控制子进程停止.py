import multiprocessing
import time
# from m_test_executor import TestExecutor 

# 子进程工作函数
def worker(stop_event,num):
    while not stop_event.is_set():
        print("子进程正在运行...")
        time.sleep(1)
        num+=1
    print("子进程已收到停止信号，正在退出...")

if __name__ == '__main__':
    # 创建Event对象用于进程间通信
    stop_event = multiprocessing.Event()
    num = 0
    # 创建并启动子进程
    process = multiprocessing.Process(target=worker, args=(stop_event,num))
    process.start()


    try:
        # 主进程继续做其他事情，比如监控或者等待用户输入
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # 如果用户中断（比如按Ctrl+C），则设置停止事件
        print("捕捉到中断信号，正在停止子进程...")
        stop_event.set()
        process.join()  # 等待子进程结束
    finally:
        # 如果子进程没有正常结束，则强制终止
        time.sleep(1)
        if process.is_alive():
            print("子进程未正常退出，正在强制终止...")
            process.terminate()
        print("所有子进程已停止，主进程退出。")