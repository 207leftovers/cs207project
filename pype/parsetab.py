
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.8'

_lr_method = 'LALR'

_lr_signature = '371EF72B57DF7D01BB0A145AD73D5ADC'
    
_lr_action_items = {'RPAREN':([11,13,14,17,21,26,28,29,31,32,33,34,35,37,38,39,40,41,42,43,44,45,48,49,50,51,52,53,54,55,56,57,58,],[18,-28,-26,-27,32,40,42,45,-15,-13,-17,48,-30,51,52,53,-11,54,-21,55,-14,-12,-23,-29,57,-24,-22,-10,-25,-20,58,-19,-16,]),'$end':([2,3,4,6,8,9,18,20,],[-5,-4,-1,0,-2,-3,-6,-7,]),'OUTPUT':([15,],[21,]),'STRING':([10,12,13,14,16,17,19,22,24,25,27,28,32,34,35,36,37,38,40,41,42,43,45,48,49,51,52,53,54,55,57,],[13,13,-28,-26,-9,-27,-8,13,13,13,13,13,-13,13,-30,13,13,13,-11,13,-21,13,-12,-23,-29,-24,-22,-10,-25,-20,-19,]),'OP_SUB':([15,],[22,]),'ASSIGN':([15,],[23,]),'OP_MUL':([15,],[24,]),'ID':([5,7,10,12,13,14,15,16,17,19,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,51,52,53,54,55,57,58,],[10,11,14,14,-28,-26,28,-9,-27,-8,33,14,36,14,14,33,14,14,33,47,-15,-13,-17,14,-30,14,14,14,33,-11,14,-21,14,-14,-12,56,-18,-23,-29,-24,-22,-10,-25,-20,-19,-16,]),'LPAREN':([0,2,3,4,8,9,10,12,13,14,16,17,18,19,20,21,22,24,25,26,27,28,29,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,48,49,51,52,53,54,55,57,58,],[1,-5,-4,1,-2,-3,15,15,-28,-26,-9,-27,-6,-8,-7,30,15,15,15,30,15,15,30,-15,-13,-17,15,-30,15,15,15,30,-11,15,-21,15,-14,-12,-23,-29,-24,-22,-10,-25,-20,-19,-16,]),'INPUT':([15,],[26,]),'OP_ADD':([15,],[25,]),'RBRACE':([12,13,14,16,17,19,32,40,42,45,48,51,52,53,54,55,57,],[20,-28,-26,-9,-27,-8,-13,-11,-21,-12,-23,-24,-22,-10,-25,-20,-19,]),'LBRACE':([0,2,3,4,8,9,18,20,],[5,-5,-4,5,-2,-3,-6,-7,]),'OP_DIV':([15,],[27,]),'IMPORT':([1,],[7,]),'NUMBER':([10,12,13,14,16,17,19,22,24,25,27,28,32,34,35,36,37,38,40,41,42,43,45,48,49,51,52,53,54,55,57,],[17,17,-28,-26,-9,-27,-8,17,17,17,17,17,-13,17,-30,17,17,17,-11,17,-21,17,-12,-23,-29,-24,-22,-10,-25,-20,-19,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'declaration_list':([21,26,],[29,39,]),'expression_list':([10,],[12,]),'component':([0,4,],[2,8,]),'declaration':([21,26,29,39,],[31,31,44,44,]),'import_statement':([0,4,],[3,9,]),'type':([30,],[46,]),'parameter_list':([22,24,25,27,28,],[34,37,38,41,43,]),'statement_list':([0,],[4,]),'expression':([10,12,22,24,25,27,28,34,36,37,38,41,43,],[16,19,35,35,35,35,35,49,50,49,49,49,49,]),'program':([0,],[6,]),}

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
