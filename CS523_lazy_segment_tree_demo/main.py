from LazySegmentTree import *
from collections import deque
from copy import deepcopy
from tkinter import *

s_width = 10  #Chiều rộng widget label nhỏ
l_width = 70  #Chiều rộng widget label lớn

x_pad = 5
y_pad = 5

canvas_width = 1000
canvas_height = 530

arr_canv_w = 850
arr_canv_h = 30

sgtree = SegmentTree()

def display_arr(arr = [], canv = None, highlight = [], cmp_arr = []):
  canv.delete("all")

  if cmp_arr == []:
    cmp_arr = arr

  for i in range(len(arr)):
    text_x = 20 + i * 30
    text_y = arr_canv_h / 3 * 2
    if (i in highlight) or (arr[i] != cmp_arr[i]):
      canv.create_text(text_x, text_y,
                       text=(str(arr[i])),
                       font=("Arial", 16),
                       fill="red")
    else:
      canv.create_text(text_x, text_y,
                       text=(str(arr[i])),
                       font=("Arial", 16),
                       fill="black")

def display_tree(sgt = None):
  visualizer.delete("all")

  queue = deque()
  queue.append({"node": 0,
                "parent": None,
                "range": [0, sgt.n - 1]})
  level = 0
  while queue:
    level_size = len(queue)

    for i in range(level_size):
      item = queue.popleft()
      parent = item["parent"]
      node = item["node"]
      node_range = item["range"]

      text_x = (canvas_width / (level_size + 1)) * (i + 1)
      text_y = 50 + 100 * level

      if node in sgt.trace:
        visualizer.create_text(text_x, text_y,
                               text=(f"{sgt.tree[node]}({sgt.lazy[node]})"),
                               font=("Arial", 12),
                               fill="red")
      else:
        visualizer.create_text(text_x, text_y,
                               text=(f"{sgt.tree[node]}({sgt.lazy[node]})"),
                               font=("Arial", 12),
                               fill="black")

      if parent:
        visualizer.create_line(parent[0], parent[1] + 10,
                         text_x, text_y - 10,
                         width=2,
                         fill="black")

      if node_range[0] != node_range[1]:
        mid = (node_range[0] + node_range[1]) // 2
        queue.append({"node": node * 2 + 1,
                      "parent": [text_x, text_y],
                      "range": [node_range[0], mid]})
        queue.append({"node": node * 2 + 2,
                      "parent": [text_x, text_y],
                      "range": [mid + 1, node_range[1]]})
      
    level += 1


def submit_input():
  input = list(map(int, input_entry.get().split() ) )

  global sgtree
  sgtree.build(input)

  arr_len_var.set(str(sgtree.n))
  #tree_arr_var.set(str([node for node in sgtree.tree]) )
  #lazy_arr_var.set(str([node for node in sgtree.lazy]) )
  previous_tree_arr_canv.delete("all")
  display_arr(sgtree.tree, tree_arr_canv)
  previous_lazy_arr_canv.delete("all")
  display_arr(sgtree.lazy, lazy_arr_canv)

  display_tree(sgt=sgtree)


def update_node():
  index_l = update_index_l_entry.get()
  index_r = update_index_r_entry.get()
  value = update_value_entry.get()
  
  #if index_l == "": index_l = "0"
  #if index_r == "": index_r = str(sgtree.n - 1)
  #if value == "": value = "0"

  tree = deepcopy(sgtree.tree)
  lazy = deepcopy(sgtree.lazy)

  warning = sgtree.update(int(index_l), int(index_r), int(value) )

  if warning == "":
    display_tree(sgt=sgtree)

    #previous_tree_arr_var.set(str([node for node in tree]) )
    #previous_lazy_arr_var.set(str([node for node in lazy]) )
    display_arr(tree, previous_tree_arr_canv)
    display_arr(lazy, previous_lazy_arr_canv)

    #tree_arr_var.set(str([node for node in sgtree.tree]) )
    #lazy_arr_var.set(str([node for node in sgtree.lazy]) )
    display_arr(sgtree.tree, tree_arr_canv, sgtree.trace, tree)
    display_arr(sgtree.lazy, lazy_arr_canv, sgtree.trace, lazy)
 
  else:
    result_var.set(warning)


def query_node():
  index_l = query_index_l_entry.get()
  index_r = query_index_r_entry.get()

  #if index_l == "": index_l = "0"
  #if index_r == "": index_r = str(sgtree.n - 1)

  tree = deepcopy(sgtree.tree)
  lazy = deepcopy(sgtree.lazy)

  result_var.set(str(sgtree.query(int(index_l), int(index_r) ) ) )

  #previous_tree_arr_var.set(str([node for node in tree]) )
  #previous_lazy_arr_var.set(str([node for node in lazy]) )
  display_arr(tree, previous_tree_arr_canv)
  display_arr(lazy, previous_lazy_arr_canv)

  #tree_arr_var.set(str([node for node in sgtree.tree]) )
  #lazy_arr_var.set(str([node for node in sgtree.lazy]) )
  display_arr(sgtree.tree, tree_arr_canv, sgtree.trace, tree)
  display_arr(sgtree.lazy, lazy_arr_canv, sgtree.trace, lazy)

  display_tree(sgt=sgtree)

