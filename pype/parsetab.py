
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.8'

_lr_method = 'LALR'

_lr_signature = 'D7D1BCF469A7160DABB9E0C3456A50E8'
    
_lr_action_items = {'NUMBER':([7,11,12,14,15,16,19,20,21,22,24,27,33,34,35,36,37,38,39,41,42,43,47,48,49,50,51,52,53,54,57,],[11,-27,-9,-26,-28,11,11,11,11,11,11,-8,-11,11,-30,11,-21,11,11,-13,11,11,-10,-29,-22,-20,-25,-23,-12,-24,-19,]),'INPUT':([13,],[18,]),'$end':([1,3,4,5,8,9,26,28,],[0,-1,-5,-4,-2,-3,-7,-6,]),'RBRACE':([11,12,14,15,16,27,33,37,41,47,49,50,51,52,53,54,57,],[-27,-9,-26,-28,26,-8,-11,-21,-13,-10,-22,-20,-25,-23,-12,-24,-19,]),'OP_SUB':([13,],[22,]),'OP_ADD':([13,],[19,]),'RPAREN':([11,14,15,17,18,20,23,29,31,32,33,34,35,36,37,38,39,40,41,42,46,47,48,49,50,51,52,53,54,55,56,57,58,],[-27,-26,-28,28,33,37,41,-17,47,-15,-11,49,-30,50,-21,51,52,53,-13,54,-14,-10,-29,-22,-20,-25,-23,-12,-24,57,58,-19,-16,]),'OP_DIV':([13,],[21,]),'LPAREN':([0,3,4,5,7,8,9,11,12,14,15,16,18,19,20,21,22,23,24,26,27,28,29,31,32,33,34,35,36,37,38,39,40,41,42,43,46,47,48,49,50,51,52,53,54,57,58,],[6,6,-5,-4,13,-2,-3,-27,-9,-26,-28,13,30,13,13,13,13,30,13,-7,-8,-6,-17,30,-15,-11,13,-30,13,-21,13,13,30,-13,13,13,-14,-10,-29,-22,-20,-25,-23,-12,-24,-19,-16,]),'ID':([2,7,10,11,12,13,14,15,16,18,19,20,21,22,23,24,25,27,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,57,58,],[7,14,17,-27,-9,20,-26,-28,14,29,14,14,14,14,29,14,43,-8,-17,44,29,-15,-11,14,-30,14,-21,14,14,29,-13,14,14,-18,56,-14,-10,-29,-22,-20,-25,-23,-12,-24,-19,-16,]),'LBRACE':([0,3,4,5,8,9,26,28,],[2,2,-5,-4,-2,-3,-7,-6,]),'STRING':([7,11,12,14,15,16,19,20,21,22,24,27,33,34,35,36,37,38,39,41,42,43,47,48,49,50,51,52,53,54,57,],[15,-27,-9,-26,-28,15,15,15,15,15,15,-8,-11,15,-30,15,-21,15,15,-13,15,15,-10,-29,-22,-20,-25,-23,-12,-24,-19,]),'OP_MUL':([13,],[24,]),'OUTPUT':([13,],[23,]),'IMPORT':([6,],[10,]),'ASSIGN':([13,],[25,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'parameter_list':([19,20,21,22,24,],[34,36,38,39,42,]),'statement_list':([0,],[3,]),'type':([30,],[45,]),'expression_list':([7,],[16,]),'declaration_list':([18,23,],[31,40,]),'component':([0,3,],[4,8,]),'expression':([7,16,19,20,21,22,24,34,36,38,39,42,43,],[12,27,35,35,35,35,35,48,48,48,48,48,55,]),'declaration':([18,23,31,40,],[32,32,46,46,]),'import_statement':([0,3,],[5,9,]),}

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
