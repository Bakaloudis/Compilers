# KATSALIROS AGGELOS A.M. 2997  cse52997
# BAKALIS DIMITRIOS A.M. 3033  cse53033 

import parser

import re,sys
import inspect
from collections import OrderedDict
counter=0
tokens = []
string = []
L_counter=0
lines_counter = 0
token_index = 0

last_token = []
quads_inside_block=[] #used for putting quads from a block in function:from_quad_to_assembly
flag_while = 0 # gia emfwleumenes while
flag_if = 0 # gia emfwleumenes if
flag_dowhile = 0  # gia emfwleumenes dowhile
flag_loop = 0 # gia emfwleumenes loop
flag_forcase = 0  # gia emfwleumenes forcase
flag_incase = 0 # gia emfwleumenes incase
flag_function = 0 # gia emfwleumenes function
default_flag=0
number_of_functions_mips=0; #counter gia na auksanoume ton arithmo twn function ston assembly
function_name=[]
special =[['PROGRAM_DEC',"program"],['ENDPROGRAM_DEC',"endprogram"],['DECLARATIONS',"declare"],['IF_DEC',"if"],['THEN_DEC',"then"],['ELSE_DEC',"else"],['ENDIF_DEC',"endif"],['DOWHILE_DEC',"dowhile"],['WHILE_DEC',"while"],['ENDWHILE',"endwhile"],['LOOP_DEC',"loop"],['ENDLOOP_DEC',"endloop"],['EXIT_DEC',"exit"],['FORCASE_DEC',"forcase"],['ENDFORCASE_DEC',"endforcase"],['INCASE_DEC',"incase"],['ENDINCASE_DEC',"endincase"],['WHEN_DEC',"when"],['ENDWHEN_DEC',"endwhen"],['DEFAULT_DEC',"default"],['ENDDEFAULT_DEC',"enddefault"],['FUNCTION_DEC',"function"],['ENDFUNCTION_DEC',"endfunction"],['RETURN_DEC',"return"],['IN_DEC',"in"],['INOUT_DEC',"inout"],['INANDOUT_DEC',"inandout"],['AND_DEC',"and"],['OR_DEC',"or"],['NOT_DEC',"not"],['INPUT_DEC',"input"],['PRINT_DEC',"print"],['LOOP_DEC',"loop"],['ENDDOWHILE_DEC',"enddowhile"]]




##############################################################
#                                                            #
#                         LEXER                              #
#                                                            #
##############################################################

