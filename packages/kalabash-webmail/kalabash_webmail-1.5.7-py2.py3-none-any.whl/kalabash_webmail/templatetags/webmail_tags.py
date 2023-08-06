# coding: utf-8
"""Custom template tags."""

from six.moves.urllib.parse import urlencode

from django import template
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.encoding import smart_str
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from ..lib import imapheader, separate_mailbox
from .. import constants

register = template.Library()


@register.simple_tag
def viewmail_menu(selection, folder, user, mail_id=None):
    """Menu of the viewmail location."""
    entries = [{
        "name": "back",
        "url": "javascript:history.go(-1)",
        "img": "fa fa-arrow-left",
        "class": "btn-default",
        "label": _("Back")
    }, {
        "name": "reply",
        "url": "action=reply&mbox=%s&mailid=%s" % (folder, mail_id),
        "img": "fa fa-mail-reply",
        "class": "btn-primary",
        "label": _("Reply"),
        "menu": [{
            "name": "replyall",
            "url": "action=reply&mbox=%s&mailid=%s&all=1" % (folder, mail_id),
            "img": "fa fa-mail-reply-all",
            "label": _("Reply all")
        }, {
            "name": "forward",
            "url": "action=forward&mbox=%s&mailid=%s" % (folder, mail_id),
            "img": "fa fa-mail-forward",
            "label": _("Forward")
        }]
    }, {
        "name": "delete",
        "img": "fa fa-trash",
        "class": "btn-danger",
        "url": u"{0}?mbox={1}&selection[]={2}".format(
            reverse("kalabash_webmail:mail_delete"), folder, mail_id),
        "title": _("Delete")
    }, {
        "name": "mark_as_junk",
        "img": "fa fa-fire",
        "class": "btn-warning",
        "url": u"{0}?mbox={1}&selection[]={2}".format(
            reverse("kalabash_webmail:mail_mark_as_junk"), folder, mail_id),
        "title": _("Mark as spam")
    }, {
        "name": "display_options",
        "title": _("Display options"),
        "img": "fa fa-cog",
        "menu": [{
            "name": "activate_links",
            "label": _("Activate links")
        }, {
            "name": "disable_links",
            "label": _("Disable links")
        }, {
            "name": "show_source",
            "label": _("Show source"),
            "url": u"{}?mbox={}&mailid={}".format(
                reverse("kalabash_webmail:mailsource_get"), folder, mail_id)
        }]
    }]
    if folder == user.parameters.get_value("junk_folder"):
        entries[3] = {
            "name": "mark_as_not_junk",
            "img": "fa fa-thumbs-up",
            "class": "btn-success",
            "url": u"{0}?mbox={1}&selection[]={2}".format(
                reverse("kalabash_webmail:mail_mark_as_not_junk"),
                folder, mail_id),
            "title": _("Mark as not spam")
        }
    menu = render_to_string('common/buttons_list.html',
                            {"selection": selection, "entries": entries,
                             "user": user, "extraclasses": "pull-left"})
    return menu


@register.simple_tag
def compose_menu(selection, backurl, user, **kwargs):
    """The menu of the compose action."""
    entries = [
        {"name": "back",
         "url": "javascript:history.go(-2);",
         "img": "fa fa-arrow-left",
         "class": "btn-default",
         "label": _("Back")},
        {"name": "sendmail",
         "url": "",
         "img": "fa fa-send",
         "class": "btn-default btn-primary",
         "label": _("Send")},
    ]
    context = {
        "selection": selection, "entries": entries, "user": user
    }
    context.update(kwargs)
    return render_to_string('kalabash_webmail/compose_menubar.html', context)


@register.simple_tag
def listmailbox_menu(selection, folder, user, **kwargs):
    """The menu of the listmailbox action."""
    entries = [{
        "name": "totrash",
        "title": _("Delete"),
        "class": "btn-danger",
        "img": "fa fa-trash",
        "url": reverse("kalabash_webmail:mail_delete")
    }, {
        "name": "mark_as_junk_multi",
        "img": "fa fa-fire",
        "class": "btn-warning",
        "url": reverse("kalabash_webmail:mail_mark_as_junk"),
        "title": _("Mark as spam")
    }, {
        "name": "actions",
        "label": _("Actions"),
        "class": "btn btn-default",
        "menu": [{
            "name": "mark-read",
            "label": _("Mark as read"),
            "url": u"{0}?status=read".format(
                reverse("kalabash_webmail:mail_mark", args=[folder]))
        }, {
            "name": "mark-unread",
            "label": _("Mark as unread"),
            "url": u"{0}?status=unread".format(
                reverse("kalabash_webmail:mail_mark", args=[folder]))
        }, {
            "name": "mark-flagged",
            "label": _("Mark as flagged"),
            "url": u"{0}?status=flagged".format(
                reverse("kalabash_webmail:mail_mark", args=[folder]))
        }, {
            "name": "mark-unflagged",
            "label": _("Mark as unflagged"),
            "url": u"{0}?status=unflagged".format(
                reverse("kalabash_webmail:mail_mark", args=[folder]))
        }]
    }]
    sort_actions = [{
        "header": True,
        "label": _("Sort by")
    }]
    current_order = kwargs.get("sort_order")
    for order in constants.SORT_ORDERS:
        entry = {
            "name": "sort_by_{}".format(order[0]),
            "label": order[1],
            "url": order[0],
            "class": "sort-order"
        }
        if current_order[1:] == order[0]:
            css = "fa fa-arrow-{}".format(
                "down" if current_order[0] == "-" else "up")
            entry.update({"img": css})
        sort_actions.append(entry)
    entries[2]["menu"] += sort_actions
    if folder == user.parameters.get_value("trash_folder"):
        entries[0]["class"] += " disabled"
        entries[2]["menu"].insert(4, {
            "name": "empty",
            "label": _("Empty folder"),
            "url": u"{0}?name={1}".format(
                reverse("kalabash_webmail:trash_empty"), folder)
        })
    elif folder == user.parameters.get_value("junk_folder"):
        entries[1] = {
            "name": "mark_as_not_junk_multi",
            "img": "fa fa-thumbs-up",
            "class": "btn-success",
            "url": reverse("kalabash_webmail:mail_mark_as_not_junk"),
            "title": _("Mark as not spam")
        }
    return render_to_string('kalabash_webmail/main_action_bar.html', {
        'selection': selection, 'entries': entries, 'user': user, 'css': "nav",
    })


