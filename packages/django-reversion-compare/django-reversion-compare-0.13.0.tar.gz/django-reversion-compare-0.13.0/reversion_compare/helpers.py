"""
    django-reversion helpers
    ~~~~~~~~~~~~~~~~~~~~~~~~

    A number of useful helper functions to automate common tasks.

    Used google-diff-match-patch [1] if installed, fallback to difflib.
    For installing use e.g. the unofficial package:

        pip install diff-match-patch

    [1] https://github.com/google/diff-match-patch

    :copyleft: 2012-2020 by the django-reversion-compare team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

import difflib
import logging

from diff_match_patch import diff_match_patch
from django.contrib import admin
from django.contrib.admin.sites import NotRegistered
from django.utils.encoding import force_str
from django.utils.html import escape
from django.utils.safestring import mark_safe


logger = logging.getLogger(__name__)


SEMANTIC = 1
EFFICIENCY = 2

# Change from diff-match-patch to ndiff if old/new values are less than X characters:
CHANGE_DIFF_THRESHOLD = 20


# https://github.com/google/diff-match-patch
dmp = diff_match_patch()


def highlight_diff(diff_text):
    """
    Simple highlight a diff text in the way pygments do it ;)
    """
    lines = []
    for line in diff_text.splitlines():
        line = escape(line)

        if line.startswith("+"):
            line = f"<ins>{line}</ins>"
        elif line.startswith("-"):
            line = f"<del>{line}</del>"

        lines.append(line)

    html = '\n'.join(lines)
    return f'<pre class="highlight">{html}</pre>'


def diff_match_patch_pretty_html(diff):
    """
    Similar to diff_match_patch.diff_prettyHtml but generated the same html as our
    reversion_compare.helpers.highlight_diff
    """
    html = ['<pre class="highlight">']
    for (op, line) in diff:
        line = escape(line)

        if op == diff_match_patch.DIFF_INSERT:
            line = f'<ins>{line}</ins>'
        elif op == diff_match_patch.DIFF_DELETE:
            line = f'<del>{line}</del>'
        elif op != diff_match_patch.DIFF_EQUAL:
            raise TypeError(f'Unknown op: {op!r}')

        html.append(line)

    html.append('</pre>')
    return ''.join(html)


def generate_dmp_diff(value1, value2, cleanup=SEMANTIC):
    """
    Generate the diff with Google diff-match-patch
    """
    diff = dmp.diff_main(
        value1, value2,
        checklines=False  # run a line-level diff first to identify the changed areas
    )
    if cleanup == SEMANTIC:
        dmp.diff_cleanupSemantic(diff)
    elif cleanup == EFFICIENCY:
        dmp.diff_cleanupEfficiency(diff)
    elif cleanup is not None:
        raise ValueError("cleanup parameter should be one of SEMANTIC, EFFICIENCY or None.")

    html = diff_match_patch_pretty_html(diff)

    return html


def generate_ndiff(value1, value2):
    value1 = value1.splitlines()
    value2 = value2.splitlines()
    diff = difflib.ndiff(value1, value2)
    diff_text = "\n".join(diff)
    html = highlight_diff(diff_text)
    return html


def html_diff(value1, value2, cleanup=SEMANTIC):
    """
    Generates a diff used google-diff-match-patch is exist or ndiff as fallback

    The cleanup parameter can be SEMANTIC, EFFICIENCY or None to clean up the diff
    for greater human readibility.
    """
    value1 = force_str(value1, errors='replace')
    value2 = force_str(value2, errors='replace')

    if len(value1) > CHANGE_DIFF_THRESHOLD or len(value2) > CHANGE_DIFF_THRESHOLD:
        # Bigger values -> use Google diff-match-patch
        html = generate_dmp_diff(value1, value2, cleanup)
    else:
        # For small content use ndiff
        html = generate_ndiff(value1, value2)

    html = mark_safe(html)
    return html


def compare_queryset(first, second):
    """
    Simple compare two querysets (used for many-to-many field compare)
    XXX: resort results?
    """
    result = []
    for item in set(first).union(set(second)):
        if item not in first:  # item was inserted
            item.insert = True
        elif item not in second:  # item was deleted
            item.delete = True
        result.append(item)
    return result


def patch_admin(model, admin_site=None, AdminClass=None, skip_non_revision=False):
    """
    Enables version control with full admin integration for a model that has
    already been registered with the django admin site.

    This is excellent for adding version control to existing Django contrib
    applications.

    :param skip_non_revision: If ==True: Skip models that are not register with ModelAdmin
    """
    admin_site = admin_site or admin.site
    try:
        ModelAdmin = admin_site._registry[model].__class__
    except KeyError:
        raise NotRegistered(f"The model {model} has not been registered with the admin site.")

    if skip_non_revision:
        if not hasattr(ModelAdmin, "object_history_template"):
            logger.info(
                f"Skip activate compare admin, because"
                f" model {model._meta.object_name!r} is not registered with revision manager."
            )
        return

    # Unregister existing admin class.
    admin_site.unregister(model)

    # Register patched admin class.
    if not AdminClass:
        from reversion_compare.admin import CompareVersionAdmin

        class PatchedModelAdmin(CompareVersionAdmin, ModelAdmin):
            pass

    else:

        class PatchedModelAdmin(AdminClass, ModelAdmin):
            pass

    admin_site.register(model, PatchedModelAdmin)
