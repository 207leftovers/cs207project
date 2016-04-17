
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.8'

_lr_method = 'LALR'

_lr_signature = 'B7DA2FE6C22431AB95D14A63E4FE0078'
    
_lr_action_items = {'OUTPUT':([17,],[21,]),'$end':([1,2,5,6,9,10,18,20,],[-5,-4,0,-1,-2,-3,-6,-7,]),'OP_SUB':([17,],[28,]),'RPAREN':([11,13,15,16,21,24,26,29,30,32,33,34,35,36,37,38,40,41,42,43,46,47,48,49,50,51,52,53,54,55,56,57,58,],[18,-28,-26,-27,33,37,40,-17,-15,47,-13,-30,48,50,-21,51,-11,53,54,55,-14,-12,-25,-29,-22,-20,57,-10,-24,-23,58,-19,-16,]),'STRING':([8,12,13,14,15,16,19,22,23,24,27,28,33,34,35,36,37,38,39,40,42,43,47,48,49,50,51,53,54,55,57,],[13,13,-28,-9,-26,-27,-8,13,13,13,13,13,-13,-30,13,13,-21,13,13,-11,13,13,-12,-25,-29,-22,-20,-10,-24,-23,-19,]),'OP_DIV':([17,],[22,]),'ASSIGN':([17,],[25,]),'OP_ADD':([17,],[23,]),'ID':([4,7,8,12,13,14,15,16,17,19,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,53,54,55,57,58,],[8,11,15,15,-28,-9,-26,-27,24,-8,29,15,15,15,39,29,15,15,-17,-15,44,29,-13,-30,15,15,-21,15,15,-11,29,15,15,-18,56,-14,-12,-25,-29,-22,-20,-10,-24,-23,-19,-16,]),'NUMBER':([8,12,13,14,15,16,19,22,23,24,27,28,33,34,35,36,37,38,39,40,42,43,47,48,49,50,51,53,54,55,57,],[16,16,-28,-9,-26,-27,-8,16,16,16,16,16,-13,-30,16,16,-21,16,16,-11,16,16,-12,-25,-29,-22,-20,-10,-24,-23,-19,]),'LPAREN':([0,1,2,6,8,9,10,12,13,14,15,16,18,19,20,21,22,23,24,26,27,28,29,30,32,33,34,35,36,37,38,39,40,41,42,43,46,47,48,49,50,51,53,54,55,57,58,],[3,-5,-4,3,17,-2,-3,17,-28,-9,-26,-27,-6,-8,-7,31,17,17,17,31,17,17,-17,-15,31,-13,-30,17,17,-21,17,17,-11,31,17,17,-14,-12,-25,-29,-22,-20,-10,-24,-23,-19,-16,]),'LBRACE':([0,1,2,6,9,10,18,20,],[4,-5,-4,4,-2,-3,-6,-7,]),'INPUT':([17,],[26,]),'IMPORT':([3,],[7,]),'RBRACE':([12,13,14,15,16,19,33,37,40,47,48,50,51,53,54,55,57,],[20,-28,-9,-26,-27,-8,-13,-21,-11,-12,-25,-22,-20,-10,-24,-23,-19,]),'OP_MUL':([17,],[27,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'type':([31,],[45,]),'expression_list':([8,],[12,]),'declaration_list':([21,26,],[32,41,]),'component':([0,6,],[1,9,]),'import_statement':([0,6,],[2,10,]),'parameter_list':([22,23,24,27,28,],[35,36,38,42,43,]),'expression':([8,12,22,23,24,27,28,35,36,38,39,42,43,],[14,19,34,34,34,34,34,49,49,49,52,49,49,]),'program':([0,],[5,]),'statement_list':([0,],[6,]),'declaration':([21,26,32,41,],[30,30,46,46,]),}

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
  ('expression -> LPAREN OP_ADD parameter_list RPAREN','expression',4,'p_op_add_expression','parser.py',92),
  ('expression -> LPAREN OP_SUB parameter_list RPAREN','expression',4,'p_op_sub_expression','parser.py',95),
  ('expression -> LPAREN OP_MUL parameter_list RPAREN','expression',4,'p_op_mul_expression','parser.py',98),
  ('expression -> LPAREN OP_DIV parameter_list RPAREN','expression',4,'p_op_div_expression','parser.py',101),
  ('expression -> ID','expression',1,'p_expression_id','parser.py',105),
  ('expression -> NUMBER','expression',1,'p_number','parser.py',109),
  ('expression -> STRING','expression',1,'p_string','parser.py',113),
  ('parameter_list -> parameter_list expression','parameter_list',2,'p_parameter_list','parser.py',117),
  ('parameter_list -> expression','parameter_list',1,'p_parameter_list','parser.py',118),
]
