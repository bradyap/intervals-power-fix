import os
import subprocess
import threading
import sys
import tkinter as tk
from tkinter import simpledialog

from intervals import IntervalsAPI
from file_ops import get_api_key, set_api_key, find_replace, rmr


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
        self.widget.see(tk.END)
        self.widget.configure(state='disabled')

    def flush(self):
        pass


def main() -> None:
    root = tk.Tk()
    root.title("Intervals.icu Activity Repair")
    root.geometry('700x500')

    def go():
        url = url_var.get()

        segments = url.split('/')
        activity_id = segments[-1]

        def worker():
            fix_activity(intervals, activity_id)

        t = threading.Thread(target=worker)
        t.start()

    def config_api():
        nonlocal api_key, intervals

        new_key = simpledialog.askstring(
            "Input", "Enter your Intervals API Key:")
        if new_key:
            set_api_key(new_key)

            api_key = get_api_key()
            intervals = IntervalsAPI(api_key)
        else:
            print("No input provided.")

    def on_close():
        rmr('temp/')
        root.destroy()

    menu_bar = tk.Menu(root)
    settings_menu = tk.Menu(menu_bar, tearoff=0)
    settings_menu.add_command(label="Set API Key", command=config_api)
    menu_bar.add_cascade(label="Settings", menu=settings_menu)
    root.config(menu=menu_bar)

    url_var = tk.StringVar()

    tk.Label(root, text="Activity URL:").grid(row=0, column=0)
    tk.Entry(root, textvariable=url_var).grid(row=1, column=0)

    tk.Button(root, text="Go!", command=go).grid(row=2, column=0)

    log_box = tk.Text(root)
    log_box.grid(row=3, column=0)
    sys.stdout = OutputRedirect(log_box)
    sys.stderr = OutputRedirect(log_box)

    try:
        api_key = get_api_key()
        intervals = IntervalsAPI(api_key)
    except ValueError as e:
        print(f"Error: {e}")

    root.protocol("WM_DELETE_WINDOW", on_close)

    root.mainloop()


def fix_activity(intervals: IntervalsAPI, activity_id: str):
    wd_path = 'temp/'
    fit_path = wd_path + 'activity.fit'
    csv_path = wd_path + 'activity.csv'

    if not os.path.exists(wd_path):
        os.makedirs(wd_path)

    print(f"Getting activity {activity_id} from intervals")
    intervals.get_activity(activity_id, fit_path)

    print("Converting FIT to CSV")
    # Use the Garmin FitCSVTool jar to convert the FIT file to CSV
    subprocess.run(['java', '-jar', 'FitCSVTool.jar', '-b',
                   fit_path, csv_path], stdout=subprocess.DEVNULL)

    print("Editing CSV")
    find_replace(csv_path, FIND_REPLACE)

    print("Converting modified CSV to FIT")
    # Convert back to FIT
    subprocess.run(['java', '-jar', 'FitCSVTool.jar', '-c',
                   csv_path, fit_path], stdout=subprocess.DEVNULL)

    print("Putting new activity")
    intervals.put_activity(fit_path)

    print(f"Deleting old activity {activity_id} from intervals")
    intervals.delete_activity(activity_id)

    print("Done!")


if __name__ == "__main__":
    main()
