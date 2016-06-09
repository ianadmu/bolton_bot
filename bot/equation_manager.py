import re

class EquationManager(object):

	def solve(self,equation):

		tokens = equation.split()
		if(len(tokens)!= 3):
			return "Ask me to solve an equation by saying 'Bolton solve <equation>'"

		try:
			return "The answer is "+str(eval(tokens[2]))+"!"
		except:
			return "I coulden't solve that equation :confounded:"