#main window
window = Tk()
window.title("Lazy segment tree demo")

window.state('zoomed')

title_label = Label(window,
                   text="Lazy sum segment tree demo",
                   font=("Arial", 30),
                   padx=x_pad,
                   pady=y_pad)
title_label.pack()

container_frame = Frame(window)
container_frame.pack()

#input
input_frame = Frame(container_frame)
input_frame.grid(row=0, column=0)

input_label = Label(input_frame,
                    text="Input data:",
                    font=("Arial", 16),
                    padx=x_pad,
                    pady=y_pad)
input_label.grid(row=0, column=0)

input_entry = Entry(input_frame,
                    font=("Arial", 16),
                    width=20)
input_entry.grid(row=0, column=1)
input_entry.insert(0, "1 2 3 4 5 6 7 8")

submit_input_button = Button(input_frame,
                             text="Build tree",
                             font=("Arial", 14),
                             command=submit_input,
                             padx=x_pad,
                             pady=y_pad)
submit_input_button.grid(row=0, column=3)

#Update
update_frame = Frame(container_frame)
update_frame.grid(row=1, column=0)

update_label = Label(update_frame,
                     text="Update",
                     font=("Arial", 16),
                     padx=x_pad,
                     pady=y_pad)
update_label.grid(row=0, column=0, columnspan=3)

#Nhập vị trí trái
update_index_l_label = Label(update_frame,
                             text="Left index",
                             font=("Arial", 16),
                             width=s_width,
                             padx=x_pad,
                             pady=y_pad)
update_index_l_label.grid(row=1, column=0)

update_index_l_entry = Entry(update_frame,
                             font=("Arial", 16),
                             width=s_width)
update_index_l_entry.grid(row=1, column=1)


#Nhập vị trí phải
update_index_r_label = Label(update_frame,
                             text="Right index",
                             font=("Arial", 16),
                             width=s_width,
                             padx=x_pad,
                             pady=y_pad)
update_index_r_label.grid(row=2, column=0)

update_index_r_entry = Entry(update_frame,
                             font=("Arial", 16),
                             width=s_width)
update_index_r_entry.grid(row=2, column=1)

#Nhập giá trị
update_value_label = Label(update_frame,
                           text="Value",
                           font=("Arial", 16),
                           width=s_width,
                           padx=x_pad,
                           pady=y_pad)
update_value_label.grid(row=3, column=0)

update_value_entry = Entry(update_frame,
                           font=("Arial", 16),
                           width=s_width)
update_value_entry.grid(row=3, column=1)

#Nút cập nhật
update_button = Button(update_frame,
                       text="Update",
                       font=("Arial", 14),
                       command=update_node,
                       padx=x_pad,
                       pady=y_pad)
update_button.grid(row=1, rowspan=3, column=2)

#Query
query_frame = Frame(container_frame)
query_frame.grid(row=2, column=0)

query_label = Label(query_frame,
                    text="Query",
                    font=("Arial", 16),
                    padx=x_pad,
                    pady=y_pad)
query_label.grid(row=0, column=0, columnspan=3)

#Nhập vị trí trái
query_index_l_label = Label(query_frame,
                            text="Left index",
                            font=("Arial", 16),
                            width=s_width,
                            padx=x_pad,
                            pady=y_pad)
query_index_l_label.grid(row=1, column=0)

query_index_l_entry = Entry(query_frame,
                            font=("Arial", 16),
                            width=s_width)
query_index_l_entry.grid(row=1, column=1)


#Nhập vị trí phải
query_index_r_label = Label(query_frame,
                            text="Right index",
                            font=("Arial", 16),
                            width=s_width,
                            padx=x_pad,
                            pady=y_pad)
query_index_r_label.grid(row=2, column=0)

query_index_r_entry = Entry(query_frame,
                            font=("Arial", 16),
                            width=s_width)
query_index_r_entry.grid(row=2, column=1)

#Nút Truy vấn
query_button = Button(query_frame,
                      text="Query",
                      font=("Arial", 14),
                      command=query_node,
                      padx=x_pad,
                      pady=y_pad)
query_button.grid(row=1, rowspan=2, column=2)

#Kết quả
result_frame = Frame(container_frame, borderwidth=2, relief="groove", bg="white")
result_frame.grid(row=3, column=0)

result_area_label = Label(result_frame,
                          text="Result",
                          font=("Arial", 16),
                          padx=x_pad,
                          pady=y_pad,
                          bg="white")
result_area_label.pack()

result_var = StringVar()
result_var.set("")

result_label = Label(result_frame,
                     textvariable=result_var,
                     font=("Arial", 16),
                     padx=x_pad,
                     pady=y_pad,
                     bg="white")
