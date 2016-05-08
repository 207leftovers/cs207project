
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.8'

_lr_method = 'LALR'

_lr_signature = 'BA90F0C8CB04659A4089667E76C36B34'
    
_lr_action_items = {'OP_ADD':([15,],[21,]),'IMPORT':([1,],[7,]),'RPAREN':([11,13,16,17,22,23,25,29,30,31,32,34,35,36,37,38,39,40,41,42,44,45,46,49,50,51,52,53,54,55,56,57,58,],[18,-26,-28,-27,32,37,40,45,-30,46,-21,-15,-17,50,-11,51,52,-13,53,54,-29,-22,-20,-14,-10,-23,-12,-25,-24,57,58,-19,-16,]),'ID':([4,7,10,12,13,14,15,16,17,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,57,58,],[10,11,13,13,-26,-9,22,-28,-27,-8,13,13,35,13,35,13,13,43,13,-30,13,-21,48,-15,-17,35,-11,13,35,-13,13,13,13,-29,-22,-20,56,-18,-14,-10,-23,-12,-25,-24,-19,-16,]),'ASSIGN':([15,],[28,]),'INPUT':([15,],[23,]),'LPAREN':([0,2,5,6,8,9,10,12,13,14,16,17,18,19,20,21,22,23,24,25,26,27,29,30,31,32,34,35,36,37,38,39,40,41,42,43,44,45,46,49,50,51,52,53,54,57,58,],[1,1,-5,-4,-2,-3,15,15,-26,-9,-28,-27,-6,-7,-8,15,15,33,15,33,15,15,15,-30,15,-21,-15,-17,33,-11,15,33,-13,15,15,15,-29,-22,-20,-14,-10,-23,-12,-25,-24,-19,-16,]),'STRING':([10,12,13,14,16,17,20,21,22,24,26,27,29,30,31,32,37,38,40,41,42,43,44,45,46,50,51,52,53,54,57,],[16,16,-26,-9,-28,-27,-8,16,16,16,16,16,16,-30,16,-21,-11,16,-13,16,16,16,-29,-22,-20,-10,-23,-12,-25,-24,-19,]),'OP_SUB':([15,],[24,]),'NUMBER':([10,12,13,14,16,17,20,21,22,24,26,27,29,30,31,32,37,38,40,41,42,43,44,45,46,50,51,52,53,54,57,],[17,17,-26,-9,-28,-27,-8,17,17,17,17,17,17,-30,17,-21,-11,17,-13,17,17,17,-29,-22,-20,-10,-23,-12,-25,-24,-19,]),'OUTPUT':([15,],[25,]),'OP_DIV':([15,],[26,]),'LBRACE':([0,2,5,6,8,9,18,19,],[4,4,-5,-4,-2,-3,-6,-7,]),'OP_MUL':([15,],[27,]),'$end':([2,3,5,6,8,9,18,19,],[-1,0,-5,-4,-2,-3,-6,-7,]),'RBRACE':([12,13,14,16,17,20,32,37,40,45,46,50,51,52,53,54,57,],[19,-26,-9,-28,-27,-8,-21,-11,-13,-22,-20,-10,-23,-12,-25,-24,-19,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'type':([33,],[47,]),'expression_list':([10,],[12,]),'declaration_list':([23,25,],[36,39,]),'declaration':([23,25,36,39,],[34,34,49,49,]),'statement_list':([0,],[2,]),'program':([0,],[3,]),'expression':([10,12,21,22,24,26,27,29,31,38,41,42,43,],[14,20,30,30,30,30,30,44,44,44,44,44,55,]),'parameter_list':([21,22,24,26,27,],[29,31,38,41,42,]),'component':([0,2,],[5,8,]),'import_statement':([0,2,],[6,9,]),}

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
