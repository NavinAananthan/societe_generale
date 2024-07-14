
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'END_KEYWORD END_STATEMENT IDENTIFIER KEYWORD LPAREN NUMBER OPERATOR RPAREN STRINGprogram : subroutine\n               | functionsubroutine : KEYWORD IDENTIFIER LPAREN RPAREN statements END_KEYWORDfunction : KEYWORD IDENTIFIER LPAREN RPAREN statements END_KEYWORDstatements : statement\n                  | statement statementsstatement : expression_statement\n                 | END_STATEMENTexpression_statement : expression END_STATEMENTexpression : STRING\n                  | NUMBER\n                  | IDENTIFIER'
    
_lr_action_items = {'KEYWORD':([0,],[4,]),'$end':([1,2,3,16,],[0,-1,-2,-3,]),'IDENTIFIER':([4,7,10,11,12,18,],[5,8,8,-7,-8,-9,]),'LPAREN':([5,],[6,]),'RPAREN':([6,],[7,]),'END_STATEMENT':([7,8,10,11,12,13,14,15,18,],[12,-12,12,-7,-8,18,-10,-11,-9,]),'STRING':([7,10,11,12,18,],[14,14,-7,-8,-9,]),'NUMBER':([7,10,11,12,18,],[15,15,-7,-8,-9,]),'END_KEYWORD':([9,10,11,12,17,18,],[16,-5,-7,-8,-6,-9,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'subroutine':([0,],[2,]),'function':([0,],[3,]),'statements':([7,10,],[9,17,]),'statement':([7,10,],[10,10,]),'expression_statement':([7,10,],[11,11,]),'expression':([7,10,],[13,13,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> subroutine','program',1,'p_program','trial.py',39),
  ('program -> function','program',1,'p_program','trial.py',40),
  ('subroutine -> KEYWORD IDENTIFIER LPAREN RPAREN statements END_KEYWORD','subroutine',6,'p_subroutine','trial.py',44),
  ('function -> KEYWORD IDENTIFIER LPAREN RPAREN statements END_KEYWORD','function',6,'p_function','trial.py',48),
  ('statements -> statement','statements',1,'p_statements','trial.py',52),
  ('statements -> statement statements','statements',2,'p_statements','trial.py',53),
  ('statement -> expression_statement','statement',1,'p_statement','trial.py',60),
  ('statement -> END_STATEMENT','statement',1,'p_statement','trial.py',61),
  ('expression_statement -> expression END_STATEMENT','expression_statement',2,'p_expression_statement','trial.py',65),
  ('expression -> STRING','expression',1,'p_expression','trial.py',69),
  ('expression -> NUMBER','expression',1,'p_expression','trial.py',70),
  ('expression -> IDENTIFIER','expression',1,'p_expression','trial.py',71),
]
