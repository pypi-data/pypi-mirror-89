from django.core import mail
from django.template.loader import render_to_string

from kalabash.lib.cryptutils import get_password
from kalabash.parameters import tools as param_tools

from ..exceptions import WebmailInternalError
from . import get_imapconnector, clean_attachments


def send_mail(request, form, posturl=None):
    """Email verification and sending.

    If the form does not present any error, a new MIME message is
    constructed. Then, a connection is established with the defined
    SMTP server and the message is finally sent.

    :param request: a Request object
    :param posturl: the url to post the message form to
    :return: a 2-uple (True|False, HttpResponse)
    """
    if not form.is_valid():
        editormode = request.user.parameters.get_value("editor")
        listing = render_to_string(
            "kalabash_webmail/compose.html",
            {"form": form, "noerrors": True,
             "body": form.cleaned_data.get("body", "").strip(),
             "posturl": posturl},
            request
        )
        return False, {"status": "ko", "listing": listing, "editor": editormode}

    msg = form.to_msg(request)
    conf = dict(param_tools.get_global_parameters("kalabash_webmail"))
    options = {
        "host": conf["smtp_server"], "port": conf["smtp_port"]
    }
    if conf["smtp_secured_mode"] == "ssl":
        options.update({"use_ssl": True})
    elif conf["smtp_secured_mode"] == "starttls":
        options.update({"use_tls": True})
    if conf["smtp_authentication"]:
        options.update({
            "username": request.user.username,
            "password": get_password(request)
        })
    try:
        with mail.get_connection(**options) as connection:
            msg.connection = connection
            msg.send()
    except Exception as inst:
        raise WebmailInternalError(str(inst))

    # Copy message to sent folder
    sentfolder = request.user.parameters.get_value("sent_folder")
    get_imapconnector(request).push_mail(sentfolder, msg.message())
    clean_attachments(request.session["compose_mail"]["attachments"])
    del request.session["compose_mail"]

    return True, {}
