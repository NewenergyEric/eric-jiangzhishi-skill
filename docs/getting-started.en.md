# Start with a question
[中文](getting-started.md) · [Making Sense Together](../README.en.md)

Download a [release](https://github.com/NewenergyEric/eric-jiangzhishi-skill/releases/latest). The small Skills archive contains two independent skill folders. The full archive adds the examples, font, videos and build source. Open the [HTML start page](getting-started.en.html) locally, or follow these steps.

## Choose your starting point

- **Content & explanation** (`knowledge-to-friendly-product`): use this when the sources still need to become an explanation. It can complete the whole illustrated guide.
- **Illustration & layout** (`knowledge-card-art-direction`): use this when the copy is approved and you want to work on the pages.

Ask an assistant with file access to read the chosen folder's `SKILL.md`. That is the instruction entry, in Chinese; each folder also includes an English overview. Ask for the output in your preferred language.

For regular use, copy the entire skill folder into a location your tool supports. The full package has a helper:

```sh
python scripts/install_skill.py knowledge-to-friendly-product --dest ./my-skills
```

This example uses a directory you choose. It does not register the skill with every host or change a global setting.

## Give it something to work with

Include the topic, the reader's background, where they will read it, sources, format, page count, language, style references and anything that must stay unchanged.

> Read knowledge-to-friendly-product. My topic is [topic], for [reader and reading context]. Use [files or links] to make [format and page count] in English. Follow [style reference] and preserve [fixed material]. Keep the explanation natural and connected. Use images and icons to explain the content. Deliver sources, editable files and a record of the checks actually performed.

For the layout skill, provide approved copy and ask it to preserve the wording unless you agree to a change.

## Review the result

Open every exported page. Check the facts and sources, then whether the illustrations and labels say the same thing as the text. Read at the intended viewing size. Keep the editable copy, chosen artwork, full prompts and layout source.

An image tool is needed for new illustrations. Rebuilding the included PDFs also requires the dependencies in `requirements.txt`. Missing tools should leave an honest unfinished item, not a claim of completion.

## Update or remove a skill

Back up an existing folder before replacing it. To remove a skill, remove only its folder. If the audience or sources change, revisit the facts and examples too.

[Installation checklist](installation-checklist.en.md) · [Verification](verification.en.md) · [Back to the project](../README.en.md)