class Lexer(object):
  
    def __init__(self, source_code):
        self.source_code = source_code

    def tokenize(self):
      
      global tokens  #krataw ta tokens poy ftiaxnei o lexer
      new_lines = [] # exw tis 8eseis twn \n

      # briskw se poio string ginetai allagh grammhs kai ta krtaw se enan pinaka new_lines
      space_counter=0
      test=self.source_code
      temp_counter=0
      while temp_counter != len(test)-1:
        if test[temp_counter]== ' ' or test[temp_counter]== '\t' and test[temp_counter-1]!= '\n':
          space_counter+=1
          while test[temp_counter] == ' ' or test[temp_counter]== '\t':
            temp_counter+=1
        if test[temp_counter]== '\n' and test[temp_counter-1]!= '\n' :
         new_lines.append(space_counter+1)
         space_counter+=1
        temp_counter+=1
      

      # to string periexei ka8e grammh toy source kwdika gia ton elegxo twn tokens ston parser
      counter_t=-1
      global string
      help=""
      for i in self.source_code:
        counter_t+=1
        if i != '\n' and i!='\t':  # thelw na krataw mono to string xwris kena tabs ktlp
          help+=i
        elif i == '\n':        # bazw (and help!= "") an xreiastei na mhn metraw tis kenes grammes
          string.append(help)
          help=""
        if counter_t == len(self.source_code)-1:
          string.append(help)

      #print(new_lines)  

      source_code= self.source_code.split() #lista apo tis le3eis toy kwdika moy

      global counter  #metrhths gia thn lista mas
 
      reminder = 0 # flag gia elgxo eidikhs le3hs
      reminder2 = 0 # flag gia elegxo eidikhs le3hs (se periptwsh string)
      reminder3 = 0 # flag gia elegxo eidikhs le3hs meta apo grouping sumbolo ( se periptwsh string)

      while counter < len(source_code):

          word = source_code[counter]
          word = word[0: 30] #diabazw ta prwta 30 grammata apo ka8e leksh
       
          #elegxos gia akeraious
          if re.match('[0-9]',word):
            word2=word
            counter2=0 # metrhths gia ka8e mia le3h tou word
            flag = 0 # elegxos gia gramma
            while counter2 != len(word2):
              if word2[counter2].isalpha():
                flag+=1
              counter2+=1
            if flag != 0:
              print('invalid string:' + word)
              quit()
            else:
              if word[len(word)-1] == ';': 
                int_word=int(word[0:len(word) - 1])
                if int_word < 32767: # elegxos gia ta oria twn integer
                	tokens.append(['INTEGER',word[0:len(word) - 1]])
                else:
                	print('error integers must be under 32767')
                	quit()
              else:
                int_word=int(word)
                if int_word < 32767: # elegxos gia ta oria twn integer
                	tokens.append(['INTEGER',word])
                else:
                	print('error integers must be under 32767')
                	quit()
          #elegxos gia operations
          if word[0] in " + - * / " :
              if len(word) >= 2:
                if(word[1].isalnum()):
                  #print(word[1])
                  pr = 0
                  error_line = 0
                  for i in string:
                    pr+=1
                    if word in i:
                      error_line=str(pr)
                      break
                  print('error: syntax error in line: ' + error_line)
                  quit()
              else:
                tokens.append(['OPERATOR',word[0]])
          #elegxos gia sugriseis
          elif word[0] in "< > <= >= = <>":
              if word[0] == ">":
                if word[1]== "=":
                  if len(word)>=3:
                    print('error: word starting with "match" operator')
                    quit()
                  else:
                    tokens.append('MATCH',">=")
                elif len(word) == 1:
                    tokens.append('MATCH',">")
                else:
                    print('error: word starting with "match" operator')
                    quit()
              elif word[0] == "<":
                if word[1]== "=":
                  if len(word)>=3:
                    print('error: word starting with "match" operator')
                    quit()
                  else:
                    tokens.append('MATCH',"<=")
                elif word[1]== ">":
                  if len(word)>=3:
                    print('error: word starting with "match" operator')
                    quit()
                  else:
                    tokens.append('MATCH',"<>")
                elif len(word) == 1:
                    tokens.append('MATCH',"<")
                else:
                    print('error: word starting with "match" operator')
                    quit()
              elif word[0] == "=":
                if len(word)>=2:
                  print('error: word starting with "match" operator')
                  quit()
                else:
                  tokens.append('MATCH',"=")
          #elegxos gia anathesh
          elif word in ":=":
              pr = 0
              error_line = 0
              for i in string:
                pr+=1
                if word in i:
                  error_line=str(pr)
                  break
              print('error: can not have := alone in line: ' + error_line)
              quit()
          #elegxos gia diaxwristes
          elif word[0] in "; , :":
              print('error: seperators can not stand alone') 
              quit()    
          #elegxos gia omadopoihsh
          elif word[0] in "( ) [ ] ":
            if word[0] == ")" or word[0] == "]":
              if len(word) > 1:
                print('error: expresion can not start with ) or ]')
                quit()
            if len(word)>1:
              if word[0] == "(" or word[0] == "[":
                tokens.append(['GROUPING_SEP',word[0]])
                if word[1].isalpha() or (word[1].isalpha())==False :
                  word_s=word[1:len(word)]
                  #print(word_s)
                  ##################################################################
                  w=""  # kratame thn le3h poy einai prin apo eidiko xarakthra
                  flag = 0 # elexgoume an meta to string exoyme eidiko xarakthra (!= tou string)
                  pol = 0 # metrhths gia thn 8esh sto word poy koitame
                  flager = 0 # elegxoume thn periptwsh poy exoyme := ,<=, >=
                  flager2 = 0 # elegxoume thn periptwsh poy exoyme <>
                  flager3 = 0 # elegxoyme to string sthn periptwsh poy einai eidikos xarakrhras
                  integer="" # krataei ari8mous poy briskontai mesa se string
                  for i in word_s:
                    pol+=1
                    flag = 0 
                    #elegxos gia operations
                    if i in " + - * / " :
                      if flager3 == 1:
                        flager3 = 0
                      else:
                        if w != "":
                          tokens.append(['IDENTIFIER',w])
                      tokens.append(['OPERATOR',i])
                      flag=1
                      w=""
                    #elegxos gia sugriseis
                    elif i in "< > <= >= = <>":
                      if i == "=":
                        if flager == 1:
                          flager = 0
                          continue
                        else:
                          if flager3 == 1:
                            flager3 = 0
                          else:
                            if w != "":
                              tokens.append(['IDENTIFIER',w])
                          tokens.append(['MATCH',i])
                          flag=1
                          w=""
                      elif i == "<":
                        flager = 1
                        if pol!=len(word_s) and word_s[pol] == "=":   # gia to <=
                          if flager3 == 1:
                            flager3 = 0
                          else:
                            if w != "":
                              tokens.append(['IDENTIFIER',w])
                          tokens.append(['MATCH',"<="])
                          flag=1
                          w=""
                        elif pol!=len(word_s) and word_s[pol] == ">": # gia to <>
                          flager2 = 1
                          if flager3 == 1:
                            flager3 = 0
                          else:
                            if w != "":
                              tokens.append(['IDENTIFIER',w])
                          tokens.append(['MATCH',"<>"])
                          flag=1
                          w=""
                        else:
                          if flager3 == 1:
                            flager3 = 0
                          else:
                            if w != "":
                              tokens.append(['IDENTIFIER',w])
                          tokens.append(['MATCH',i])
                          flag=1
                          w=""
                      elif i == ">":
                        if flager2 == 1:
                          flager2 = 0
                          continue
                        flager = 1
                        if pol!=len(word_s) and word_s[pol] == "=":   # gia to >=
                          if flager3 == 1:
                            flager3 = 0
                          else:
                            if w != "":
                              tokens.append(['IDENTIFIER',w])
                          tokens.append(['MATCH',">="])
                          flag=1
                          w=""
                        else:
                          if flager3 == 1:
                            flager3 = 0
                          else:
                            if w != "":
                              tokens.append(['IDENTIFIER',w])
                          tokens.append(['MATCH',i])
                          flag=1
                          w=""
                    #elegxos gia diaxwristes
                    elif i in "; , :":
                      if i == ":":
                        flager=1
                        if pol!=len(word_s) and word_s[pol] == "=":   # gia thn ana8esh :=
                          if flager3 == 1:
                            flager3 = 0
                          else:
                            if w != "":
                              tokens.append(['IDENTIFIER',w])
                          tokens.append(['SETTING',":="])
                          flag=1
                          w=""
                        else:
                          if flager3 == 1:
                            flager3 = 0
                          else:
                            if w != "":
                              tokens.append(['IDENTIFIER',w])
                          tokens.append(['SEPERATORS',i])
                          flag=1
                          w=""
                      else:
                        if flager3 == 1:
                          flager3 = 0
                        else:
                          if w != "":
                            tokens.append(['IDENTIFIER',w])
                        tokens.append(['SEPERATORS',i])
                        flag=1
                        w=""
                    #elegxos gia omadopoihsh
                    elif i in "( ) [ ] ":
                      if flager3 == 1:
                        flager3 = 0
                      else:
                        if w != "":
                          tokens.append(['IDENTIFIER',w])
                      tokens.append(['GROUPING',i])
                      flag=1
                      w=""
                    elif i.isalpha() and flag == 0:
                      w+=i
                      if(pol == len(word_s)):
                      #elegxos gia eidikh leksh
                        for i in special:
                          if w == i[1]:
                            tokens.append(i)
                            reminder2 = 1
                            break
                          else:
                            reminder2 = 0
                        if reminder2 == 0:
                          if w != "":
                            tokens.append(['IDENTIFIER',w])
                        if w[len(w)-1] == ';':
                          tokens.append(['IDENTIFIER',w])  
                      elif word_s[pol] in "( ) [ ] ":          # elegxo to epomeno gramma an einai sumbolo omadopoihshs
                      #elegxos gia eidikh le3h
                        for i in special:
                          if w == i[1]:
                            flager3=1
                            tokens.append(i)
                            reminder3 = 1
                            break
                          else:
                            reminder3 = 0
                      elif word_s[pol] in "+ - * / ":          # elegxo to epomeno gramma an einai operation symbol
                      #elegxos gia eidikh le3h
                        for i in special:
                          if w == i[1]:
                            flager3=1
                            tokens.append(i)
                            reminder3 = 1
                            break
                          else:
                            reminder3 = 0
                      elif word_s[pol] in "< > >= <= = <> ":          # elegxo to epomeno gramma an einai match symbol
                      #elegxos gia eidikh le3h
                        for i in special:
                          if w == i[1]:
                            flager3=1
                            tokens.append(i)
                            reminder3 = 1
                            break
                          else:
                            reminder3 = 0
                      elif word_s[pol] in "; , :":          # elegxo to epomeno gramma an einai seperators
                      #elegxos gia eidikh le3h
                        for i in special:
                          if w == i[1]:
                            flager3=1
                            tokens.append(i)
                            reminder3 = 1
                            break
                          else:
                            reminder3 = 0  
                    elif i.isnumeric() and flag == 0: 
                      if pol != len(word_s):
                        if word_s[pol-2].isalpha():
                          for x in range((pol-1),len(word_s)):
                            if word_s[x].isalnum():
                              w+=word[x]
                            else:
                              break
                        elif (word_s[pol-2].isnumeric()==False):
                          for x in range((pol-1),len(word_s)):
                            if word_s[x].isnumeric():
                              integer+=word_s[x]
                            elif word_s[x].isalpha():
                              print('invalid string:' + word_s)
                              quit()
                            else:
                              break
                          if int(integer)>32767:
                            print('error:integer bigger than 32767')
                            quit()
                          tokens.append(['INTEGER',integer])
                          integer="" 
                      if pol == len(word_s):
                        if word_s[pol-2].isalpha():
                          w+=i
                          tokens.append(['IDENTIFIER',w])
                        elif (word_s[pol-2].isnumeric()==False):
                          integer+=word_s[pol-1]
                          if int(integer)>32767:
                            print('error:integer bigger than 32767')
                            quit()
                          tokens.append(['INTEGER',integer])
            elif len(word) == 1:
              tokens.append(['GROUPING_SEP',word[0]])
                  ################################################################# 
          #elegxos gia diaxwristes sxoliwn
          if word in "/* */ // ":
              #tokens.append(['COMMENT_SEP',word])
              word2=word
              counter2=counter
              word3=word
              if word2 == "/*":
                while word2 != "*/": 
                  counter2+=1
                  if source_code[counter2] == "/*": # elegxos gia synexomena sxolia 
                     pr = 0
                     error_line = 0
                     for i in string:
                       pr+=1
                       if word in i:
                         error_line=str(pr)
                         break
                     print('error: consecutive /* in line: '+ error_line)
                     quit()
                  elif source_code[counter2] == "*/": # elegxos gia termatismo sxoliwn 
                     #tokens.append(['COMMENT_SEP',source_code[counter2]]) 
                     counter=counter2
                     break
                  elif source_code[counter2] == "//":
                    pr = 0
                    error_line = 0
                    for i in string:
                      pr+=1
                      if word in i:
                        error_line=str(pr)
                        break
                    print('error: nested commmets in line: ' + error_line)
                    quit()
                  if counter2 == len(source_code)-1:
                    pr = 0
                    error_line = 0
                    for i in string:
                      pr+=1
                      if word in i:
                        error_line=str(pr)
                        break
                    print('error: unclosed comments in line: ' + error_line)
                    quit()
                  word2=source_code[counter2]
              elif word2 == "*/":
                pr = 0
                error_line = 0
                for i in string:
                  pr+=1
                  if word in i:
                    error_line=str(pr)
                    break
                print('error: starting with */ in line: ' + error_line)
                quit()
              if word3 == "//":
                for i in new_lines:
                  if counter < i:
                    counter = i -1
                    break
          #elegxos gia eidikh leksh
          for i in special:
            if word == i[1]:
              tokens.append(i)
              reminder = 1
              break
            else:
              reminder = 0
          #elegxos gia grammata kefalaia kai mh
          if reminder!=1 and (re.match('[a-z]',word) or re.match('[A-Z]',word)):
            #print(word)
            w=""  # kratame thn le3h poy einai prin apo eidiko xarakthra
            flag = 0 # elexgoume an meta to string exoyme eidiko xarakthra (!= tou string)
            pol = 0 # metrhths gia thn 8esh sto word poy koitame
            flager = 0 # elegxoume thn periptwsh poy exoyme := ,<=, >=
            flager2 = 0 # elegxoume thn periptwsh poy exoyme <>
            flager3 = 0 # elegxoyme to string sthn periptwsh poy einai eidikos xarakrhras
            integer="" # krataei ari8mous poy briskontai mesa se string
            for i in word:
              pol+=1
              flag = 0 
              #elegxos gia operations
              if i in " + - * / " :
                if flager3 == 1:
                  flager3 = 0
                else:
                  if w != "":
                    tokens.append(['IDENTIFIER',w])
                tokens.append(['OPERATOR',i])
                flag=1
                w=""
              #elegxos gia sugriseis
              elif i in "< > <= >= = <>":
                if i == "=":
                  if flager == 1:
                    flager = 0
                    continue
                  else:
                    if flager3 == 1:
                      flager3 = 0
                    else:
                      if w != "":
                        tokens.append(['IDENTIFIER',w])
                    tokens.append(['MATCH',i])
                    flag=1
                    w=""
                elif i == "<":
                  flager = 1
                  if pol!=len(word) and word[pol] == "=":   # gia to <=
                    if flager3 == 1:
                      flager3 = 0
                    else:
                      if w != "":
                        tokens.append(['IDENTIFIER',w])
                    tokens.append(['MATCH',"<="])
                    flag=1
                    w=""
                  elif pol!=len(word) and word[pol] == ">": # gia to <>
                    flager2 = 1
                    if flager3 == 1:
                      flager3 = 0
                    else:
                      if w != "":
                        tokens.append(['IDENTIFIER',w])
                    tokens.append(['MATCH',"<>"])
                    flag=1
                    w=""
                  else:
                    if flager3 == 1:
                      flager3 = 0
                    else:
                      if w != "":
                        tokens.append(['IDENTIFIER',w])
                    tokens.append(['MATCH',i])
                    flag=1
                    w=""
                elif i == ">":
                  if flager2 == 1:
                    flager2 = 0
                    continue
                  flager = 1
                  if pol!=len(word) and word[pol] == "=":   # gia to >=
                    if flager3 == 1:
                      flager3 = 0
                    else:
                      if w != "":
                        tokens.append(['IDENTIFIER',w])
                    tokens.append(['MATCH',">="])
                    flag=1
                    w=""
                  else:
                    if flager3 == 1:
                      flager3 = 0
                    else:
                      if w != "":
                        tokens.append(['IDENTIFIER',w])
                    tokens.append(['MATCH',i])
                    flag=1
                    w=""
              #elegxos gia diaxwristes
              elif i in "; , :":
                if i == ":":
                  flager=1
                  if pol!=len(word) and word[pol] == "=":   # gia thn ana8esh :=
                    if flager3 == 1:
                      flager3 = 0
                    else:
                      if w != "":
                        tokens.append(['IDENTIFIER',w])
                    tokens.append(['SETTING',":="])
                    flag=1
                    w=""
                  else:
                    if flager3 == 1:
                     flager3 = 0
                    else:
                      if w != "":
                        tokens.append(['IDENTIFIER',w])
                    tokens.append(['SEPERATORS',i])
                    flag=1
                    w=""
                else:
                   if flager3 == 1:
                     flager3 = 0
                   else:
                     if w != "":
                       tokens.append(['IDENTIFIER',w])
                   tokens.append(['SEPERATORS',i])
                   flag=1
                   w=""
              #elegxos gia omadopoihsh
              elif i in "( ) [ ] ":
                if flager3 == 1:
                  flager3 = 0
                else:
                  if w != "":
                    tokens.append(['IDENTIFIER',w])
                tokens.append(['GROUPING',i])
                flag=1
                w=""
              elif i.isalpha() and flag == 0:
                w+=i
                if(pol == len(word)):
                  #elegxos gia eidikh leksh
                  for i in special:
                    if w == i[1]:
                      tokens.append(i)
                      reminder2 = 1
                      break
                    else:
                      reminder2 = 0
                  if reminder2 == 0:
                    if w != "":
                      tokens.append(['IDENTIFIER',w])
                  if w[len(w)-1] == ';':
                    tokens.append(['IDENTIFIER',w])  
                elif word[pol] in "( ) [ ] ":          # elegxo to epomeno gramma an einai sumbolo omadopoihshs
                  #elegxos gia eidikh le3h
                  for i in special:
                    if w == i[1]:
                      flager3=1
                      tokens.append(i)
                      reminder3 = 1
                      break
                    else:
                      reminder3 = 0
                elif word[pol] in "+ - * / ":    # elegxo to epomeno gramma an einai operation symbol
                  #elegxos gia eidikh le3h
                  for i in special:
                    if w == i[1]:
                      flager3=1
                      tokens.append(i)
                      reminder3 = 1
                      break
                    else:
                      reminder3 = 0
                elif word[pol] in "< > <= >= = <> ":    # elegxo to epomeno gramma an einai match symbol
                  #elegxos gia eidikh le3h
                  for i in special:
                    if w == i[1]:
                      flager3=1
                      tokens.append(i)
                      reminder3 = 1
                      break
                    else:
                      reminder3 = 0
                elif word[pol] in "; , : ":    # elegxo to epomeno gramma an einai diaxwrisths
                  #elegxos gia eidikh le3h
                  for i in special:
                    if w == i[1]:
                      flager3=1
                      tokens.append(i)
                      reminder3 = 1
                      break
                    else:
                      reminder3 = 0
              elif i.isnumeric() and flag == 0: 
                if pol != len(word):
                  if word[pol-2].isalpha():
                    for x in range((pol-1),len(word)):
                      if word[x].isalnum():
                        w+=word[x]
                      else:
                        break
                  elif (word[pol-2].isnumeric()==False):
                    for x in range((pol-1),len(word)):
                      if word[x].isnumeric():
                        integer+=word[x]
                      elif word[x].isalpha():
                        print('invalid string:' + word)
                        quit()
                      else:
                        break
                    if int(integer) > 32767:
                            print('error:integer bigger than 32767')
                            quit()
                    tokens.append(['INTEGER',integer])
                    integer="" 
                if pol == len(word):
                  if word[pol-2].isalpha():
                    w+=i
                    tokens.append(['IDENTIFIER',w])
                  elif (word[pol-2].isnumeric()==False):
                    integer+=word[pol-1]
                    if int(integer)>32767:
                            print('error:integer bigger than 32767')
                            quit()
                    tokens.append(['INTEGER',integer])
 
               
          counter += 1
      
      #print(string)
      #print('---------------------------------------------------------------------------------------')
      #print (tokens)
      #print('number of tokens: ' + str(len(tokens)))
    
      return tokens
