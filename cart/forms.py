from django import forms

ITEM_QUANTITY=[(i,str(i)) for i in range(1,11)]

class CartCountForm(forms.Form):
    quantity=forms.TypedChoiceField(choices=ITEM_QUANTITY,coerce=int)
