Translate the following English MDX article into $language_name ($lang_code).

The input is an independent Jev AI Guide article. Translate all prose naturally
for readers who use $language_name. Do not add facts, remove useful details, or
rewrite the article's intent.

Formatting rules:
1. Preserve all Markdown structure exactly: ## headings, optional ### headings,
   lists, bold text, inline code, Markdown tables, blockquotes, and link syntax.
2. Preserve all HTML tags exactly if they appear.
3. Preserve every URL exactly. Translate descriptive link text when natural,
   but never translate or edit the URL.
4. Preserve the article structure, ordering, and approximate length.
5. Do not add an H1 heading. The metadata title is rendered as the page H1.
6. Do not add internal links, imports, JSX, scripts, or new sections.

Metadata rules:
1. Translate only these metadata values when present: title, description, and
   summary.
2. Keep every other metadata field unchanged, including category, date,
   lastModified, image, status, and any other non-prose field.
3. Keep the JavaScript metadata export format exactly. Do not convert it to
   YAML frontmatter.
4. The output must begin exactly with `export const metadata = {`.

Quality rules:
1. Use natural, fluent $language_name appropriate for a technical tutorial.
2. Keep product names, company names, model names, API names, code identifiers,
   file paths, and technical terms accurate. Do not translate Jev, TypeSafe,
   System One, Noul, Choice, Score, or code identifiers unless the source
   explicitly provides an established localized form.
3. Do not translate text inside inline code or fenced code if code is present.
4. Keep Markdown table column counts and row structure unchanged.
5. Do not add translator notes, explanations, citations, or commentary.

Target language: $language_name ($lang_code)

English source:

$content

Output requirements:
1. Output only the translated MDX content.
2. Do not wrap the output in a code fence.
3. Do not add any text before or after the MDX.
4. Return valid MDX beginning with the JavaScript metadata export and followed
   by the translated Markdown body.
