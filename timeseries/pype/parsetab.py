
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.8'

_lr_method = 'LALR'

_lr_signature = 'E1FCB2EDDF1216D4CA039394CC93A7CE'
    
_lr_action_items = {'RBRACE':([11,13,14,15,16,27,34,39,40,45,46,47,50,52,53,54,57,],[-28,-27,-26,-9,26,-8,-11,-21,-13,-23,-25,-22,-10,-20,-12,-24,-19,]),'LBRACE':([0,1,3,6,9,10,26,28,],[2,-5,-4,2,-2,-3,-7,-6,]),'ID':([2,7,8,11,12,13,14,15,16,18,19,20,21,22,23,24,25,27,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,57,58,],[7,14,17,-28,22,-27,-26,-9,14,14,14,14,33,14,33,14,43,-8,14,-30,14,14,-17,-11,-15,48,33,14,-21,-13,33,14,14,-29,-23,-25,-22,-18,56,-10,-14,-20,-12,-24,-19,-16,]),'STRING':([7,11,13,14,15,16,18,19,20,22,24,27,29,30,31,32,34,38,39,40,42,43,44,45,46,47,50,52,53,54,57,],[11,-28,-27,-26,-9,11,11,11,11,11,11,-8,11,-30,11,11,-11,11,-21,-13,11,11,-29,-23,-25,-22,-10,-20,-12,-24,-19,]),'LPAREN':([0,1,3,6,7,9,10,11,13,14,15,16,18,19,20,21,22,23,24,26,27,28,29,30,31,32,33,34,35,37,38,39,40,41,42,43,44,45,46,47,50,51,52,53,54,57,58,],[4,-5,-4,4,12,-2,-3,-28,-27,-26,-9,12,12,12,12,36,12,36,12,-7,-8,-6,12,-30,12,12,-17,-11,-15,36,12,-21,-13,36,12,12,-29,-23,-25,-22,-10,-14,-20,-12,-24,-19,-16,]),'NUMBER':([7,11,13,14,15,16,18,19,20,22,24,27,29,30,31,32,34,38,39,40,42,43,44,45,46,47,50,52,53,54,57,],[13,-28,-27,-26,-9,13,13,13,13,13,13,-8,13,-30,13,13,-11,13,-21,-13,13,13,-29,-23,-25,-22,-10,-20,-12,-24,-19,]),'OP_ADD':([12,],[20,]),'OP_DIV':([12,],[19,]),'INPUT':([12,],[21,]),'$end':([1,3,5,6,9,10,26,28,],[-5,-4,0,-1,-2,-3,-7,-6,]),'OUTPUT':([12,],[23,]),'IMPORT':([4,],[8,]),'RPAREN':([11,13,14,17,21,22,23,29,30,31,32,33,34,35,37,38,39,40,41,42,44,45,46,47,50,51,52,53,54,55,56,57,58,],[-28,-27,-26,28,34,39,40,45,-30,46,47,-17,-11,-15,50,52,-21,-13,53,54,-29,-23,-25,-22,-10,-14,-20,-12,-24,57,58,-19,-16,]),'OP_MUL':([12,],[24,]),'OP_SUB':([12,],[18,]),'ASSIGN':([12,],[25,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'parameter_list':([18,19,20,22,24,],[29,31,32,38,42,]),'component':([0,6,],[1,9,]),'type':([36,],[49,]),'expression':([7,16,18,19,20,22,24,29,31,32,38,42,43,],[15,27,30,30,30,30,30,44,44,44,44,44,55,]),'import_statement':([0,6,],[3,10,]),'declaration':([21,23,37,41,],[35,35,51,51,]),'program':([0,],[5,]),'declaration_list':([21,23,],[37,41,]),'expression_list':([7,],[16,]),'statement_list':([0,],[6,]),}

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
