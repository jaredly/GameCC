import pygame
from pygame.locals import *
import math
from game import Vector,Point

class Sprite:
  def __init__(self, parent, pos):
    self.parent = parent
    self.pos = pos
    self.v = Vector(0,0)
    self.gravity = Vector(0,0)
  
  def draw(self,screen):
    pass
    
  def _step(self):
    self.pos.x += self.v.x()
    self.pos.y += self.v.y()
    
    keys = pygame.key.get_pressed()

    if keys[K_KP_MINUS]:self.key_down_keypad_minus()
    if keys[K_F1]:self.key_down_f1()
    if keys[K_F2]:self.key_down_f2()
    if keys[K_PAUSE]:self.key_down_pause()
    if keys[K_COLON]:self.key_down_colon()
    if keys[K_F5]:self.key_down_f5()
    if keys[K_F6]:self.key_down_f6()
    if keys[K_F7]:self.key_down_f7()
    if keys[K_F8]:self.key_down_f8()
    if keys[K_F9]:self.key_down_f9()
    if keys[K_LEFT]:self.key_down_left_arrow()
    if keys[K_COMMA]:self.key_down_comma()
    if keys[K_RIGHT]:self.key_down_right_arrow()
    if keys[K_F3]:self.key_down_f3()
    if keys[K_EQUALS]:self.key_down_equals_sign()
    if keys[K_F4]:self.key_down_f4()
    if keys[K_SEMICOLON]:self.key_down_semicolon()
    if keys[K_AMPERSAND]:self.key_down_ampersand()
    if keys[K_n]:self.key_down_n()
    if keys[K_NUMLOCK]:self.key_down_numlock()
    if keys[K_CLEAR]:self.key_down_clear()
    if keys[K_KP2]:self.key_down_keypad_2()
    if keys[K_KP_PLUS]:self.key_down_keypad_plus()
    if keys[K_QUESTION]:self.key_down_question_mark()
    if keys[K_KP_EQUALS]:self.key_down_keypad_equals()
    if keys[K_RMETA]:self.key_down_right_meta()
    if keys[K_EURO]:self.key_down_euro()
    if keys[K_SCROLLOCK]:self.key_down_scrollock()
    if keys[K_PERIOD]:self.key_down_period()
    if keys[K_a]:self.key_down_a()
    if keys[K_SPACE]:self.key_down_space()
    if keys[K_KP3]:self.key_down_keypad_3()
    if keys[K_INSERT]:self.key_down_insert()
    if keys[K_DELETE]:self.key_down_delete()
    if keys[K_CARET]:self.key_down_caret()
    if keys[K_HOME]:self.key_down_home()
    if keys[K_i]:self.key_down_i()
    if keys[K_LSUPER]:self.key_down_left_windows_key()
    if keys[K_5]:self.key_down_5()
    if keys[K_GREATER]:self.key_down_greater_than_sign()
    if keys[K_LMETA]:self.key_down_left_meta()
    if keys[K_TAB]:self.key_down_tab()
    if keys[K_RALT]:self.key_down_right_alt()
    if keys[K_KP_PERIOD]:self.key_down_keypad_period()
    if keys[K_MODE]:self.key_down_mode_shift()
    if keys[K_RIGHTPAREN]:self.key_down_right_parenthesis()
    if keys[K_RIGHTBRACKET]:self.key_down_right_bracket()
    if keys[K_LSHIFT]:self.key_down_left_shift()
    if keys[K_LEFTPAREN]:self.key_down_left_parenthesis()
    if keys[K_F13]:self.key_down_f13()
    if keys[K_F10]:self.key_down_f10()
    if keys[K_F11]:self.key_down_f11()
    if keys[K_F14]:self.key_down_f14()
    if keys[K_F15]:self.key_down_f15()
    if keys[K_y]:self.key_down_y()
    if keys[K_x]:self.key_down_x()
    if keys[K_z]:self.key_down_z()
    if keys[K_KP_ENTER]:self.key_down_keypad_enter()
    if keys[K_8]:self.key_down_8()
    if keys[K_q]:self.key_down_q()
    if keys[K_p]:self.key_down_p()
    if keys[K_s]:self.key_down_s()
    if keys[K_r]:self.key_down_r()
    if keys[K_HASH]:self.key_down_hash()
    if keys[K_t]:self.key_down_t()
    if keys[K_w]:self.key_down_w()
    if keys[K_v]:self.key_down_v()
    if keys[K_DOWN]:self.key_down_down_arrow()
    if keys[K_h]:self.key_down_h()
    if keys[K_k]:self.key_down_k()
    if keys[K_j]:self.key_down_j()
    if keys[K_m]:self.key_down_m()
    if keys[K_LEFTBRACKET]:self.key_down_left_bracket()
    if keys[K_o]:self.key_down_o()
    if keys[K_RSUPER]:self.key_down_right_windows_key()
    if keys[K_END]:self.key_down_end()
    if keys[K_UP]:self.key_down_up_arrow()
    if keys[K_c]:self.key_down_c()
    if keys[K_b]:self.key_down_b()
    if keys[K_e]:self.key_down_e()
    if keys[K_d]:self.key_down_d()
    if keys[K_g]:self.key_down_g()
    if keys[K_f]:self.key_down_f()
    if keys[K_ASTERISK]:self.key_down_asterisk()
    if keys[K_AT]:self.key_down_at()
    if keys[K_PAGEUP]:self.key_down_page_up()
    if keys[K_CAPSLOCK]:self.key_down_capslock()
    if keys[K_LESS]:self.key_down_less_than_sign()
    if keys[K_PRINT]:self.key_down_print_screen()
    if keys[K_SLASH]:self.key_down_forward_slash()
    if keys[K_LCTRL]:self.key_down_left_ctrl()
    if keys[K_BACKSLASH]:self.key_down_backslash()
    if keys[K_RETURN]:self.key_down_return()
    if keys[K_MINUS]:self.key_down_minus_sign()
    if keys[K_0]:self.key_down_0()
    if keys[K_KP8]:self.key_down_keypad_8()
    if keys[K_DOLLAR]:self.key_down_dollar()
    if keys[K_PAGEDOWN]:self.key_down_page_down()
    if keys[K_EXCLAIM]:self.key_down_exclaim()
    if keys[K_1]:self.key_down_1()
    if keys[K_HELP]:self.key_down_help()
    if keys[K_3]:self.key_down_3()
    if keys[K_2]:self.key_down_2()
    if keys[K_BREAK]:self.key_down_break()
    if keys[K_4]:self.key_down_4()
    if keys[K_POWER]:self.key_down_power()
    if keys[K_6]:self.key_down_6()
    if keys[K_F12]:self.key_down_f12()
    if keys[K_7]:self.key_down_7()
    if keys[K_ESCAPE]:self.key_down_escape()
    if keys[K_BACKSPACE]:self.key_down_backspace()
    if keys[K_MENU]:self.key_down_menu()
    if keys[K_u]:self.key_down_u()
    if keys[K_PLUS]:self.key_down_plus_sign()
    if keys[K_KP6]:self.key_down_keypad_6()
    if keys[K_UNDERSCORE]:self.key_down_underscore()
    if keys[K_QUOTE]:self.key_down_quote()
    if keys[K_l]:self.key_down_l()
    if keys[K_KP0]:self.key_down_keypad_0()
    if keys[K_QUOTEDBL]:self.key_down_quotedbl()
    if keys[K_KP_MULTIPLY]:self.key_down_keypad_multiply()
    if keys[K_RSHIFT]:self.key_down_right_shift()
    if keys[K_KP1]:self.key_down_keypad_1()
    if keys[K_9]:self.key_down_9()
    if keys[K_KP9]:self.key_down_keypad_9()
    if keys[K_KP4]:self.key_down_keypad_4()
    if keys[K_KP5]:self.key_down_keypad_5()
    if keys[K_BACKQUOTE]:self.key_down_grave()
    if keys[K_KP7]:self.key_down_keypad_7()
    if keys[K_RCTRL]:self.key_down_right_ctrl()
    if keys[K_LALT]:self.key_down_left_alt()
    if keys[K_KP_DIVIDE]:self.key_down_keypad_divide()
    if keys[K_SYSREQ]:self.key_down_sysrq()
    
    if not self.collideRect(0,0,self.parent.size[0],self.parent.size[1]):
      self.off_screen()
    
    self.step()
  
  def mouse_down(self, e=None):pass
  def mouse_up(self, e=None):pass
  def mouse_wheel(self, e=None):pass
  def mouse_move(self, e=None):pass
  def key_down(self, e=None):pass
  def _key_down(self, e):
    self.key_down(e)

    if e.key == K_KP_MINUS:self.key_press_keypad_minus()
    if e.key == K_F1:self.key_press_f1()
    if e.key == K_F2:self.key_press_f2()
    if e.key == K_PAUSE:self.key_press_pause()
    if e.key == K_COLON:self.key_press_colon()
    if e.key == K_F5:self.key_press_f5()
    if e.key == K_F6:self.key_press_f6()
    if e.key == K_F7:self.key_press_f7()
    if e.key == K_F8:self.key_press_f8()
    if e.key == K_F9:self.key_press_f9()
    if e.key == K_LEFT:self.key_press_left_arrow()
    if e.key == K_COMMA:self.key_press_comma()
    if e.key == K_RIGHT:self.key_press_right_arrow()
    if e.key == K_F3:self.key_press_f3()
    if e.key == K_EQUALS:self.key_press_equals_sign()
    if e.key == K_F4:self.key_press_f4()
    if e.key == K_SEMICOLON:self.key_press_semicolon()
    if e.key == K_AMPERSAND:self.key_press_ampersand()
    if e.key == K_n:self.key_press_n()
    if e.key == K_NUMLOCK:self.key_press_numlock()
    if e.key == K_CLEAR:self.key_press_clear()
    if e.key == K_KP2:self.key_press_keypad_2()
    if e.key == K_KP_PLUS:self.key_press_keypad_plus()
    if e.key == K_QUESTION:self.key_press_question_mark()
    if e.key == K_KP_EQUALS:self.key_press_keypad_equals()
    if e.key == K_RMETA:self.key_press_right_meta()
    if e.key == K_EURO:self.key_press_euro()
    if e.key == K_SCROLLOCK:self.key_press_scrollock()
    if e.key == K_PERIOD:self.key_press_period()
    if e.key == K_a:self.key_press_a()
    if e.key == K_SPACE:self.key_press_space()
    if e.key == K_KP3:self.key_press_keypad_3()
    if e.key == K_INSERT:self.key_press_insert()
    if e.key == K_DELETE:self.key_press_delete()
    if e.key == K_CARET:self.key_press_caret()
    if e.key == K_HOME:self.key_press_home()
    if e.key == K_i:self.key_press_i()
    if e.key == K_LSUPER:self.key_press_left_windows_key()
    if e.key == K_5:self.key_press_5()
    if e.key == K_GREATER:self.key_press_greater_than_sign()
    if e.key == K_LMETA:self.key_press_left_meta()
    if e.key == K_TAB:self.key_press_tab()
    if e.key == K_RALT:self.key_press_right_alt()
    if e.key == K_KP_PERIOD:self.key_press_keypad_period()
    if e.key == K_MODE:self.key_press_mode_shift()
    if e.key == K_RIGHTPAREN:self.key_press_right_parenthesis()
    if e.key == K_RIGHTBRACKET:self.key_press_right_bracket()
    if e.key == K_LSHIFT:self.key_press_left_shift()
    if e.key == K_LEFTPAREN:self.key_press_left_parenthesis()
    if e.key == K_F13:self.key_press_f13()
    if e.key == K_F10:self.key_press_f10()
    if e.key == K_F11:self.key_press_f11()
    if e.key == K_F14:self.key_press_f14()
    if e.key == K_F15:self.key_press_f15()
    if e.key == K_y:self.key_press_y()
    if e.key == K_x:self.key_press_x()
    if e.key == K_z:self.key_press_z()
    if e.key == K_KP_ENTER:self.key_press_keypad_enter()
    if e.key == K_8:self.key_press_8()
    if e.key == K_q:self.key_press_q()
    if e.key == K_p:self.key_press_p()
    if e.key == K_s:self.key_press_s()
    if e.key == K_r:self.key_press_r()
    if e.key == K_HASH:self.key_press_hash()
    if e.key == K_t:self.key_press_t()
    if e.key == K_w:self.key_press_w()
    if e.key == K_v:self.key_press_v()
    if e.key == K_DOWN:self.key_press_down_arrow()
    if e.key == K_h:self.key_press_h()
    if e.key == K_k:self.key_press_k()
    if e.key == K_j:self.key_press_j()
    if e.key == K_m:self.key_press_m()
    if e.key == K_LEFTBRACKET:self.key_press_left_bracket()
    if e.key == K_o:self.key_press_o()
    if e.key == K_RSUPER:self.key_press_right_windows_key()
    if e.key == K_END:self.key_press_end()
    if e.key == K_UP:self.key_press_up_arrow()
    if e.key == K_c:self.key_press_c()
    if e.key == K_b:self.key_press_b()
    if e.key == K_e:self.key_press_e()
    if e.key == K_d:self.key_press_d()
    if e.key == K_g:self.key_press_g()
    if e.key == K_f:self.key_press_f()
    if e.key == K_ASTERISK:self.key_press_asterisk()
    if e.key == K_AT:self.key_press_at()
    if e.key == K_PAGEUP:self.key_press_page_up()
    if e.key == K_CAPSLOCK:self.key_press_capslock()
    if e.key == K_LESS:self.key_press_less_than_sign()
    if e.key == K_PRINT:self.key_press_print_screen()
    if e.key == K_SLASH:self.key_press_forward_slash()
    if e.key == K_LCTRL:self.key_press_left_ctrl()
    if e.key == K_BACKSLASH:self.key_press_backslash()
    if e.key == K_RETURN:self.key_press_return()
    if e.key == K_MINUS:self.key_press_minus_sign()
    if e.key == K_0:self.key_press_0()
    if e.key == K_KP8:self.key_press_keypad_8()
    if e.key == K_DOLLAR:self.key_press_dollar()
    if e.key == K_PAGEDOWN:self.key_press_page_down()
    if e.key == K_EXCLAIM:self.key_press_exclaim()
    if e.key == K_1:self.key_press_1()
    if e.key == K_HELP:self.key_press_help()
    if e.key == K_3:self.key_press_3()
    if e.key == K_2:self.key_press_2()
    if e.key == K_BREAK:self.key_press_break()
    if e.key == K_4:self.key_press_4()
    if e.key == K_POWER:self.key_press_power()
    if e.key == K_6:self.key_press_6()
    if e.key == K_F12:self.key_press_f12()
    if e.key == K_7:self.key_press_7()
    if e.key == K_ESCAPE:self.key_press_escape()
    if e.key == K_BACKSPACE:self.key_press_backspace()
    if e.key == K_MENU:self.key_press_menu()
    if e.key == K_u:self.key_press_u()
    if e.key == K_PLUS:self.key_press_plus_sign()
    if e.key == K_KP6:self.key_press_keypad_6()
    if e.key == K_UNDERSCORE:self.key_press_underscore()
    if e.key == K_QUOTE:self.key_press_quote()
    if e.key == K_l:self.key_press_l()
    if e.key == K_KP0:self.key_press_keypad_0()
    if e.key == K_QUOTEDBL:self.key_press_quotedbl()
    if e.key == K_KP_MULTIPLY:self.key_press_keypad_multiply()
    if e.key == K_RSHIFT:self.key_press_right_shift()
    if e.key == K_KP1:self.key_press_keypad_1()
    if e.key == K_9:self.key_press_9()
    if e.key == K_KP9:self.key_press_keypad_9()
    if e.key == K_KP4:self.key_press_keypad_4()
    if e.key == K_KP5:self.key_press_keypad_5()
    if e.key == K_BACKQUOTE:self.key_press_grave()
    if e.key == K_KP7:self.key_press_keypad_7()
    if e.key == K_RCTRL:self.key_press_right_ctrl()
    if e.key == K_LALT:self.key_press_left_alt()
    if e.key == K_KP_DIVIDE:self.key_press_keypad_divide()
    if e.key == K_SYSREQ:self.key_press_sysrq()





  def off_screen(self):pass
  def create(self):pass
  def collide(self, other):pass
  def destroy(self):pass
  def step(self):pass
