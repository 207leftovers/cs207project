
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.8'

_lr_method = 'LALR'

_lr_signature = 'B7DA2FE6C22431AB95D14A63E4FE0078'
    
_lr_action_items = {'RPAREN':([12,15,16,17,19,24,25,29,30,31,32,34,35,37,38,39,40,41,42,43,44,45,48,49,50,51,52,53,54,55,56,57,58,],[-28,-27,-26,28,32,40,42,-30,44,-15,-13,-17,49,51,52,53,-11,54,-21,55,-24,-29,-14,-12,57,-23,-25,-22,-10,-20,58,-19,-16,]),'OP_MUL':([13,],[18,]),'OUTPUT':([13,],[19,]),'STRING':([7,11,12,14,15,16,18,21,22,23,25,26,29,30,32,36,37,38,39,40,42,43,44,45,49,51,52,53,54,55,57,],[12,-9,-28,12,-27,-26,12,12,12,12,12,-8,-30,12,-13,12,12,12,12,-11,-21,12,-24,-29,-12,-23,-25,-22,-10,-20,-19,]),'LPAREN':([0,3,4,6,7,9,10,11,12,14,15,16,18,19,21,22,23,24,25,26,27,28,29,30,31,32,34,35,36,37,38,39,40,41,42,43,44,45,48,49,51,52,53,54,55,57,58,],[5,-4,-5,5,13,-3,-2,-9,-28,13,-27,-26,13,33,13,13,13,33,13,-8,-7,-6,-30,13,-15,-13,-17,33,13,13,13,13,-11,33,-21,13,-24,-29,-14,-12,-23,-25,-22,-10,-20,-19,-16,]),'IMPORT':([5,],[8,]),'OP_SUB':([13,],[21,]),'RBRACE':([11,12,14,15,16,26,32,40,42,44,49,51,52,53,54,55,57,],[-9,-28,27,-27,-26,-8,-13,-11,-21,-24,-12,-23,-25,-22,-10,-20,-19,]),'$end':([1,3,4,6,9,10,27,28,],[0,-4,-5,-1,-3,-2,-7,-6,]),'INPUT':([13,],[24,]),'OP_DIV':([13,],[22,]),'NUMBER':([7,11,12,14,15,16,18,21,22,23,25,26,29,30,32,36,37,38,39,40,42,43,44,45,49,51,52,53,54,55,57,],[15,-9,-28,15,-27,-26,15,15,15,15,15,-8,-30,15,-13,15,15,15,15,-11,-21,15,-24,-29,-12,-23,-25,-22,-10,-20,-19,]),'ASSIGN':([13,],[20,]),'OP_ADD':([13,],[23,]),'LBRACE':([0,3,4,6,9,10,27,28,],[2,-4,-5,2,-3,-2,-7,-6,]),'ID':([2,7,8,11,12,13,14,15,16,18,19,20,21,22,23,24,25,26,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,51,52,53,54,55,57,58,],[7,16,17,-9,-28,25,16,-27,-26,16,34,36,16,16,16,34,16,-8,-30,16,-15,-13,47,-17,34,16,16,16,16,-11,34,-21,16,-24,-29,56,-18,-14,-12,-23,-25,-22,-10,-20,-19,-16,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'declaration':([19,24,35,41,],[31,31,48,48,]),'program':([0,],[1,]),'expression_list':([7,],[14,]),'expression':([7,14,18,21,22,23,25,30,36,37,38,39,43,],[11,26,29,29,29,29,29,45,50,45,45,45,45,]),'component':([0,6,],[4,10,]),'parameter_list':([18,21,22,23,25,],[30,37,38,39,43,]),'import_statement':([0,6,],[3,9,]),'declaration_list':([19,24,],[35,41,]),'type':([33,],[46,]),'statement_list':([0,],[6,]),}

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