#############################################################
#                                                           #
#                    SYMBOL TABLE                           #
#                                                           #
#############################################################
scope_counter=0
scopes_array = [] #list of scopes that are being used at the moment
main_framelength=-1
class Scope():
    def __init__(self,nested_level=0,enclosing_scope=None):
      global scope_counter
      self.entities=[]
      self.nested_level=nested_level 
      self.enclosing_scope=enclosing_scope
      self.tmp_offset = 12
      self.scope_counter=scope_counter
    def addEntity(self,entity):
      self.entities.append(entity)
    def get_offset(self):
        self.tmp_offset+=4
        return (self.tmp_offset-4)
    def __str__(self):
      if(self.enclosing_scope==None):
        return self.__repr__() + ': ('+ str(self.nested_level) +')'
      return self.__repr__() + ': ('+ str(self.nested_level) + ', ' + self.enclosing_scope.__repr__() +',Enclose Scope Object level:'+str(self.enclosing_scope.scope_counter)+ ')'
      #return "Scope Object" + ': ('+ str(self.nested_level) + ', ' + self.enclosing_scope.__repr__() + ')'
################################################################################################################
class Argument():
  def __init__(self,parMode,next_argument=None):
    self.parMode=parMode
    self.next_argument=next_argument
  def set_next(self,next_argument):
    self.next_argument=next_argument
  def __str__(self):
    return self.__repr__() + ': (' + self.parMode + ',\t' + self.next_argument.__repr__() + ')'
    #return "Argument Object" + ': (' + self.parMode + ',\t' + self.next_argument.__repr__() + ')'
###################################################################################################################
class Entity():
  def __init__(self,name,type):
    self.name=name
    self.type=type
    self.next=None
  def __str__(self):
    return self.type + ':' + self.name
###################################################################################################################
class Variable(Entity):
  def __init__(self,name,offset=-1):
    super().__init__(name,"VARIABLE")
    self.offset=offset
  def __str__(self):
    return super().__str__() + ', offset: ' + str(self.offset)
###################################################################################################################
class Function(Entity):
  def __init__(self,name,startQuad=-1):
    super().__init__(name,"FUNCTION")
    self.startQuad=startQuad
    self.arguments=[]
    self.frame_length=-1
  def add_arguments(self,arg):
    self.arguments.append(arg)
  def set_framelength(self,frame_length):
    self.frame_length = frame_length
  def set_startsquad(self,startQuad):
    self.startQuad=startQuad
  def __str__(self):
    return super().__str__() + ', startquad: ' + str(self.startQuad) + ', framelength: ' +str(self.frame_length)
 ###################################################################################################################
class TempVariable(Entity):
  def __init__(self,name,offset=-1):
    super().__init__(name,"TMPVAR")
    self.offset=offset
  def __str__(self):
    return super().__str__() + ', offset: ' + str(self.offset)
################################################################################################################
class Parameter(Entity):
    def __init__(self,name,parMode,offset=-1):
        super().__init__(name,"PARAMETER")
        self.parMode=parMode
        self.offset=offset
    def __str__(self):
      return super().__str__() + ', mode: ' + self.parMode + ', offset: ' + str(self.offset)
###################################################################################################################
def add_newScope():
  global scope_counter
  scope_counter+=1
  upper_scope = scopes_array[-1] ##from right to left 
  curr_scope = Scope(upper_scope.nested_level +1,upper_scope)
  scopes_array.append(curr_scope)


def add_function_entity(name):
    # Function declarations are on the enclosing scope of
    # the current scope.
    nested_level = scopes_array[-1].enclosing_scope.nested_level
    if not unique_entity(name, "FUNCTION", nested_level):
        print('add_func entity error ')
        quit()
    scopes_array[-2].addEntity(Function(name)) 

def add_parameter_entity(name, par_mode):
    nested_level = scopes_array[-1].nested_level
    parameter_offset   = scopes_array[-1].get_offset()
    if not unique_entity(name, "PARAMETER", nested_level):
        print('add param entity error')
        quit()
    scopes_array[-1].addEntity(Parameter(name, par_mode, parameter_offset))
def add_variable_entity(name):
    nested_level = scopes_array[-1].nested_level
    var_offset   = scopes_array[-1].get_offset()
    if not unique_entity(name, "VARIABLE", nested_level):  #semantic anlysis
        print('add variable_entity ,not unique entity error')
        quit()
    if variable_is_parameter(name, nested_level):
        print('add var entity ,var is param error ' )
        quit()
    scopes_array[-1].addEntity(Variable(name, var_offset))
def add_function_argument(func_name, parMode):
    if (parMode == 'in'):
        new_arg = Argument('CV')
    elif (parMode == 'inout'):
        new_arg = Argument('REF')
    elif (parMode == 'inandout'):
      new_arg =Argument('INANDOUT')
    func_entity = search_entity(func_name, "FUNCTION")[0]
    if func_entity == None:
        print('add func arg error')
        quit()
            
    if func_entity.arguments != list():
        func_entity.arguments[-1].set_next(new_arg)
    func_entity.add_arguments(new_arg)
def search_entity(name, etype):
    if scopes_array == list():
        return
    tmp_scope = scopes_array[-1]
    while tmp_scope != None:
        for entity in tmp_scope.entities:
            if entity.name == name and entity.type == etype:
                return entity, tmp_scope.nested_level
        tmp_scope = tmp_scope.enclosing_scope
    tmp_scope=scopes_array[0]
    for entity in tmp_scope.entities:
            if entity.name == name  and entity.type == etype:
                return entity, tmp_scope.nested_level
def search_entity_by_name(name):
    if scopes_array == list():
        return
    tmp_scope = scopes_array[-1]
    while tmp_scope != None:
        for entity in tmp_scope.entities:
            if entity.name == name:
                return entity, tmp_scope.nested_level

        tmp_scope = tmp_scope.enclosing_scope
    tmp_scope=scopes_array[0]
    for entity in tmp_scope.entities:
            if entity.name == name:
                return entity, tmp_scope.nested_level
def unique_entity(name, etype, nested_level):
    if scopes_array[-1].nested_level < nested_level:
       return
    scope = scopes_array[nested_level]
    list_len = len(scope.entities)
    for i in range(list_len):
        for j in range(list_len):
            e1 = scope.entities[i]
            e2 = scope.entities[j]
            if e1.name == e2.name and e1.type == e2.type \
                    and e1.name == name and e1.type == etype:
                return False
    return True
def print_scopes():
  print('Printing Scopes:\n')
  for scope in scopes_array:
    nest_level= scope.nested_level +1
    print('\t'* nest_level + str(scope))
    for entity in scope.entities:
      print('|\t'*nest_level +str(entity))
      if isinstance(entity,Function):
        for arg in entity.arguments:
          print('|\t'*nest_level + '|\t' + str(arg))
  print('\n')
def variable_is_parameter(name, nested_level):
    if scopes_array[-1].nested_level < nested_level:
        return
    scope = scopes_array[nested_level]
    list_size = len(scope.entities)
    for i in range(list_size):
        e = scope.entities[i]
        if e.type == "PARAMETER" and e.name == name:
            return True
    return False
def update_quad_function_entity(name):
    start_quad = nextQuad()
    if name == tokens[1][1]:
        return start_quad
    func_entity = search_entity(name, "FUNCTION")[0]
    func_entity.set_startsquad(start_quad)
    return start_quad
def update_func_entity_framelength(name, framelength):
    global main_framelength
    if name == tokens[1][1]:
        main_framelength = framelength
        return
    func_entity = search_entity(name, "FUNCTION")[0]
    func_entity.set_framelength(framelength)
#############################################################
#                                                           #
#                    INTERMEDIATE CODE                      #
#                                                           #
#############################################################

quad_List = [] #array me ola ta quads  
nextquad = 0 #index pou deixnei se poio stoixeio tou quad list eimaste
var_dict=dict() #dictionary gia na krataei olous tous arithmous metablitwn px. L_1,L_2

next_temp_num_vars =1 #xrisimopoieite gia na auksithei to noumero twn metablitwn

class Quad():
    def __init__(self, label, op, arg1, arg2, res):
        self.label=label 
        self.op=op
        self.arg1=arg1 
        self.arg2 =arg2
        self.res = res

    def __str__(self):
        return '(' + str(self.label) + ': ' + str(self.op)+ ', ' + \
            str(self.arg1) + ', ' + str(self.arg2) + ', ' + str(self.res) + ')'

    def tofile(self):                                                        ##just a function to call it in create_int_file method
        return str(self.label) + ': (' + str(self.op)+ ', ' + \
            str(self.arg1) + ', ' + str(self.arg2) + ', ' + str(self.res) + ')'

def nextQuad():
  return nextquad

def generate_quad(op=None,arg1='_',arg2='_',res='_'):
  global nextquad
  newQuad = Quad(nextquad,op,arg1,arg2,res)
  quad_List.append(newQuad)
  nextquad +=1
def new_temp():
  global var_dict,next_temp_num_vars
  dict_key ='T_' + str(next_temp_num_vars)
  var_dict[dict_key]=None
  next_temp_num_vars+=1
  scopes_array[-1].addEntity(TempVariable(dict_key,scopes_array[-1].get_offset()))
  return dict_key
def backpatch(temp_list,result):
  global quad_code
  for quad in quad_List:
    if quad.label in temp_list:
      quad.res = result
def empty_list():
  return list()
def make_list(label):
  newlist = list()
  newlist.append(label)
  return newlist
def merge(list1,list2):
  return list1+list2
