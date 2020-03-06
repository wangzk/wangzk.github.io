---
title: 'Fixing "File conversion failed" error in the Elsevier EVISE System'
date: 2020-03-06 09:30:00 +0800
categories: academy 
---

*EVISE* is the new editorial system of many Elsevier journals. Compared to the previous system *Elsevier Editorial System* (EES), EVISE is easier to use. However, it is much more difficult to debug when someone meets troubles during submission because the information given for troubleshooting is much vaguer than EES.

I met the problem of "file conversion failed" when submitting the LaTeX source files in a zip format. The journal that I submitted to required me to submit a PDF file as "Manuscript" along with a zip file as "LaTeX source file".
The PDF file was easy to submit.
When I submitted the LaTeX source file as a zip, EVISE prompted me "File conversion failed" for the zip file and prevented me from continuing my submission.
The promption was vague and it did not provide any information on what is going wrong.

After searching the Internet and going through trial and error, I summarize the following notes for LaTeX source file submission in EVISE:

1. When the EVISE system prompts "File conversion failed" for the zipped LaTeX source file, it means that EVISE meets errors when it compiles the LaTeX files.
2. Do not contain any directories in the zip file. Since the EVISE system (and also EES) cannot process directories correctly, put all the TeX files, figures and other files under the root of the zip file.

    ```text
    my-submission.zip
        |- main.tex
        |- ref.bib
        |- fig1.eps
        |- fig2.eps
        |- xxx.sty
        |- xxx.bst
        ...
    ```

3. Use `latex` or `pdflatex` to compile. EVISE and EES only support `latex` and `pdflatex`. `latex` is recommended. The figure files had better to be stored in the eps format.
4. Manually add `sty`/`bst` files for advanced LaTeX packages and bibtex styles in the zip file. The TeX environment used by EVISE only contains basic packages. Some advanced packages like `algorithmic` are missing. Therefore, one should manually copy the `sty` files of the used packages in the zip file. One can find the list of used sty files in the debug information printted during the compilation.

Good luck with your submission.
