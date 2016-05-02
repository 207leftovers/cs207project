
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.8'

_lr_method = 'LALR'

_lr_signature = 'D7D1BCF469A7160DABB9E0C3456A50E8'
    
_lr_action_items = {'LBRACE':([0,1,3,4,7,8,19,28,],[5,5,-4,-5,-3,-2,-7,-6,]),'INPUT':([12,],[21,]),'RPAREN':([13,14,15,17,21,24,25,29,30,31,32,33,35,37,38,39,40,41,42,43,44,45,46,47,50,51,52,53,54,55,56,57,58,],[-28,-27,-26,28,32,38,40,44,-30,-17,-11,46,-15,51,-13,52,-21,53,54,55,-24,-29,-10,-14,57,-23,-12,-20,-25,-22,58,-19,-16,]),'LPAREN':([0,1,3,4,7,8,9,11,13,14,15,16,18,19,20,21,23,24,25,26,27,28,29,30,31,32,33,35,36,37,38,39,40,41,42,43,44,45,46,47,51,52,53,54,55,57,58,],[6,6,-4,-5,-3,-2,12,12,-28,-27,-26,-9,-8,-7,12,34,12,34,12,12,12,-6,12,-30,-17,-11,34,-15,12,12,-13,34,-21,12,12,12,-24,-29,-10,-14,-23,-12,-20,-25,-22,-19,-16,]),'STRING':([9,11,13,14,15,16,18,20,23,25,26,27,29,30,32,36,37,38,40,41,42,43,44,45,46,51,52,53,54,55,57,],[13,13,-28,-27,-26,-9,-8,13,13,13,13,13,13,-30,-11,13,13,-13,-21,13,13,13,-24,-29,-10,-23,-12,-20,-25,-22,-19,]),'RBRACE':([11,13,14,15,16,18,32,38,40,44,46,51,52,53,54,55,57,],[19,-28,-27,-26,-9,-8,-11,-13,-21,-24,-10,-23,-12,-20,-25,-22,-19,]),'OP_SUB':([12,],[23,]),'NUMBER':([9,11,13,14,15,16,18,20,23,25,26,27,29,30,32,36,37,38,40,41,42,43,44,45,46,51,52,53,54,55,57,],[14,14,-28,-27,-26,-9,-8,14,14,14,14,14,14,-30,-11,14,14,-13,-21,14,14,14,-24,-29,-10,-23,-12,-20,-25,-22,-19,]),'OUTPUT':([12,],[24,]),'ID':([5,9,10,11,12,13,14,15,16,18,20,21,22,23,24,25,26,27,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,51,52,53,54,55,57,58,],[9,15,17,15,25,-28,-27,-26,-9,-8,15,31,36,15,31,15,15,15,15,-30,-17,-11,31,49,-15,15,15,-13,31,-21,15,15,15,-24,-29,-10,-14,56,-18,-23,-12,-20,-25,-22,-19,-16,]),'IMPORT':([6,],[10,]),'OP_DIV':([12,],[26,]),'$end':([1,2,3,4,7,8,19,28,],[-1,0,-4,-5,-3,-2,-7,-6,]),'ASSIGN':([12,],[22,]),'OP_MUL':([12,],[20,]),'OP_ADD':([12,],[27,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'statement_list':([0,],[1,]),'declaration':([21,24,33,39,],[35,35,47,47,]),'program':([0,],[2,]),'import_statement':([0,1,],[3,7,]),'parameter_list':([20,23,25,26,27,],[29,37,41,42,43,]),'type':([34,],[48,]),'component':([0,1,],[4,8,]),'expression_list':([9,],[11,]),'declaration_list':([21,24,],[33,39,]),'expression':([9,11,20,23,25,26,27,29,36,37,41,42,43,],[16,18,30,30,30,30,30,45,50,45,45,45,45,]),}

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