def create_int_file():
  if len(sys.argv)<2:
    int_file=open('test'+'.int','w',encoding = 'utf-8')
  else:
    if default_flag==1:
      int_file = open(sys.argv[1][:-4]+'.int','w',encoding = 'utf-8')
    else:
      int_file=open('test'+'.int','w',encoding = 'utf-8')
  for quad in quad_List:
    int_file.write(quad.tofile() +'\n')

  int_file.close()
def variable_declarations(quad):
    variables = dict()
    index = quad_List.index(quad) + 1
    while True:
        q = quad_List[index]
        if q.op == 'end_block':
            break
        if q.arg2 not in ('CV', 'REF', 'RET') and q.op != 'call':
            if isinstance(q.arg1, str):
                if q.arg1.isdigit()==False:
                  variables[q.arg1] = 'int'
            if isinstance(q.arg2, str):
                if q.arg2.isdigit()==False:
                  variables[q.arg2] = 'int'
            if isinstance(q.res, str):
                if q.res.isdigit()==False:
                  variables[q.res] = 'int'
        index += 1
    if '_' in variables:
        del variables['_']
    return OrderedDict(sorted(variables.items()))
def transform_declarations(variables):
    flag = False
    dec_value = '\n\tint '
    for var in variables:
        flag = True
        dec_value += var + ', '
    if flag == True:
        return dec_value[:-2] + ';'
    else:
        return ''
def transform_code_to_c(quad):
    addlabel = True
    if quad.op == 'jump':
        dec_value = 'goto L_' + str(quad.res) + ';'
    elif quad.op in ('=', '<>', '<', '<=', '>', '>='):
        op = quad.op
        if op == '=':
            op = '=='
        elif op == '<>':
            op = '!='
        dec_value = 'if (' + str(quad.arg1) + ' ' + op + ' ' + \
            str(quad.arg2) + ') goto L_' + str(quad.res) + ';'
    elif quad.op == ':=':
        dec_value = quad.res + ' = ' + str(quad.arg1) + ';'
    elif quad.op in ('+', '-', '*', '/'):
        dec_value = quad.res + ' = ' + str(quad.arg1) + ' ' + \
            str(quad.op) + ' ' + str(quad.arg2) + ';'
    elif quad.op == 'out':
        dec_value = 'printf("%d\\n", ' + str(quad.arg1) + ');'
    elif quad.op == 'retv':
        dec_value = 'return (' + str(quad.arg1) + ');'
    elif quad.op == 'begin_block':
        addlabel = False
        if quad.arg1 == tokens[1][1]:
            dec_value = 'int main(void)\n{'
        else: # Should never reach else.
            dec_value = 'int ' + quad.arg1 + '()\n{'
        variables = variable_declarations(quad)
        dec_value += transform_declarations(variables)
        dec_value += '\n\tL_' + str(quad.label) + ':'
    elif quad.op == 'call':
        # Should never reach this line.
        dec_value = quad.arg1 + '();'
    elif quad.op == 'end_block':
        addlabel = False
        dec_value = '\tL_' + str(quad.label) + ': {}\n'
        dec_value += '}\n'
    elif quad.op == 'halt':
        dec_value = 'return 0;' # change to exit() if arbitrary
                             # halt statements are enabled
                             # at a later time.
    else:
        return None
    if addlabel == True:
        dec_value = '\tL_' + str(quad.label) + ': ' + dec_value
    return dec_value


def create_c_code_file():
  global default_flag
  if len(sys.argv)<2:
    c_file = open('test'+'.c','w',encoding = 'utf-8')
  else:
    if default_flag==1:
      c_file = open(sys.argv[1][:-4]+'.c','w',encoding = 'utf-8')
    else:
      c_file = open('test'+'.c','w',encoding = 'utf-8')
  c_file.write('#include<stdio.h>\n\n\n')
  for quad in quad_List:
    temp_String =transform_code_to_c(quad)
    if temp_String!=None:
      c_file.write(temp_String +' //'+str(quad)+ '\n')
  c_file.close()




##############################################################
#                                                            #
#                         FINAL CODE                         #
#                                                            #
##############################################################

assembly_file = open(sys.argv[1][:-4]+'.asm','w',encoding = 'utf-8')


def gnvlcode(variable):

    global assembly_file

    entity, entity_level  = search_entity_by_name(variable)   

    current_level = scopes_array[-1].nested_level
    assembly_file.write('    lw      $t0, -4($sp)\n')

    counter = current_level - entity_level - 1 
    while  counter > 0:
        assembly_file.write('    lw      $t0, -4($t0)\n')
        counter -= 1

    assembly_file.write('    addi    $t0, $t0, -%d\n' % entity.offset)

def loadvr(variable,register):

    global assembly_file

    if str(variable).isdigit():
      assembly_file.write('    li      $t%s, %d\n' % (register, int(variable)))
    else:
        entity, entity_level = search_entity_by_name(variable)
        current_level  = scopes_array[-1].nested_level
        if entity.type == 'VARIABLE' and entity_level == 0:
          assembly_file.write('    lb      $t%s, -%d($s0)\n' % (register, entity.offset))
        elif entity.type == 'VARIABLE' and entity_level == current_level:
          assembly_file.write('    lb      $t%s, -%d($sp)\n' % (register, entity.offset))
        elif entity.type == 'PARAMETER' and entity.par_mode == 'in' and entity_level == current_level:
          assembly_file.write('    lb      $t%s, -%d($sp)\n' % (register, entity.offset))
        elif entity.type == 'TMPVAR':
          assembly_file.write('    lb      $t%s, -%d($sp)\n' % (register, entity.offset))
        elif entity.type == 'PARAMETER' and entity.par_mode == 'inout' and entity_level == current_level:
          assembly_file.write('    lb      $t0, -%d($sp)\n' % (entity.offset))
          assembly_file.write('    lb      $t%s, ($t0)\n' % (register))
        elif entity.type == 'VARIABLE' and entity_level < current_level:
          gnvlcode(variable)
          assembly_file.write('    lb      $t%s, ($t0)\n' % (register))
        elif entity.type == 'PARAMETER' and entity.par_mode == 'in' and entity_level < current_level:
          gnvlcode(variable)
          assembly_file.write('    lb      $t%s, ($t0)\n' % (register))
        elif entity.type == 'PARAMETER' and entity.par_mode == 'inout' and entity_level < current_level:
          gnvlcode(variable)
          assembly_file.write('    lb      $t0, ($t0)\n')
          assembly_file.write('    lb      $t%s, ($t0)\n' % (register))
        elif entity.type == 'FUNCTION':
          print()
        else:
        	print('cannot load argument from quad to a register')
        	quit()


def storerv(register,variable):
    
    global assembly_file
    #try:
    entity, entity_level = search_entity_by_name(variable)

    #except:
          # print("Variable %s is not declared"%variable)  
           #quit() 
    current_level  = scopes_array[-1].nested_level
    if entity.type == 'VARIABLE' and entity_level == 0:
      assembly_file.write('    sb      $t%s, -%d($s0)\n' % (register, entity.offset))
    elif entity.type == 'VARIABLE' and entity_level == current_level:
      assembly_file.write('    sb      $t%s, -%d($sp)\n' % (register, entity.offset))
    elif entity.type == 'PARAMETER' and entity.par_mode == 'in' and entity_level == current_level:
      assembly_file.write('    sb      $t%s, -%d($sp)\n' % (register, entity.offset))
    elif entity.type == 'TMPVAR':
      assembly_file.write('    sb      $t%s, -%d($sp)\n' % (register, entity.offset))
    elif entity.type == 'PARAMETER' and entity.par_mode == 'inout' and entity_level == current_level:
      assembly_file.write('    lb      $t0, -%d($sp)\n' % (entity.offset))
      assembly_file.write('    sb      $t%s, ($t0)\n' % (register))
    elif entity.type == 'VARIABLE' and entity_level < current_level:
      gnvlcode(variable)
      assembly_file.write('    sb      $t%s, ($t0)\n' % (register))
    elif entity.type == 'PARAMETER' and entity.par_mode == 'in' and entity_level < current_level:
      gnvlcode(variable)
      assembly_file.write('    sb      $t%s, ($t0)\n' % (register))
    elif entity.type == 'PARAMETER' and entity.par_mode == 'inout' and entity_level < current_level:
      gnvlcode(variable)
      assembly_file.write('    lb      $t0, ($t0)\n')
      assembly_file.write('    sb      $t%s, ($t0)\n' % (register)) 
    
    elif entity.type == 'FUNCTION':
      assembly_file.write('    sb      $t%s, ($t0)\n' % (register))
    else:
      print('cannot save argument from quad to a register')
      quit()


