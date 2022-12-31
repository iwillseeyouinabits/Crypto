import virtualbox
import time


class VMAPI:
    def __init__(self, shell) -> None:
        self.shell = shell

    def deploy(self):
        vbox = virtualbox.VirtualBox()
        session = virtualbox.Session()
        machine = vbox.find_machine("HostVM")
        progress = machine.launch_vm_process(session, "headless", [])
        progress.wait_for_completion()
        time.sleep(60)
        session.console.keyboard.put_keys("issinger\n")
        session.console.keyboard.put_keys("1234\n")
        session.console.keyboard.put_keys(self.shell + "\n")