## all the keys

  def key_down_keypad_minus(self):pass
  def key_down_f1(self):pass
  def key_down_f2(self):pass
  def key_down_pause(self):pass
  def key_down_colon(self):pass
  def key_down_f5(self):pass
  def key_down_f6(self):pass
  def key_down_f7(self):pass
  def key_down_f8(self):pass
  def key_down_f9(self):pass
  def key_down_left_arrow(self):pass
  def key_down_comma(self):pass
  def key_down_right_arrow(self):pass
  def key_down_f3(self):pass
  def key_down_equals_sign(self):pass
  def key_down_f4(self):pass
  def key_down_semicolon(self):pass
  def key_down_ampersand(self):pass
  def key_down_n(self):pass
  def key_down_numlock(self):pass
  def key_down_clear(self):pass
  def key_down_keypad_2(self):pass
  def key_down_keypad_plus(self):pass
  def key_down_question_mark(self):pass
  def key_down_keypad_equals(self):pass
  def key_down_right_meta(self):pass
  def key_down_euro(self):pass
  def key_down_scrollock(self):pass
  def key_down_period(self):pass
  def key_down_a(self):pass
  def key_down_space(self):pass
  def key_down_keypad_3(self):pass
  def key_down_insert(self):pass
  def key_down_delete(self):pass
  def key_down_caret(self):pass
  def key_down_home(self):pass
  def key_down_i(self):pass
  def key_down_left_windows_key(self):pass
  def key_down_5(self):pass
  def key_down_greater_than_sign(self):pass
  def key_down_left_meta(self):pass
  def key_down_tab(self):pass
  def key_down_right_alt(self):pass
  def key_down_keypad_period(self):pass
  def key_down_mode_shift(self):pass
  def key_down_right_parenthesis(self):pass
  def key_down_right_bracket(self):pass
  def key_down_left_shift(self):pass
  def key_down_left_parenthesis(self):pass
  def key_down_f13(self):pass
  def key_down_f10(self):pass
  def key_down_f11(self):pass
  def key_down_f14(self):pass
  def key_down_f15(self):pass
  def key_down_y(self):pass
  def key_down_x(self):pass
  def key_down_z(self):pass
  def key_down_keypad_enter(self):pass
  def key_down_8(self):pass
  def key_down_q(self):pass
  def key_down_p(self):pass
  def key_down_s(self):pass
  def key_down_r(self):pass
  def key_down_hash(self):pass
  def key_down_t(self):pass
  def key_down_w(self):pass
  def key_down_v(self):pass
  def key_down_down_arrow(self):pass
  def key_down_h(self):pass
  def key_down_k(self):pass
  def key_down_j(self):pass
  def key_down_m(self):pass
  def key_down_left_bracket(self):pass
  def key_down_o(self):pass
  def key_down_right_windows_key(self):pass
  def key_down_end(self):pass
  def key_down_up_arrow(self):pass
  def key_down_c(self):pass
  def key_down_b(self):pass
  def key_down_e(self):pass
  def key_down_d(self):pass
  def key_down_g(self):pass
  def key_down_f(self):pass
  def key_down_asterisk(self):pass
  def key_down_at(self):pass
  def key_down_page_up(self):pass
  def key_down_capslock(self):pass
  def key_down_less_than_sign(self):pass
  def key_down_print_screen(self):pass
  def key_down_forward_slash(self):pass
  def key_down_left_ctrl(self):pass
  def key_down_backslash(self):pass
  def key_down_return(self):pass
  def key_down_minus_sign(self):pass
  def key_down_0(self):pass
  def key_down_keypad_8(self):pass
  def key_down_dollar(self):pass
  def key_down_page_down(self):pass
  def key_down_exclaim(self):pass
  def key_down_1(self):pass
  def key_down_help(self):pass
  def key_down_3(self):pass
  def key_down_2(self):pass
  def key_down_break(self):pass
  def key_down_4(self):pass
  def key_down_power(self):pass
  def key_down_6(self):pass
  def key_down_f12(self):pass
  def key_down_7(self):pass
  def key_down_escape(self):pass
  def key_down_backspace(self):pass
  def key_down_menu(self):pass
  def key_down_u(self):pass
  def key_down_plus_sign(self):pass
  def key_down_keypad_6(self):pass
  def key_down_underscore(self):pass
  def key_down_quote(self):pass
  def key_down_l(self):pass
  def key_down_keypad_0(self):pass
  def key_down_quotedbl(self):pass
  def key_down_keypad_multiply(self):pass
  def key_down_right_shift(self):pass
  def key_down_keypad_1(self):pass
  def key_down_9(self):pass
  def key_down_keypad_9(self):pass
  def key_down_keypad_4(self):pass
  def key_down_keypad_5(self):pass
  def key_down_grave(self):pass
  def key_down_keypad_7(self):pass
  def key_down_right_ctrl(self):pass
  def key_down_left_alt(self):pass
  def key_down_keypad_divide(self):pass
  def key_down_sysrq(self):pass

  def key_press_keypad_minus(self):pass
  def key_press_f1(self):pass
  def key_press_f2(self):pass
  def key_press_pause(self):pass
  def key_press_colon(self):pass
  def key_press_f5(self):pass
  def key_press_f6(self):pass
  def key_press_f7(self):pass
  def key_press_f8(self):pass
  def key_press_f9(self):pass
  def key_press_left_arrow(self):pass
  def key_press_comma(self):pass
  def key_press_right_arrow(self):pass
  def key_press_f3(self):pass
  def key_press_equals_sign(self):pass
  def key_press_f4(self):pass
  def key_press_semicolon(self):pass
  def key_press_ampersand(self):pass
  def key_press_n(self):pass
  def key_press_numlock(self):pass
  def key_press_clear(self):pass
  def key_press_keypad_2(self):pass
  def key_press_keypad_plus(self):pass
  def key_press_question_mark(self):pass
  def key_press_keypad_equals(self):pass
  def key_press_right_meta(self):pass
  def key_press_euro(self):pass
  def key_press_scrollock(self):pass
  def key_press_period(self):pass
  def key_press_a(self):pass
  def key_press_space(self):pass
  def key_press_keypad_3(self):pass
  def key_press_insert(self):pass
  def key_press_delete(self):pass
  def key_press_caret(self):pass
  def key_press_home(self):pass
  def key_press_i(self):pass
  def key_press_left_windows_key(self):pass
  def key_press_5(self):pass
  def key_press_greater_than_sign(self):pass
  def key_press_left_meta(self):pass
  def key_press_tab(self):pass
  def key_press_right_alt(self):pass
  def key_press_keypad_period(self):pass
  def key_press_mode_shift(self):pass
  def key_press_right_parenthesis(self):pass
  def key_press_right_bracket(self):pass
  def key_press_left_shift(self):pass
  def key_press_left_parenthesis(self):pass
  def key_press_f13(self):pass
  def key_press_f10(self):pass
  def key_press_f11(self):pass
  def key_press_f14(self):pass
  def key_press_f15(self):pass
  def key_press_y(self):pass
  def key_press_x(self):pass
  def key_press_z(self):pass
  def key_press_keypad_enter(self):pass
  def key_press_8(self):pass
  def key_press_q(self):pass
  def key_press_p(self):pass
  def key_press_s(self):pass
  def key_press_r(self):pass
  def key_press_hash(self):pass
  def key_press_t(self):pass
  def key_press_w(self):pass
  def key_press_v(self):pass
  def key_press_down_arrow(self):pass
  def key_press_h(self):pass
  def key_press_k(self):pass
  def key_press_j(self):pass
  def key_press_m(self):pass
  def key_press_left_bracket(self):pass
  def key_press_o(self):pass
  def key_press_right_windows_key(self):pass
  def key_press_end(self):pass
  def key_press_up_arrow(self):pass
  def key_press_c(self):pass
  def key_press_b(self):pass
  def key_press_e(self):pass
  def key_press_d(self):pass
  def key_press_g(self):pass
  def key_press_f(self):pass
  def key_press_asterisk(self):pass
  def key_press_at(self):pass
  def key_press_page_up(self):pass
  def key_press_capslock(self):pass
  def key_press_less_than_sign(self):pass
  def key_press_print_screen(self):pass
  def key_press_forward_slash(self):pass
  def key_press_left_ctrl(self):pass
  def key_press_backslash(self):pass
  def key_press_return(self):pass
  def key_press_minus_sign(self):pass
  def key_press_0(self):pass
  def key_press_keypad_8(self):pass
  def key_press_dollar(self):pass
  def key_press_page_down(self):pass
  def key_press_exclaim(self):pass
  def key_press_1(self):pass
  def key_press_help(self):pass
  def key_press_3(self):pass
  def key_press_2(self):pass
  def key_press_break(self):pass
  def key_press_4(self):pass
  def key_press_power(self):pass
  def key_press_6(self):pass
  def key_press_f12(self):pass
  def key_press_7(self):pass
  def key_press_escape(self):pass
  def key_press_backspace(self):pass
  def key_press_menu(self):pass
  def key_press_u(self):pass
  def key_press_plus_sign(self):pass
  def key_press_keypad_6(self):pass
  def key_press_underscore(self):pass
  def key_press_quote(self):pass
  def key_press_l(self):pass
  def key_press_keypad_0(self):pass
  def key_press_quotedbl(self):pass
  def key_press_keypad_multiply(self):pass
  def key_press_right_shift(self):pass
  def key_press_keypad_1(self):pass
  def key_press_9(self):pass
  def key_press_keypad_9(self):pass
  def key_press_keypad_4(self):pass
  def key_press_keypad_5(self):pass
  def key_press_grave(self):pass
  def key_press_keypad_7(self):pass
  def key_press_right_ctrl(self):pass
  def key_press_left_alt(self):pass
  def key_press_keypad_divide(self):pass
  def key_press_sysrq(self):pass



  def key_release_keypad_minus(self):pass
  def key_release_f1(self):pass
  def key_release_f2(self):pass
  def key_release_pause(self):pass
  def key_release_colon(self):pass
  def key_release_f5(self):pass
  def key_release_f6(self):pass
  def key_release_f7(self):pass
  def key_release_f8(self):pass
  def key_release_f9(self):pass
  def key_release_left_arrow(self):pass
  def key_release_comma(self):pass
  def key_release_right_arrow(self):pass
  def key_release_f3(self):pass
  def key_release_equals_sign(self):pass
  def key_release_f4(self):pass
  def key_release_semicolon(self):pass
  def key_release_ampersand(self):pass
  def key_release_n(self):pass
  def key_release_numlock(self):pass
  def key_release_clear(self):pass
  def key_release_keypad_2(self):pass
  def key_release_keypad_plus(self):pass
  def key_release_question_mark(self):pass
  def key_release_keypad_equals(self):pass
  def key_release_right_meta(self):pass
  def key_release_euro(self):pass
  def key_release_scrollock(self):pass
  def key_release_period(self):pass
  def key_release_a(self):pass
  def key_release_space(self):pass
  def key_release_keypad_3(self):pass
  def key_release_insert(self):pass
  def key_release_delete(self):pass
  def key_release_caret(self):pass
  def key_release_home(self):pass
  def key_release_i(self):pass
  def key_release_left_windows_key(self):pass
  def key_release_5(self):pass
  def key_release_greater_than_sign(self):pass
  def key_release_left_meta(self):pass
  def key_release_tab(self):pass
  def key_release_right_alt(self):pass
  def key_release_keypad_period(self):pass
  def key_release_mode_shift(self):pass
  def key_release_right_parenthesis(self):pass
  def key_release_right_bracket(self):pass
  def key_release_left_shift(self):pass
  def key_release_left_parenthesis(self):pass
  def key_release_f13(self):pass
  def key_release_f10(self):pass
  def key_release_f11(self):pass
  def key_release_f14(self):pass
  def key_release_f15(self):pass
  def key_release_y(self):pass
  def key_release_x(self):pass
  def key_release_z(self):pass
  def key_release_keypad_enter(self):pass
  def key_release_8(self):pass
  def key_release_q(self):pass
  def key_release_p(self):pass
  def key_release_s(self):pass
  def key_release_r(self):pass
  def key_release_hash(self):pass
  def key_release_t(self):pass
  def key_release_w(self):pass
  def key_release_v(self):pass
  def key_release_down_arrow(self):pass
  def key_release_h(self):pass
  def key_release_k(self):pass
  def key_release_j(self):pass
  def key_release_m(self):pass
  def key_release_left_bracket(self):pass
  def key_release_o(self):pass
  def key_release_right_windows_key(self):pass
  def key_release_end(self):pass
  def key_release_up_arrow(self):pass
  def key_release_c(self):pass
  def key_release_b(self):pass
  def key_release_e(self):pass
  def key_release_d(self):pass
  def key_release_g(self):pass
  def key_release_f(self):pass
  def key_release_asterisk(self):pass
  def key_release_at(self):pass
  def key_release_page_up(self):pass
  def key_release_capslock(self):pass
  def key_release_less_than_sign(self):pass
  def key_release_print_screen(self):pass
  def key_release_forward_slash(self):pass
  def key_release_left_ctrl(self):pass
  def key_release_backslash(self):pass
  def key_release_return(self):pass
  def key_release_minus_sign(self):pass
  def key_release_0(self):pass
  def key_release_keypad_8(self):pass
  def key_release_dollar(self):pass
  def key_release_page_down(self):pass
  def key_release_exclaim(self):pass
  def key_release_1(self):pass
  def key_release_help(self):pass
  def key_release_3(self):pass
  def key_release_2(self):pass
  def key_release_break(self):pass
  def key_release_4(self):pass
  def key_release_power(self):pass
  def key_release_6(self):pass
  def key_release_f12(self):pass
  def key_release_7(self):pass
  def key_release_escape(self):pass
  def key_release_backspace(self):pass
  def key_release_menu(self):pass
  def key_release_u(self):pass
  def key_release_plus_sign(self):pass
  def key_release_keypad_6(self):pass
  def key_release_underscore(self):pass
  def key_release_quote(self):pass
  def key_release_l(self):pass
  def key_release_keypad_0(self):pass
  def key_release_quotedbl(self):pass
  def key_release_keypad_multiply(self):pass
  def key_release_right_shift(self):pass
  def key_release_keypad_1(self):pass
  def key_release_9(self):pass
  def key_release_keypad_9(self):pass
  def key_release_keypad_4(self):pass
  def key_release_keypad_5(self):pass
  def key_release_grave(self):pass
  def key_release_keypad_7(self):pass
  def key_release_right_ctrl(self):pass
  def key_release_left_alt(self):pass
  def key_release_keypad_divide(self):pass
  def key_release_sysrq(self):pass

  
  def key_up(self, e):pass
  def _key_up(self, e):
    self.key_up(e)

    if e.key == K_KP_MINUS:self.key_release_keypad_minus()
    if e.key == K_F1:self.key_release_f1()
    if e.key == K_F2:self.key_release_f2()
    if e.key == K_PAUSE:self.key_release_pause()
    if e.key == K_COLON:self.key_release_colon()
    if e.key == K_F5:self.key_release_f5()
    if e.key == K_F6:self.key_release_f6()
    if e.key == K_F7:self.key_release_f7()
    if e.key == K_F8:self.key_release_f8()
    if e.key == K_F9:self.key_release_f9()
    if e.key == K_LEFT:self.key_release_left_arrow()
    if e.key == K_COMMA:self.key_release_comma()
    if e.key == K_RIGHT:self.key_release_right_arrow()
    if e.key == K_F3:self.key_release_f3()
    if e.key == K_EQUALS:self.key_release_equals_sign()
    if e.key == K_F4:self.key_release_f4()
    if e.key == K_SEMICOLON:self.key_release_semicolon()
    if e.key == K_AMPERSAND:self.key_release_ampersand()
    if e.key == K_n:self.key_release_n()
    if e.key == K_NUMLOCK:self.key_release_numlock()
    if e.key == K_CLEAR:self.key_release_clear()
    if e.key == K_KP2:self.key_release_keypad_2()
    if e.key == K_KP_PLUS:self.key_release_keypad_plus()
    if e.key == K_QUESTION:self.key_release_question_mark()
    if e.key == K_KP_EQUALS:self.key_release_keypad_equals()
    if e.key == K_RMETA:self.key_release_right_meta()
    if e.key == K_EURO:self.key_release_euro()
    if e.key == K_SCROLLOCK:self.key_release_scrollock()
    if e.key == K_PERIOD:self.key_release_period()
    if e.key == K_a:self.key_release_a()
    if e.key == K_SPACE:self.key_release_space()
    if e.key == K_KP3:self.key_release_keypad_3()
    if e.key == K_INSERT:self.key_release_insert()
    if e.key == K_DELETE:self.key_release_delete()
    if e.key == K_CARET:self.key_release_caret()
    if e.key == K_HOME:self.key_release_home()
    if e.key == K_i:self.key_release_i()
    if e.key == K_LSUPER:self.key_release_left_windows_key()
    if e.key == K_5:self.key_release_5()
    if e.key == K_GREATER:self.key_release_greater_than_sign()
    if e.key == K_LMETA:self.key_release_left_meta()
    if e.key == K_TAB:self.key_release_tab()
    if e.key == K_RALT:self.key_release_right_alt()
    if e.key == K_KP_PERIOD:self.key_release_keypad_period()
    if e.key == K_MODE:self.key_release_mode_shift()
    if e.key == K_RIGHTPAREN:self.key_release_right_parenthesis()
    if e.key == K_RIGHTBRACKET:self.key_release_right_bracket()
    if e.key == K_LSHIFT:self.key_release_left_shift()
    if e.key == K_LEFTPAREN:self.key_release_left_parenthesis()
    if e.key == K_F13:self.key_release_f13()
    if e.key == K_F10:self.key_release_f10()
    if e.key == K_F11:self.key_release_f11()
    if e.key == K_F14:self.key_release_f14()
    if e.key == K_F15:self.key_release_f15()
    if e.key == K_y:self.key_release_y()
    if e.key == K_x:self.key_release_x()
    if e.key == K_z:self.key_release_z()
    if e.key == K_KP_ENTER:self.key_release_keypad_enter()
    if e.key == K_8:self.key_release_8()
    if e.key == K_q:self.key_release_q()
    if e.key == K_p:self.key_release_p()
    if e.key == K_s:self.key_release_s()
    if e.key == K_r:self.key_release_r()
    if e.key == K_HASH:self.key_release_hash()
    if e.key == K_t:self.key_release_t()
    if e.key == K_w:self.key_release_w()
    if e.key == K_v:self.key_release_v()
    if e.key == K_DOWN:self.key_release_down_arrow()
    if e.key == K_h:self.key_release_h()
    if e.key == K_k:self.key_release_k()
    if e.key == K_j:self.key_release_j()
    if e.key == K_m:self.key_release_m()
    if e.key == K_LEFTBRACKET:self.key_release_left_bracket()
    if e.key == K_o:self.key_release_o()
    if e.key == K_RSUPER:self.key_release_right_windows_key()
    if e.key == K_END:self.key_release_end()
    if e.key == K_UP:self.key_release_up_arrow()
    if e.key == K_c:self.key_release_c()
    if e.key == K_b:self.key_release_b()
    if e.key == K_e:self.key_release_e()
    if e.key == K_d:self.key_release_d()
    if e.key == K_g:self.key_release_g()
    if e.key == K_f:self.key_release_f()
    if e.key == K_ASTERISK:self.key_release_asterisk()
    if e.key == K_AT:self.key_release_at()
    if e.key == K_PAGEUP:self.key_release_page_up()
    if e.key == K_CAPSLOCK:self.key_release_capslock()
    if e.key == K_LESS:self.key_release_less_than_sign()
    if e.key == K_PRINT:self.key_release_print_screen()
    if e.key == K_SLASH:self.key_release_forward_slash()
    if e.key == K_LCTRL:self.key_release_left_ctrl()
    if e.key == K_BACKSLASH:self.key_release_backslash()
    if e.key == K_RETURN:self.key_release_return()
    if e.key == K_MINUS:self.key_release_minus_sign()
    if e.key == K_0:self.key_release_0()
    if e.key == K_KP8:self.key_release_keypad_8()
    if e.key == K_DOLLAR:self.key_release_dollar()
    if e.key == K_PAGEDOWN:self.key_release_page_down()
    if e.key == K_EXCLAIM:self.key_release_exclaim()
    if e.key == K_1:self.key_release_1()
    if e.key == K_HELP:self.key_release_help()
    if e.key == K_3:self.key_release_3()
    if e.key == K_2:self.key_release_2()
    if e.key == K_BREAK:self.key_release_break()
    if e.key == K_4:self.key_release_4()
    if e.key == K_POWER:self.key_release_power()
    if e.key == K_6:self.key_release_6()
    if e.key == K_F12:self.key_release_f12()
    if e.key == K_7:self.key_release_7()
    if e.key == K_ESCAPE:self.key_release_escape()
    if e.key == K_BACKSPACE:self.key_release_backspace()
    if e.key == K_MENU:self.key_release_menu()
    if e.key == K_u:self.key_release_u()
    if e.key == K_PLUS:self.key_release_plus_sign()
    if e.key == K_KP6:self.key_release_keypad_6()
    if e.key == K_UNDERSCORE:self.key_release_underscore()
    if e.key == K_QUOTE:self.key_release_quote()
    if e.key == K_l:self.key_release_l()
    if e.key == K_KP0:self.key_release_keypad_0()
    if e.key == K_QUOTEDBL:self.key_release_quotedbl()
    if e.key == K_KP_MULTIPLY:self.key_release_keypad_multiply()
    if e.key == K_RSHIFT:self.key_release_right_shift()
    if e.key == K_KP1:self.key_release_keypad_1()
    if e.key == K_9:self.key_release_9()
    if e.key == K_KP9:self.key_release_keypad_9()
    if e.key == K_KP4:self.key_release_keypad_4()
    if e.key == K_KP5:self.key_release_keypad_5()
    if e.key == K_BACKQUOTE:self.key_release_grave()
    if e.key == K_KP7:self.key_release_keypad_7()
    if e.key == K_RCTRL:self.key_release_right_ctrl()
    if e.key == K_LALT:self.key_release_left_alt()
    if e.key == K_KP_DIVIDE:self.key_release_keypad_divide()
    if e.key == K_SYSREQ:self.key_release_sysrq()

  def limitPos(self, x, y, w, h, margin = 0, bounce = False):
    
    if self.pos.x<x+margin:
      self.pos.x = x+margin
      if bounce:
        self.v.bounce_off(math.pi/2)
      else:
        self.v.addTo(self.v.clone().bounce_off(math.pi/2))
    
    if self.pos.y<y+margin:
      self.pos.y = y+margin
      if bounce:
        self.v.bounce_off(0)
      else:
        self.v.addTo(self.v.clone().bounce_off(0))
    
    if self.pos.x>self.parent.size[0]-margin:
      self.pos.x = self.parent.size[0]-margin
      if bounce:
        self.v.bounce_off(math.pi/2)
      else:
        self.v.addTo(self.v.clone().bounce_off(math.pi/2))
    
    if self.pos.y>self.parent.size[1]-margin:
      self.pos.y = self.parent.size[1]-margin
      if bounce:
        self.v.bounce_off(0)
      else:
        self.v.addTo(self.v.clone().bounce_off(0))
    
  
  def collideRect(self, x, y, w, h):
    if x<self.pos.x and self.pos.x<x+w and y<self.pos.y and self.pos.y<y+h:
      return True
    else:
      return False
    
  def newObject(self, type, x, y, relative):
    if relative:
      x+=self.pos.x
      y+=self.pos.y
    self.parent.objects.push(self.parent.objectdict[type](self.parent, Point(x,y)))
  
