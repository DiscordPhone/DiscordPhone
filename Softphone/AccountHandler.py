
import threading
import pjsuaxt as pj
from .CallHandler import CallHandler

class AccountHandler(pj.AccountCallback):
    """ Handle callback events from account.
        This function handles everything that prepares for, and accepts call (before CallHandler).
        Account events are handled first, then we establish the call, and handle the call's callbacks with CallHandler.
    """

    sem = None

    def __init__(self, lib, account=None):
        pj.AccountCallback.__init__(self, account)  # Can this be written differently ? Python is dirty
        self.lib = lib


    def wait(self):
        """ Wait for the registration to finish.
        """
        self.sem = threading.Semaphore(0)
        self.sem.acquire()


    def on_reg_state(self):
        """ Stop waiting if the registration process has ended.
        """

        print("[AccountHandler]: Registration state: %s" % str(self.account.info().reg_status))
        if self.sem:
            if self.account.info().reg_status >= 200:
                self.sem.release()


    def on_incoming_call(self, call): # TODO: Add self.current_call here... somehow...
        """Notification and handling of an incoming call
        """

        print("[AccountHandler]: Call recieved: %s" % call)
        remote_uri = call.info().remote_uri

        if self.current_call or (remote_uri in "blacklist"):
            call.answer(486, "Busy")
            return # is this return needed?

        else:
            call_handler = CallHandler(lib=self.lib, call=call)
            call.set_callback(call_handler)
            call.answer(180) # why 180?
            print("[AccountHandler]: Answered incoming call from ", call.info().remote_uri)

