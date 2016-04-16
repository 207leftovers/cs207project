
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.8'

_lr_method = 'LALR'

_lr_signature = 'B7DA2FE6C22431AB95D14A63E4FE0078'
    
_lr_action_items = {'OP_SUB':([16,],[20,]),'$end':([2,3,4,5,8,9,19,28,],[-4,0,-5,-1,-3,-2,-7,-6,]),'ID':([1,7,10,11,12,13,14,15,16,18,20,21,22,23,24,25,26,27,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,48,49,50,51,52,53,54,55,56,58,],[7,12,17,-9,-26,12,-27,-28,21,-8,12,12,33,12,36,12,36,12,-30,12,-21,12,12,12,-15,-17,36,52,-11,12,36,-13,12,-29,-23,-20,-24,-14,-10,57,-18,-25,-12,-22,-19,-16,]),'OP_ADD':([16,],[27,]),'ASSIGN':([16,],[22,]),'OP_MUL':([16,],[23,]),'RBRACE':([11,12,13,14,15,18,31,39,42,45,46,48,50,53,54,55,56,],[-9,-26,19,-27,-28,-8,-21,-11,-13,-23,-20,-24,-10,-25,-12,-22,-19,]),'LBRACE':([0,2,4,5,8,9,19,28,],[1,-4,-5,1,-3,-2,-7,-6,]),'INPUT':([16,],[24,]),'OP_DIV':([16,],[25,]),'OUTPUT':([16,],[26,]),'NUMBER':([7,11,12,13,14,15,18,20,21,23,25,27,29,30,31,32,33,34,39,40,42,43,44,45,46,48,50,53,54,55,56,],[14,-9,-26,14,-27,-28,-8,14,14,14,14,14,-30,14,-21,14,14,14,-11,14,-13,14,-29,-23,-20,-24,-10,-25,-12,-22,-19,]),'LPAREN':([0,2,4,5,7,8,9,11,12,13,14,15,18,19,20,21,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,39,40,41,42,43,44,45,46,48,49,50,53,54,55,56,58,],[6,-4,-5,6,16,-3,-2,-9,-26,16,-27,-28,-8,-7,16,16,16,38,16,38,16,-6,-30,16,-21,16,16,16,-15,-17,38,-11,16,38,-13,16,-29,-23,-20,-24,-14,-10,-25,-12,-22,-19,-16,]),'STRING':([7,11,12,13,14,15,18,20,21,23,25,27,29,30,31,32,33,34,39,40,42,43,44,45,46,48,50,53,54,55,56,],[15,-9,-26,15,-27,-28,-8,15,15,15,15,15,-30,15,-21,15,15,15,-11,15,-13,15,-29,-23,-20,-24,-10,-25,-12,-22,-19,]),'IMPORT':([6,],[10,]),'RPAREN':([12,14,15,17,21,24,26,29,30,31,32,34,35,36,37,39,40,41,42,43,44,45,46,47,48,49,50,53,54,55,56,57,58,],[-26,-27,-28,28,31,39,42,-30,45,-21,46,48,-15,-17,50,-11,53,54,-13,55,-29,-23,-20,56,-24,-14,-10,-25,-12,-22,-19,58,-16,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'expression':([7,13,20,21,23,25,27,30,32,33,34,40,43,],[11,18,29,29,29,29,29,44,44,47,44,44,44,]),'declaration':([24,26,37,41,],[35,35,49,49,]),'import_statement':([0,5,],[2,8,]),'program':([0,],[3,]),'component':([0,5,],[4,9,]),'declaration_list':([24,26,],[37,41,]),'statement_list':([0,],[5,]),'expression_list':([7,],[13,]),'type':([38,],[51,]),'parameter_list':([20,21,23,25,27,],[30,32,34,40,43,]),}

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
