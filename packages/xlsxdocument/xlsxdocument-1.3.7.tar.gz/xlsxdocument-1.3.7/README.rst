============
XLSXDocument
============

This is a wrapper for openpyxl_ which makes creating XLSX documents with
the purpose of exporting data less boring::

    from xlsxdocument import XLSXDocument

    def xlsx_export(request):
        some_data = Bla.objects.all()

        xlsx = XLSXDocument()
        xlsx.table_from_queryset(Bla.objects.all())
        return xlsx.to_response('bla.xlsx')


Adding in additional cells at the end is also possible::

    xlsx = XLSXDocument()
    xlsx.table_from_queryset(
        Bla.objects.all(),
        additional=[(
            'Full URL',
            lambda instance: 'http://example.com%s' % (
                instance.get_absolute_url(),
            ),
        )],
    )


You can also easily add the facility to export rows to Django's
administration interface::

    from django.contrib import admin
    from django.utils.translation import gettext_lazy as _

    from xlsxdocument import export_selected

    from app import models


    class AttendanceAdmin(admin.ModelAdmin):
        list_filter = ('event',)
        actions = (export_selected,)


    admin.site.register(models.Event)
    admin.site.register(models.Attendance, AttendanceAdmin)


If you require additional columns with ``export_selected`` use this
snippet instead::

    from xlsxdocument import create_export_selected

    class AttendanceAdmin(...):
        actions = [
            create_export_selected(
                additional=[
                    # ... see above
                ]
            )
        ]


.. _openpyxl: https://openpyxl.readthedocs.io/