@register.simple_tag
def print_mailboxes(
        tree, selected=None, withunseen=False, selectonly=False,
        hdelimiter='.'):
    """Display a tree of mailboxes and sub-mailboxes.

    :param tree: the mailboxes to display
    """
    result = ""

    for mbox in tree:
        cssclass = ""
        name = mbox["path"] if "sub" in mbox else mbox["name"]
        label = (
            mbox["label"] if "label" in mbox else
            separate_mailbox(mbox["name"], hdelimiter)[0])
        if mbox.get("removed", False):
            cssclass = "disabled"
        elif selected == name:
            cssclass = "active"
        result += "<li name='%s' class='droppable %s'>\n" % (name, cssclass)
        cssclass = ""
        extra_attrs = ""
        if withunseen and "unseen" in mbox:
            label += " (%d)" % mbox["unseen"]
            cssclass += " unseen"
            extra_attrs = ' data-toggle="%d"' % mbox["unseen"]

        if "sub" in mbox:
            if selected is not None and selected != name and selected.count(
                    name):
                ul_state = "visible"
                div_state = "expanded"
            else:
                ul_state = "hidden"
                div_state = "collapsed"
            result += "<div class='clickbox %s'></div>" % div_state

        result += "<a href='%s' class='%s' name='%s'%s>" % (
            "path" in mbox and mbox["path"] or mbox["name"], cssclass,
            'selectfolder' if selectonly else 'loadfolder', extra_attrs
        )

        iclass = mbox["class"] if "class" in mbox \
            else "fa fa-folder"
        result += "<span class='%s'></span> %s</a>" % (iclass, label)

        if "sub" in mbox and mbox["sub"]:
            result += "<ul name='%s' class='nav nav-pills nav-stacked %s'>" % (
                mbox["path"], ul_state) + print_mailboxes(
                    mbox["sub"], selected, withunseen, selectonly, hdelimiter
            ) + "</ul>\n"
        result += "</li>\n"
    return mark_safe(result)


@register.simple_tag
def mboxes_menu():
    """Mailboxes menu."""
    entries = [
        {"name": "newmbox",
         "url": reverse("kalabash_webmail:folder_add"),
         "img": "fa fa-plus",
         "label": _("Create a new folder"),
         "modal": True,
         "modalcb": "webmail.mboxform_cb",
         "closecb": "webmail.mboxform_close",
         "class": "btn-default btn-xs"},
        {"name": "editmbox",
         "url": reverse("kalabash_webmail:folder_change"),
         "img": "fa fa-edit",
         "label": _("Edit the selected folder"),
         "class": "btn-default btn-xs"},
        {"name": "removembox",
         "url": reverse("kalabash_webmail:folder_delete"),
         "img": "fa fa-trash",
         "label": _("Remove the selected folder"),
         "class": "btn-default btn-xs"},
        {"name": "compress",
         "img": "fa fa-compress",
         "label": _("Compress folder"),
         "class": "btn-default btn-xs",
         "url": reverse("kalabash_webmail:folder_compress")}
    ]

    context = {
        "entries": entries,
        "css": "dropdown-menu",
    }
    return render_to_string('common/menu.html', context)


@register.filter
def parse_imap_header(value, header):
    """Simple template tag to display a IMAP header."""
    safe = True
    try:
        value = getattr(imapheader, "parse_%s" % header)(value)
    except AttributeError:
        pass
    if header == "from":
        value = value[0]
    elif header == "subject":
        safe = False
    return value if not safe else mark_safe(value)


@register.simple_tag
def attachment_url(mbox, mail_id, fname, key):
    """Return full download url of an attachment."""
    url = reverse("kalabash_webmail:attachment_get")
    params = {
        "mbox": mbox,
        "mailid": mail_id,
        "fname": smart_str(fname),
        "partnumber": key
    }
    url = "{}?{}".format(url, urlencode(params))
    return url
