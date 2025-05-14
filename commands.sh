# Remove the submodule reference
git rm --cached Text-to-Speech-API-
rm -rf .git/modules/Text-to-Speech-API-
# Then commit the changes
git commit -m "Remove submodule reference"
git push