def from_quad_to_assembly(quad, block):

  global quads_inside_block
  global assembly_file,number_of_functions_mips,L_counter

    
  if quad.op == 'jump':
    assembly_file.write('L_%d:\n'%(quad.label))
    assembly_file.write('    j       L_%s\n' % quad.res)
  elif quad.op == '=':
    relop = 'beq'
    assembly_file.write('L_%d:\n'%(quad.label))
    loadvr(quad.arg1, '1')
    loadvr(quad.arg2, '2')
    assembly_file.write('    %s     $t1, $t2, L_%d\n' % (relop, quad.res))
  elif quad.op == '<>':
    relop = 'bne'
    assembly_file.write('L_%d:\n'%(quad.label))
    loadvr(quad.arg1, '1')
    loadvr(quad.arg2, '2')
    assembly_file.write('    %s     $t1, $t2, L_%d\n' % (relop, quad.res))
  elif quad.op == '<':
    relop = 'blt'
    assembly_file.write('L_%d:\n'%(quad.label))
    loadvr(quad.arg1, '1')
    loadvr(quad.arg2, '2')
    assembly_file.write('    %s     $t1, $t2, L_%d\n' % (relop, quad.res))
  elif quad.op == '<=':
    relop = 'ble'
    assembly_file.write('L_%d:\n'%(quad.label))
    loadvr(quad.arg1, '1')
    loadvr(quad.arg2, '2')
    assembly_file.write('    %s     $t1, $t2, L_%d\n' % (relop, quad.res))
  elif quad.op == '>':
    relop = 'bgt'
    assembly_file.write('L_%d:\n'%(quad.label))
    loadvr(quad.arg1, '1')
    loadvr(quad.arg2, '2')
    assembly_file.write('    %s     $t1, $t2, L_%d\n' % (relop, quad.res))
  elif quad.op == '>=':
    relop = 'bge'
    assembly_file.write('L_%d:\n'%(quad.label))
    loadvr(quad.arg1, '1')
    loadvr(quad.arg2, '2')
    assembly_file.write('    %s     $t1, $t2, L_%d\n' % (relop, quad.res))
  elif quad.op == ':=': ################# orisma ################# 
    assembly_file.write('L_%d:\n' % (quad.label))
    loadvr(quad.arg1, '1')
    storerv('1', quad.res)
  elif quad.op == '+':
    oper = 'add'
    assembly_file.write('L_%d:\n'%(quad.label))
    loadvr(quad.arg1, '1')
    loadvr(quad.arg2, '2')
    assembly_file.write('    %s     $t1, $t1, $t2\n' % oper)
    storerv('1', quad.res)
  elif quad.op == '-':
    oper = 'sub'
    assembly_file.write('L_%d:\n'%(quad.label))
    loadvr(quad.arg1, '1')
    loadvr(quad.arg2, '2')
    assembly_file.write('    %s     $t1, $t1, $t2\n' % oper)
    storerv('1', quad.res)
  elif quad.op == '*':
    oper = 'mul'
    assembly_file.write('L_%d:\n'%(quad.label))
    loadvr(quad.arg1, '1')
    loadvr(quad.arg2, '2')
    assembly_file.write('    %s     $t1, $t1, $t2\n' % oper)
    storerv('1', quad.res)
  elif quad.op == '/':
    oper = 'div'
    assembly_file.write('L_%d:\n'%(quad.label))
    loadvr(quad.arg1, '1')
    loadvr(quad.arg2, '2')
    assembly_file.write('    %s     $t1, $t1, $t2\n' % oper)
    storerv('1', quad.res)
  elif quad.op == 'out':
    assembly_file.write('L_%d:\n'%(quad.label))
    loadvr(quad.arg1,'1')
    assembly_file.write('    li      $v0, 1\n')
    assembly_file.write('    add      $a0,$zero,$t1 \n')
    assembly_file.write('    syscall       \n')
  elif quad.op == 'in':
    assembly_file.write('    li      $v0, 5\n')
    assembly_file.write('    syscall       \n')
  elif quad.op == 'retv':
    loadvr(quad.arg1, '1')
    assembly_file.write('    lb      $t0, -8($sp)\n')
    assembly_file.write('    sb      $t1, -8($t0)\n')
    assembly_file.write('    jr      $ra\n\n') # kanw jump sto address
    assembly_file.write('L_t%d:\n'%(L_counter))
    L_counter+=1
  elif quad.op == 'par':
    if block == tokens[1][1]:
      level_of_called_function = 0
      framelength = main_framelength
    else:
      entity, level_of_called_function = search_entity(block, 'FUNCTION')
      framelength = entity.framelength
    if quads_inside_block == []:
      assembly_file.write('    addi    $fp, $sp, -%d\n' % framelength)
      quads_inside_block.append(quad)
      temp_offset = 12 + 4 * quads_inside_block.index(quad)
      if quad.arg2 == 'CV':
        loadvr(quad.arg1, '0')
        assembly_file.write('    sb      $t0, -%d($fp)\n' % temp_offset)
      elif quad.arg2 == 'REF':
        
        variable_entity, variable_level = search_entity_by_name(quad.arg1)
        if level_of_called_function == variable_level:
          if variable_entity.type == 'VARIABLE':
            assembly_file.write('    addi    $t0, $sp, -%s\n' % variable_entity.offset)
            assembly_file.write('    sb      $t0, -%d($fp)\n' % temp_offset) 
          elif variable_entity.type == 'PARAMETER' and variable_entity.par_mode == 'in':
            assembly_file.write('    addi    $t0, $sp, -%s\n' % variable_entity.offset)
            assembly_file.write('    sb      $t0, -%d($fp)\n' % temp_offset)
          elif variable_entity.type == 'PARAMETER' and variable_entity.par_mode == 'inout':
            assembly_file.write('    lb      $t0, -%d($sp)\n' % variable_entity.offset)
            assembly_file.write('    sb      $t0, -%d($fp)\n' % temp_offset)
        else:
          if variable_entity.type == 'VARIABLE':
            gnvlcode(quad.arg1)
            assembly_file.write('    sb      $t0, -%d($fp)\n' % temp_offset)	
          elif variable_entity.type == 'PARAMETER' and variable_entity.par_mode == 'in':
            gnvlcode(quad.arg1)
            assembly_file.write('    sb      $t0, -%d($fp)\n' % temp_offset)
          elif variable_entity.type == 'PARAMETER' and variable_entity.par_mode == 'inout':
            gnvlcode(quad.arg1)
            assembly_file.write('    lb      $t0, 0($t0)\n')
            assembly_file.write('    sb      $t0, -%d($fp)\n' % temp_offset)
      elif quad.arg2 == 'RET':
        variable_entity, variable_level = search_entity_by_name(quad.arg1)
        assembly_file.write('    addi    $t0, $sp, -%d\n' % variable_entity.offset)  #addi =register+value
        assembly_file.write('    sb      $t0, -8($fp)\n')
  elif quad.op == 'call':
        if block == tokens[1][1]:
            level_of_called_function = 0
            framelength = main_framelength 
        else:
            entity, level_of_called_function = search_entity(block, 'FUNCTION')#parent
            framelength = entity.framelength
        nested_function_entity, nested_function_level = search_entity(quad.arg1, 'FUNCTION') #child
        #check_subprog_args(nested_function_level.name)
        if level_of_called_function == nested_function_level:
            assembly_file.write('    lb      $t0, -4($sp)\n')
            assembly_file.write('    sb      $t0, -4($fp)\n')
        else:
            assembly_file.write('    sb      $sp, -4($fp)\n')
        assembly_file.write('    addi    $sp, $sp, %d\n' % framelength)
        assembly_file.write('    jal     L_%s\n' % str(nested_function_entity.startQuad))
        assembly_file.write('    addi    $sp, $sp, -%d\n' % framelength)
  elif quad.op == 'begin_block':
        
        if block == tokens[1][1]:

            #assembly_file.seek(0,0)
            assembly_file.write('    j       L_0\n')
            assembly_file.write('L_0:\n')
            assembly_file.seek(0,2)   # Go to the end of the assembly file
            assembly_file.write('    addi    $sp, $sp, %d\n' % main_framelength)
            assembly_file.write('    move    $s0, $sp\n')
            #assembly_file.seek(0,2)
        else:
            assembly_file.write('    j 		L_t%d\n'%(L_counter))
            number_of_functions_mips += 1
            assembly_file.write('L_d%d:\n' % (number_of_functions_mips))
            assembly_file.write('    sb      $ra, 0($sp)\n')

  elif quad.op == 'halt':
    assembly_file.write('L_%d:\n'%(quad.label))
    assembly_file.write('    li      $v0, 10   # service code 10: exit\n')
    assembly_file.write('    syscall\n')
  elif quad.op == 'end_block':
       
        assembly_file.write('    lb      $ra, 0($sp)\n')
        assembly_file.write('    jr      $ra\n\n')









##############################################################
#                                                            #
#                         PARSER                             #
#                                                            #
##############################################################

def parse(self):
  
  global token_index # metraei se poio token briskomaste
  global last_token 
  generate_quad('begin_block',tokens[1][1])
  from_quad_to_assembly(quad_List[0],tokens[1][1])
  scopes_array.append(Scope())
  while token_index < len(tokens):
    
    token_type = tokens[token_index][0] # krataei ton typo tou token
    token_value = tokens[token_index][1] # krataei thn timh tou token
  
    if tokens[0][1] != 'program' or tokens[len(tokens)-1][1] != 'endprogram': # periptwsh poy den 3ekinaei me program h den teleiwnei me endprogram 
      print('error: program needs to start with "program <identifier>" and end with "endprogram" in line:' + lines())
      quit()
    else:
      if token_index == 0:
        token_index+=1
        if tokens[token_index][0] != 'IDENTIFIER': # periptwsh poy meta apo to program den erxetai identifier
          print('error: after "program" expect identifier in line:' + lines())
          quit()
      else:
        if len(tokens) == 3: # periptwsh poy dex exoyme block meta3y twn program kai endprogram
          print('error: there is no code between program and endprogram in line:' + lines())
          quit()
        
        block(tokens[1][1])
        
    token_index+=1
  generate_quad('halt')
  generate_quad('end_block',tokens[1][1])
  from_quad_to_assembly(quad_List[-2],tokens[1][1])
  from_quad_to_assembly(quad_List[-1],tokens[1][1])
def block(string):

  global token_index # metraei se poio token briskomaste
  global last_token
  #print("Entering ",string)
  #print_scopes() #  print symbol table
  declarations()
  subprograms()   
  start_quad_in_block=update_quad_function_entity(string)
  statements()
  update_func_entity_framelength(string,scopes_array[-1].tmp_offset)
  print("LEAVING ",string)
  print_scopes() #####printarete ena epipleon scope.object to opoio einai to arxiko pou balame sto def parser me scopes_array.append(Scope())
  if quad_List[start_quad_in_block-1].op== 'begin_block' and quad_List[start_quad_in_block-1].arg1!=tokens[1][1] :

    for quad in quad_List[start_quad_in_block-1:]:
  	  from_quad_to_assembly(quad,string)
  else:
    for quad in quad_List[start_quad_in_block:]:
  	  from_quad_to_assembly(quad,string)

  if len(scopes_array)!=1:
    scopes_array.pop()
  return

def declarations():

  global token_index # metraei se poio token briskomaste
  global last_token

  if tokens[token_index][0] != 'DECLARATIONS':
    return
  else:
    token_index+=1
    varlist()
    token_index+=1
    while tokens[token_index][1] == "declare": 
      token_index+=1
      varlist()
      token_index+=1 # proxwrame sthn epomenh le3h kai elegxoyme an yparxei pali declare
    return


def varlist():

  global token_index # metraei se poio token briskomaste
  global last_token

  if tokens[token_index][0] == 'IDENTIFIER':
    while tokens[token_index][1] != ';':
      if (tokens[token_index][0] == 'IDENTIFIER' or tokens[token_index][1] == ','):
        for i in last_token:
          if token_index == i and tokens[token_index][1]!= ';':
            print('error: declare must be followd by "identifier" or "," and end with ";" in line:' + lines())
            quit()
        if(tokens[token_index][0]=='IDENTIFIER'):
            add_variable_entity(tokens[token_index][1])
        token_index+=1
      else:
        print('error: after declare expect "identifier" or "," in line:' + lines())
        quit() 
    return 
  else:
    print('error: after declare expect identifier in line:' + lines())
    quit()
    

def subprograms():

  global token_index # metraei se poio token briskomaste
  global last_token
  global function_name
  subprogram()
  #generate_quad('end_block',function_name[-1])
  #function_name.pop()
  while tokens[token_index][1] == "FUNCTION_DEC":
    subprogram()
    #generate_quad('end_block',function_name[-1])
    #function_name.pop()
    token_index+=1
  return


def subprogram():

  global token_index # metraei se poio token briskomaste
  global last_token
  global flag_function
  global function_name
  tag = 0
  tag2 = 0
  count = 0

  if tokens[token_index][0] == "FUNCTION_DEC":
    if flag_function == 0:
      for x in range(token_index,len(tokens)):
        if tokens[x][1] == "function":
          tag+=1
      for x in range(token_index,len(tokens)):
        if tokens[x][1] == "endfunction":
          tag2+=1
      if tag != tag2:
        print('error: all "function" statements must be closed by "endfunction" in line:' + lines())
        quit()
      else:
        for x in range(0,len(tokens)):
          if tokens[x][1] == "return":
            count+=1
        if (count < tag and flag_function==0):
          print('error: every function-endfunction statement must have at least one return statement in line:' + lines())
          quit()
        if (count > tag and flag_function==0):
          print('error: every function-endfunction statement must have at max one return statement in line:' + lines())
          quit()
        flag_function = 1

    
    token_index+=1
    temp_func_name_for_block=tokens[token_index][1]
    if tokens[token_index][0] == "IDENTIFIER":
      function_name.append(tokens[token_index][1])
      generate_quad('begin_block',temp_func_name_for_block)
      add_newScope()
      add_function_entity(tokens[token_index][1])
      token_index+=1
      funcbody(tokens[token_index-1][1])
      if tokens[token_index+1][1]=='return':
        token_index+=1
        return_stat()
      generate_quad('end_block',temp_func_name_for_block)

      return
    else:
      print('error: after "function" expect identifier in line:' + lines())
      quit()
  else:
    return

