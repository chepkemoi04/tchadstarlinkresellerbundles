from django import forms


class CheckoutForm(forms.Form):
    PAYMENT_CHOICES = (("airtel_money", "Airtel Money"), ("moov_money", "Moov Money"))
    payment_method = forms.ChoiceField(choices=PAYMENT_CHOICES, widget=forms.RadioSelect)
    phone_number = forms.CharField(max_length=15)
    pin_code = forms.CharField(max_length=4, min_length=4)
    otp_code = forms.CharField(max_length=6, min_length=4)

    def clean_pin_code(self):
        pin = self.cleaned_data.get("pin_code", "")
        if not pin.isdigit() or len(pin) != 4:
            raise forms.ValidationError("Le PIN doit comporter exactement 4 chiffres.")
        return pin

    def clean(self):
        cleaned_data = super().clean()
        method = cleaned_data.get("payment_method")
        otp = cleaned_data.get("otp_code", "")
        phone = cleaned_data.get("phone_number", "")

        if not phone.isdigit():
            self.add_error("phone_number", "Numéro de téléphone non valide.")

        if not otp.isdigit():
            self.add_error("otp_code", "OTP non valide.")
            return cleaned_data

        if method == "airtel_money" and len(otp) != 4:
            self.add_error("otp_code", "L'OTP Airtel Money nécessite exactement 4 chiffres.")
        elif method == "moov_money" and len(otp) != 6:
            self.add_error("otp_code", "L'OTP Moov Money nécessite exactement 6 chiffres.")

        return cleaned_data