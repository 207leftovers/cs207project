
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.8'

_lr_method = 'LALR'

_lr_signature = 'D7D1BCF469A7160DABB9E0C3456A50E8'
    
_lr_action_items = {'NUMBER':([7,11,12,13,14,16,19,21,22,24,25,27,32,34,35,36,37,39,40,41,42,43,45,48,49,50,51,52,53,55,57,],[14,-26,-28,14,-27,-9,-8,14,14,14,14,14,-13,14,-21,-30,14,-11,14,14,14,14,-12,-20,-29,-25,-10,-24,-22,-23,-19,]),'OUTPUT':([15,],[20,]),'ID':([1,7,8,11,12,13,14,15,16,19,20,21,22,23,24,25,26,27,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,55,57,58,],[7,11,17,-26,-28,11,-27,21,-9,-8,33,11,11,33,11,11,42,11,33,-15,47,-13,-17,11,-21,-30,11,33,-11,11,11,11,11,-14,-12,56,-18,-20,-29,-25,-10,-24,-22,-23,-19,-16,]),'OP_DIV':([15,],[22,]),'STRING':([7,11,12,13,14,16,19,21,22,24,25,27,32,34,35,36,37,39,40,41,42,43,45,48,49,50,51,52,53,55,57,],[12,-26,-28,12,-27,-9,-8,12,12,12,12,12,-13,12,-21,-30,12,-11,12,12,12,12,-12,-20,-29,-25,-10,-24,-22,-23,-19,]),'LBRACE':([0,2,5,6,9,10,18,28,],[1,-5,1,-4,-2,-3,-7,-6,]),'RBRACE':([11,12,13,14,16,19,32,35,39,45,48,50,51,52,53,55,57,],[-26,-28,18,-27,-9,-8,-13,-21,-11,-12,-20,-25,-10,-24,-22,-23,-19,]),'INPUT':([15,],[23,]),'$end':([2,4,5,6,9,10,18,28,],[-5,0,-1,-4,-2,-3,-7,-6,]),'IMPORT':([3,],[8,]),'LPAREN':([0,2,5,6,7,9,10,11,12,13,14,16,18,19,20,21,22,23,24,25,27,28,29,30,32,33,34,35,36,37,38,39,40,41,42,43,44,45,48,49,50,51,52,53,55,57,58,],[3,-5,3,-4,15,-2,-3,-26,-28,15,-27,-9,-7,-8,31,15,15,31,15,15,15,-6,31,-15,-13,-17,15,-21,-30,15,31,-11,15,15,15,15,-14,-12,-20,-29,-25,-10,-24,-22,-23,-19,-16,]),'RPAREN':([11,12,14,17,20,21,23,29,30,32,33,34,35,36,37,38,39,40,41,43,44,45,48,49,50,51,52,53,54,55,56,57,58,],[-26,-28,-27,28,32,35,39,45,-15,-13,-17,48,-21,-30,50,51,-11,52,53,55,-14,-12,-20,-29,-25,-10,-24,-22,57,-23,58,-19,-16,]),'OP_MUL':([15,],[24,]),'ASSIGN':([15,],[26,]),'OP_SUB':([15,],[27,]),'OP_ADD':([15,],[25,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'declaration_list':([20,23,],[29,38,]),'parameter_list':([21,22,24,25,27,],[34,37,40,41,43,]),'declaration':([20,23,29,38,],[30,30,44,44,]),'component':([0,5,],[2,9,]),'program':([0,],[4,]),'statement_list':([0,],[5,]),'import_statement':([0,5,],[6,10,]),'type':([31,],[46,]),'expression_list':([7,],[13,]),'expression':([7,13,21,22,24,25,27,34,37,40,41,42,43,],[16,19,36,36,36,36,36,49,49,49,49,54,49,]),}

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
