import os
import signal
import sys
import psutil
import time
from daemon import DaemonContext

class MyDaemon(DaemonContext):
    def __init__(self, pidfile):
        super().__init__(pidfile=pidfile)

    def start(self):
        # Your daemon logic goes here
        print("My daemon is running...", os.getpid())
        for process in psutil.process_iter():
            if process.name() == "spt":
                # Check process status and perform actions
                if process.status() == "running":
                    print("Process 'spt' is running.")
                else:
                    print("Process 'spt' is not running! Restarting...")
                    break
        print("killing.....", os.getpid())
        time.sleep(2)
        os.kill(os.getpid(), signal.SIGTERM)
        return
                
    def stop(self):
        print("Stopping MyDaemon...")
        # Terminate any running processes
        for process in psutil.process_iter():
            if process.name() == "your_process_name":
                process.terminate()
        # Optionally: remove PID file
        os.remove(self.pidfile)

    def restart(self):
        print("Restarting MyDaemon...")
        self.stop()
        self.start()
    
    def stop(self):
        print("Stopping MyDaemon...")
        # Optionally: remove PID file
        os.remove(self.pidfile)
        self.stop()

# main class for the program
if __name__ == "__main__":
    pidfile = "./mydaemon.pid"
    daemon = MyDaemon(pidfile)

    if len(sys.argv) > 1:
        if sys.argv[1] == "start":
            daemon.start()
        elif sys.argv[1] == "stop":
            daemon.stop()
            sys.exit(0)
        elif sys.argv[1] == "restart":
            daemon.restart()
        else:
            print("Unknown command")
            sys.exit(1)
    else:
        daemon.start()