# What is mkdocs?
mkdocs - utility for generating documentation/other in different formats (now only pure HTML supported) from common .doc files (that have lightweight syntax)

mkdocs is written in pure python and under development now

## Usage example
if you want to compile whole folder of .doc files
```
mkdocs dir docsdir generateddir
``` 

if you want to compile single .doc file
```
mkdocs file file.doc page.html
```

if you want to use python for this
```
python -m mkdocs dir generateddir
```

## Download
You can download precompiled .exe binaries for Windows from the releases page. Package was builded using PyInstaller (with --onefile flag)

## Note
.doc files are not associated with word or microsoft, just file extension