def funcbody(function_name):

  global token_index # metraei se poio token briskomaste
  global last_token

  formalpars(function_name)
  token_index+=1
  block(function_name)
  return

def formalpars(function_name):

  global token_index # metraei se poio token briskomaste
  global last_token

  blank = -1 # me auto elegxo an metaksi twn "(" kai ")" den exw tipota 

  if tokens[token_index][1] == '(':
    temp_index=token_index
    for i in last_token:         # elegxo an o teleutaios xarakthras ths grammhs einai ) 
      if temp_index > i:
        print
      elif temp_index < i:
        temp_index+=1
        for x in range(temp_index,i+1):
          blank+=1
          if x == i and tokens[x][1] == ";":
            if tokens[x-1][1] != ")":
              print('error: the "(" statement must be closed by ")" in line:' + lines())
              quit()
          elif (x == i and tokens[x][1] != ")"):
            print('error: the "(" statement must be closed by ")" in line:' + lines())
            quit()
        break
    if blank == 1:
      return
    formalparlist(function_name)
    return
  else:
    print('error: after the id expect "(" in line:' + lines())
    quit()

def formalparlist(function_name):

  global token_index # metraei se poio token briskomaste
  global last_token

  formalparitem(function_name)
  token_index+=1
  while tokens[token_index][1] != ")":
    if tokens[token_index][1]!= ",":
      print('error: special characters (in,inout or inandout with "id") must be seperated by "," in line:' + lines())
      quit()
    else:
      formalparitem(function_name)
      token_index+=1
  return


def formalparitem(function_name):

  global token_index # metraei se poio token briskomaste
  global last_token
  temp_parameter=''
  token_index+=1
  if (tokens[token_index][0] == "IN_DEC") or (tokens[token_index][0] == "INOUT_DEC") or (tokens[token_index][0] == "INANDOUT_DEC"):
    temp_parameter+=tokens[token_index][1]
    token_index+=1
    if tokens[token_index][0] != 'IDENTIFIER':
      print('error: after special character (in,inout or inandout) expect identifier in line:' + lines())
      quit()
    else:
      add_function_argument(function_name,temp_parameter)
      add_parameter_entity(tokens[token_index][1],temp_parameter)
      return
  elif tokens[token_index][1]==')':
    token_index-=1
  else:
    return

def statements():

  global token_index # metraei se poio token briskomaste
  global last_token

  statement()
  if(tokens[token_index][0] == "IDENTIFIER" and tokens[token_index-1][1] != ";"):
  	print('error: expect ";" in previous line in line: ' + lines())
  	quit()
  if(tokens[token_index][1] == ";" and ( tokens[token_index+1][1] == "endif" or tokens[token_index+1][1] == "enddowhile" or tokens[token_index+1][1] == "endloop" or tokens[token_index+1][1] == "endprogram" or tokens[token_index+1][1] == "endwhile" or tokens[token_index+1][1] == "endforcase" or tokens[token_index+1][1] == "endincase" or tokens[token_index+1][1] == "endfunction" or tokens[token_index+1][1] == "enddefault" )):
    print('error: did not expect ";" before special "end-" commands in line: ' + lines())
    quit()
  if tokens[token_index][1] == "endprogram":
    return
  while tokens[token_index][1] == ";":
    #tokens[token_index-1][1] ="consumed" #### dhmiougoutan infinite loop epeidh evlepe prin ; kai meta desmeumenh leksi
    token_index+=1
    if tokens[token_index][0] =='IDENTIFIER':
  	    if tokens[token_index+1][0] != 'SETTING':
  		    return
    elif tokens[token_index][1]=="function" :
  	    token_index-=1
  	    return	
    
    statement()
  return

def statement():

  global token_index # metraei se poio token briskomaste
  global last_token

  assignment_stat()

  if_stat()

  while_stat()

  do_while_stat()

  loop_stat()

  exit_stat()

  

  forcase_stat()

  incase_stat()

  return_stat()

  input_stat()

  print_stat()

  endfunction_stat()

  endloop_stat()

  endif_stat()

  return


def endfunction_stat():
  global scope_counter
  count = 0

  if tokens[token_index][1] == "endfunction":
    scope_counter-=1
    for x in range(0, token_index):
      if tokens[x][1] == "function":
        count+=1
    if ( count == 0 ):
      print('error: "endfunction" must have the "function" statement above it to be correct in line ' + lines())
      quit()

def endloop_stat():
  global exit_stat_list
  count = 0

  if tokens[token_index][1] == "endloop":
    for x in range(0, token_index):
      if tokens[x][1] == "loop":
        count+=1
    if ( count == 0 ):
      print('error: "endloop" must have the "loop" statement above it to be correct in line ' + lines())
      quit()
    backpatch(exit_stat_list,nextQuad())
def endif_stat():

  count = 0

  if tokens[token_index][1] == "endif":
    for x in range(0, token_index):
      if tokens[x][1] == "if":
        count+=1
    if ( count == 0 ):
      print('error: "endif" must have the "if" statement above it to be correct in line ' + lines())
      quit()

def assignment_stat():

  global token_index # metraei se poio token briskomaste
  global last_token

  if tokens[token_index][0] != "IDENTIFIER":
    return
  else:
    assign_var=tokens[token_index][1]
    token_index+=1
    if tokens[token_index][0] == 'SETTING':
      token_index+=1
      value =expression()
      generate_quad(':=',value,'_',assign_var)
      return
    else:
      print('error: to assign something in a variable  expect ":=" after identifier in line:' + lines()) 
      quit()

def expression():

  global token_index # metraei se poio token briskomaste
  global last_token

  temp_optional_sign=optional_sign()
  temp_term=term()
  
  if temp_optional_sign!=None:
    tmp_sign=new_temp()
    generate_quad(temp_optional_sign,0,temp_term,tmp_sign)
    temp_term =tmp_sign
  if tokens[token_index][1] == "endprogram" or tokens[token_index][1] == "dowhile" or tokens[token_index][1] == "enddowhile" or tokens[token_index][1] == "return" or tokens[token_index][1] == "function" or tokens[token_index][1] == "endfunction" or tokens[token_index][1]==')' or tokens[token_index][1]==';':
    return temp_term

  while tokens[token_index][1] == "+" or tokens[token_index][1] == "-":

    temp_index=token_index
    for i in last_token:         # elegxo an o teleutaios xarakthras ths grammhs einai ";" "integer" "identifier" 
      if temp_index > i:
        print
      elif temp_index == i:
        if tokens[temp_index+1][1] != ";" and tokens[temp_index][0] != "INTEGER" and tokens[temp_index][0] != "IDENTIFIER" and tokens[temp_index][1] != ')':
          print('1error: line must end with ";", "identifier" or "integer" in line:' + lines())
          quit()
        break

    op=add_oper()

    temp_index=token_index
    for i in last_token:         # elegxo an o teleutaios xarakthras ths grammhs einai ";" "integer" "identifier" 
      if temp_index > i:
        print
      elif temp_index == i:
        if tokens[temp_index][1] != ";" and tokens[temp_index][0] != "INTEGER" and tokens[temp_index][0] != "IDENTIFIER":
          print('2error: line must end with ";", "identifier" or "integer" in line:' + lines())
          quit()
        break
    
    temp_term2=term()
    tmpvar=new_temp()
    generate_quad(op,temp_term,temp_term2,tmpvar)
    temp_term =tmpvar
  if tokens[token_index][1] == "endprogram" or tokens[token_index][1] == "dowhile" or tokens[token_index][1] == "enddowhile" or tokens[token_index][1] == "return" or tokens[token_index][1] == "function" or tokens[token_index][1] == "endfunction" or tokens[token_index][1]==')' or tokens[token_index][1]=='else' or tokens[token_index][1]=='endif':
    
    return temp_term

  #temp_index=token_index
  #for i in last_token:         # elegxo an o teleutaios xarakthras ths grammhs einai ";" "integer" "identifier" 
    #if temp_index > i:
      #print
    #elif temp_index == i and token_index != len(tokens)-1:
      #if tokens[temp_index][1] != ";" and tokens[temp_index][0] != "INTEGER" and tokens[temp_index][0] != "IDENTIFIER" :
        #print(tokens[token_index][1])
        #print('3error: line must end with ";", "identifier" or "integer" in line:' + lines())
        #quit()
      #break



  

  return temp_term

def optional_sign():

  global token_index # metraei se poio token briskomaste
  global last_token

  temp_add_oper=add_oper()
  return temp_add_oper

def add_oper():

  global token_index # metraei se poio token briskomaste
  global last_token

  if tokens[token_index][1] == "+" or tokens[token_index][1] == "-":
    token_index+=1
    return tokens[token_index-1][1]
  else:
    return

def term():

  global token_index # metraei se poio token briskomaste
  global last_token

  temp_factor=factor()
  token_index+=1
  while tokens[token_index][1] == "*" or tokens[token_index][1] == "/":
    temp_mul_oper=mul_oper()
    temp_factor2=factor()
    tmpvar=new_temp()
    generate_quad(temp_mul_oper,temp_factor,temp_factor2,tmpvar)
    temp_factor=tmpvar
    token_index+=1
  return temp_factor

def mul_oper():

  global token_index # metraei se poio token briskomaste
  global last_token

  if tokens[token_index][1] == "*" or tokens[token_index][1] == "/":
    token_index+=1
    return tokens[token_index-1][1]
  else:
    print('error :to put another factor need * or /')
    return

def factor():

  global token_index # metraei se poio token briskomaste
  global last_token

  blank = -1

  if tokens[token_index][0] == 'INTEGER':
    return tokens[token_index][1]
  elif tokens[token_index][0] == 'IDENTIFIER':
    temp_ident=tokens[token_index][1]
    temp_idtail=idtail()
    return temp_ident
  elif tokens[token_index][1] == "(" :
    temp_index=token_index
    for i in last_token:         # elegxo an o teleutaios xarakthras ths grammhs einai ) 
      if temp_index > i:
        print
      elif temp_index < i:
        temp_index+=1
        for x in range(temp_index,i+1):
          blank+=1
          if x == i and tokens[x][1] == ";":
            if tokens[x-1][1] != ")":
              print('error: the "(" statement must be closed by ")" in line:' + lines())
              quit()
          elif (x == i and tokens[x][1] != ")"):
            print('error: the "(" statement must be closed by ")" in line:' + lines())
            quit()
        break
    if blank < 1:
      print('error: must have something between "(" and ")" in line:' + lines())
      quit()
    token_index+=1
    temp_expr =expression()
    return temp_expr
  else:
    print('error: after match operator ":=" expect "constant","id" or "(" in line:' + lines())
    quit()

