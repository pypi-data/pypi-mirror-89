from fast_mail_parser import PyMail


def test__attachments_are_available(attachment_mail: PyMail):
    assert len(attachment_mail.attachments) is 4


def test__base64_content_is_decoded(attachment_mail: PyMail):
    attachment = list(filter(lambda a: a.mimetype == 'image/png', attachment_mail.attachments)).pop()

    assert attachment.content == b'PNG here'


def test__attachment_has_a_name(large_mail: PyMail):
    payment_invoice_exists = len([a for a in large_mail.attachments if a.filename == 'Payment Invoice.zip'])

    assert payment_invoice_exists == 1
