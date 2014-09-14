
class MetaIRC(type):
	def __new__(cls, name, bases, attrs):

		if len(bases) != 1:
			raise TypeError("MetaIRC only accepts single inheritance")

		new_regd_funcs = bases[0].regd_funcs.copy()
		new_attrs = attrs.copy()
	
		for name, attr in attrs.items():
			if (hasattr(attr, "__annotations__") and
				 "return" in attr.__annotations__):
				new_regd_funcs[attr.__annotations__["return"]] = attr
		
		new_attrs["regd_funcs"] = new_regd_funcs

		return super().__new__(cls, name, bases, new_attrs)
				