class Image:
  def __init__(self,img):
    self.img = img
    self.width,self.height = self.img.get_rect().size
    

class ImageSprite(Sprite):
  imageCache = {}
  
  def __init__(self, parent, pos, image):
    Sprite.__init__(self,parent,pos)
    self._image = parent.images[image]['src']
    parent.log += 'sprite w/ image '+self._image+'\n'
    self.loaded = True
    if not ImageSprite.imageCache.has_key(self._image):
      ImageSprite.imageCache[self._image] = Image(pygame.image.load('../projects/Example1/images/'+self._image))
    
    self.create()
  
  def _step(self):
    Sprite._step(self)
    
    for obj in self.parent.objects:
      if obj is self:continue;
      if self.collidesWith(obj):
        self.collide(obj)
  
  def image(self):
    return ImageSprite.imageCache[self._image]
  
  def draw(self, screen):
    screen.blit(self.image().img,self.pos.pos())
  
  def limitPos(self, x, y, w, h, margin = 1, bounce = False):
    margin=5
    if self.pos.x<x+margin:
      self.pos.x = x+margin
      if bounce:
        self.v.bounce_off(math.pi/2)
      else:
        self.v.addTo(self.v.part(0).reverse())
    
    if self.pos.y<y+margin:
      self.pos.y = y+margin
      if bounce:
        self.v.bounce_off(0)
      else:
        self.v.addTo(self.v.part(math.pi/2).reverse())
    
    if self.pos.x+self.image().width>self.parent.size[0]-margin:
      self.pos.x = self.parent.size[0]-margin-self.image().width-1
      if bounce:
        self.v.bounce_off(math.pi/2)
      else:
        self.v.addTo(self.v.part(0).reverse())
    
    if self.pos.y+self.image().height>self.parent.size[1]-margin:
      self.pos.y = self.parent.size[1]-margin-self.image().height
      if bounce:
        self.v.bounce_off(0)
      else:
        self.v.addTo(self.v.part(math.pi/2).reverse())
  
  def collidesWith(self, other):
    if self.pos.x<=other.pos.x and other.pos.x<=self.pos.x+self.image().width or other.pos.x<=self.pos.x and self.pos.x<=other.pos.x+other.image().width:
      if self.pos.y<=other.pos.y and other.pos.y<=self.pos.y+self.image().height or other.pos.y<=self.pos.y and self.pos.y<=other.pos.y+other.image().height:
        return True
    return False
  
  def limitPosToScreen(self, bounce):
    self.limitPos(0,0,parent.size[0],parent.size[1],0,bounce)
  
  


