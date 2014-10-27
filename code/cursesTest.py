#-*- coding: utf-8 -*-
#!/usr/bin/env python
from os import system
import curses

#初始化 curses
curses.initscr()
screen = curses.newwin(30, 80, 0, 0)
curses.start_color()
# 不在当前屏幕输出当前的输入
curses.noecho()

# screen.border(0)
# 80(宽) x 25(高)是屏幕大小
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
screen.addstr(12,40, "curses", curses.color_pair(1))
screen.addstr(13, 40, "hhhh")
screen.refresh()
char = screen.getch()

i = 0;

while char != ord('q'):# 按Q键退出
	char = screen.getch()
	# screen.clear()
	# screen.border(0)
	# stdscr.addstr("Pretty text", curses.color_pair(1))
	# stdscr.refresh()
	# screen.addstr(12, 40, "rand" + str(i), curses.COLOR_RED)

	screen.refresh()

	# i += 1
	# screen.addstr(0,0, char)
curses.endwin()


 
# def get_param(prompt_string):
#      screen.clear()
#      screen.border(0)
#      screen.addstr(2, 2, prompt_string)
#      screen.refresh()
#      input = screen.getstr(10, 10, 60)
#      return input
 
# def execute_cmd(cmd_string):
#      system("clear")
#      a = system(cmd_string)
#      print ""
#      if a == 0:
#           print "Command executed correctly"
#      else:
#           print "Command terminated with error"
#      raw_input("Press enter")
#      print ""
 
# x = 0
 
# while x != ord('4'):
#      screen = curses.initscr()
 
#      screen.clear()
#      screen.border(0)
#      screen.addstr(2, 2, "Please enter a number...")
#      screen.addstr(4, 4, "1 - Add a user")
#      screen.addstr(5, 4, "2 - Restart Apache")
#      screen.addstr(6, 4, "3 - Show disk space")
#      screen.addstr(7, 4, "4 - Exit")
#      screen.refresh()
 
#      x = screen.getch()
 
#      if x == ord('1'):
#           username = get_param("Enter the username")
#           homedir = get_param("Enter the home directory, eg /home/nate")
#           groups = get_param("Enter comma-separated groups, eg adm,dialout,cdrom")
#           shell = get_param("Enter the shell, eg /bin/bash:")
#           curses.endwin()
#           execute_cmd("useradd -d " + homedir + " -g 1000 -G " + groups + " -m -s " + shell + " " + username)
#      if x == ord('2'):
#           curses.endwin()
#           execute_cmd("apachectl restart")
#      if x == ord('3'):
#           curses.endwin()
#           execute_cmd("df -h")
 
# curses.endwin()