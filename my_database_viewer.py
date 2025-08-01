import sqlite3
import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


def read_tblRangeHitRate(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT Customer,TargetNoSKU,PurchaseSKU FROM tblRangeHitRate")
    return cursor.fetchall()

def read_customer():
    conn = open_file()
    tb1_data = read_tblRangeHitRate(conn)
    cursor = conn.cursor()
    cursor.execute("SELECT custCode, custName, mcpDay FROM tblCustomer")
    customer_data = cursor.fetchall()
    
    cust_lookup = {code: (name, mcp_day) for code, name, mcp_day in customer_data}
    
    for item1 in tb1_data:
        c_code = item1[0]
        
        cust_info = cust_lookup.get(c_code)
        if cust_info:
            cust_name, mcp_day = cust_info
            modefied_data = (cust_name,) + item1 + (mcp_day,)
            tree_data.append(modefied_data)
    if tree_data:
        update_treeview(tree_data)
        

def filter_view(day):
    days_dic = {"1": "MONDAY","2": "TUESDAY","3": "WEDNESDAY","4": "THURSDAY","5": "FRIDAY","6": "SATURDAY"}
    if tree_data:
        filter_data = [f for f in tree_data if f[4] == day]
        if not filter_data:
            filter_data = tree_data
        update_treeview(filter_data)
        if day == "0":
            days_label.config(text="All Days")
        else:
            days_label.config(text=f"{days_dic[str(day)]}")
    

def update_treeview(tree_data):
    treeview.delete(*treeview.get_children())  # Clear all rows
    hit_count = 0
    not_hit_count = 0
    for item in tree_data:
        range_status = "Hit" if item[3] >= item[2] else "Not Hit"
        tag = "hit" if range_status == "Hit" else "not_hit"
        if range_status == "Hit":
            hit_count += 1
        else:
            not_hit_count += 1
        allmcp_label.config(text=f"Total MCP: {len(tree_data)}")
        range_hit_label.config(text=f"Range Hit: {hit_count}")
        percent_hit = hit_count/len(tree_data)*100
        range_nothit_label.config(text=f"Balance Range: {not_hit_count}    ({percent_hit:.2f}%)")
        treeview.insert("", "end", values=(item[1], item[0], item[2], item[3], range_status),tags=(tag,))
        range_big(tree_data)
        range_small(tree_data)
        


def range_big(data):
    big_count = [f for f in data if f[2] == 26]  # Filter accounts with TargetRange == 26
    range_big_total.config(text=f"Total Big Accounts: {len(big_count)}")

    if big_count:
        hit_count = sum(1 for item in big_count if item[3] >= 26)
        not_hit_count = len(big_count) - hit_count
        range_big_hit.config(text=f"Big Range Hit: {hit_count}")
        percent_hit = hit_count/len(big_count)*100
        range_big_balance.config(text=f"Big Range Balance: {not_hit_count}    ({percent_hit:.2f}%)")
    else:
        range_big_hit.config(text=f"Big Range Hit: 0")
        range_big_balance.config(text=f"Big Range Balance: 0")
        
def range_small(data):
    small_count = [f for f in data if f[2] == 15]  # Filter accounts with TargetRange == 26
    range_small_total.config(text=f"Total Small Accounts: {len(small_count)}")

    if small_count:
        hit_count = sum(1 for item in small_count if item[3] >= 15)
        not_hit_count = len(small_count) - hit_count
        range_small_hit.config(text=f"Small Range Hit: {hit_count}")
        percent_hit = hit_count/len(small_count)*100
        range_small_balance.config(text=f"Small Range Balance: {not_hit_count}     ({percent_hit:.2f}%)")
        
def open_file():
    file_path = filedialog.askopenfilename(
        title="Select an Excel File",
        filetypes=[("SQLite Files", "*.db *.sqlite"), ("All Files", "*.*")]
    )
    if file_path:
        #full_path = os.path.join(os.getcwd(), file_path)
        if file_entry:
            file_entry.delete(0, "end")
            file_entry.insert(0, file_path)
        try:
           conn = sqlite3.connect(file_path)
           return conn
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")


root = tk.Tk()
root.title("DataBase Reader")
root.geometry("1000x600")
tree_data = []
header_frame = tk.Frame(root)
header_frame.pack(side=tk.TOP, fill=tk.X)
#MCP Days Buttons
all_button = tk.Button(header_frame, text="All",relief=tk.FLAT, command=lambda: filter_view("0"))
all_button.pack(side=tk.LEFT, padx=2, pady=2)
monday_button = tk.Button(header_frame, text="MONDAY",relief=tk.FLAT, command=lambda: filter_view("1"))
monday_button.pack(side=tk.LEFT, padx=2, pady=2)
tuesday_button = tk.Button(header_frame, text="TUESDAY",relief=tk.FLAT, command=lambda: filter_view("2"))
tuesday_button.pack(side=tk.LEFT, padx=2, pady=2)
wednesday_button = tk.Button(header_frame, text="WEDNESDAY",relief=tk.FLAT, command=lambda: filter_view("3"))
wednesday_button.pack(side=tk.LEFT, padx=2, pady=2)
thursday_button = tk.Button(header_frame, text="THURSDAY",relief=tk.FLAT, command=lambda: filter_view("4"))
thursday_button.pack(side=tk.LEFT, padx=2, pady=2)
friday_button = tk.Button(header_frame, text="FRIDAY",relief=tk.FLAT, command=lambda: filter_view("5"))
friday_button.pack(side=tk.LEFT, padx=2, pady=2)
sunday_button = tk.Button(header_frame, text="SATURDAY",relief=tk.FLAT, command=lambda: filter_view("6"))
sunday_button.pack(side=tk.LEFT, padx=2, pady=2)
stock_list_button = tk.Button(header_frame, text="Stocks List",relief=tk.FLAT, command=None)
stock_list_button.pack(side=tk.LEFT, padx=2, pady=2)

frame_left = tk.Frame(root)
frame_left.pack(side="left", fill="both", expand=True, padx=10, pady=10)
frame_right = tk.Frame(root)
frame_right.pack(side="right", fill="both", expand=True, padx=10, pady=10)
#Tree View
treeview = ttk.Treeview(frame_left, columns=("Cust Code", "Customer Name", "TargetRange", "RangeHit", "Status"), show="headings",height=8)
treeview.heading("Cust Code", text="Cust Code", anchor="w")
treeview.heading("Customer Name", text="Customer Name", anchor="w")
treeview.heading("TargetRange", text="TargetRange", anchor="w")
treeview.heading("RangeHit", text="RangeHit", anchor="w")
treeview.heading("Status", text="Status", anchor="w")
# Set column widths
treeview.column("Cust Code", width=200, anchor="w")
treeview.column("Customer Name", width=200, anchor="w")
treeview.column("TargetRange", width=60, anchor="w")
treeview.column("RangeHit", width=60, anchor="w")
treeview.column("Status", width=60, anchor="w")
treeview.pack(fill="both", expand=True, pady=5, padx=5)
treeview.tag_configure("hit", background="lightgreen")
treeview.tag_configure("not_hit", background="lightcoral")
#File Picker
frame = tk.Frame(frame_right)
frame.pack(anchor="nw",pady=5)
add_file_button = tk.Button(frame, text="Open Database", command=read_customer)
add_file_button.pack(side="left",pady=5)
file_entry = tk.Entry(frame, width=50)
file_entry.pack(side="left",padx=5,pady=5)
#Days Label
days_label = tk.Label(frame_right, text="Days",font=("Arial", 12, "bold"))
days_label.pack(anchor="nw", padx=5)
#Total Range Label
frame_label = tk.LabelFrame(frame_right, relief="raised",bd=5)
frame_label.pack(anchor="nw",fill="x",pady=5)
allmcp_label = tk.Label(frame_label, text="",font=("Arial", 12, "bold"))
allmcp_label.pack(anchor="nw", padx=5)
range_hit_label = tk.Label(frame_label, text="",font=("Arial", 12, "bold"))
range_hit_label.pack(anchor="nw", padx=5)
range_nothit_label = tk.Label(frame_label, text="",font=("Arial", 12, "bold"))
range_nothit_label.pack(anchor="nw", padx=5)
#Big Range Label
frame_label = tk.LabelFrame(frame_right, relief="raised", bd=5)
frame_label.pack(anchor="nw",fill="x",pady=5)
range_big_total = tk.Label(frame_label, text="",font=("Arial", 12, "bold"))
range_big_total.pack(anchor="nw", padx=5)
range_big_hit= tk.Label(frame_label, text="",font=("Arial", 12, "bold"))
range_big_hit.pack(anchor="nw", padx=5)
range_big_balance = tk.Label(frame_label, text="",font=("Arial", 12, "bold"))
range_big_balance.pack(anchor="nw", padx=5)
#Small Range Labels
frame_label = tk.LabelFrame(frame_right, relief="raised", bd=5)
frame_label.pack(anchor="nw",fill="x",pady=5)
range_small_total = tk.Label(frame_label, text="",font=("Arial", 12, "bold"))
range_small_total.pack(anchor="nw", padx=5)
range_small_hit= tk.Label(frame_label, text="",font=("Arial", 12, "bold"))
range_small_hit.pack(anchor="nw", padx=5)
range_small_balance = tk.Label(frame_label, text="",font=("Arial", 12, "bold"))
range_small_balance.pack(anchor="nw", padx=5)
root.mainloop()
