
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.8'

_lr_method = 'LALR'

_lr_signature = 'E1FCB2EDDF1216D4CA039394CC93A7CE'
    
_lr_action_items = {'STRING':([7,11,12,14,15,16,18,20,21,22,25,27,29,30,31,36,37,38,39,40,42,43,44,45,47,50,51,52,53,55,57,],[11,-28,-26,-27,11,-9,11,11,11,11,11,-8,11,-21,-30,-13,11,11,11,-11,11,11,-20,-29,-12,-25,-23,-22,-10,-24,-19,]),'ID':([1,7,8,11,12,13,14,15,16,18,19,20,21,22,23,24,25,27,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,55,57,58,],[7,12,17,-28,-26,18,-27,12,-9,12,35,12,12,12,35,42,12,-8,12,-21,-30,-15,35,48,-17,-13,12,12,12,-11,35,12,12,-20,-29,-14,-12,-18,56,-25,-23,-22,-10,-24,-19,-16,]),'OUTPUT':([13,],[19,]),'OP_DIV':([13,],[20,]),'INPUT':([13,],[23,]),'OP_MUL':([13,],[25,]),'OP_SUB':([13,],[21,]),'NUMBER':([7,11,12,14,15,16,18,20,21,22,25,27,29,30,31,36,37,38,39,40,42,43,44,45,47,50,51,52,53,55,57,],[14,-28,-26,-27,14,-9,14,14,14,14,14,-8,14,-21,-30,-13,14,14,14,-11,14,14,-20,-29,-12,-25,-23,-22,-10,-24,-19,]),'$end':([3,4,5,6,9,10,26,28,],[-4,0,-1,-5,-3,-2,-7,-6,]),'LPAREN':([0,3,5,6,7,9,10,11,12,14,15,16,18,19,20,21,22,23,25,26,27,28,29,30,31,32,33,35,36,37,38,39,40,41,42,43,44,45,46,47,50,51,52,53,55,57,58,],[2,-4,2,-5,13,-3,-2,-28,-26,-27,13,-9,13,34,13,13,13,34,13,-7,-8,-6,13,-21,-30,-15,34,-17,-13,13,13,13,-11,34,13,13,-20,-29,-14,-12,-25,-23,-22,-10,-24,-19,-16,]),'RPAREN':([11,12,14,17,18,19,23,29,30,31,32,33,35,36,37,38,39,40,41,43,44,45,46,47,50,51,52,53,54,55,56,57,58,],[-28,-26,-27,28,30,36,40,44,-21,-30,-15,47,-17,-13,50,51,52,-11,53,55,-20,-29,-14,-12,-25,-23,-22,-10,57,-24,58,-19,-16,]),'ASSIGN':([13,],[24,]),'RBRACE':([11,12,14,15,16,27,30,36,40,44,47,50,51,52,53,55,57,],[-28,-26,-27,26,-9,-8,-21,-13,-11,-20,-12,-25,-23,-22,-10,-24,-19,]),'IMPORT':([2,],[8,]),'OP_ADD':([13,],[22,]),'LBRACE':([0,3,5,6,9,10,26,28,],[1,-4,1,-5,-3,-2,-7,-6,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'declaration':([19,23,33,41,],[32,32,46,46,]),'declaration_list':([19,23,],[33,41,]),'parameter_list':([18,20,21,22,25,],[29,37,38,39,43,]),'import_statement':([0,5,],[3,9,]),'program':([0,],[4,]),'expression_list':([7,],[15,]),'expression':([7,15,18,20,21,22,25,29,37,38,39,42,43,],[16,27,31,31,31,31,31,45,45,45,45,54,45,]),'statement_list':([0,],[5,]),'type':([34,],[49,]),'component':([0,5,],[6,10,]),}

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
