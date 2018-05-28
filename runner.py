import plex

class ParseError(Exception): #gia ta lathh
	pass
class RunError(Exception): #gia logika lathh
	pass
class MyParser: #klash me onoma MyParser
	def __init__(self): #sunarthsh arxikopoihshs
		self.st={}

	def create_scanner(self,fp):
		letter=plex.Range('azAZ') #ena gramma
		digit=plex.Range('09') #ena pshfio		

		telesths3=plex.Str('=')

		parenthesis = plex.Str('(',')')
		name=letter+plex.Rep(letter|digit) #gramma kai  perissotera pshfia  h grammata
		boolFalse = plex.NoCase(plex.Str('false','f','0'))
		boolTrue = plex.NoCase(plex.Str('true','t','1'))
		space=plex.Rep1(plex.Any(' \n\t'))
		keyword=plex.Str('print','not','or','and')

		simple_comment=plex.Str('//')+plex.Rep(plex.AnyBut('\n')) #sbhnei ta sxolia kati pou den einai new line

		lexicon=plex.Lexicon([
				(keyword,plex.TEXT),
				(boolTrue,'true'),
				(boolFalse,'false'),
				(name,'IDENTIFIER'),
				(space,plex.IGNORE),
				(telesths3,'='),
				(parenthesis,plex.TEXT),
				(simple_comment,plex.IGNORE) #kanei ignore ta comment
				])
	
	
		self.scanner=plex.Scanner(lexicon,fp)
		self.la, self.val = self.next_token()
	

	
	def parse(self,fp):  #pernas to fp kai to self
				self.create_scanner(fp)  
				self.stmt_list() #epeidh einai mesa sthn class gi auto bazoume self "san adikeimeno"
		#		while True:
		#		token,text=self.next_token()
		#			if token is None:
		#					break
		#		print(token,text)
		
	def match(self,token): #koitaei ean to token einai idio me auto pou exw krathsei 
		#print("match")	
		if self.la == token:
			self.la,self.val=self.next_token()
		else:
			raise ParseError('waiting token , but came la')

	def next_token(self): #epistrefei to epomeno token
		return self.scanner.read()
		
	def stmt_list(self):
			if self.la == 'IDENTIFIER' or self.la == 'print':
					self.stmt()
					self.stmt_list()
			elif self.la is	None:
					return
			else:
				 ParseError('waiting for identifier or print')
						
	def stmt(self):
			if self.la == 'IDENTIFIER'  or self.la =='=':
					varname=self.val
					self.match('IDENTIFIER')
					self.match('=')
					self.st[varname]=self.expr()
					
			elif self.la == 'print':		
					self.match('print')
					print(self.expr())
			else:
					raise ParseError('waiting for identifier or print')	
				
	def expr(self):
			if self.la == '(' or self.la == 'IDENTIFIER' or self.la == 'true' or self.la == 'false':
					t = self.term()
					tt = self.term_tail()
					if tt is None:
						return t
					if tt[0] =='or':
						return t or tt[1]
					if tt[0] == 'and':
						return t and tt[1]
				
			else:
					 ParseError('waiting for ( or IDENTIFIER or BOOLEAN')
	
		
			
	def term_tail(self):
			if self.la == 'and' or self.la == 'or':
					a_op = self.Or_And_op()
					t = self.term()
					tt = self.term_tail()
					if tt is None:
						return a_op,t
					if tt[0] == 'or':
						return a_op, t or tt[1]
					if tt[0] == 'and':
						return a_op, t and tt[1]
			
			elif self.la =='IDENTIFIER' or self.la =='print'  or self.la is None:
					return 
			else:
					raise ParseError('waiting for and')
		

	def term(self):
			if self.la == '('  or self.la == 'IDENTIFIER' or self.la == 'true' or self.la == 'false' or self.la == 'not':
					f = self.factor()
					ft = self.factor_tail()
					if ft is None:
								return f
					if ft[0] == 'not':
								return not f			
					
			else:
					raise ParseError('waiting for ( or IDENTIFIER or BOOLEAN')
			
	
	def factor_tail(self):
			if self.la == 'not':
					 op = self.Not_op() 
					 f = self.factor() 
					 ft = self.factor_tail() 
					 if ft is None:
								return op,f
					 if ft[0] =='not':
								return op, not f			
					
			elif self.la =='and' or self.la=='or' or self.la =='print' or self.la =='IDENTIFIER' or self.la is None:
					return
			else:
				raise ParseError('error ,not')
		

	def factor(self):
			if self.la =='(':
					self.match('(')
					e = self.expr()
					self.match(')')
					return e

			elif self.la =='IDENTIFIER':
					varname = self.val
					self.match('IDENTIFIER')
					if varname in self.st:
						return self.st[varname]
						
			elif self.la == 'true':
				
					self.match('true')
					return True
					
			elif self.la == 'false':
				
					self.match('false')
					return False
			elif self.la =='not' or self.la =='and' or self.la =='or' or self.la =='print' or self.la is None:
				return
			else:
				raise ParseError("expected id, boolean")
			
				

			
	def Or_And_op(self):
			if self.la == 'and':
					self.match('and')
					return 'and'
					
			elif self.la == 'or':
					self.match('or')
					return 'or'
			else:
				raise ParseError('expected or and')
			
	def Not_op(self):
			if self.la == 'not':
					self.match('not')
					return 'not'
			else:
				raise ParseError('expected not')
	
	
parser = MyParser()	 #adikeimeno ths klasshs myparser

with open('data.txt') as fp:
		try:
			parser.parse(fp) 							 #sto adikeimeno ths klasshs myparser na kanei parse
		except ParseError as perr:
			print(perr)







