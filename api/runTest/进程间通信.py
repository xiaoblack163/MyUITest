from multiprocessing import Process, Manager
import time

def worker(shared_data):
    for i in range(5):
        shared_data['value'] = i
        time.sleep(1)

if __name__ == '__main__':
    manager = Manager()
    shared_data = manager.dict()

    # 创建子进程
    p = Process(target=worker, args=(shared_data,))
    p.start()

    # 主进程每秒读取共享数据
    for i in range(5):
        time.sleep(1)
        print(f"主进程读取到的数据: {shared_data['value']}")

    # 等待子进程完成
    p.join()

    # 输出最终的数据
    print(f"最终的数据: {shared_data['value']}")