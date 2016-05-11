
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.8'

_lr_method = 'LALR'

_lr_signature = '55C53B9434ED5FC68BBE31AE8D09ED67'
    
_lr_action_items = {'INPUT':([12,],[20,]),'OP_SUB':([12,],[21,]),'LPAREN':([0,3,5,6,7,9,10,11,13,14,15,16,18,19,20,21,22,23,24,26,27,28,29,30,32,33,34,35,36,37,38,39,40,41,42,43,46,47,48,49,50,51,52,54,55,57,58,],[4,-4,-5,4,12,-3,-2,12,-27,-9,-26,-28,-8,-7,31,12,12,31,12,12,12,-6,-15,-17,-11,31,12,-30,12,-13,31,12,12,12,-21,12,-14,-10,-29,-23,-22,-12,-24,-20,-25,-19,-16,]),'IMPORT':([4,],[8,]),'$end':([1,3,5,6,9,10,19,28,],[0,-4,-5,-1,-3,-2,-7,-6,]),'RPAREN':([13,15,16,17,20,23,26,29,30,32,33,34,35,36,37,38,39,41,42,43,46,47,48,49,50,51,52,53,54,55,56,57,58,],[-27,-26,-28,28,32,37,42,-15,-17,-11,47,49,-30,50,-13,51,52,54,-21,55,-14,-10,-29,-23,-22,-12,-24,57,-20,-25,58,-19,-16,]),'OP_ADD':([12,],[22,]),'OUTPUT':([12,],[23,]),'RBRACE':([11,13,14,15,16,18,32,37,42,47,49,50,51,52,54,55,57,],[19,-27,-9,-26,-28,-8,-11,-13,-21,-10,-23,-22,-12,-24,-20,-25,-19,]),'ASSIGN':([12,],[25,]),'LBRACE':([0,3,5,6,9,10,19,28,],[2,-4,-5,2,-3,-2,-7,-6,]),'OP_MUL':([12,],[24,]),'ID':([2,7,8,11,12,13,14,15,16,18,20,21,22,23,24,25,26,27,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,54,55,57,58,],[7,15,17,15,26,-27,-9,-26,-28,-8,30,15,15,30,15,40,15,15,-15,-17,45,-11,30,15,-30,15,-13,30,15,15,15,-21,15,56,-18,-14,-10,-29,-23,-22,-12,-24,-20,-25,-19,-16,]),'STRING':([7,11,13,14,15,16,18,21,22,24,26,27,32,34,35,36,37,39,40,41,42,43,47,48,49,50,51,52,54,55,57,],[16,16,-27,-9,-26,-28,-8,16,16,16,16,16,-11,16,-30,16,-13,16,16,16,-21,16,-10,-29,-23,-22,-12,-24,-20,-25,-19,]),'NUMBER':([7,11,13,14,15,16,18,21,22,24,26,27,32,34,35,36,37,39,40,41,42,43,47,48,49,50,51,52,54,55,57,],[13,13,-27,-9,-26,-28,-8,13,13,13,13,13,-11,13,-30,13,-13,13,13,13,-21,13,-10,-29,-23,-22,-12,-24,-20,-25,-19,]),'OP_DIV':([12,],[27,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'type':([31,],[44,]),'program':([0,],[1,]),'expression':([7,11,21,22,24,26,27,34,36,39,40,41,43,],[14,18,35,35,35,35,35,48,48,48,53,48,48,]),'parameter_list':([21,22,24,26,27,],[34,36,39,41,43,]),'declaration':([20,23,33,38,],[29,29,46,46,]),'import_statement':([0,6,],[3,9,]),'expression_list':([7,],[11,]),'component':([0,6,],[5,10,]),'statement_list':([0,],[6,]),'declaration_list':([20,23,],[33,38,]),}

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
