import sys
import subprocess
import threading
from sequence_filter import EOS


class TestProcessEngine(object):
    foreign_process = None
    target = "../sequence_filter/core.py"
    exit_code = 1
    timeout = 1

    def __init__(self):
        self.test_process = subprocess.Popen([sys.executable, self.target],
                                stdout = subprocess.PIPE, stdin=subprocess.PIPE)

    def run(self):
        event = threading.Event()
        test_thread = threading.Thread(target=self.test, args=(event,))
        monitor_thread = threading.Thread(target=self.watchDog, args=(event, self.timeout))
        test_thread.start()
        monitor_thread.start()
        test_thread.join()
        monitor_thread.join()
        sys.exit(self.exit_code)

    def test(self, event):
        sequence = ["", "", "abc", "123", "", "x", "", "", "", "", "y", "", ""]
        self.test_process.stdin.write("\n".join(sequence))
        self.test_process.stdin.write(EOS)
        out = [line.strip("\n") for line in self.test_process.stdout]
        assert out == ['abc', '123', '', 'x', '', 'y']
        event.set()
        self.exit_code = 0


    def watchDog(self, event, timeout):
        """
        event: threading.Event
        timeout: Int (in sec.)

        If anything goes wrong and test process doesn't respond.
        """
        event.wait(timeout)
        self.test_process.terminate()


def main():
    tpe = TestProcessEngine()
    tpe.run()


if __name__ == '__main__':
    main()