def idtail():

  global token_index # metraei se poio token briskomaste
  global last_token

  temp_actualparse=actualparse()
  return temp_actualparse


def actualparse():

  global token_index # metraei se poio token briskomaste
  global last_token
  temp_ident= tokens[token_index][1]
  blank = -1
  temp_actualpalist=tokens[token_index][1]       
  if tokens[token_index+1][1] == "(":  # elegxo an exw meta apo ton xarakthra moy "("
    temp_string_un_func=tokens[token_index][1]
    temp_index=token_index
    for i in last_token:         # elegxo an o teleutaios xarakthras ths grammhs einai ) 
      if temp_index > i:
        print
      elif temp_index < i:
        temp_index+=1
        for x in range(temp_index,i+1):
          blank+=1
          if x == i and tokens[x][1] == ";":
            if tokens[x-1][1] != ")":
              print('error: the "(" statement must be closed by ")" in line:' + lines())
              quit()
          elif (x == i and tokens[x][1] != ")"):
            print('error: the "(" statement must be closed by ")" in line:' + lines())
            quit()
        break
    if blank == 1:
      return
    token_index+=1
    actualparlist()
    temp_var=new_temp()
    generate_quad('par',temp_var,'RET')
    generate_quad('call',temp_ident)
    return
  else:
    return temp_actualpalist


def actualparlist():

  global token_index # metraei se poio token briskomaste
  global last_token

  actualparitem()
  while tokens[token_index][1] == ',' or tokens[token_index+1][1] == ',' :
    if tokens[token_index+1][1] == ',':
      token_index+=1
    actualparitem()
    token_index+=1
  return


def actualparitem():

  global token_index # metraei se poio token briskomaste
  global last_token

  
  token_index+=1
  if tokens[token_index][0] == "IN_DEC":
    token_index+=1
    exp =expression()
    generate_quad('par',exp,'CV')
    return
  elif tokens[token_index][0] == "INOUT_DEC" or tokens[token_index][0] == "INANDOUT_DEC":
    temp_param_type=tokens[token_index][1]
    token_index+=1
    temp_string_for_quad=tokens[token_index][1]
    if tokens[token_index][0] != 'IDENTIFIER':
      print('error: after "inout" or "inandout" expect id in line:' + lines())
      quit()
    else:
      if temp_param_type=='inout':
        generate_quad('par',temp_string_for_quad,'REF')
      elif temp_param_type=='inandout':
        generate_quad('par',temp_string_for_quad,'INANDOUT')
      return
  elif tokens[token_index][1]==')':
  	return
  else:
    print('Expect parameter type but nothing found at line:' + lines())
    quit()


#def expression3():

  #global token_index # metraei se poio token briskomaste
  #global last_token

  #optional_sign()
  #term()


  #if(tokens[token_index][0] == "IDENTIFIER" or tokens[token_index][0] == "INTEGER" or tokens[token_index][1] == "+" or tokens[token_index][1] == "-" ):
  	#print
  #else:
  	#return
 
  #while(tokens[token_index][1] == "+" or tokens[token_index][1] == "-" ):
  	#optional_sign()
  	#term()
  	

  #if(tokens[token_index][0] == "IDENTIFIER" or tokens[token_index][0] == "INTEGER" or tokens[token_index][1] == "+" or tokens[token_index][1] == "-" ):
  	#expression3()
  	#return
  #else:
  	#return
  	

def if_stat():

  global token_index # metraei se poio token briskomaste
  global last_token
  global flag_if

  tag = 0
  tag2 = 0
  blank = -1


  if tokens[token_index][1] == "if":
    if flag_if == 0:
      for x in range(token_index,len(tokens)):
        if tokens[x][1] == "if":
          tag+=1
      for x in range(token_index,len(tokens)):
        if tokens[x][1] == "endif":
          tag2+=1
      if tag != tag:
        print('error: all "if" statements must be closed by "endif" in line:' + lines())
        quit()
      else:
        flag_if = 1
    token_index+=1
    if tokens[token_index][1] == "(":
      temp_index=token_index
      for i in last_token:         # elegxo an o teleutaios xarakthras ths grammhs einai ) 
        if temp_index > i:
          print
        elif temp_index < i:
          temp_index+=1
          for x in range(temp_index,i+1):
            blank+=1
            if x == i and tokens[x][1] == "then" and tokens[x-1][1] != ")" :
              print('error: the "(" must be closed with ")" in line:' + lines())
              quit()
          break
      if blank == 1:
        print('error: must have something between "(" and ")" in line:' + lines())
        quit()
      token_index+=1

      (b_true,b_false)=condition()
      if(tokens[token_index][1] == "]"):
        token_index+=1
        if(tokens[token_index][1] == ")"):
          token_index+=1
      elif tokens[token_index][1] == ")":
      	token_index+=1
      if tokens[token_index][1] == "then":
        token_index+=1
        backpatch(b_true,nextQuad())
        statements()
        temp_list=make_list(nextQuad())
        generate_quad('jump')
        backpatch(b_false,nextQuad())
        else_part()
        backpatch(temp_list,nextQuad())
        if(tokens[token_index][1] == "endif"):
        	token_index+=1
        	if(tokens[token_index][1] == ";"):
        		token_index+=1
        return
      else:
        print('error: after if and (...) expect "then" in line:' + lines())
        quit()
  else:
    return



def else_part():

  global token_index # metraei se poio token briskomaste
  global last_token
  token_index+=1
  statements()
  return


def condition():

  global token_index # metraei se poio token briskomaste
  global last_token

  (b_true,b_false)=(q1_true,q1_false)=bool_term()

  while tokens[token_index][1] == "or":
    backpatch(b_false,nextQuad())
    (q2_true,q2_false)=bool_term()
    b_true=merge(b_true,q2_true)
    b_false= q2_false
    token_index+=1

  return (b_true,b_false)

def bool_term():

  global token_index # metraei se poio token briskomaste
  global last_token

  (q_true,q_false)=(r1_true,r1_false)=bool_factor()
  while tokens[token_index][1] == "and":
    backpatch(q_true,nextQuad())
    token_index+=1
    (r2_true,r2_false)=bool_factor()
    q_false=merge(q_false,r2_false)
    q_true =r2_true
    token_index+=1

  return (q_true,q_false)

def bool_factor():

  global token_index # metraei se poio token briskomaste
  global last_token

  blank = -1 

  if tokens[token_index][1] == "not":
    token_index+=1
    if tokens[token_index][1] == "[":
      temp_index=token_index
      for i in last_token:         # elegxo an o teleutaios xarakthras ths grammhs einai ] 
        if temp_index > i:
          print
        elif temp_index < i:
          temp_index+=1
          for x in range(temp_index,i+1):
            blank+=1
            if x == i and tokens[x][1] == "then" and tokens[x-1][1] == ")" and tokens[x-2][1]!="]" :
              print('error: the "[" must be closed by "]" in line:' + lines())
              quit()
          break
      if blank == 1:
        print('error: must have something between "[" and "]" in line:' + lines())
        quit()
      token_index+=1
      result=condition()
      result=list(reversed(result)) ########to kanv epidh sauth th periptwsh exv not ara true kai flase enalassontai
      return result
    else:
      print('error: after special character "not" expect "]" in line:' + lines())
      quit()
  elif tokens[token_index][1] == "[":
    temp_index=token_index
    for i in last_token:         # elegxo an o teleutaios xarakthras ths grammhs einai ]
      if temp_index > i:
        print
      elif temp_index < i:
        temp_index+=1
        for x in range(temp_index,i+1):
          blank+=1
          if x == i and tokens[x][1] != "]":
            print('error: last token of line must be "]" in line:' + lines())
            quit()
        break
    if blank == 1:
      print('error: must have something between "[" and "]" in line:' + lines())
      quit()
    result=condition()
    return
  else:
    resL=expression()
    temp_string=relational_oper()
    resR=expression()
    r_true = make_list(nextQuad())
    generate_quad(temp_string,resL,resR)
    r_false=make_list(nextQuad())
    generate_quad('jump')
    result=(r_true,r_false)
    return result


#def expression2():

  #global token_index # metraei se poio token briskomaste
  #lobal last_token

  #optional_sign()
  #term()
  
  #while tokens[token_index][1] == "+" or tokens[token_index][1] == "-":

    #add_oper()
    #term()

  #return

#def term2():

  #global token_index # metraei se poio token briskomaste
  #global last_token

  #mul_oper()
  #factor()

  #while tokens[token_index][1] == "*" or tokens[token_index][1] == "/":
   # mul_oper()
   # factor()
    #token_index+=1
  #return

def relational_oper():

  global token_index # metraei se poio token briskomaste
  global last_token


  if tokens[token_index][1] == "=" or tokens[token_index][1] == "<=" or tokens[token_index][1] == ">=" or tokens[token_index][1] == ">" or tokens[token_index][1] == "<" or tokens[token_index][1] == "<>":
    token_index+=1
    return tokens[token_index-1][1]
  else:
    print('error:expected rel oper at line :' + lines())
    quit()
    



def while_stat():

  global token_index # metraei se poio token briskomaste
  global last_token
  global flag_while

  tag = 0
  tag2 = 0
  blank = -1

  if tokens[token_index][1] == "while":
    if flag_while == 0:
      for x in range(token_index,len(tokens)):
        if tokens[x][1] == "while":
          tag+=1
      for x in range(token_index,len(tokens)):
        if tokens[x][1] == "endwhile":
          tag2+=1
      if tag != tag2:
        print('error: all "while" statements must be closed by "endwhile" in line:' + lines())
        quit()
      else:
        flag_while = 1
    token_index+=1
    quad_1 =nextQuad()
    if tokens[token_index][1] == "(":
      temp_index=token_index
      for i in last_token:         # elegxo an o teleutaios xarakthras ths grammhs einai ) 
        if temp_index > i:
          print
        elif temp_index < i:
          temp_index+=1
          for x in range(temp_index,i+1):
            blank+=1
            if x == i and tokens[x][1] != ")":
              print('error: last token of line must be ")" in line:' + lines())
              quit()
          break
      if blank == 1:
        print('error: must have something between "(" and ")" in line:' + lines())
        quit()
      token_index+=1
      (quad_1_true,quad_1_false)=condition()
      token_index+=1
      backpatch(quad_1_true,nextQuad())
      statements()
      generate_quad('jump','_','_',quad_1)
      backpatch(quad_1_false,nextQuad())
      return
  else:
    return


