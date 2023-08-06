#####
Setup
#####

To use it, go to the online panel and modify the following parameters
to communicate with your *IMAP* server (under *IMAP settings*):

+--------------------+--------------------+--------------------+
|Name                |Description         |Default value       |
+====================+====================+====================+
|Server address      |Address of your IMAP|127.0.0.1           |
|                    |server              |                    |
+--------------------+--------------------+--------------------+
|Use a secured       |Use a secured       |no                  |
|connection          |connection to access|                    |
|                    |IMAP server         |                    |
+--------------------+--------------------+--------------------+
|Server port         |Listening port of   |143                 |
|                    |your IMAP server    |                    |
+--------------------+--------------------+--------------------+

Do the same to communicate with your SMTP server (under *SMTP settings*):

+--------------------+--------------------+--------------------+
|Name                |Description         |Default value       |
+====================+====================+====================+
|Server address      |Address of your SMTP|127.0.0.1           |
|                    |server              |                    |
+--------------------+--------------------+--------------------+
|Secured connection  |Use a secured       |None                |
|mode                |connection to access|                    |
|                    |SMTP server         |                    |
+--------------------+--------------------+--------------------+
|Server port         |Listening port of   |25                  |
|                    |your SMTP server    |                    |
+--------------------+--------------------+--------------------+
|Authentication      |Server needs        |no                  |
|required            |authentication      |                    |
+--------------------+--------------------+--------------------+

.. note::

   The size of each attachment sent with a message is limited. You can
   change the default value by modifying the **Maximum attachment
   size** parameter.

Using CKeditor
==============

Kalabash supports CKeditor to compose HTML messages. Each user has the
possibility to choose between CKeditor and the raw text editor to
compose their messages. (see *User > Settings > Preferences >
Webmail*)