result_label.pack()

#visual frame
visual_frame = Frame(container_frame)
visual_frame.grid(row=0, rowspan=4, column=1)


#arr len area label
arr_len_area_label = Label(visual_frame,
                          text="Data array length",
                          font=("Arial", 16),
                          padx=x_pad,
                          pady=y_pad,)
arr_len_area_label.grid(row=0, column=0)

#arr len label
arr_len_var = StringVar()
arr_len_var.set("")

arr_len_label = Label(visual_frame,
                        textvariable=arr_len_var,
                        font=("Arial", 16),
                        width=s_width,
                        padx=x_pad,
                        pady=y_pad,
                        borderwidth=2,
                        relief="groove",
                        bg="white")
arr_len_label.grid(row=0, column=1)


#previous tree arr area label
previous_tree_arr_area_label = Label(visual_frame,
                          text="Previous tree array",
                          font=("Arial", 16),
                          padx=x_pad,
                          pady=y_pad,)
previous_tree_arr_area_label.grid(row=1, column=0)

#previous_tree node label
previous_tree_arr_var = StringVar()
previous_tree_arr_var.set("")

previous_tree_arr_label = Label(visual_frame,
                        textvariable=previous_tree_arr_var,
                        font=("Arial", 16),
                        width=l_width,
                        padx=x_pad,
                        pady=y_pad,
                        borderwidth=2,
                        relief="groove",
                        bg="white")
#previous_tree_arr_label.grid(row=1, column=1)

#previous tree arr canv
previous_tree_arr_canv = Canvas(visual_frame,
                                width=str(arr_canv_w),
                                height=str(arr_canv_h),
                                borderwidth=2,
                                relief="groove",
                                bg="white")
previous_tree_arr_canv.grid(row=1, column=1)

#Tree arr area label
tree_arr_area_label = Label(visual_frame,
                          text="Tree array",
                          font=("Arial", 16),
                          padx=x_pad,
                          pady=y_pad)
tree_arr_area_label.grid(row=2, column=0)

#Tree arr label
tree_arr_var = StringVar()
tree_arr_var.set("")

tree_arr_label = Label(visual_frame,
                        textvariable=tree_arr_var,
                        font=("Arial", 16),
                        width=l_width,
                        padx=x_pad,
                        pady=y_pad,
                        borderwidth=2,
                        relief="groove",
                        bg="white")
#tree_arr_label.grid(row=2, column=1)

#tree arr canv
tree_arr_canv = Canvas(visual_frame,
                                width=str(arr_canv_w),
                                height=str(arr_canv_h),
                                borderwidth=2,
                                relief="groove",
                                bg="white")
tree_arr_canv.grid(row=2, column=1)

#previous lazy arr area label
previous_lazy_arr_area_label = Label(visual_frame,
                          text="Previous lazy array",
                          font=("Arial", 16),
                          padx=x_pad,
                          pady=y_pad)
previous_lazy_arr_area_label.grid(row=3, column=0)

#previous lazy arr label
previous_lazy_arr_var = StringVar()
previous_lazy_arr_var.set("")

previous_lazy_arr_label = Label(visual_frame,
                        textvariable=previous_lazy_arr_var,
                        font=("Arial", 16),
                        width=l_width,
                        padx=x_pad,
                        pady=y_pad,
                        borderwidth=2,
                        relief="groove",
                        bg="white")
#previous_lazy_arr_label.grid(row=3, column=1)

#previous lazy arr canv
previous_lazy_arr_canv = Canvas(visual_frame,
                                width=str(arr_canv_w),
                                height=str(arr_canv_h),
                                borderwidth=2,
                                relief="groove",
                                bg="white")
previous_lazy_arr_canv.grid(row=3, column=1)

#lazy node area label
lazy_arr_area_label = Label(visual_frame,
                          text="Lazy array",
                          font=("Arial", 16),
                          padx=x_pad,
                          pady=y_pad)
lazy_arr_area_label.grid(row=4, column=0)

#Lazy arr label
lazy_arr_var = StringVar()
lazy_arr_var.set("")

lazy_arr_label = Label(visual_frame,
                        textvariable=lazy_arr_var,
                        font=("Arial", 16),
                        width=l_width,
                        padx=x_pad,
                        pady=y_pad,
                        borderwidth=2,
                        relief="groove",
                        bg="white")
#lazy_arr_label.grid(row=4, column=1)

#previous lazy arr canv
lazy_arr_canv = Canvas(visual_frame,
                                width=str(arr_canv_w),
                                height=str(arr_canv_h),
                                borderwidth=2,
                                relief="groove",
                                bg="white")
lazy_arr_canv.grid(row=4, column=1)

#Visualizer
visualizer = Canvas(visual_frame,
                    width=str(canvas_width),
                    height=str(canvas_height),
                    borderwidth=2,
                    relief="solid",
                    bg="white")
visualizer.grid(row=5, column=0, columnspan=2)


window.mainloop()