def do_while_stat():

  global token_index # metraei se poio token briskomaste
  global last_token
  global flag_dowhile

  blank = 0

  tag = 0
  tag2 = 0

  if tokens[token_index][1] == "dowhile":
    quad_2=nextQuad()
    if flag_dowhile == 0:
      for x in range(token_index,len(tokens)):
        if tokens[x][1] == "dowhile":
          tag+=1
      for x in range(token_index,len(tokens)):
        if tokens[x][1] == "enddowhile":
          tag2+=1
      if tag != tag2:
        print('error: all "dowhile" statements must be closed by "enddowhile" in line:' + lines())
        quit()
      else:
        flag_dowhile = 1
    token_index+=1
    statements()
    while(tokens[token_index][1] != "enddowhile"):
      statements()
      if(tokens[token_index][1] == ";"):
        token_index+=1
    if tokens[token_index][1] == "enddowhile":
      token_index+=1
      if tokens[token_index][1] == "(":
        temp_index=token_index
        for i in last_token:         # elegxo an o teleutaios xarakthras ths grammhs einai )
          if temp_index > i:
            print
          elif temp_index < i:
            temp_index+=1
            for x in range(temp_index,i+1):
              blank+=1
              if x == i and tokens[x][1] == ";" and tokens[x-1][1] != ")":
                print('error: the "(" must be closed by ")" in line:' + lines())
                quit()
              elif x == i and tokens[x][1] == ";":
              	print
              elif x == i and tokens[x][1] != ")":
                print('error: the "(" must be closed by ")" in line:' + lines())
                quit()
            break
        if blank == 1:
          print('error: must have something between "(" and ")" in line:' + lines())
          quit()
        token_index+=1
        (condition_true,condition_false)=condition()
        backpatch(condition_true,quad_2)
        quad_3=nextQuad()
        backpatch(condition_false,quad_3)
        return
      else:
        print('error: after enddowhile , in the case of do-while, expect "(" in line:' + lines())
        quit()
  else:
    return



def loop_stat():

  global token_index # metraei se poio token briskomaste
  global last_token
  global flag_loop

  tag = 0
  tag2 = 0
  
  if tokens[token_index][1] == "loop":
    quad_for_loop=nextQuad()
    if flag_loop == 0:
      for x in range(token_index,len(tokens)):
        if tokens[x][1] == "loop":
          tag+=1
      for x in range(token_index,len(tokens)):
        if tokens[x][1] == "endloop":
          tag2+=1
      if tag != tag2:
        print('error: all "loop" statements must be closed by "endloop" in line:' + lines())
        quit()
      else:
        flag_loop = 1
    token_index+=1
    statements()
    print(quad_List[-1])
    generate_quad('jump','_','_',quad_for_loop)
    return
  else:
    return

exit_stat_list=empty_list()
def exit_stat():

  global token_index # metraei se poio token briskomaste
  global last_token,exit_stat_list

  count = 0
  if tokens[token_index][1] == "exit":
   exit_stat_list=make_list(nextQuad())
   generate_quad('jump','_','_','_')
   token_index+=1
   return 
  else:
    return

def forcase_stat():

  global token_index # metraei se poio token briskomaste
  global last_token
  global flag_forcase

  tag = 0
  tag2 = 0
  blank = -1
  if tokens[token_index][1] == "forcase":
    quad_for_loop=nextQuad()
    default_list=empty_list()
    if flag_forcase == 0:
      for x in range(token_index,len(tokens)):
        if tokens[x][1] == "forcase":
          tag+=1
      for x in range(token_index,len(tokens)):
        if tokens[x][1] == "endforcase":
          tag2+=1
      if tag != tag2:
        print('error: all "forcase" statements must be closed by "endforcase" in line:' + lines())
        quit()
      else:
        flag_forcase = 1
    token_index+=1
    while tokens[token_index][1] == "when":
      blank = -1
      token_index+=1
      if tokens[token_index][1] == "(":
        temp_index=token_index
        for i in last_token:         # elegxo an o teleutaios xarakthras ths grammhs einai ) 
          if temp_index > i:
            print
          elif temp_index <= i:
            temp_index+=1
            for x in range(temp_index,i+1):
              blank+=1
              if x == i and tokens[x][1] == ":" and tokens[x-1][1] != ")" :
                print('error: the "(" must be closed with ")" in line:' + lines())
                quit()
              elif x == i and tokens[x][1] != ":" :
                print('error: after "when" and "(...)" expect ":" in line:' + lines())
                quit()
            break
        if blank == 1:
          print('error: must have something between "(" and ")" in line:' + lines())
          quit()
        token_index+=1
        (condition_true,condition_false)=condition()
        token_index+=2 # gia na kanoyme skip thn : gia na doyme to epomeno token
        backpatch(condition_true,nextQuad())
        statements()
        temp_list=make_list(nextQuad())
        generate_quad('jump')
        backpatch(condition_false,nextQuad())
        default_list=merge(default_list,temp_list)
        backpatch(default_list,nextQuad())
      else:
        print('error: after when expect "(" in line:' + lines())
        quit()
    if tokens[token_index][1] == "default":
      for x in range(token_index,len(tokens)):
        if tokens[x][1] == "enddefault":
          break
        elif x == len(tokens)-1 and tokens[x][1] != "enddefault":
          print('error: "default" statement must be closed with "enddefault" in line:' + lines())
          quit()
      token_index+=1
      if tokens[token_index][1] == ":":
        token_index+=1
        statements()
        generate_quad('jump','_','_',quad_for_loop)
        backpatch(default_list,nextQuad())
        return
      else:
        print('error: after "default" expect ":" in line:' + lines())
        quit()
    else:
      print('error: in forcase statement there is no "default" in line:' + lines())
      quit()


def incase_stat():

  global token_index # metraei se poio token briskomaste
  global last_token
  global flag_incase

  tag = 0
  tag2 = 0
  blank = -1

  if tokens[token_index][1] == "incase":
    temp__quad_incase=nextQuad()
    if flag_incase == 0:
      for x in range(token_index,len(tokens)):
        if tokens[x][1] == "incase":
          tag+=1
      for x in range(token_index,len(tokens)):
        if tokens[x][1] == "endincase":
          tag2+=1
      if tag != tag2:
        print('error: all "incase" statements must be closed by "endincase" in line:' + lines())
        quit()
      else:
        flag_incase = 1
    token_index+=1
    while tokens[token_index][1] == "when":
      blank = -1
      token_index+=1
      if tokens[token_index][1] == "(":
        temp_index=token_index
        for i in last_token:         # elegxo an o teleutaios xarakthras ths grammhs einai ) 
          if temp_index > i:
            print
          elif temp_index <= i:
            temp_index+=1
            for x in range(temp_index,i+1):
              blank+=1
              if x == i and tokens[x][1] == ":" and tokens[x-1][1] != ")" :
                print('error: the "(" must be closed with ")" in in line:' + lines())
                quit()
              elif x == i and tokens[x][1] != ":" :
                print('error: after "when" and "(...)" expect ":" in line:' + lines())
                quit()
            break
        if blank == 1:
          print('error: must have something between "(" and ")" in lines:' + lines())
          quit()
        token_index+=1
        (condition_true,condition_false)=condition()
        token_index+=2 # gia na kanoyme skip thn : gia na doyme to epomeno token
        backpatch(condition_true,nextQuad())
        statements()
        temp_list=make_list(nextQuad())
        generate_quad('jump','_','_',temp__quad_incase)
        backpatch(condition_false,nextQuad())
      else:
        print('error: after "when" expect "(" in line:' + lines())
        quit()
    return
  else:
    return

def input_stat():

  global token_index # metraei se poio token briskomaste
  global last_token

  if tokens[token_index][1] == "input":
    token_index+=1
    if tokens[token_index][0] == 'IDENTIFIER':
      generate_quad('inp',tokens[token_index][1],'_','_')
      return
    else:
      print('error: after input expect identifier in line:' + lines())
  else:
    return


def print_stat():

  global token_index # metraei se poio token briskomaste
  global last_token

  if tokens[token_index][1] == "print":
    token_index+=1
    temp_expr= expression()
    generate_quad('out',temp_expr)
  else:
    return

def return_stat():

  global token_index # metraei se poio token briskomaste
  global last_token

  count = 0
  flag = 0 

  if tokens[token_index][1] == "return":
    if (tokens[token_index-1][1] != ";"):
      print('error: previous statement of "return" must end with ";"  in lines:' + lines())
      quit()
    for x in range(token_index,len(tokens)):
      if tokens[x][1] == "endfunction":
        count+=1
    if(count == 0 ):
    	print('error: return statement must be between "function" and "endfunction" in line:' + lines())
    	quit()
    for x in range (token_index,len(tokens)):
    	if tokens[x][1] == "endfunction":
    		flag = x
    		break
    for z in range(token_index+1, flag):
    	if tokens[z][1] == "return":
          print('error: cannot have multiple return statements in one function-endfunction in line:' + lines())
          quit()
    	if tokens[z][1] == "function" :
          print('error: cannot have "return" before "function" statement in line:' + lines())
          quit()
    token_index+=1
    temp_expr=expression()
    generate_quad('retv',temp_expr)
  else:
    return


def lines():

  global token_index # metraei se poio token briskomaste
  global last_token
  global string

  counter1 = 0
  counter = 0

  flag = 0

  array = []

  for i in string: # periexei to arithmo twn kenwn grammwn mexri thn mh-kenh grammh a8roistika
    if i == "":
      counter1+=1
    else:
      array.append(counter1)

  for i in last_token: # elegxei se poia grammh brisketai to twrino token
    counter+=1
    if token_index>i:
      flag+=1
    elif token_index <= i:
      return (str(array[flag]+counter)) 


 
##############################################################
#                                                            #
#                         MAIN                               #
#                                                            #
##############################################################


def changed_lines():

  char_c = 0 # metrhths gia ton pinaka char_p
  char_p = [] # pinakas poy periexei ton arithmo twn grammatwn apo ka8e grammh toyu pinaka string

  global last_token 

  for i in string:
    for x in i:
      if x != ' ':
        char_c+=1
    char_p.append(char_c)
    char_c=0
  
  met = 0 # topikos athroisths gia ta tokens
  counter = 0 # metrhths gai ton pinaka char_p
  thesh = -1 # metrhths gia na 3eroume se poio token briskomaste
 
  for i in tokens:
    while char_p[counter] == 0:  # periptwsh poy exoume sunexwmena kena
      if counter == len(char_p)-1: # periptwsh pou eimaste sto teleutaio token
        thesh+=1
        last_token.append(thesh)
        break
      counter+=1
    thesh+=1
    met+=len(i[1])
    if met < char_p[counter]:
      continue
    elif met == char_p[counter]:
      last_token.append(thesh)
      counter+=1
      met = 0

 
  #print (tokens)
  #print(last_token)

    

def main():
  global default_flag
  content = ""
  #text=raw_input("Press 1 if you want to put a specific input file else will read text.stl file") ##version 2 python
  default_flag=1
  if len(sys.argv)<2:
   print('Please put file name')
   quit()
  if sys.argv[1][-4:]!='.stl':
   print('wrong file type,expected .stl')
   quit()
  with open(sys.argv[1], 'r') as file:
    content = file.read() 
   

  lex=Lexer(content) 
  tokens=lex.tokenize()

  changed_lines()

  parse(tokens)
  create_int_file()
  create_c_code_file()
main()





