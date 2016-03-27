
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.8'

_lr_method = 'LALR'

_lr_signature = '55C53B9434ED5FC68BBE31AE8D09ED67'
    
_lr_action_items = {'INPUT':([16,],[20,]),'LBRACE':([0,1,4,5,7,8,19,28,],[2,2,-4,-5,-3,-2,-7,-6,]),'OP_DIV':([16,],[21,]),'OP_ADD':([16,],[26,]),'ID':([2,9,10,11,12,13,14,15,16,18,20,21,22,23,24,25,26,27,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,54,55,57,58,],[9,11,17,-26,-9,-27,11,-28,22,-8,31,11,11,11,11,40,11,31,-15,31,-17,-11,47,-30,11,11,-21,11,11,11,11,31,-13,-14,-10,56,-18,-29,-25,-20,-23,-24,-22,-12,-19,-16,]),'OP_SUB':([16,],[23,]),'STRING':([9,11,12,13,14,15,18,21,22,23,24,26,32,34,35,36,37,38,39,40,41,43,45,48,49,50,51,52,54,55,57,],[15,-26,-9,-27,15,-28,-8,15,15,15,15,15,-11,-30,15,15,-21,15,15,15,15,-13,-10,-29,-25,-20,-23,-24,-22,-12,-19,]),'ASSIGN':([16,],[25,]),'OP_MUL':([16,],[24,]),'RBRACE':([11,12,13,14,15,18,32,37,43,45,49,50,51,52,54,55,57,],[-26,-9,-27,19,-28,-8,-11,-21,-13,-10,-25,-20,-23,-24,-22,-12,-19,]),'OUTPUT':([16,],[27,]),'NUMBER':([9,11,12,13,14,15,18,21,22,23,24,26,32,34,35,36,37,38,39,40,41,43,45,48,49,50,51,52,54,55,57,],[13,-26,-9,-27,13,-28,-8,13,13,13,13,13,-11,-30,13,13,-21,13,13,13,13,-13,-10,-29,-25,-20,-23,-24,-22,-12,-19,]),'$end':([1,3,4,5,7,8,19,28,],[-1,0,-4,-5,-3,-2,-7,-6,]),'IMPORT':([6,],[10,]),'RPAREN':([11,13,15,17,20,22,27,29,30,31,32,34,35,36,37,38,39,41,42,43,44,45,48,49,50,51,52,53,54,55,56,57,58,],[-26,-27,-28,28,32,37,43,-15,45,-17,-11,-30,49,50,-21,51,52,54,55,-13,-14,-10,-29,-25,-20,-23,-24,57,-22,-12,58,-19,-16,]),'LPAREN':([0,1,4,5,7,8,9,11,12,13,14,15,18,19,20,21,22,23,24,26,27,28,29,30,31,32,34,35,36,37,38,39,40,41,42,43,44,45,48,49,50,51,52,54,55,57,58,],[6,6,-4,-5,-3,-2,16,-26,-9,-27,16,-28,-8,-7,33,16,16,16,16,16,33,-6,-15,33,-17,-11,-30,16,16,-21,16,16,16,16,33,-13,-14,-10,-29,-25,-20,-23,-24,-22,-12,-19,-16,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'type':([33,],[46,]),'expression':([9,14,21,22,23,24,26,35,36,38,39,40,41,],[12,18,34,34,34,34,34,48,48,48,48,53,48,]),'declaration':([20,27,30,42,],[29,29,44,44,]),'declaration_list':([20,27,],[30,42,]),'statement_list':([0,],[1,]),'expression_list':([9,],[14,]),'program':([0,],[3,]),'import_statement':([0,1,],[4,7,]),'component':([0,1,],[5,8,]),'parameter_list':([21,22,23,24,26,],[35,36,38,39,41,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> statement_list','program',1,'p_program','parser.py',8),
  ('statement_list -> statement_list component','statement_list',2,'p_statement_list','parser.py',13),
  ('statement_list -> statement_list import_statement','statement_list',2,'p_statement_list','parser.py',14),
  ('statement_list -> import_statement','statement_list',1,'p_statement_list','parser.py',15),
  ('statement_list -> component','statement_list',1,'p_statement_list','parser.py',16),
  ('import_statement -> LPAREN IMPORT ID RPAREN','import_statement',4,'p_import','parser.py',26),
  ('component -> LBRACE ID expression_list RBRACE','component',4,'p_component','parser.py',30),
  ('expression_list -> expression_list expression','expression_list',2,'p_expression_list','parser.py',34),
  ('expression_list -> expression','expression_list',1,'p_expression_list','parser.py',35),
  ('expression -> LPAREN INPUT declaration_list RPAREN','expression',4,'p_inputExpr','parser.py',43),
  ('expression -> LPAREN INPUT RPAREN','expression',3,'p_inputExpr','parser.py',44),
  ('expression -> LPAREN OUTPUT declaration_list RPAREN','expression',4,'p_outputExpr','parser.py',51),
  ('expression -> LPAREN OUTPUT RPAREN','expression',3,'p_outputExpr','parser.py',52),
  ('declaration_list -> declaration_list declaration','declaration_list',2,'p_declaration_list','parser.py',59),
  ('declaration_list -> declaration','declaration_list',1,'p_declaration_list','parser.py',60),
  ('declaration -> LPAREN type ID RPAREN','declaration',4,'p_id','parser.py',68),
  ('declaration -> ID','declaration',1,'p_id','parser.py',69),
  ('type -> ID','type',1,'p_type_id','parser.py',76),
  ('expression -> LPAREN ASSIGN ID expression RPAREN','expression',5,'p_assignExpr','parser.py',80),
  ('expression -> LPAREN ID parameter_list RPAREN','expression',4,'p_named_function_operation','parser.py',84),
  ('expression -> LPAREN ID RPAREN','expression',3,'p_named_function_operation','parser.py',85),
  ('expression -> LPAREN OP_ADD parameter_list RPAREN','expression',4,'p_add','parser.py',92),
  ('expression -> LPAREN OP_SUB parameter_list RPAREN','expression',4,'p_sub','parser.py',96),
  ('expression -> LPAREN OP_MUL parameter_list RPAREN','expression',4,'p_mul','parser.py',100),
  ('expression -> LPAREN OP_DIV parameter_list RPAREN','expression',4,'p_div','parser.py',104),
  ('expression -> ID','expression',1,'p_expression_id','parser.py',108),
  ('expression -> NUMBER','expression',1,'p_number','parser.py',112),
  ('expression -> STRING','expression',1,'p_string','parser.py',116),
  ('parameter_list -> parameter_list expression','parameter_list',2,'p_parameter_list','parser.py',120),
  ('parameter_list -> expression','parameter_list',1,'p_parameter_list','parser.py',121),
]
