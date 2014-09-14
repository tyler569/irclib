
class MetaIRC(type):
	def __init__(self, name, bases, attrs):

		if len(bases) != 1:
			raise TypeError("MetaIRC only accepts single inheritance")

		regd_funcs = bases[0].regd_funcs
		newattrs = attrs.copy()
	
		for name, attr in attrs.items():
			if (hasattr(attr, "__annotations__") and
				 "return" in attr.__annotations__):
				regd_funcs[attr.__annotations__["return"]] = attr
		
		newattrs["regd_funcs"] = regd_funcs

		return super().__init__(name, bases, newattrs)
				
