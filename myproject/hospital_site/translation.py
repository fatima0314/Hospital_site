from .models import *
from modeltranslation.translator import TranslationOptions,register


@register(Speciality)
class ProductTranslationOptions(TranslationOptions):
    fields = ('speciality_name',)


@register(Doctor)
class ProductTranslationOptions(TranslationOptions):
    fields = ('qualification',)


@register(Patient)
class ProductTranslationOptions(TranslationOptions):
    fields = ('allergies', 'medical_history')


@register(Department)
class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'location')


@register(Appointment)
class ProductTranslationOptions(TranslationOptions):
    fields = ('status', 'notes')


@register(MedicalRecord)
class ProductTranslationOptions(TranslationOptions):
    fields = ('diagnosis','treatment')


@register(Prescriptions)
class ProductTranslationOptions(TranslationOptions):
    fields = ('medication', 'dosage')


@register(Feedback)
class ProductTranslationOptions(TranslationOptions):
    fields = ('comment', )