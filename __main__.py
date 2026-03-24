import os
import subprocess
import threading
import sys
from dotenv import load_dotenv
import tkinter as tk

from intervals import IntervalsAPI

FIND_REPLACE = {
    'Power3': 'Power',
    'Cadence3': 'Cadence'
}

class OutputRedirect:
    def __init__(self, widget):
        self.widget = widget

    def write(self, message):
        self.widget.after(0, self._safe_write, message)

    def _safe_write(self, message):
        self.widget.configure(state='normal')
        self.widget.insert(tk.END, message)
        self.widget.see(tk.END) # auto-scroll
        self.widget.configure(state='disabled')

    def flush(self):
        pass

def main() -> None:
    load_dotenv()
    API_KEY = os.getenv('INTERVALS_API_KEY')

    if API_KEY is None:
        raise ValueError("Intervals API key not found. Please set INTERVALS_API_KEY in your .env file.")

    intervals = IntervalsAPI(API_KEY)   
    
    root = tk.Tk()
    root.title("Intervals.icu Activity Repair")
    root.geometry('570x400')
    root.resizable(False, False)
    
    def go():
        url = url_var.get()
        
        segments = url.split('/')
        activity_id = segments[-1]
         
        def worker():
            fix_activity(intervals, activity_id)         

        t = threading.Thread(target=worker)
        t.start()
   
  
    url_var = tk.StringVar()
 
    label = tk.Label(root, text="Activity URL:").grid(row=0, column=0)
    tk.Entry(root, textvariable=url_var).grid(row=1, column=0)    
    
    tk.Button(root, text="Go!", command=go).grid(row=2, column=0)

    log_box = tk.Text(root)
    log_box.grid(row=3, column=0)
    sys.stdout = OutputRedirect(log_box)
    sys.stderr = OutputRedirect(log_box)

    root.mainloop()

def fix_activity(intervals: IntervalsAPI, activity_id: str):
    wd_path = 'data/'
    fit_path = wd_path + 'activity.fit'
    csv_path = wd_path + 'activity.csv'

    print(f"Getting activity {activity_id} from intervals")
    intervals.get_activity(activity_id, fit_path)

    print("Converting FIT to CSV")
    # Use the Garmin FitCSVTool jar to convert the FIT file to CSV
    subprocess.run(['java', '-jar', 'FitCSVTool.jar', '-b', fit_path, csv_path], stdout=subprocess.DEVNULL)

    print("Editing CSV")
    find_replace(csv_path, FIND_REPLACE)
    
    print("Converting modified CSV to FIT")
    # Convert back to FIT
    subprocess.run(['java', '-jar', 'FitCSVTool.jar', '-c', csv_path, fit_path], stdout=subprocess.DEVNULL)

    print("Putting new activity")
    #intervals.put_activity(fit_path)

    print(f"Deleting old activity {activity_id} from intervals")
    #intervals.delete_activity(activity_id)

    print("Done!")

def find_replace(fpath: str, find_replace: dict[str, str]):
    """Does find/replace on a file for a given set of values.

    :param fpath: Path to the file
    :type fpath: str
    :param find_replace: Dict where keys are what to find, values are what to replace with
    :type find_replace: dict[str, str]
    """
    with open(fpath, 'r') as f:
        csv_data = f.read()

    for k, v in find_replace.items():
        csv_data = csv_data.replace(k, v)

    with open(fpath, 'w') as f:
        f.write(csv_data)


if __name__ == "__main__":
    main()
