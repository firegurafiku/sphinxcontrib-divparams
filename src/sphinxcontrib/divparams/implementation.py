# -*- coding: utf-8 -*-
# This file is a part of 'sphinxcontrib.divparams' project, which is an HTML
# postprocessor to achieve parameter list flat design. See sphinx/index.rst for
# more information.
#
# Copyright (c) 2015 Pavel Kretov.
# Provided under the terms of MIT license.
import os
import re
import bs4


def transform_parameter_list_item(item, soup):
    # Parameter 'item' may refer to either <li> or <p class="first last"> tag.
    # The latter case means that it's the only one list item, reduced by Sphinx
    # to single paragraph. If so, expand <p> back to <ul><li>...</li></ul>.
    if item.name == "p":
        item.name = "li"
        item["class"] = "divparams-single-par"
        item.wrap(soup.new_tag("ul"))

    # Create regular expressions only once.
    re_opening_paren = re.compile("^\\s*\\(")
    re_closing_paren = re.compile("^\\s*\\)\\s+–\\s+", re.M)

    if len(item.contents) < 4:
        return

    # Python 2 doesn't support modern list unpacking, so make
    # sure that length matches.
    strong, paren_op, em, paren_cl = item.contents[0:4]
    looks_fine = (isinstance(strong,   bs4.Tag)    and
                  isinstance(em,       bs4.Tag)    and
                  isinstance(paren_op, str)        and
                  isinstance(paren_cl, str)        and
                  strong.name == "strong"          and
                  em.name     == "em"              and
                  re_opening_paren.match(paren_op) and
                  re_closing_paren.match(paren_cl))

    if not looks_fine:
        return

    paren_op.replace_with(": ")
    paren_cl.insert_before(soup.new_tag("br"))
    paren_cl.replace_with(re_closing_paren.sub("", paren_cl))


def transform_html(soup):
    tables = soup.find_all("table", class_=["docutils", "field-list"])
    for table in tables:
        ths = table.find_all("th", class_="field-name")
        tds = table.find_all("td", class_="field-body")

        replacement = soup.new_tag("div", class_="divparams-list")
        for th, td in zip(ths, tds):

            header = th.extract()
            header.name = "div"
            header["class"] = "divparams-name"

            param_list = td.extract()
            param_list.name = "div"
            param_list["class"] = "divparams-body"

            for p in param_list.findChildren("li"):
                transform_parameter_list_item(p, soup)

            for p in param_list.findChildren("p", class_=["first", "last"]):
                transform_parameter_list_item(p, soup)

            replacement.contents.append(header)
            replacement.contents.append(param_list)

        table.insert_before(replacement)
        table.decompose()


def process_build_finished(app, exception):

    # Don't risk doing anything if Sphinx failed in building HTML.
    if exception is not None:
        return

    if not app.config.divparams_enable_postprocessing:
        return

    excludes = app.config.divparams_exclude_sources

    # Find all files eligible for DOM transform.
    # See also: http://stackoverflow.com/a/33640970/1447225
    target_files = []
    for doc in app.env.found_docs:
        if doc in excludes:
            continue

        target_filename = app.builder.get_target_uri(doc)
        target_filename = os.path.join(app.outdir, target_filename)
        target_filename = os.path.abspath(target_filename)
        target_files.append(target_filename)

    for fn in target_files:
        try:
            with open(fn, mode="rb") as f:
                soup = bs4.BeautifulSoup(f.read(), "html.parser")

            transform_html(soup)
            html = soup.prettify(encoding=app.config.html_output_encoding)

            with open(fn, mode='wb') as f:
                f.write(html)

        except Exception as exc:
            app.warn("exception raised during HTML tweaking: %s"
                     % exc, location=os.path.basename(fn))
